# Start work on trigonometric functions
import math
def isOperator(c:str):
    if c in "+-*/()^":
        return 0
    return 1

def isFunction(c:str):
    if c in "sin cos tan asin acos atan log abs sqrt".split(" "):
        return True
    return False
def compare_precedence(op1, op2):
    # Define operator precedence levels
    precedence = {
    '(': 0, ')': 0,  # Parentheses
    '+': 1, '-': 1,  # Addition and subtraction
    '*': 2, '/': 2, '%': 2,  # Multiplication, division, modulus
    '//': 2,  # Floor division
    '^': 3,  # Exponentiation
    "sqrt":3,
    'sin': 4, 'cos': 4, 'tan': 4,  # Trigonometric functions
    'asin': 4, 'acos': 4, 'atan': 4,  # Inverse trigonometric functions
    'log': 4,  # Logarithm
    'abs': 4,  # Absolute value
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
        case "sin":
            return math.sin(y)
        case "cos":
            return math.cos(y)
        case "tan":
            return math.tan(y)
        case "asin":
            return math.asin(y)
        case "acos":
            return math.acos(y)
        case "atan":
            return math.atan(y)
        case "log":
            return math.log10(y)
        case "abs":
            return math.fabs(y)
        case "sqrt":
            return math.sqrt(y)

class RPN:
    def __init__(self,infix:str):
        self.infix = infix
        self.variables = {}
        self.rpn = self.parser(infix)
        self.parseVariables()
        self.lastEvaluation = ""
        self.unresolvedEval = ""
        self.resolved = True
    
    def parser(self,exp=""):
        if exp == "":
            exp = self.infix
        opStack = []
        altStack = []
        numBuf = ""
        doubleOp = False
        for c in exp:
            if doubleOp == True and c == "-":
                numBuf += c
                continue
            elif c == "-" and opStack == [] and numBuf == "" and altStack == []:
                numBuf += c
                continue
                
            isFunc = isFunction(numBuf+c)
            if isOperator(c) == 0 or isFunc:
                if isFunc:
                    c = numBuf+c
                    numBuf = ""
                doubleOp = True
                if numBuf != "" and not isFunc:
                    altStack.append(numBuf)
                    numBuf = ""
                
                if c == ")":
                    popping = True
                    while popping == True and len(opStack) > 0:
                        current = opStack[len(opStack)-1]
                        if current != "(":
                            altStack.append(current) 
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
                    if (p == 0 and c != "^" and c != "(") or (p == -1 and c != "^") and c != "(" and not isFunc:
                        altStack.append(opStack.pop())
                    else:
                        opStack.append(c)
                        popping = False
                if len(opStack) < 1:
                    opStack.append(c) 
            else:
                if c == " " and numBuf == "":
                    continue
                elif c == " " and numBuf != "":
                    altStack.append(numBuf)
                    numBuf = ""
                elif c != " ":
                    doubleOp = False
                    numBuf += c
        if numBuf != "":
            altStack.append(numBuf)
        for i in reversed(opStack):
            if i in "()":
                print("Mismatched paranthesis!")
                return ""
            altStack.append(i)
        return altStack
        
    
    def parseVariables(self): # Used to identify the unknowns
        for i in self.rpn:
            if isOperator(i) == 1 and i.isnumeric() == False and not isFunction(i):
                self.variables.update({i:None})

    def alternateEval(self):
        constStack = []
        output = ""
        for i in self.rpn:
            if isOperator(i) == 1 and not isFunction(i):
                constStack.append(i)
            elif isOperator(i) == 0 or isFunction(i):
                if len(constStack) == 0:
                    print("Calculation error.")
                    self.lastEvaluation = None
                    return

                if isFunction(i):
                    x = constStack.pop()
                    a = ""
                    if "-" in x:
                        a = "-"
                    if self.variables.get(x) != None:
                        x = a+self.variables.get(x)
                    
                    if x.isalpha():
                        output += " ".join(constStack)+ " ".join([x]) + " " + i # Add the buffer to the output variable as this cant be computed for now
                        # constStack.pop()
                        # constStack.pop()
                        constStack = []
                        self.resolved = False
                        continue
                    try:
                        res = performBasic(0,x,i)
                    except ValueError as e:
                        print("Error: ",e)
                        self.lastEvaluation = None
                        self.resolved = False
                        self.unresolvedEval = self.rpn
                        return
                    constStack.append(str(res))
                    continue
                x = constStack.pop()
                y = constStack.pop()
                a = ""
                b = ""
                if "-" in x:
                    a = "-"
                if "-" in y:
                    b = "-"

                if self.variables.get(x) != None:
                    x = a+self.variables.get(x) 
                if self.variables.get(y) != None:
                    y = b+self.variables.get(y) 
                
                if x.isalpha() or y.isalpha():
                    output += " ".join(constStack)+ " ".join([x,y]) + " " + i # Add the buffer to the output variable as this cant be computed for now
                    # constStack.pop()
                    # constStack.pop()
                    constStack = []
                    self.resolved = False
                    continue
                res = performBasic(y,x,i)
                constStack.append(str(res))
        
        if self.resolved == True:
            self.lastEvaluation = float(constStack[0])
            self.unresolvedEval = ""
        elif self.resolved == False:
            self.lastEvaluation = None
            self.unresolvedEval = output + " " +  str(constStack)

    def evaluate(self,exp=None):
        print("WARNING: This version of the evaluation engine is being deprecated and will not work with default parsed expressions. Use alternateEval unless you know what you are doing.")
        return
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

