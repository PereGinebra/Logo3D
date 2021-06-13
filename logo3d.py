from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import visitor
import sys

input_stream = FileStream(sys.argv[1])

lexer = logo3dLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = logo3dParser(token_stream)
tree = parser.root()
# print(tree.toStringTree(recog=parser))

args = sys.argv[2:]
visit = visitor()
visit.visit(tree)
visit.doFunction(args)
sys.exit()
