from rpn import Expression,isFunction,isOperator,compare_precedence

# Still at work. Very early testing stage.
class Equation():
    def __init__(self,exp1:Expression,exp2:Expression):
        self.exp1 = exp1
        self.exp2 = exp2

        self.sameUnk = None
    
    @classmethod
    def from_str(cls,exp1:str,exp2:str):
        return cls(Expression(exp1),Expression(exp2))

    def seperate(self,exp:Expression):
        print(exp.rpn)
        res = []
        temp = []
        for i in exp.rpn:
            if isOperator(i) == 1 and not isFunction(i):
                temp.append(i)
            elif isOperator(i) == 0 or isFunction(i):
                temp.append(i)
                res.append(temp)
                temp = []
        return res
    
    def simplify(self,expList:list[list[str]]):
        for i in range(len(expList)):
            if len(expList[i]) == 1 or len(expList[i]) == 0:
                continue
            print(i,expList[i])
            op1 = expList[i][len(expList[i])-1]
            for j in range(i+1,len(expList)):
                op2 = expList[j][len(expList[j])-1]
                if compare_precedence(op1,op2) == 0:
                    for k in range(len(expList[i])):
                        c = expList[i][k]
                        if c.isnumeric():
                            if (len(expList[j]) == 2) and not (expList[j][0].isnumeric()):
                                continue

                            while len(expList[j]) > 0 :
                                print(expList[j][len(expList[j])-1])
                                expList[i].insert(k+1,expList[j].pop())
        return expList
    def resolveList(self,expList:list[list[str]]):
        res = []
        for i in expList:
            for j in i:
                res.append(j)
        # for i in expList:
        #     if i == []:
        #         continue
        #     print(i)
        #     e = Expression("").from_rpn(i)
        #     e.alternateEval()
        #     if e.resolved:
        #         res.append(e.lastEvaluation)
        #         continue
        #     res.append(e.rpn)
        print(j)
        print(res)
        e = Expression("").from_rpn(res)
        e.alternateEval()
        print(e.unresolvedEval)
    def __str__(self):
        return f"{self.exp1.infix} = {self.exp2.infix}"

a=Equation(Expression("9 / x ^ 2 + 3"),Expression("2+x"))
print(a)
l = a.seperate(a.exp1)
print(l)
l = a.simplify(l)
print(l)
a.resolveList(l)