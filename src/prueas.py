grammar = [['expression`', '-->', 'expression'], ['expression', '-->', 'expression', 'PLUS', 'term'], ['expression', '-->', 'term'], ['term', '-->', 'term', 'TIMES', 'factor'], ['term', '-->', 'factor'], ['factor', '-->', 'LPAREN', 'expression', 'RPAREN'], ['factor', '-->', 'ID']]
terminals = ['ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN']

from Tools.utils import *

z = FOLLOW('expression', grammar, 'expression`', terminals)

print(z)