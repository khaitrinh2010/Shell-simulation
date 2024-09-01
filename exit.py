import sys
def handleExit(command):
    if len(command) > 2:
        sys.stderr.write("exit: too many arguments\n")
        return
    elif not command[1].isdecimal():
        sys.stderr.write(f"exit: non-integer exit code provided: {command[1]}\n")
        return
    print()
    sys.exit(int(command[1]) if len(command) == 2 else 0)
