import os
import sys

def handleDirectory(command):
    if(command[0] == "cd"):
        if(len(command) > 2):
            sys.stderr.write("cd: too many arguments\n")
            return
        #Only cd
        if(len(command) == 1):
            os.chdir(os.path.expanduser("~"))
            os.environ["PWD"] = os.path.expanduser("~")
            return
        path = command[1]
        try:
            if os.path.isabs(path):
                os.chdir(path) 
                os.environ["PWD"] = path
            if(command[1] == "~"):
                # change to the home directory
                os.chdir(os.path.expanduser("~"))
                os.environ["PWD"] = os.path.expanduser("~")
            elif(command[1] == ".."):
                os.chdir("..")
                os.environ["PWD"] = os.getcwd()
            else:
                newPath = os.path.normpath(os.path.join(os.environ["PWD"], path))
                os.chdir(newPath)
                os.environ["PWD"] = newPath
        except FileNotFoundError:
            sys.stderr.write(f"cd: no such file or directory: {command[1]}\n")
            return
        except NotADirectoryError:
            sys.stderr.write(f"cd: not a directory: {command[1]}\n")
            return
        except PermissionError:
            sys.stderr.write(f"cd: permission denied: {command[1]}\n")
            return

    elif command[0] == "pwd":
        if len(command) > 1:
            #Get the first option only
            option = command[1][:2]
            if(option == "-P"):
                print(os.getcwd())
            else:
                sys.stderr.write(f"pwd: invalid option: {option}\n")
        else:
            try:
                print(os.environ["PWD"])
            except Exception:
                sys.stderr.write("There's something wrong\n")
