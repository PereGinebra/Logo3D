from vpython import *
from turtle3d import Turtle3D
import sys
if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor


class visitor(logo3dVisitor):

    def __init__(self):
        self.level = 0
        self.vars = {}
        self. funcs = {}
        self.exprValues = []
        self.boolxValues = []
        self.defArgs = []
        self.inArgs = []
        self.turtleIn = False

    def doFunction(self, func):
        if(len(func) > 0 and func[0] in self.funcs):
            f = func[0]
        else:
            f = "main"

        if(f in self.funcs):
            funcInfo = self.funcs[f]
            if(f == "main"):
                args = func[:]
            else:
                args = func[1:]
            if(len(args) == (len(funcInfo)-1)):
                saveVars = self.vars
                self.vars.clear()
                # posem els valors de els parametres al diccionari de variables
                i = 0
                while i < len(args):
                    self.vars[funcInfo.pop(0)] = args[i]
                    i += 1
                self.visit(funcInfo.pop(0))
                self.vars.clear()
                self.vars = saveVars

            elif(len(args) < (len(funcInfo)-1)):
                print("Exception: There are missing arguments in call to procedure " +
                      f+"/"+str(len(funcInfo)-1)+':')
                print("Expected "+str(len(funcInfo)-1) +
                      " and got "+str(len(args)))
            elif(len(args) > (len(funcInfo)-1)):
                print("Exception: There are too many arguments in call to procedure " +
                      f+"/"+str(len(funcInfo)-1)+':')
                print("Expected "+str(len(funcInfo)-1) +
                      " and got "+str(len(args)))
        elif len(func) > 0:
            print("Exception: There is no procedure called main or "+func[0])
            sys.exit()

    def operation(self, val1, val2, OP):
        if(OP == '+'):
            return val1 + val2
        elif(OP == '-'):
            return val1 - val2
        elif(OP == '*'):
            return val1 * val2
        elif(OP == '/'):
            if(val2 == 0):
                print("Exception: Attempted to divide by 0")
                sys.exit()
            else:
                return val1 / val2

    def boolToNum(b):
        if(b):
            return 1
        else:
            return 0

    def numToBool(num):
        if(num > -0.000001 and num < 0.000001):
            return False
        else:
            return True

    def boolOp(self, val1, val2, OP):
        if(OP == '>'):
            return visitor.boolToNum(val1 > val2)
        elif(OP == '<'):
            return visitor.boolToNum(val1 < val2)
        elif(OP == '>='):
            return visitor.boolToNum(val1 >= val2)
        elif(OP == '<='):
            return visitor.boolToNum(val1 <= val2)
        elif(OP == '=='):
            return visitor.boolToNum(val1 == val2)
        elif(OP == '!='):
            return visitor.boolToNum(val1 != val2)
        elif(OP == '||'):
            return visitor.boolToNum(visitor.numToBool(val1) or
                                     visitor.numToBool(val2))
        elif(OP == '&&'):
            return visitor.boolToNum(visitor.numToBool(val1) and
                                     visitor.numToBool(val2))
        else:
            print("Exception: Operation either doesn't exist or isn't implemented")
            sys.exit()

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if(len(l) == 1):  # NUM o ID
            if(logo3dParser.symbolicNames[l[0].getSymbol().type] == "NUM"):
                self.exprValues.append(l[0].getText())
            elif (l[0].getText() in self.vars):
                self.exprValues.append(self.vars[l[0].getText()])
            else:
                print("Exception: Variable used has no value")
                sys.exit()
        elif(l[0].getText() != '('):  # expresio 'normal'
            self.level += 1
            self.visit(l[0])
            self.visit(l[2])
            v2 = float(self.exprValues.pop())
            v1 = float(self.exprValues.pop())
            self.exprValues.append(self.operation(v1, v2, l[1].getText()))
            self.level -= 1
        else:  # expr entre parentesis
            self.visit(l[1])

    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        inp = input("reading var " + l[1].getText() + ": ")
        self.vars[l[1].getText()] = inp

    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[1])
        if(len(self.exprValues) != 0):
            print(self.exprValues.pop())
        else:
            print(self.boolxValues.pop())

    def visitAssig(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[2])
        if(len(self.exprValues) != 0):
            self.vars[l[0].getText()] = self.exprValues.pop()
        else:
            self.vars[l[0].getText()] = self.boolxValues.pop()

    def visitBoolex(self, ctx):
        l = list(ctx.getChildren())
        if(len(l) == 1):  # NUM o ID
            if(logo3dParser.symbolicNames[l[0].getSymbol().type] == "NUM"):
                self.boolxValues.append(l[0].getText())
            elif (l[0].getText() in self.vars):
                self.boolxValues.append(self.vars[l[0].getText()])
            else:
                print("Exception: Variable used has no value")
                sys.exit()
        elif (l[0].getText() != '('):  # 'normal' boolean expression
            self.level += 1
            self.visit(l[0])
            self.visit(l[2])
            v2 = float(self.boolxValues.pop())
            v1 = float(self.boolxValues.pop())
            self.boolxValues.append(self.boolOp(v1, v2, l[1].getText()))
            self.level -= 1
        else:  # entre parentesis
            self.visit(l[1])

    def visitCond(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[1])
        if(visitor.numToBool(self.boolxValues.pop())):
            self.visit(l[3])
        elif(len(l) > 5):  # if there is an else statement
            self.visit(l[5])

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[1])
        while visitor.numToBool(self.boolxValues.pop()):
            self.visit(l[3])
            self.visit(l[1])

    def visitFor(self, ctx):
        l = list(ctx.getChildren())

        iindex = l[1].getText()

        if(logo3dParser.symbolicNames[l[3].getSymbol().type] == "NUM"):
            self.vars[iindex] = l[3].getText()
        else:
            self.vars[iindex] = self.vars[l[3].getText()]
        if(logo3dParser.symbolicNames[l[5].getSymbol().type] == "NUM"):
            end = int(l[5].getText())
        else:
            end = int(self.vars[l[5].getText()])

        while float(self.vars[iindex]) <= end:
            self.vars[iindex] = float(self.vars[iindex])+1
            self.visit(l[7])

    def visitStat(self, ctx):
        l = list(ctx.getChildren())
        if(len(l) > 0):
            self.visit(l[0])
            self.visit(l[1])

    def visitArg1(self, ctx):
        l = list(ctx.getChildren())
        if(len(l) > 0):
            self.defArgs.append(l[0].getText())
            if(len(l) > 1):
                self.visit(l[2])

    def visitProc(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[3])
        self.defArgs.append(l[6])
        self.funcs[l[1].getText()] = self.defArgs[:]
        self.defArgs.clear()

    def visitArgSimp(self, ctx):
        l = list(ctx.getChildren())
        if(len(l) > 0):
            if(logo3dParser.symbolicNames[l[0].getSymbol().type] == "NUM"):
                self.inArgs.append(l[0].getText())
            else:
                self.inArgs.append(self.vars[l[0].getText()])

            if(len(l) > 1):
                self.visit(l[2])

    def visitArgExpr(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])
        self.inArgs.append(self.exprValues.pop(0))

        if(len(l) > 1):
            self.visit(l[2])

    def visitInvoc(self, ctx):
        l = list(ctx.getChildren())
        funcName = l[0].getText()
        if(funcName in self.funcs):
            funcInfo = self.funcs[funcName][:]
            self.visit(l[2])
            if(len(self.inArgs) == (len(funcInfo)-1)):
                saveVars = dict(self.vars)
                self.vars.clear()
                # posem els valors de els parametres al diccionari de variables
                while len(self.inArgs) > 0:
                    self.vars[funcInfo.pop(0)] = self.inArgs.pop(0)
                self.visit(funcInfo.pop(0))
                self.vars.clear()
                self.vars = dict(saveVars)
                saveVars.clear()

            elif(len(self.inArgs) < (len(funcInfo)-1)):
                print("Exception: There is a missing argument in call to procedure " +
                      funcName+"/"+str(len(funcInfo)-1)+':')
                print("Expected "+str(len(funcInfo)-1)+" and got " +
                      str(len(self.inArgs)))
                sys.exit()
            elif(len(self.inArgs) > (len(funcInfo)-1)):
                print("Exception: There are too many arguments in call to procedure " +
                      funcName+"/"+str(len(funcInfo)-1)+':')
                print("Expected "+str(len(funcInfo)-1)+" and got " +
                      str(len(self.inArgs)))
                sys.exit()

        else:
            self.visit(l[2])
            arg = self.inArgs[:]
            self.inArgs.clear()
            if(funcName == "forward"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.forward(float(arg[0]))
            elif(funcName == "backward"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.backward(float(arg[0]))
            elif(funcName == "right"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.right(float(arg[0]))
            elif(funcName == "left"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.left(float(arg[0]))
            elif(funcName == "up"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.up(float(arg[0]))
            elif(funcName == "down"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.down(float(arg[0]))
            elif(funcName == "hide"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.hide()
            elif(funcName == "show"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.show()
            elif(funcName == "color"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.color(float(arg[0]), float(arg[1]), float(arg[2]))
            elif(funcName == "home"):
                if(not self.turtleIn):
                    self.turtle = Turtle3D()
                    self.turtleIn = True
                self.turtle.home()
            else:
                print("Exception: Procedure "+funcName+" does not exist")
                sys.exit()
