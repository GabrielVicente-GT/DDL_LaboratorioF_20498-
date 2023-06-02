""" The InfixToPostfix class serves the purpose of its name, going through cleanup and error identification. """
from Tools.utils import *

class InfixToPostfix(object):
    def __init__(self, regex):
        # InfixToPostfix variables and final result
        self.regex          = regex
        self.issues         = []
        self.postfix        = []
        self.regex_array    = []
        self.postfix_operators      = ['(','.','|',')']
        self.regex_operators_ni     = ['(',')','|','*','?','+']
        self.postfix_stack  = []

        # Transform if it is possible
        if 'ERROR' not in self.regex:
            self.transform_regex()
        else:
            banner(' Tree not available ', False)
            self.postfix.append('ERROR')

    # Function needed for postfix logic
    def priority(self, operando, pilalast):
        valor = -1
        if operando== '.' and pilalast == '|':
            valor = 1
        elif pilalast == '.' and operando == '|':
            valor = 0
        elif pilalast == operando:
            valor = 0

        return valor

    # Transformation infix to postfix
    def transform_regex(self):

        # regex_array fill (needed for postfix logic)
        for symbol in self.regex:
            self.regex_array.append(symbol)

        # POSTFIX LOGIC (inspired in the shunting yard algorithm)
        for nodo in self.regex_array:
            # If not a operator is going to the stack
            if nodo not in self.postfix_operators:
                self.postfix.append(nodo)

            # If the character read is a left parenthesis it is added to the stack
            elif nodo == '(':
                self.postfix_stack.append(nodo)

            # If the character read corresponds to a right parenthesis, all the operators
            # inside the self.postfix_stack are added to the postfix expression until its
            # left parenthesis is found and inside the self.postfix_stack all the parentheses
            # used and operators added to the expression are removed

            elif nodo == ')':
                while(self.postfix_stack[-1] !='('):
                    self.postfix.append(self.postfix_stack.pop())
                self.postfix_stack.pop()

            # If the read character is an operation, using the priority function, if the priority of
            # the read character is greater than the priority of the operator on top of the self.postfix_stack,
            # the read character is added to the postfix, otherwise, the operator is added on the top of the
            # self.postfix_stack to the postfix and the read character is added to the self.postfix_stack
            else:
                if len(self.postfix_stack)==0:
                    self.postfix_stack.append(nodo)
                else:
                    if self.priority(nodo, self.postfix_stack[-1]) == 1 or self.priority(nodo, self.postfix_stack[-1]) == -1:
                        self.postfix_stack.append(nodo)

                    elif self.priority(nodo, self.postfix_stack[-1]) == 0 :
                        self.postfix += self.postfix_stack.pop()
                        self.postfix_stack += nodo


        temporal_postfix = []
        for position, value in enumerate(self.postfix):
            if value == '?':
                temporal_postfix.append('E')
                temporal_postfix.append('|')
            else:
                temporal_postfix.append(value)
        self.postfix = temporal_postfix
        # replacing ? by or epsilon
        # for i in range(len(self.postfix)):
        #     if "?" in self.postfix[i]:
        #         self.postfix[i] = self.postfix[i].replace("?", "?")

        # Regex transformation to original
        self.regex = ''.join(self.regex)

    # Easy print of InfixToPostfix class
    def __str__(self):

        if self.postfix == 'ERROR':
            cadena = f'Regex -> {self.regex} || Postfix -> {self.postfix}\n\n{"─"*117}\n{"─"*50}REGEX HAS ISSUES{"─"*51}\n{"─"*117}\n\n --> Handle the next problems:'
            for mistake in self.issues:
                cadena = cadena + mistake
        else:
            cadena = f'Regex -> {self.regex} || Postfix -> {self.postfix}'
        return cadena

# Nodo Class that will be useful later
class Nodo:

    # Value and ASCII value
    def __init__(self, value):

        self.value = value
        self.ascii_value = ord(value)

    # Easy print on Nodo class
    def __str__(self):
        return f'Valor -> {self.value} ASCII -> {self.ascii_value}'