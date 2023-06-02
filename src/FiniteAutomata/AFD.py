""" The AFN class contains all the necessary properties to describe an AFD"""
# graphviz allow us to do an AFN grahp
import graphviz

# tabulate allow us to print the properties in a fancy way (it is not elementary)
from tabulate import tabulate

# utils is usefull to rename the sets and prints
from Tools.utils import *

class AFD_from_AFN(object):
    def __init__(self, AFN):
        self.unmarked   = []
        self.asignacion = {}
        self.AFN        = AFN
        self.postfix    = self.AFN.postfix
        '''AFD consist of:'''
        #The values of these variables will change

        # Initial state
        self.q_o    = None
        # Transition function
        self.delta  = {}
        # Input simbols
        self.sigma  = []
        # Finite set of states
        self.que    = []
        # Acceptence states
        self.F      = []

        # AFD and graph properties

        if self.AFN.postfix == 'ERROR':
            banner(' AFD from AFN not available ', False)
        else:
            self.transform_afn_to_afd()
            finite_automaton_graph(self.F, self.q_o, self.delta,'AFD_from_AFN')


    def transform_afn_to_afd(self):

        # Initial state from AFN q_o
        self.q_o = E_closure([self.AFN.q_o], self.AFN.delta)

        # Existing states
        self.que.append(self.q_o)

        # Both alphabets are equal
        self.sigma = self.AFN.sigma

        # Filling the transition function
        self.delta = {str(state): {} for state in self.que}
        self.delta = {x: {letra: [] for letra in self.sigma} for x in self.delta}

        # Unmarked states as the Dragon books says
        self.unmarked.append(self.q_o)

        # Subset construcion logic
        while len(self.unmarked) != 0:
            actual_state = self.unmarked.pop()
            for Symbol in self.sigma:
                U = E_closure(move(actual_state, Symbol, self.AFN.delta), self.AFN.delta)
                if U not in self.que and str(U) != 'set()':
                    self.que.append(U)
                    self.delta[str(U)] = {}
                    for letra in self.sigma:
                        self.delta[str(U)][letra] = []
                    self.unmarked.append(U)
                if str(U) != 'set()':
                    self.delta[str(actual_state)][Symbol].append(str(U))

        # Final state
        self.F = [state for state in self.que if any(acceptance_state in state for acceptance_state in self.AFN.F)]

        # Easy read
        self.asignacion = {str(state): letter_rename(position) for position, state in enumerate(self.que)}
        self.que        = [self.asignacion[str(state)] for state in self.que]
        self.F          = [self.asignacion[str(state)] for state in self.F]
        self.q_o        = self.asignacion[str(self.q_o)]
        self.delta = {self.asignacion[str(conjunto)]: {k: [self.asignacion[s] if s in self.asignacion else s for s in v] for k, v in valores.items()} for conjunto, valores in self.delta.items()}
        self.delta = dict(sorted(self.delta.items(), key=lambda x: x[0]))

        """AFD from AFN FINAL RESULTS"""

        banner(' AFD from AFN final results ')

        """ Fancy prints with tabulate"""

        finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta)

        """ Final prints without tabulate"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta,False)

class Direct_AFD(object):
    def __init__(self,postfix, name):

        #Process variables
        self.binary_tree        = []
        self.followpost_table   = []
        self.numeral_id         = []
        self.postfix            = postfix
        self.numbering_exceptions   = list("*|.?+")
        self.temporal_transitions   = []
        self.asignacion = {}

        self.Id_designation = {}
        self.F_designation = {}

        '''AFD consist of:'''
        #The values of these variables will change

        # Initial state
        self.q_o = None
        # Transition function
        self.delta = {}
        # Input simbols
        self.sigma = set()
        # Finite set of states
        self.que = []
        # Acceptence states
        self.F = []

        # AFD and graph properties
        if self.postfix == 'ERROR':

            banner(' AFD is not available ', False)

        else:

            # self.postfix.append('#')
            # self.postfix.append('.')
            print(f'AFD Postfix -> {self.postfix}\n')
            self.transform_postfix_to_afd()
            # finite_automaton_graph(self.F, self.q_o, self.delta,'Direct_AFD')
            finite_automaton_graph(self.F, self.q_o, self.delta,str('Direct_AFD_' + name))

    def transform_postfix_to_afd(self):

        self.postfix = list(self.postfix)

        # Binary_tree fill
        for symbol in range(len(self.postfix)):
            self.binary_tree.append(AFD_node(self.postfix[symbol]))

        # Enumerate principal leafs and firstpos, lastpos, nullable and followpos_table
        initial_id = 1
        for leaf in self.binary_tree:
            if leaf.value not in self.numbering_exceptions:
                leaf.id = initial_id
                leaf.nullable = False
                leaf.firstpos.add(initial_id)
                leaf.lastpos.add(initial_id)
                self.followpost_table.append(AFD_followpos(leaf.value, initial_id))
                if '#' in leaf.value:
                    self.numeral_id.append(str(initial_id))
                    self.Id_designation[initial_id] = leaf.value.replace('#','')
                initial_id += 1
            if leaf.value == '':
                leaf.nullable = True

        # for key, value in self.Id_designation.items():
        #     print(key,value)

        # Nullable function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.nullable = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '+':
                leaf.nullable = self.binary_tree[child_node(position, self.binary_tree)[0]].nullable
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '|':
                leaf.nullable = self.binary_tree[child_node(position, self.binary_tree)[1]].nullable or self.binary_tree[child_node(position, self.binary_tree)[0]].nullable
                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                # print('\nPosicion', self.binary_tree[position])
                # print('A', self.binary_tree[position-1])
                # print('B', self.binary_tree[position-2])
                # print('hijos nulable')
                # # print(self.binary_tree[child_node(position, self.binary_tree)[1]].nullable)
                # print(self.binary_tree[child_node(position, self.binary_tree)[0]].nullable)


                leaf.nullable = self.binary_tree[child_node(position, self.binary_tree)[1]].nullable and self.binary_tree[child_node(position, self.binary_tree)[0]].nullable
                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

        # print('-'*10)
        # for leaf in self.binary_tree:
        #     print(leaf)

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False

        # Firstpos function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.firstpos = self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '+':
                leaf.firstpos = self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '|':
                leaf.firstpos = self.binary_tree[child_node(position, self.binary_tree)[1]].firstpos | self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos
                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                if self.binary_tree[child_node(position, self.binary_tree)[1]].nullable == True:
                    leaf.firstpos = self.binary_tree[child_node(position, self.binary_tree)[1]].firstpos  | self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos
                    self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True
                else:
                    leaf.firstpos = self.binary_tree[child_node(position, self.binary_tree)[1]].firstpos
                    self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False


        # Lastpos function

        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                leaf.lastpos = self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '+':
                leaf.lastpos = self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '|':
                leaf.lastpos = self.binary_tree[child_node(position, self.binary_tree)[1]].lastpos | self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                if self.binary_tree[child_node(position, self.binary_tree)[0]].nullable == True:
                    leaf.lastpos = self.binary_tree[child_node(position, self.binary_tree)[1]].lastpos  | self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                    self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True
                else:
                    leaf.lastpos = self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                    self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                    self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

        # Cleaning binary_tree
        for leaf in self.binary_tree:
            leaf.analyzed = False

        # Binary Tree
        # print(f'--> Binary Tree:')
        # for leaf in self.binary_tree:
        #     print(leaf)

        # Followpos function
        for position, leaf in enumerate(self.binary_tree):
            if leaf.value == '*':
                A = self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                B = self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos

                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

                for f_row in self.followpost_table:
                    if f_row.id in A:
                        f_row.followpos = f_row.followpos | B

            elif leaf.value == '+':
                A = self.binary_tree[child_node(position, self.binary_tree)[0]].lastpos
                B = self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos

                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

                for f_row in self.followpost_table:
                    if f_row.id in A:
                        f_row.followpos = f_row.followpos | B

            elif leaf.value == '|':
                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

            elif leaf.value == '.':
                A = self.binary_tree[child_node(position, self.binary_tree)[1]].lastpos
                B = self.binary_tree[child_node(position, self.binary_tree)[0]].firstpos

                self.binary_tree[child_node(position, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(position, self.binary_tree)[0]].analyzed = True

                for f_row in self.followpost_table:
                    if f_row.id in A:
                        f_row.followpos = f_row.followpos | B

        # print(f'\n--> Followpos table:')
        # for f_row in self.followpost_table:
        #     print(f_row)



        # Alfabeto
        for char in self.postfix:
            if char not in self.numbering_exceptions and char != '#':
                self.sigma.add(char)

        self.sigma = list(self.sigma)

        # Transition function
        # self.delta.append(AFD_row(self.binary_tree[-1].firstpos,self.followpost_table, self.sigma))


        # print('\nTransiton creation\n')

        already_registrated = []
        already_registrated.append(self.binary_tree[-1].firstpos)
        self.q_o = str(self.binary_tree[-1].firstpos)
        self.que.append(str(self.binary_tree[-1].firstpos))

        while len(already_registrated) != 0:
            self.temporal_transitions.append(AFD_row(already_registrated.pop(), self.followpost_table, self.sigma))

            for p_new_state in self.temporal_transitions[-1].different_states:
                if str(p_new_state) != 'set()':
                    if str(p_new_state) not in self.que and p_new_state not in already_registrated:
                        already_registrated.append(p_new_state)
                        self.que.append(str(p_new_state))

        for transition in self.temporal_transitions:
            self.delta[str(transition.state)] = {}
        for state in self.delta:
            for letter in self.sigma:
                self.delta[state][letter] = []


        for afd_row in self.delta:
            for transition in self.temporal_transitions:
                if str(transition.state) == afd_row:
                    for letter in self.sigma:
                        if str(transition.transitions[letter]) != 'set()':
                            self.delta[afd_row][letter].append(str(transition.transitions[letter]))

        for afd_row in self.delta:
            temp = afd_row.replace("{", "").replace("}", "").replace("'", "").replace(" ", "")
            set_temp = set(temp.split(","))
            for state in set_temp:
                if state in self.numeral_id:
                    self.F.append(afd_row)

        for key in self.F:
            for state, name in self.Id_designation.items():
                if str(state) in key:
                    self.F_designation[key] = name
        # print('-'*10)

        # for x,y in self.F_designation.items():
        #     print(x,y)


        # Pasar de numeros a letras
        # Name reasignation

        for position, state in enumerate(self.que):
            self.asignacion[str(state)] = letter_rename(position)

        print()
        print(self.asignacion)
        print()

        self.que    = [self.asignacion[str(state)] for state in self.que]
        self.F      = [self.asignacion[str(state)] for state in self.F]
        self.q_o    = self.asignacion[str(self.q_o)]

        tempora_ld = {}
        for state,Id in self.F_designation.items():
            tempora_ld[self.asignacion[str(state)]] = Id

        # for x, y in tempora_ld.items():
        #     print(x,y)

        self.F_designation = tempora_ld

        delta_letras = {}
        for conjunto, valores in self.delta.items():
            letra = self.asignacion[str(conjunto)]
            valores_letras = {}
            for k, v in valores.items():
                valores_letras[k] = [self.asignacion[s] if s in self.asignacion else s for s in v]
            delta_letras[letra] = valores_letras
        self.delta = delta_letras
        self.delta = dict(sorted(self.delta.items(), key=lambda x: x[0]))

        """AFD FINAL RESULTS"""

        banner(' Direct AFD final results ')

        """ Fancy prints with tabulate (No delta)"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta, None)

        """ Fancy prints with tabulate"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta)

        """ Final prints without tabulate"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta,False)

