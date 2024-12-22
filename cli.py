# This file is mainly for quick use of the calculator and testing edge cases quickly
from rpn import RPN

while True:
    exp = input("Enter an expression: ")
    if exp == "exit":
        break
    rpn = RPN(exp)
    if rpn.variables != {}:
        print("Variables found. You may add variable definitions in the form 'x = 5'. Type 'done' when done with definitions.")
        while True:
            var = input("$")
            if var == "done":
                break
            var = var.split("=")
            rpn.variables[var[0].strip()] = var[1].strip()
    print("[INFO] RPN Parsing is: ",rpn.rpn)
    rpn.alternateEval()
    if rpn.resolved == False:
        print("[INFO] Expression didnt resolve fully.")
        print(rpn.unresolvedEval)
    else:
        print("[INFO] Result is: ",rpn.lastEvaluation)