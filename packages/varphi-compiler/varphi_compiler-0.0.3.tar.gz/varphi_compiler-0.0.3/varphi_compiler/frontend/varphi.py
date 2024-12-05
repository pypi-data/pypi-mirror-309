import sys
import json
from collections import defaultdict
from enum import Enum, auto
import random

class TapeCharacter(Enum):
    """
    Enum class defining the allowed tape characters in the Varphi language.
    
    TapeCharacter represents a unary Turing machine's tape symbol:
    
    - `BLANK`: Represented as 0, indicates the absence of a tally mark.
    - `TALLY`: Represented as 1, indicates the presence of a tally mark.
    """
    BLANK = auto()
    TALLY = auto()

class Tape:
    tape: defaultdict[int, TapeCharacter]
    _maxAccessedIndex: int
    _minAccessedIndex: int

    def __init__(self) -> None:
        self.tape = defaultdict(lambda: TapeCharacter.BLANK)
        self._maxAccessedIndex = 0
        self._minAccessedIndex = 0
    
    def _updateInternalsAfterTapeAccess(self, index: int) -> None:
        if index > self._maxAccessedIndex:
            self._maxAccessedIndex = index
        if index < self._minAccessedIndex:
            self._minAccessedIndex = index
    
    def __getitem__(self, index: int) -> TapeCharacter:
        self._updateInternalsAfterTapeAccess(index)
        return self.tape[index]
    
    def __setitem__(self, index: int, value: TapeCharacter) -> None:
        self._updateInternalsAfterTapeAccess(index)
        self.tape[index] = value
    
    def __repr__(self) -> str:
        representation = ""
        for i in range(self._minAccessedIndex, self._maxAccessedIndex + 1):
            representation += '1' if self.tape[i] == TapeCharacter.TALLY else '0'
        return representation
    
class Head:
    tape: Tape
    currentTapeCell: int

    def __init__(self, tape: Tape, initialTapeCell: int = 0) -> None:
        self.tape = tape
        self.currentTapeCell = initialTapeCell
    
    def right(self) -> None:
        self.currentTapeCell += 1
    
    def left(self) -> None:
        self.currentTapeCell -= 1
    
    def read(self) -> TapeCharacter:
        return self.tape[self.currentTapeCell]
    
    def write(self, value: TapeCharacter) -> None:
        self.tape[self.currentTapeCell] = value
    
    def __repr__(self) -> str:
        return str(self.currentTapeCell)

def getTapeFromStdin() -> Tape:
    tape = Tape()
    inputCharacter = sys.stdin.read(1)
    i = 0
    while inputCharacter not in {'\n', '\r'}:
        if inputCharacter == '0':
            tape[i] = TapeCharacter.BLANK
        elif inputCharacter == '1':
            tape[i] = TapeCharacter.TALLY
        else:
            print(f"Error: Invalid tape character (ASCII {ord(inputCharacter)}).")
            sys.exit(-1)
        inputCharacter = sys.stdin.read(1)
        i += 1
    return tape

def getHeadPointingAtFirstTally(tape: Tape) -> Head:
    for i in range(tape._minAccessedIndex, tape._maxAccessedIndex + 1):
        if tape[i] == TapeCharacter.TALLY:
            return Head(tape, i)
    print("Error: It is required that at least one tally is provided on the input tape, but none were found.")
    sys.exit(-1)

def printDebugData(state: str, 
                   tape: Tape, 
                   head: Head, 
                   lineNumber: int, 
                   line: str, 
                   halted: bool) -> None:
    debugData = {}
    debugData["state"] = state
    debugData["tape"] = tape.__str__()
    debugData["head"] = head.currentTapeCell
    debugData["lineNumber"] = lineNumber
    debugData["line"] = line
    debugData["halted"] = halted
    debugData["tapeZero"] = -tape._minAccessedIndex
    print(json.dumps(debugData))

def waitForEnterKey():
    while sys.stdin.read(1) not in {'\n', '\r'}:
        continue
