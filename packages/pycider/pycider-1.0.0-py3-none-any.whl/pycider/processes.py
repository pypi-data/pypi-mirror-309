from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

from pycider.deciders import Decider

E = TypeVar("E")
C = TypeVar("C")
S = TypeVar("S")


class IProcess(ABC, Generic[E, C, S]):
    """Prototype for Process implementations.

    All Processes should be implemented using this prototype.
    """

    @abstractmethod
    def evolve(self, state: S, event: E) -> S:
        """Returns an updated state based on the current event.

        Paramters
            state: State of the current process
            event: Event generated from commands procesed

        Returns
            An updated state.
        """
        pass

    @abstractmethod
    def resume(self, state: S) -> Iterator[C]:
        """Returns an iterator of commands to resume a process from a given state.

        Parameters
            state: State of the current process

        Returns
            An iterator of commands to act on.
        """
        pass

    @abstractmethod
    def react(self, state: S, event: E) -> Iterator[C]:
        """Returns an iterator of commands as a reaction to an event.

        Parameters
            state: State of the current process
            event: Event currently being processed

        Returns
            An iterator of commands to act on.
        """
        pass

    @abstractmethod
    def initial_state(self) -> S:
        """Returns the starting state for a process.

        Returns
            A state representing the start of a process.
        """
        pass

    @abstractmethod
    def is_terminal(self, state: S) -> bool:
        """Returns if a process's state is terminal.

        Parameters
            state: State of the current process

        Returns
            A boolean indicating if a process has run till completion.
        """
        pass


EI = TypeVar("EI")
CI = TypeVar("CI")
EO = TypeVar("EO")
CO = TypeVar("CO")


class ProcessAdapt(Generic[EI, CI, S, EO, CO]):
    """Adapt process Commands / Events into new output Commands and Events."""

    @classmethod
    def build(
        cls,
        select_event: Callable[[EI], EO | None],
        convert_command: Callable[[CO], CI],
        p: IProcess[EO, CO, S],
    ) -> IProcess[EI, CI, S]:
        """Convert Commands/Events into output variants.

        Parameters:
            select_event: A callaback that converts input Events to output Events.
            convert_command: A callback that converts input Commands to output Commands.

        Returns:
            A new Process that can given input Events/Commands return new output variants.
        """

        class InternalProcess(IProcess[EI, CI, S]):
            def evolve(self, state: S, event: EI) -> S:
                new_event = select_event(event)
                if new_event is None:
                    return state
                return p.evolve(state, new_event)

            def resume(self, state: S) -> Iterator[CI]:
                yield from map(convert_command, p.resume(state))

            def react(self, state: S, event: EI) -> Iterator[CI]:
                new_event = select_event(event)
                if new_event is None:
                    yield from []
                else:
                    yield from map(convert_command, p.react(state, new_event))

            def initial_state(self) -> S:
                return p.initial_state()

            def is_terminal(self, state: S) -> bool:
                return p.is_terminal(state)

        return InternalProcess()


def process_collect_fold(
    proc: IProcess[E, C, S], state: S, events: list[E]
) -> Iterator[C]:
    new_state = state
    while len(events) > 0:
        event = events.pop(0)
        new_state = proc.evolve(state, event)
        commands = proc.react(new_state, event)
        yield from commands


PS = TypeVar("PS")
DS = TypeVar("DS")


class ProcessCombineWithDecider(Generic[E, C, PS, DS]):
    """Combine a Processor with a Decider together."""

    @classmethod
    def build(
        cls, proc: IProcess[E, C, PS], decider: Decider[E, C, DS]
    ) -> Decider[E, C, tuple[DS, PS]]:
        """Combine a Process and a Decider into a single Decider.

        Parameters:
            proc: The process being combined.
            decider: The decider its being combined with.

        Results:
            A single Decider.

        Note: This function's generated `decide` function deviates from the model used by the original material. `decide` in this code takes a command and state tuple.

        For each command issued this code will do the following:

        #. create a command list `commands` initialized as [commands]
        #. create a event list `events` initialized as []
        #. run `decider.decide` on a popped entry from commands
        #. append the results to events array
        #. create a copy of state and run `decider.evolve` on it
        #. run `process.react` to generate new commands appended to the commands list.
        #. run `process.evolve` on each new event.
        #. loop back to 2 with remaining commands and the copy of decider's state.
        #. one commands is empty, return all events collected during the above.

        The state of neither process nor decider is actually changed by `decide`. You will still need to call `evolve` to reach the final end states.
        """

        class InternalDecider(Decider[E, C, tuple[DS, PS]]):
            def decide(self, command: C, state: tuple[DS, PS]) -> Iterator[E]:
                # NOTE: This is a deviation.
                decider_state = state[0]
                commands = [command]
                while len(commands) > 0:
                    command = commands.pop(0)
                    new_events = list(decider.decide(command, decider_state))
                    # NOTE: This is a deviation.
                    for event in new_events:
                        decider_state = decider.evolve(decider_state, event)
                    new_commands = process_collect_fold(
                        proc, state[1], new_events.copy()
                    )
                    commands.extend(new_commands)
                    yield from new_events

            def evolve(self, state: tuple[DS, PS], event: E) -> tuple[DS, PS]:
                return (decider.evolve(state[0], event), proc.evolve(state[1], event))

            def initial_state(self) -> tuple[DS, PS]:
                return (decider.initial_state(), proc.initial_state())

            def is_terminal(self, state: tuple[DS, PS]) -> bool:
                return decider.is_terminal(state[0]) and proc.is_terminal(state[1])

        return InternalDecider()
