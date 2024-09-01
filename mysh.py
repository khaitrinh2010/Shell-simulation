import signal
import shlex
import os
import re
import sys
import json
from parsing import split_by_pipe_op
from setup import loadMyShrc, setDefault
from directory import handleDirectory
from exit import handleExit
from variable_substitute import variableSubstitution
from var import handleVar
from which import handleWhich
from other_commands import executeOtherCommands
from piping import handlePiping
from parse_command import parseCommand, processInnput


# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    
def handleCommand(command):
    command = variableSubstitution(command)
    if not checkCommandError(command):
        return
    if command[0] == "var":
        return handleVar(command)
    elif command[0] == "cd" or command[0] == "pwd":
        return handleDirectory(command)
    elif command[0] == "exit":
        return handleExit(command)
    elif command[0] == "which":
        handleWhich(command)
    else:
        return executeOtherCommands(command)
    return None
    
def checkCommandError(command):
    if not command:
        return
    cmd =  command[0]
    builtinCommands = ["cd", "pwd", "which", "var", "exit"]
    executable = False
    isBuiltinCommand = True
    #3 cases
    if "/" in cmd:
        if os.path.isdir(cmd):
            print(f"mysh: is a directory: {cmd}")
            return False
        elif not os.path.exists(cmd):
            print(f"mysh: no such file or directory: {cmd}")
            return False
        elif not os.access(cmd, os.X_OK):
            print(f"mysh: permission denied: {cmd}")
            return False
        else:
            return True
    else:
        if cmd not in builtinCommands:
            isBuiltinCommand = False
            for path in os.environ["PATH"].split(":"):
                candidate = os.path.join(path, cmd) 
                if(os.path.exists(candidate) and os.access(candidate, os.X_OK)):
                    executable = True
                    break
    if not executable and not isBuiltinCommand:
        print(f"mysh: command not found: {cmd}")
        return False 
    return True


def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()
    setDefault()
    loadMyShrc()

    if "PATH" not in os.environ:
        os.environ["PATH"] = os.defpath
    # Start your code here!
    while True:
        try:
            start = os.getenv("PROMPT")
            sys.stdout.write(start)
            sys.stdout.flush()
            command = parseCommand(input())
            if(command):
                if(command[0] == "exit" and len(command) == 1): #exit with out any option
                    return
                handleCommand(command)
            else:
                continue
        except EOFError:
            print()
            break

if __name__ == "__main__":
    main()
