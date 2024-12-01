def OLDGOODPARSER(self,exp:str):
        opStack = []
        constStack = ""
        for c in exp:
            if c == " ":
                continue
            if isOperator(c) == 0:
                if c == ")":
                    popping = True
                    while popping and len(opStack) > 0:
                        current = opStack[len(opStack)-1]
                        if current != "(":
                            constStack += current + " "
                            opStack.pop()
                        elif current == "(":
                            opStack.pop()
                            break
                    continue

                popping = True
                n = 0
                while popping and len(opStack) > 0:
                    p = compare_precedence(c,opStack[len(opStack)-1])
                    if (p == 0 and c != "^" and c != "(") or (p == -1 and c != "^") and c != "(":
                        constStack += opStack[len(opStack)-1] + " "
                        opStack.pop()
                    else:
                        opStack.append(c)
                        popping = False
                if len(opStack) < 1:
                    opStack.append(c)
            else:
                constStack += c +" "
            #SmartDisp(opStack,constStack,c)
        for i in reversed(opStack):
            constStack += i + " "
        return constStack
def shuntingYard(exp:str):
    opStack = []
    constStack = ""
    for c in exp:
        if c == " ":
            continue
        if isOperator(c) == 0: 
            if c == ")": # If we get a bracket closure, start popping to get to the beginner
                popping = True
                while popping and len(opStack) > 0:
                    current = opStack[len(opStack)-1]
                    if current != "(":
                        constStack += current + " "
                        opStack.pop()
                    elif current == "(":
                        opStack.pop()
                        break
                continue

            popping = True
            n = 0
            while popping and len(opStack) > 0: # Pop according to the conditions
                p = compare_precedence(c,opStack[len(opStack)-1])
                if (p == 0 and c != "^" and c != "(") or (p == -1 and c != "^") and c != "(": # No predence and no right-way and no starter or smaller precedence and no right-way and no closure beginner
                    constStack += opStack[len(opStack)-1] + " "
                    opStack.pop()
                else:
                    opStack.append(c)
                    popping = False
            if len(opStack) < 1:
                opStack.append(c)
        else:
            constStack += c +" "
        #SmartDisp(opStack,constStack,c)
    for i in reversed(opStack): # Append the stack when reading is done
        constStack += i + " "
    return constStack