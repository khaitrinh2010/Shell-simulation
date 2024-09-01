import os  
import sys   

def handleWhich(command):
    builtinCommand = ["var", "which", "cd", "pwd", "exit"]
    found = False    
    if(len(command) == 1):
        sys.stderr.write("usage: which command ...\n")
        return
    else:
        for i in range(1, len(command)):
            if(command[i] in builtinCommand):
                print(f"{command[i]}: shell built-in command")
            else:
                allPaths = os.environ.get("PATH").split(":")
                for path in allPaths:
                    checkedpath = os.path.join(path, command[i])
                    if(os.path.isfile(checkedpath) and os.access(checkedpath, os.X_OK)):
                        found = True
                        print(checkedpath)
                        break
                if not found:
                    sys.stderr.write(f"{command[i]} not found\n")
