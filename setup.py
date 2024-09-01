import json
import sys  
import os
import shlex
from check_variable_syntax import checkSyntaxVariableName
from variable_substitute import variableSubstitution

def loadMyShrc():
    path = None
    if os.getenv("MYSHDOTDIR"):
        path = os.path.join(os.getenv("MYSHDOTDIR"), ".myshrc")
    else:
        path = os.path.expanduser("~/.myshrc")
    try:
        with open(path, "r") as f:
            #take a file object
            contents = json.load(f)  
            for key, value in contents.items():
                if not isinstance(value, str):
                    sys.stderr.write(f"mysh: .myshrc: {key}: not a string\n")
                    return
                if checkSyntaxVariableName(key):
                    os.environ[key] = " ".join(variableSubstitution(shlex.split(value)))
                else:
                    sys.stderr.write(f"mysh: .myshrc: {key}: invalid characters for variable name\n")
    except json.JSONDecodeError:
        sys.stderr.write("mysh: invalid JSON format for .myshrc\n")
    except Exception:
        pass
def setDefault():
    if "PROMPT" not in os.environ:
        os.environ["PROMPT"] = ">> "
    if "MYSH_VERSION" not in os.environ:
        os.environ["MYSH_VERSION"] = "1.0"