class AFD_row(object):
    def __init__(self, state, f_table, sigma):

        self.f_table    = f_table
        self.alphabet   = sigma
        self.different_states  = []
        self.state      = state
        self.transitions    = {}
        self.states_values = []

        for char in self.alphabet:
            self.transitions[char] = set()

        for state in self.state:
            for f_row in self.f_table:
                if state == f_row.id:
                    self.states_values.append(f_row)

        for char in self.alphabet:
            for state_value in self.states_values:
                if char == state_value.value:
                    self.transitions[char] = self.transitions[char] | state_value.followpos

        for tran in self.transitions:
            if self.transitions[tran] != self.state and str(self.transitions[tran] != 'set()'):
                self.different_states.append(self.transitions[tran])

        # Remove duplicate elements
        self.different_states = list(set([tuple(element) for element in self.different_states]))
        self.different_states = [set(element) for element in self.different_states]


    def __str__(self):
        return f"Estado: {self.state} Transitions:{self.transitions}"

class AFD_node(object):

    def __init__(self, value, id=None):

        self.id         = id
        self.value      = value
        self.nullable   = None
        self.firstpos   = set([])
        self.lastpos    = set([])
        self.analyzed   = False

    def __str__(self):

        cadena="Id:" +str(self.id)+"\t\t"+self.value+"\t\tNullable:" +str(self.nullable)+"\t\tFirstpos:" +str(self.firstpos)+"\t\tLastpos:" +str(self.lastpos)
        return cadena

class AFD_followpos(object):
    def __init__(self,value,id):
        self.id         = id
        self.value      = value
        self.followpos = set([])

    def __str__(self):
        return f" Id: {self.id}\tValue: {self.value}\tFollowpos: {self.followpos}"


