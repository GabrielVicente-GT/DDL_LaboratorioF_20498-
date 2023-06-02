""" The InfixToPostfix class serves the purpose of its name, going through cleanup and error identification. """

class InfixToPostfix(object):
    def __init__(self, regex):
        # InfixToPostfix variables and final result
        self.regex          = regex
        self.issues         = []
        self.postfix        = ''
        self.regex_array    = []
        self.postfix_operators      = ['(','.','|',')']
        self.regex_operators_ni     = ['(',')','|','*','?','+']
        self.postfix_stack  = []

        # InfixToPostfix process
        self.clean_regex()
        self.error_handling_regex()

        # Transform if it is possible
        if self.postfix != 'ERROR':
            self.transform_regex()


    def clean_regex(self):

        # Remove whitespace
        self.regex = self.regex.replace(' ','')

        # Add '.' between each character
        self.regex = '.'.join([caracter for caracter in self.regex])

        # STR to LIST transformation
        self.regex = list(self.regex)

        # Each one of the points is evaluated and depending on the situation, it is left or replaced by a blank space.
        for symbol, char in enumerate(self.regex):
            if char == '.' and 0 < symbol < len(self.regex) - 1:
                prev_char = self.regex[symbol - 1]
                next_char = self.regex[symbol + 1]
                if prev_char not in self.regex_operators_ni and next_char not in self.regex_operators_ni:
                    self.regex[symbol] = '.'
                elif prev_char == '*' and next_char not in self.regex_operators_ni:
                    self.regex[symbol] = '.'
                elif prev_char == '*' and next_char == '(':
                    self.regex[symbol] = '.'
                elif prev_char == '+' and next_char not in self.regex_operators_ni:
                    self.regex[symbol] = '.'
                elif prev_char == '+' and next_char == '(':
                    self.regex[symbol] = '.'
                elif prev_char == ')' and next_char not in self.regex_operators_ni:
                    self.regex[symbol] = '.'
                elif prev_char == '?' and next_char not in self.regex_operators_ni:
                    self.regex[symbol] = '.'
                elif prev_char == '?' and next_char == '(':
                    self.regex[symbol] = '.'
                elif prev_char not in self.regex_operators_ni and next_char == '(':
                    self.regex[symbol] = '.'
                elif prev_char == ')' and next_char == '(':
                    self.regex[symbol] = '.'
                else:
                    self.regex[symbol] = ''
        self.regex = ''.join(self.regex)

        # Add parentheses at the beginning and the end
        self.regex = '('+self.regex+')'

    def error_handling_regex(self):
        # STR to LIST transformation
        self.regex = list(self.regex)

        # Parenthesis count
        left = 0
        right = 0
        for symbol, char in enumerate(self.regex):
                if char == ')':
                    right += 1
                elif char == '(':
                    left += 1
        if left != right:
            self.postfix = 'ERROR'
            self.issues.append('\n\t*\tClose all parenthesis')
        # Operators
        binary_operators = ['.','|']
        singular_operators = ['+','?','*']

        # Binary operators error handling
        for symbol, char in enumerate(self.regex):
            if char in binary_operators and 0 < symbol < len(self.regex) - 1:
                prev_char = self.regex[symbol - 1]
                next_char = self.regex[symbol + 1]
                if next_char == ')':
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tBinary operator missing right child')
                elif prev_char == '(':
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tBinary operator missing left child')
                elif next_char in binary_operators or next_char in singular_operators:
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tBinary operator missing right child')


        # Singular operators error handling
        for symbol, char in enumerate(self.regex):
            if char in singular_operators and 0 < symbol < len(self.regex) - 1:
                prev_char = self.regex[symbol - 1]
                next_char = self.regex[symbol + 1]
                if prev_char == '(':
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tSingular operator missing child (left)')
        # Empty agrupation key
        for symbol, char in enumerate(self.regex):
            if char == ')'and 0 < symbol < len(self.regex) - 1:
                prev_char = self.regex[symbol - 1]
                next_char = self.regex[symbol + 1]
                if prev_char == '(' and next_char in singular_operators:
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tSingular operator empty child (left)')
        for symbol, char in enumerate(self.regex):
            if char == '('and 0 < symbol < len(self.regex) - 1:
                prev_char = self.regex[symbol - 1]
                next_char = self.regex[symbol + 1]
                if next_char == ')':
                    self.postfix = 'ERROR'
                    self.issues.append('\n\t*\tEmpty value not valid')


        # Empty regex
        if self.regex == ['(',')']:
            self.postfix = 'ERROR'
            self.issues.append('\n\t*\tEmpty value not valid')

        self.regex = ''.join(self.regex)


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

        # STR to LIST regex
        self.regex = list(self.regex)

        # regex_array fill (needed for postfix logic)
        for symbol in self.regex:
            self.regex_array.append(Nodo(symbol))

        # POSTFIX LOGIC (inspired in the shunting yard algorithm)
        for nodo in self.regex_array:

            # If not a operator is going to the stack
            if nodo.value not in self.postfix_operators:
                self.postfix += nodo.value

            # If the character read is a left parenthesis it is added to the stack
            elif nodo.value == '(':
                self.postfix_stack.append(nodo.value)

            # If the character read corresponds to a right parenthesis, all the operators
            # inside the self.postfix_stack are added to the postfix expression until its
            # left parenthesis is found and inside the self.postfix_stack all the parentheses
            # used and operators added to the expression are removed

            elif nodo.value == ')':
                while(self.postfix_stack[-1] !='('):
                    self.postfix += self.postfix_stack.pop()
                self.postfix_stack.pop()

            # If the read character is an operation, using the priority function, if the priority of
            # the read character is greater than the priority of the operator on top of the self.postfix_stack,
            # the read character is added to the postfix, otherwise, the operator is added on the top of the
            # self.postfix_stack to the postfix and the read character is added to the self.postfix_stack
            else:
                if len(self.postfix_stack)==0:
                    self.postfix_stack.append(nodo.value)
                else:
                    if self.priority(nodo.value, self.postfix_stack[-1]) == 1 or self.priority(nodo.value, self.postfix_stack[-1]) == -1:
                        self.postfix_stack.append(nodo.value)

                    elif self.priority(nodo.value, self.postfix_stack[-1]) == 0 :
                        self.postfix += self.postfix_stack.pop()
                        self.postfix_stack += nodo.value

        # replacing ? by or epsilon
        self.postfix = self.postfix.replace('?','E|')

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