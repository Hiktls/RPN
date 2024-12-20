
"""




"""


def isOperator(c:str):
    match c:
        case '+':
            return 0
        case '-':
            return 0
        case '*':
            return 0
        case '/':
            return 0
        case '(':
            return 0
        case ')':
            return 0
        case '^':
            return 0
        case _:
            return 1
 

        
            
def compare_precedence(op1, op2):
    # Define operator precedence levels
    precedence = {
        '(': 0, ')': 0,  # Parentheses for completeness, precedence is handled separately in expressions
        '+': 1, '-': 1,  # Addition and subtraction
        '*': 2, '/': 2, '%': 2,  # Multiplication, division, and modulus
        '^': 3,  # Exponentiation
        '//': 2,  # Floor division
    }
    
    # Check if both operators are valid
    if op1 not in precedence or op2 not in precedence:
        raise ValueError(f"Invalid operator(s): {op1}, {op2}")
    
    # Compare precedence
    if precedence[op1] < precedence[op2]:
        return -1
    elif precedence[op1] > precedence[op2]:
        return 1
    else:
        return 0

def SmartDisp(op,cons,c):
    print("-"*50)
    print("Operations: ",op)
    print("Current cons stack:",cons)
    print("Current i:",c)
    


        

def performBasic(x,y,op):
    x = float(x)
    y = float(y)
    match op:
        case "+":
            return str(x+y)
        case "-":
            return str(x-y)
        case "*":
            return str(x * y)
        case "/":
            return str(x / y)
        case "^":
            return str(x**y)

class RPN:
    def __init__(self,infix:str):
        self.infix = infix
        self.variables = {}
        self.rpn = self.parser(infix)
        self.parseVariables()
        self.lastEvaluation = ""
        self.testMat = self.rpn.split(" ")
        while "" in self.testMat:
            self.testMat.remove("")
        self.unresolvedEval = ""
        self.resolved = True
    
    def parser(self,exp=""):
        if exp == "":
            exp = self.infix
        opStack = []
        constStack = ""
        for c in exp:
            if isOperator(c) == 0:
                constStack += ""
                if c == ")":
                    popping = True
                    while popping == True and len(opStack) > 0:
                        current = opStack[len(opStack)-1]
                        if current != "(":
                            constStack += " "+ current 
                            opStack.pop()
                        elif current == "(":
                            opStack.pop()
                            popping = False
                    if popping == True and len(opStack) == 0:
                        print("Mismatched Parenthesis!")
                        return ""
                    continue
                

                popping = True
                while popping and len(opStack) > 0:
                    p = compare_precedence(c,opStack[len(opStack)-1])
                    if (p == 0 and c != "^" and c != "(") or (p == -1 and c != "^") and c != "(":
                        constStack += " " + opStack[len(opStack)-1]
                        opStack.pop()
                    else:
                        opStack.append(c)
                        popping = False
                if len(opStack) < 1:
                    opStack.append(c) 
            else:
                constStack += c
                # if c == " " and numberBuffer != "":
                #     constStack += numberBuffer + " "
                #     numberBuffer = "" 
                # elif c != " ":
                #     numberBuffer += c
            #SmartDisp(opStack,constStack,c)
        for i in reversed(opStack):
            if i in "()":
                print("Mismatched paranthesis!")
                return ""
            constStack += " " + i

        return constStack
        
    
    def parseVariables(self): # Used to identify the unknowns
        for i in self.rpn:
            if i == " ":
                continue
            if isOperator(i) == 1 and i.isnumeric() == False:
                self.variables.update({i:None})

    def alternateEval(self):
        constStack = []
        output = ""
        for i in self.testMat:
            if isOperator(i) == 1:
                constStack.append(i)
            elif isOperator(i) == 0:
                if len(constStack) == 0:
                    print("Calculation error.")
                    self.lastEvaluation = None
                    return

                x = constStack.pop()
                y = constStack.pop()

                if self.variables.get(x) != None:
                    x = self.variables.get(x)
                if self.variables.get(y) != None:
                    y = self.variables.get(y)
                
                if x.isalpha() or y.isalpha():
                    output += " ".join(constStack)+ " ".join([x,y]) + " " + i # Add the buffer to the output variable as this cant be computed for now
                    # constStack.pop()
                    # constStack.pop()
                    constStack = []
                    self.resolved = False
                    continue
                res = performBasic(y,x,i)
                print("RES:",res)
                constStack.append(str(res))
        
        if self.resolved == True:
            self.lastEvaluation = float(constStack[0])
            self.unresolvedEval = ""
        elif self.resolved == False:
            self.lastEvaluation = None
            self.unresolvedEval = output + " " +  str(constStack)


    def evaluate(self,exp=None):
        if exp == None:
            exp = self.rpn
        constStack = []
        temp = ""
        output = ""
        numberBuffer = ""
        for i in exp:
            
            n = len(constStack)-1
            temp += i
            if n+1 >= 2:
                None
            if isOperator(i) == 1:# Append constants
                if i.isalpha() == False and i != "":
                    if i == " " and numberBuffer != "":
                        constStack.append(numberBuffer)
                        numberBuffer = ""
                    elif i != " ":
                        numberBuffer += i
                elif i.isalpha() and i != " ":
                    constStack.append(i)
            elif isOperator(i) == 0:
                if (len(constStack) < 2) and numberBuffer == "": # Not enough variables to compute, thus add these to the output as well
                    output += " " +  " ".join(constStack) + " " + numberBuffer + i
                    temp = ""
                    numberBuffer = ""
                    constStack = []
                    continue
                elif (len(constStack)<2) and numberBuffer != "":
                    output += " ".join(constStack) + numberBuffer 
                    numberBuffer = ""
                    continue
                x = constStack[n-1] 
                y = constStack[n]
                if self.variables.get(x) != None:
                    x = self.variables.get(x)
                if self.variables.get(y) != None:
                    y = self.variables.get(y)
                if x.isalpha() or y.isalpha():
                    output += " ".join(constStack) + " " + i # Add the buffer to the output variable as this cant be computed for now
                    temp = ""
                    # constStack.pop()
                    # constStack.pop()
                    constStack = []
                    continue
                res = performBasic(x,y,i)
                # Clear the used constants from the stack
                temp = " ".join(constStack) + " " + str(res) + " "
                constStack.pop()
                constStack.pop()
                constStack.append(res)
        if  len(constStack) == 1: # Merge the uncomputed with the computed values
            output += " " + constStack[0]
        elif len(constStack) > 1:
            print("Calculation error!")
        self.lastEvaluation = float(output)


    def __str__(self):
        return self.infix + " , [" + self.rpn + "]"

e = RPN("a + 5")
e.alternateEval()
print(e.unresolvedEval)