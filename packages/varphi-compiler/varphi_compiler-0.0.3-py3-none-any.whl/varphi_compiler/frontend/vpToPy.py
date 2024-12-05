import sys
from pathlib import Path

from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from varphi_parsing_tools import *
from .VarphiRepresentor import VarphiRepresentor
from ..model import State, Instruction, HeadDirection, TapeCharacter

def getVarphiSourceAsString() -> str:
    with open(Path(__file__).resolve().parents[0] / "varphi.py") as varphiSource:
        return varphiSource.read()

def getStateEnum(representor: VarphiRepresentor, indentLevel: int) -> str:
    stateEnum = "class State(Enum):\n"
    for stateName in representor.stateNameToObject:
        stateEnum += f"\t{stateName} = auto()\n"
    return stateEnum

def statesToPython(representor: VarphiRepresentor, debug: bool, indentLevel: int, program: list[str]) -> str:
    python = ""
    for stateObject in representor.stateNameToObject.values():
        python += stateToPython(stateObject, debug, indentLevel, program)
    return python


def stateToPython(state: State, debug: bool, indentLevel: int, program: list[str]) -> str:
    indent = "\t" * indentLevel
    python = f"{indent}if state == State.{state.name}:\n"
    python += getStateOnTallyPython(state, debug, indentLevel + 1, program)
    python += getStateOnBlankPython(state, debug, indentLevel + 1, program)
    return python

def instructionToPython(instruction: Instruction, indentLevel: int) -> str:
    indent = "\t" * indentLevel
    python = f"{indent}state = State.{instruction.nextState.name}\n"
    if instruction.characterToPlace == TapeCharacter.TALLY:
        python += f"{indent}head.write(TapeCharacter.TALLY)\n"
    else:
        python += f"{indent}head.write(TapeCharacter.BLANK)\n"
    
    if instruction.directionToMove == HeadDirection.RIGHT:
        python += f"{indent}head.right()\n"
    else:
        python += f"{indent}head.left()\n"
    python += f"{indent}continue\n"
    return python

def getStateOnTallyPython(state: State, debug: bool, indentLevel: int, program: list[str]) -> str:
    indent = "\t" * indentLevel
    indentPlusOne = indent + '\t'
    indentPlusTwo = indentPlusOne + '\t'
    python = f"{indent}if tapeCharacter == TapeCharacter.TALLY:\n"
    if len(state.onTally) == 0:
        if debug:
            python += f"{indentPlusOne}printDebugData(\"{state.name}\", tape, head, -1, \"\", True)\n"
            python += f"{indentPlusOne}waitForEnterKey()\n"
        python += f"{indentPlusOne}print(tape)\n"
        python += f"{indentPlusOne}break\n"
    else:
        python += f"{indentPlusOne}choice = random.randint(0, {len(state.onTally) - 1})\n"
        for i in range(len(state.onTally)):
            python += f"{indentPlusOne}if choice == {i}:\n"
            if debug:
                python += f"{indentPlusTwo}printDebugData(\"{state.name}\", tape, head, {state.onTally[i].lineNumber}, \"{program[state.onTally[i].lineNumber - 1]}\", False)\n"
                python += f"{indentPlusTwo}waitForEnterKey()\n"
            python += instructionToPython(state.onTally[i], indentLevel + 2)
    return python


def getStateOnBlankPython(state: State, debug: bool, indentLevel: int, program: list[str]) -> str:
    indent = "\t" * indentLevel
    indentPlusOne = indent + '\t'
    indentPlusTwo = indentPlusOne + '\t'
    python = f"{indent}if tapeCharacter == TapeCharacter.BLANK:\n"
    if len(state.onBlank) == 0:
        if debug:
            python += f"{indentPlusOne}printDebugData(\"{state.name}\", tape, head, -1, \"\", True)\n"
            python += f"{indentPlusOne}waitForEnterKey()\n"
        python += f"{indentPlusOne}print(tape)\n"
        python += f"{indentPlusOne}break\n"
    else:
        python += f"{indentPlusOne}choice = random.randint(0, {len(state.onBlank) - 1})\n"
        for i in range(len(state.onBlank)):
            python += f"{indentPlusOne}if choice == {i}:\n"
            if debug:
                python += f"{indentPlusTwo}printDebugData(\"{state.name}\", tape, head, {state.onBlank[i].lineNumber}, \"{program[state.onBlank[i].lineNumber - 1]}\", False)\n"
                python += f"{indentPlusTwo}waitForEnterKey()\n"
            python += instructionToPython(state.onBlank[i], indentLevel + 2)
    return python
    

def getMain(representor: VarphiRepresentor, debug: bool, program: list[str]) -> str:
    main = "if __name__ == \"__main__\":\n"
    main += f"\tstate = State.{representor.initialState.name}\n"
    main += "\ttape = getTapeFromStdin()\n"
    main += "\thead = getHeadPointingAtFirstTally(tape)\n"

    main += "\twhile True:\n"
    main += "\t\ttapeCharacter = head.read()\n"
    main += statesToPython(representor, debug, 2, program)
    return main

def representorToPython(representor: VarphiRepresentor, debug: bool, program: list[str]) -> str:
    python = getVarphiSourceAsString()
    python += getStateEnum(representor, 1)
    python += getMain(representor, debug, program)
    return python


def programToPython(programPath: str, debug: bool) -> str:
    with open(programPath, 'r') as file:
        program = file.read()

    input_stream = InputStream(program)
    lexer = VarphiLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(VarphiSyntaxErrorListener(program))
    token_stream = CommonTokenStream(lexer)
    parser = VarphiParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(VarphiSyntaxErrorListener(program))
    try:
        tree = parser.program()
    except Exception as e:
        sys.stderr.write(str(e))
        exit(-1)
    representor = VarphiRepresentor()
    walker = ParseTreeWalker()
    walker.walk(representor, tree)
    
    return representorToPython(representor, debug, program.splitlines())