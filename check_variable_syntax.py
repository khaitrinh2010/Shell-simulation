def checkSyntaxVariableName(name):
    for char in name:
        if not char.isalnum():
            if not char == "_":
                return False 
    return True


