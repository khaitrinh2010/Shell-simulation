import os
import shlex  
import sys
from parsing import split_by_pipe_op

def needPiping(command):
    single = False 
    double = False
    for char in command:
        if char == "|" and not single and not double:
            return True 
        elif char == "'":
            single = not single
        elif char == '"':
            double = not double
    return False
def checkPipingSyntax(command):
    potential = False
    quote  = False
    if command.strip()[-1] == "|":
        sys.stderr.write("mysh: syntax error: expected command after pipe\n")
        return False
    for i in range(len(command)):
        if(command[i] == "'"):
            quote = not quote
        if(command[i] == " "): continue
        if(command[i] == "|" and potential and not quote):
            sys.stderr.write("mysh: syntax error: expected command after pipe\n")
            return False
        elif(command[i]  == "|" and not potential and not quote):
            potential =  True
        else:
            potential = False
    return True

def handlePiping(command):
    siu = None
    if not checkPipingSyntax(command):
        return
    fullCommand = split_by_pipe_op(command)
    output = ""
    prevOutput = None
    n = len(fullCommand) 
    for i in range(n):
        #execute each command one by one
        firstCmd = shlex.split(fullCommand[i]) 
        if i < n - 1:
            r,w = os.pipe() 
        else:
            r,w = None, None
        pid = os.fork() 
        if pid == 0:
            #There is an output from previous pipe
            if prevOutput:
                os.dup2(prevOutput, 0) #read 
                os.close(prevOutput) 
            if w:
                os.dup2(w, 1) #write the the pipe write end
                os.close(w) 
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
