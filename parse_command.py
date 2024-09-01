from piping import handlePiping, needPiping
import shlex

def processInnput(command):
    if "\\" not in command:
        return command
    single = False 
    startQuote = False
    escape = False
    full =  []
    n = len(command) 
    current = ""
    #backlash and substitute 
    if "$" in command:
        fullList = list(command)
        for i in range(len(fullList)):
            if fullList[i] == "\\":
                fullList[i] = "\\\\"
        return  "".join(fullList)

    #backlash and no substitute
    for i in range(n):
        char = command[i] 
        if startQuote:
            if char == "\\":
                escape = True
            elif i > 0 and char != "$" and command[i - 1] == "\\":
                current += char  
                escape = False
            elif char == "'" and not escape:
                current += '"' 
                escape = False
                startQuote = False
                full.append(current)
                current = ""
            else:
                current += char
        else:
            if char == "'" and not startQuote:
                startQuote = True
                current += '"' 
            else:
                full.append(char)
    return "".join(full)

def parseCommand(command):
    if needPiping(command):
        return handlePiping(command)
    command = processInnput(command)
    # print(command)
    try:
        command = shlex.split(command, posix=True)
    except ValueError as e:
        if("No closing quotation" in str(e)):
            print("mysh: syntax error: unterminated quote")
            return
    return command
