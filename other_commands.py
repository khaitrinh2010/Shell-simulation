import os
def executeOtherCommands(command):
    command = [os.path.expanduser(cmd) for cmd in command]
    pid = os.fork() 
    #child process
    if(pid == 0):
        os.setpgid(0, 0) 
        try:
            os.execvp(command[0], command)
        except Exception:
            sys.stderr.write("Hahahaha\n")
            sys.exit(1)
    else:
        #wait for the child process
        try:
            os.setpgid(pid, pid) 
        except PermissionError:
            pass  
        child_pgid = os.getpgid(pid)
        #open withh read and write mode
        f = os.open("/dev/tty", os.O_RDWR)
        try:
            os.tcsetpgrp(f, child_pgid)
            os.waitpid(pid, 0)
        finally:
            parentGid = os.getpgrp()
            os.tcsetpgrp(f, parentGid) 
            os.close(f)
