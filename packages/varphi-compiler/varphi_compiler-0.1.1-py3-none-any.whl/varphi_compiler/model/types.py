from dataclasses import dataclass
from enum import Enum, auto

class TapeCharacter(Enum):
    """
    Enum class defining the allowed tape characters in the Varphi language.
    
    TapeCharacter represents a unary Turing machine's tape symbol:
    
    - `BLANK`: Represented as 0, indicates the absence of a tally mark.
    - `TALLY`: Represented as 1, indicates the presence of a tally mark.
    """
    BLANK = auto()
    TALLY = auto()


class HeadDirection(Enum):
    """
    Defines two directions that the Turing machine head can move in.

    Enums:
        - LEFT (auto): Represents a move to the left on the tape.
        - RIGHT (auto): Represents a move to the right on the tape.
    """
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Instruction:
    """
    Represents an instruction for a (potentially non-deterministic)
    Turing machine.

    Each instruction specifies:
    - The next state the Turing machine should transition to.
    - The tape character that should be placed on the current cell.
    - The direction in which the machine's head should move after placing the
      character.

    Attributes:
        - nextState (State): The state to transition to after this instruction.
        - characterToPlace (TapeCharacter): The character to place on the tape
          at the current position.
        - directionToMove (HeadDirection): The direction in which the head
          should move after placing the character.
    """
    nextState: "State"  # Quotes for forward reference
    characterToPlace: TapeCharacter
    directionToMove: HeadDirection
    lineNumber: int
    line: str


@dataclass
class State:
    """
    Represents a state of a (potentially non-deterministic) Turing machine.

    Each state can define different instructions based on whether a tally or a
    blank is encountered at the current position of the tape head.

    In non-deterministic Turing machines, multiple instructions can be provided
    for the same input, and the machine non-deterministically selects one to
    follow.

    Attributes:
        - onTally (list[Instruction]): A list of instructions to execute if the
          machine encounters a tally at the current tape position while in this
          state.
        - onBlank (list[Instruction]): A list of instructions to execute if the
          machine encounters a blank at the current tape position while in this
          state.

    Methods:
        - addOnTallyInstruction(instruction: Instruction): Adds an instruction
          to follow when a tally is encountered on the tape.
        - addOnBlankInstruction(instruction: Instruction): Adds an instruction
          to follow when a blank is encountered on the tape.
    """
    name: str
    onTally: list[Instruction]
    onBlank: list[Instruction]

    def __init__(self, name: str) -> None:
        """
        Initializes a new state with empty lists of instructions for tallies
        and blanks.

        This constructor ensures that `onTally` and `onBlank` start as empty
        lists, allowing multiple instructions to be added later (e.g., for
        non-deterministic Turing machines).
        """
        self.name = name
        self.onTally = []
        self.onBlank = []

    def addOnTallyInstruction(self, instruction: Instruction) -> None:
        """
        Adds an instruction to follow when a tally is encountered at the
        current tape position.

        Since this implementation supports non-deterministic Turing machines,
        multiple instructions can be added.
        The machine will non-deterministically select one instruction to follow
        from the list of available instructions.

        Parameters:
            - instruction (Instruction): The instruction to add for
              encountering a tally.
        """
        self.onTally.append(instruction)

    def addOnBlankInstruction(self, instruction: Instruction) -> None:
        """
        Adds an instruction to follow when a blank is encountered at the
        current tape position.

        Since this implementation supports non-deterministic Turing machines,
        multiple instructions can be added.
        The machine will non-deterministically select one instruction to follow
        from the list of available instructions.

        Parameters:
            - instruction (Instruction): The instruction to add for
              encountering a blank.
        """
        self.onBlank.append(instruction)
