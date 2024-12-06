import sys

from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from varphi_parsing_tools import *
from .VarphiRepresentor import VarphiRepresentor
from ..model import State, Instruction, HeadDirection, TapeCharacter

def getIncludes() -> str:
    headers = "#include <stdio.h>\n"
    headers += "#include <stdlib.h>\n"
    headers += "#include <varphi.h>\n"
    headers += "#include <limits.h>\n"
    headers += "#include <time.h>\n"
    return headers

def getStateEnum(representor: VarphiRepresentor) -> str:
    stateEnum = "enum {"
    for stateName in representor.stateNameToObject:
        stateEnum += f"{stateName},"
    stateEnum += f"}} state = {representor.initialState.name};"
    return stateEnum

def statesToC(representor: VarphiRepresentor, debug: bool) -> str:
    c = ""
    for stateObject in representor.stateNameToObject.values():
        c += stateToC(stateObject, debug)
    return c


def stateToC(state: State, debug: bool) -> str:
    c = f"if (state == {state.name}) {{"
    c += getStateOnTallyC(state, debug)
    c += getStateOnBlankC(state, debug)
    c += "}"
    return c

def instructionToC(instruction: Instruction) -> str:
    c = f"state = {instruction.nextState.name}; // {instruction.line}\n"
    if instruction.characterToPlace == TapeCharacter.TALLY:
        c += "headWrite(head, tape, TALLY);"
    else:
        c += "headWrite(head, tape, BLANK);"
    
    if instruction.directionToMove == HeadDirection.RIGHT:
        c += "headRight(head);"
    else:
        c += "headLeft(head);"
    c += "continue;"
    return c

def getStateOnTallyC(state: State, debug: bool) -> str:
    c = "if (tapeCharacter == TALLY) {"
    if len(state.onTally) == 0:
        if debug:
            c += f"dumpDebugInfo(tape, head, \"{state.name}\", -1, 1, \"\");"
            c += "waitForEnterKey();"
        c += "printTape(tape);"
        c += f"break;"
    else:
        c += f"long long int choice = rand() % {len(state.onTally)};"
        for i in range(len(state.onTally)):
            c += f"if (choice == {i}) {{"
            if debug:
                c += f"dumpDebugInfo(tape, head, \"{state.name}\", {state.onTally[i].lineNumber}, 0, \"{state.name} 1 {state.onTally[i].nextState.name} {state.onTally[i].characterToPlace.value} {state.onTally[i].directionToMove.value}\");"
                c += "waitForEnterKey();"
            c += instructionToC(state.onTally[i])
            c += "}"
    c += "}"
    return c


def getStateOnBlankC(state: State, debug: bool) -> str:
    c = "if (tapeCharacter == BLANK) {"
    if len(state.onBlank) == 0:
        if debug:
            c += f"dumpDebugInfo(tape, head, \"{state.name}\", -1, 1, \"\");"
            c += "waitForEnterKey();"
        c += "printTape(tape);"
        c += f"break;"
    else:
        c += f"long long int choice = rand() % {len(state.onBlank)};"
        for i in range(len(state.onBlank)):
            c += f"if (choice == {i}) {{"
            if debug:
                c += f"dumpDebugInfo(tape, head, \"{state.name}\", {state.onBlank[i].lineNumber}, 0, \"{state.name} 0 {state.onBlank[i].nextState.name} {state.onBlank[i].characterToPlace.value} {state.onBlank[i].directionToMove.value}\");"
                c += "waitForEnterKey();"
            c += instructionToC(state.onBlank[i])
            c += "}"
    c += "}"
    return c
    

def getMain(representor: VarphiRepresentor, debug: bool) -> str:
    main = "int main() {"
    main += "srand (time(NULL));"
    main += getStateEnum(representor)
    if debug:
        main += "struct Tape* tape = getInputTapeDebug();"
    else:
        main += "struct Tape* tape = getInputTape();"
    main += "struct Head* head = newHead();"
    main += "headToFirstTally(head, tape);"

    main += "while (1) {"
    main += "char tapeCharacter = headRead(head, tape);"
    main += statesToC(representor, debug)
    main += "}"
    main += "freeTape(tape);"
    main += "freeHead(head);"
    main += "return 0;"
    main += "}"
    return main

def representorToC(representor: VarphiRepresentor, debug: bool) -> str:
    c = getIncludes()
    c += getMain(representor, debug)
    return c


def programToC(programPath: str, debug: bool) -> str:
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
    
    return representorToC(representor, debug)