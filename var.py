import os 
import shlex  
import sys
from check_variable_syntax import checkSyntaxVariableName
from piping import needPiping
from parsing import split_by_pipe_op
def handleVar(command):
    output = ""
    if(len(command) < 3):
        sys.stderr.write(f"var: expected 2 arguments, got {len(command) - 1}\n")
        return
    varName = None
    varValue = None
    if(len(command) == 3):
        if (not checkSyntaxVariableName(command[1])):
            sys.stderr.write(f"var: invalid characters for variable {command[1]}\n")
            return
        varName = command[1]
        varValue = command[2]
        if varValue.startswith("'") and varValue.endswith("'"):
            varValue = varValue[1:-1]
        os.environ[varName] = varValue
        return
    elif(len(command) > 3):
        if(command[1] == "-s"):
            varName = command[2]
            if (not checkSyntaxVariableName(varName)):
                sys.stderr.write(f"var: invalid characters for variable {command[1]}\n")
                return
            if needPiping(command[3]):
                main_r, main_w = os.pipe()
                fullCommand = split_by_pipe_op(command[3])
                prevOutput = None
                n = len(fullCommand) 
                for i in range(n):
                    #execute each command one by one
                    firstCmd = shlex.split(fullCommand[i]) 
                    if i < n - 1:
                        r,w = os.pipe() 
                    else:
                        r,w = None, main_w
                    pid = os.fork() 
                    if pid == 0:
                        #There is an output from previous pipe
                        if prevOutput:
                            os.dup2(prevOutput, 0) #read 
                            os.close(prevOutput) 
                        if w:
                            os.dup2(w, 1) #write the the pipe write end
                            os.close(w) 
                            if r:
                                os.close(r) 
                        os.setpgid(0,0)
                        try:
                            os.execvp(firstCmd[0], firstCmd)
                        except Exception:
                            sys.stderr.write("There's something wrong\n")
                    else:
                        if prevOutput:
                            os.close(prevOutput)
                        if w:
                            os.close(w)
                        prevOutput = r
                        os.waitpid(pid, 0)
                os.environ[varName] = os.read(main_r, 4096).decode()
            elif not needPiping(command[3]):
                runCommand = shlex.split(command[3])
                runCommand = [os.path.expanduser(cmd) for cmd in runCommand]
                r,w = os.pipe() 
                pid = os.fork()
                if pid == 0:
                    os.close(r) 
                    os.dup2(w, 1)
                    os.close(w) 
                    try:
                        os.execvp(runCommand[0], runCommand)
                    except Exception:
                        sys.exit(1)
                else:
                    os.close(w)
                    os.waitpid(pid, 0)
                    while True:
                        part = os.read(r, 4096)
                        if not part:
                            break
                        output += part.decode('utf-8')
                    os.close(r) 

                    if '\n' in output[:-1]:
                        os.environ[varName] = output
                    else:
                        os.environ[varName] = output.strip()
        else:
            #other flags
            if(command[1].startswith("-")):
                sys.stderr.write(f"var: invalid option: {command[1][:2]}\n")
            #Got too mmany arguments
            else:
                sys.stderr.write(f"var: expected 2 arguments, got {len(command) - 1}\n")
