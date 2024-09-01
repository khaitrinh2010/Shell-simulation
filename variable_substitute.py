import shlex
import os
import sys
from parse_command import parseCommand
from check_variable_syntax import checkSyntaxVariableName

def neededToSubStitute(command):
    pot = False
    if isinstance(command, list):
        for each in command:
            if "$" in each:
                return True 
        return False
    else:
        for i in range(len(command)):
            char = command[i]
            if char == "$" and i < len(command) - 1 and command[i + 1] == "{":
                pot = True
            if char == "}" and pot:
                return True 
    return False

def variableSubstitution(command):
    original = command
    segment = []
    if not neededToSubStitute(command):
        return original
    for i in range(len(command)):
        segment = command[i] 
        if " " in segment or neededToSubStitute(segment):
            segment = f"'{segment}'"
            command[i] = segment
    command = " ".join(command) 
    if("$" not in command):
        return original
    else:
        if "{" not in command or "}" not in command:
            return original
    n = len(command)
    i = 0
    while i < n - 1:
        if command[i] == "\\" and i < n - 1 and command[i + 1] == "$":
            command = command[:i] + command[i + 1:]
            n -= 1
            i += 1
        elif command[i] == "$" and command[i + 1] == "{":
            start = i
            varName = "" 
            i += 2
            while i < n and command[i] != "}":
                varName += command[i]
                i += 1
            if i < n and command[i] == "}":
                end = i + 1
                if not checkSyntaxVariableName(varName):
                    sys.stderr.write(f"mysh: syntax error: invalid characters for variable {varName}\n")
                    return
                varValue = os.environ.get(varName, "")
                
                command = command[: start] + varValue + command[end:]
                n = len(command)
                i = start + len(varValue) - 1
        i += 1

    temp = list(command)
    count = 0
    for i in range(len(temp)):
        if temp[i] == "'":
            count += 1
    if not (count % 2 ==  0):
        for i in range(len(temp)):
            if temp[i] == "'":
                temp[i] = '"'
                break
        for i in range(len(temp) - 1, -1, -1):
            if temp[i] == "'":
                temp[i] = '"'
                break
    return parseCommand("".join(temp))
