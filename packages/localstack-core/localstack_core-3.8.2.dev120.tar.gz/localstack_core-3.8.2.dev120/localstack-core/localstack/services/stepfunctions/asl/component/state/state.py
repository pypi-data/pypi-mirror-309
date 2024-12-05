from __future__ import annotations

import abc
import copy
import datetime
import json
import logging
from abc import ABC
from typing import Final, Optional, Union

from localstack.aws.api.stepfunctions import (
    ExecutionFailedEventDetails,
    HistoryEventExecutionDataDetails,
    HistoryEventType,
    StateEnteredEventDetails,
    StateExitedEventDetails,
)
from localstack.services.stepfunctions.asl.component.common.catch.catcher_decl import CatcherOutput
from localstack.services.stepfunctions.asl.component.common.comment import Comment
from localstack.services.stepfunctions.asl.component.common.error_name.failure_event import (
    FailureEvent,
    FailureEventException,
)
from localstack.services.stepfunctions.asl.component.common.error_name.states_error_name import (
    StatesErrorName,
)
from localstack.services.stepfunctions.asl.component.common.error_name.states_error_name_type import (
    StatesErrorNameType,
)
from localstack.services.stepfunctions.asl.component.common.flow.end import End
from localstack.services.stepfunctions.asl.component.common.flow.next import Next
from localstack.services.stepfunctions.asl.component.common.path.input_path import InputPath
from localstack.services.stepfunctions.asl.component.common.path.output_path import OutputPath
from localstack.services.stepfunctions.asl.component.eval_component import EvalComponent
from localstack.services.stepfunctions.asl.component.state.state_continue_with import (
    ContinueWith,
    ContinueWithEnd,
    ContinueWithNext,
)
from localstack.services.stepfunctions.asl.component.state.state_props import StateProps
from localstack.services.stepfunctions.asl.component.state.state_type import StateType
from localstack.services.stepfunctions.asl.eval.contextobject.contex_object import State
from localstack.services.stepfunctions.asl.eval.environment import Environment
from localstack.services.stepfunctions.asl.eval.event.event_detail import EventDetails
from localstack.services.stepfunctions.asl.eval.program_state import ProgramRunning
from localstack.services.stepfunctions.asl.utils.encoding import to_json_str
from localstack.services.stepfunctions.quotas import is_within_size_quota

LOG = logging.getLogger(__name__)


class CommonStateField(EvalComponent, ABC):
    name: str

    # The state's type.
    state_type: StateType

    # There can be any number of terminal states per state machine. Only one of Next or End can
    # be used in a state. Some state types, such as Choice, don't support or use the End field.
    continue_with: ContinueWith

    # Holds a human-readable description of the state.
    comment: Optional[Comment]

    # A path that selects a portion of the state's input to be passed to the state's state_task for processing.
    # If omitted, it has the value $ which designates the entire input.
    input_path: InputPath

    # A path that selects a portion of the state's output to be passed to the next state.
    # If omitted, it has the value $ which designates the entire output.
    output_path: OutputPath

    state_entered_event_type: Final[HistoryEventType]
    state_exited_event_type: Final[Optional[HistoryEventType]]

    def __init__(
        self,
        state_entered_event_type: HistoryEventType,
        state_exited_event_type: Optional[HistoryEventType],
    ):
        self.comment = None
        self.input_path = InputPath(InputPath.DEFAULT_PATH)
        self.output_path = OutputPath(OutputPath.DEFAULT_PATH)
        self.state_entered_event_type = state_entered_event_type
        self.state_exited_event_type = state_exited_event_type

    def from_state_props(self, state_props: StateProps) -> None:
        self.name = state_props.name
        self.state_type = state_props.get(StateType)
        self.continue_with = (
            ContinueWithEnd() if state_props.get(End) else ContinueWithNext(state_props.get(Next))
        )
        self.comment = state_props.get(Comment)
        self.input_path = state_props.get(InputPath) or InputPath(InputPath.DEFAULT_PATH)
        self.output_path = state_props.get(OutputPath) or OutputPath(OutputPath.DEFAULT_PATH)

    def _set_next(self, env: Environment) -> None:
        if env.next_state_name != self.name:
            # Next was already overridden.
            return

        if isinstance(self.continue_with, ContinueWithNext):
            env.next_state_name = self.continue_with.next_state.name
        elif isinstance(self.continue_with, ContinueWithEnd):  # This includes ContinueWithSuccess
            env.set_ended()
        else:
            LOG.error("Could not handle ContinueWith type of '%s'.", type(self.continue_with))

    def _get_state_entered_event_details(self, env: Environment) -> StateEnteredEventDetails:
        return StateEnteredEventDetails(
            name=self.name,
            input=to_json_str(env.inp, separators=(",", ":")),
            inputDetails=HistoryEventExecutionDataDetails(
                truncated=False  # Always False for api calls.
            ),
        )

    def _get_state_exited_event_details(self, env: Environment) -> StateExitedEventDetails:
        return StateExitedEventDetails(
            name=self.name,
            output=to_json_str(env.inp, separators=(",", ":")),
            outputDetails=HistoryEventExecutionDataDetails(
                truncated=False  # Always False for api calls.
            ),
        )

    def _verify_size_quota(self, env: Environment, value: Union[str, json]) -> None:
        is_within: bool = is_within_size_quota(value)
        if is_within:
            return
        error_type = StatesErrorNameType.StatesStatesDataLimitExceeded
        cause = (
            f"The state/task '{self.name}' returned a result with a size exceeding "
            f"the maximum number of bytes service limit."
        )
        raise FailureEventException(
            failure_event=FailureEvent(
                env=env,
                error_name=StatesErrorName(typ=error_type),
                event_type=HistoryEventType.TaskFailed,
                event_details=EventDetails(
                    executionFailedEventDetails=ExecutionFailedEventDetails(
                        error=error_type.to_name(),
                        cause=cause,
                    )
                ),
            )
        )

    @abc.abstractmethod
    def _eval_state(self, env: Environment) -> None: ...

    def _eval_body(self, env: Environment) -> None:
        env.event_manager.add_event(
            context=env.event_history_context,
            event_type=self.state_entered_event_type,
            event_details=EventDetails(
                stateEnteredEventDetails=self._get_state_entered_event_details(env=env)
            ),
        )

        env.context_object_manager.context_object["State"] = State(
            EnteredTime=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(), Name=self.name
        )

        # Filter the input onto the stack.
        if self.input_path:
            self.input_path.eval(env)

        # Exec the state's logic.
        self._eval_state(env)
        #
        if not isinstance(env.program_state(), ProgramRunning):
            return

        # Obtain a reference to the state output.
        output = env.stack[-1]

        # CatcherOutputs (i.e. outputs of Catch blocks) are never subjects of output normalisers,
        # the entire value is instead passed by value as input to the next state, or program output.
        if isinstance(output, CatcherOutput):
            env.inp = copy.deepcopy(output)
        else:
            # Ensure the state's output is within state size quotas.
            self._verify_size_quota(env=env, value=output)

            # Filter the input onto the input.
            if self.output_path:
                self.output_path.eval(env)

        if self.state_exited_event_type is not None:
            env.event_manager.add_event(
                context=env.event_history_context,
                event_type=self.state_exited_event_type,
                event_details=EventDetails(
                    stateExitedEventDetails=self._get_state_exited_event_details(env=env),
                ),
            )

        # Set next state or halt (end).
        self._set_next(env)
