""" The AFN class contains all the necessary properties to describe it and giving a clear print and if desired a graph """

# graphviz allow us to do an AFN grahp
import graphviz

# tabulate allow us to print the properties in a fancy way (it is not elementary)
from tabulate import tabulate

# utils is usefull to rename the sets and prints
from Tools.utils import *

class AFN(object):
    def __init__(self, postfix, name):

        #Process variables
        self.binary_tree    = []
        self.postfix        = postfix
        self.operators      = ['(',')','|','*','?','+','.']
        self.estados_borrar     = []
        self.movement_record    = []

        '''AFN consist of:'''
        #The values of these variables will change

        # Initial state
        self.q_o = None
        # Transition function
        self.delta = {}
        # Input simbols
        self.sigma = []
        # Finite set of states
        self.que = []
        # Acceptence states
        self.F = []

        # AFN and graph properties
        if self.postfix == 'ERROR':
            banner(' AFN is not available ', False)
        else:
            self.transform_postfix_to_afn()
            # finite_automaton_graph(self.F, self.q_o, self.delta,'AFN')
            finite_automaton_graph(self.F, self.q_o, self.delta,str('AFN_' + name))

    # This function allow us to get an AFN from a postfix expression
    def transform_postfix_to_afn(self):

        # STR to LIST postifx
        self.postfix = list(self.postfix)

        # Binary_tree fill
        for symbol in range(len(self.postfix)):
            self.binary_tree.append(AFN_node(self.postfix[symbol],0,0))

        # Lead transition only

        # For every lead transition a new satate is created and a transition
        # in movement record

        for node in self.binary_tree:
            if node.value not in self.operators:
                node.former = 'q'+str(len(self.que))
                node.after = 'q'+str(len(self.que)+1)
                self.que.append('q'+str(len(self.que)))
                self.que.append('q'+str(len(self.que)))
                self.movement_record.append(AFN_tran(node.value, node.former, node.after))

        # Lead plus operators relantions and transitions

        # For every operator there has to be a transition registration
        # And a new states creation

        for node in range(len(self.binary_tree)):
            if self.binary_tree[node].value == '*':

                # Start and End respectively
                self.binary_tree[node].former = 'q'+str(len(self.que))
                self.binary_tree[node].after= 'q'+str(len(self.que)+1)

                # New states
                self.que.append('q'+str(len(self.que)))
                self.que.append('q'+str(len(self.que)))

                # Transitions
                # The end of your child is connected to the beginning of your child
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[0]].after, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # Kleene's start connects to his son's start
                self.movement_record.append(AFN_tran("E",self.binary_tree[node].former, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # The end of his son connects to the end of Kleene
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[0]].after,self.binary_tree[node].after))

                # The start of Klene connects to the end of Kleene
                self.movement_record.append(AFN_tran("E",self.binary_tree[node].former,self.binary_tree[node].after))

                # The sons are already analyzed
                self.binary_tree[child_node(node, self.binary_tree)[0]].analyzed = True

            elif self.binary_tree[node].value == '.':

                # To simulate the merge of a state we need to erase a state and the reconect his transitions too the new states
                self.estados_borrar.append(self.binary_tree[child_node(node, self.binary_tree)[1]].after)

                # Identify the transitions to replicate
                transition_replicate = []
                for transition in self.movement_record:
                    if transition.fin in self.estados_borrar:
                        transition_replicate.append(transition)

                # For every transition identify we reconnect to the initial state of the right child
                for replicate in transition_replicate:
                    self.movement_record.append(AFN_tran(replicate.dato, replicate.inicio, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # We delete the transition of the state erased
                delete_transition=[]
                for transitions in self.movement_record:
                    if transitions.fin in self.estados_borrar:
                        delete_transition.append(transitions)

                    if transitions.inicio in self.estados_borrar:
                        delete_transition.append(transitions)
                for x in delete_transition:
                    if x in self.movement_record:
                        self.movement_record.remove(x)

                # Start and end of node
                self.binary_tree[node].former = self.binary_tree[child_node(node, self.binary_tree)[1]].former
                self.binary_tree[node].after = self.binary_tree[child_node(node, self.binary_tree)[0]].after

                # The childs are already analyzed
                self.binary_tree[child_node(node, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(node, self.binary_tree)[0]].analyzed = True

            elif self.binary_tree[node].value == '|':

                # Start and end of node
                self.binary_tree[node].former = 'q'+str(len(self.que))
                self.binary_tree[node].after = 'q'+str(len(self.que) + 1)
                self.que.append('q'+str(len(self.que)))
                self.que.append('q'+str(len(self.que)))

                # Register transitions
                # The beginning of or connects to the beginnings of its children
                self.movement_record.append(AFN_tran("E",self.binary_tree[node].former, self.binary_tree[child_node(node, self.binary_tree)[1]].former))
                self.movement_record.append(AFN_tran("E",self.binary_tree[node].former, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # The endings of its children connect to the ending of or
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[1]].after,self.binary_tree[node].after))
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[0]].after,self.binary_tree[node].after))

                # Mark that it was already visited
                self.binary_tree[child_node(node, self.binary_tree)[1]].analyzed = True
                self.binary_tree[child_node(node, self.binary_tree)[0]].analyzed = True

            elif self.binary_tree[node].value == '+':

                # Start and End respectively
                self.binary_tree[node].former = 'q'+str(len(self.que))
                self.binary_tree[node].after= 'q'+str(len(self.que)+1)

                # New states
                self.que.append('q'+str(len(self.que)))
                self.que.append('q'+str(len(self.que)))

                # Transitions
                # The end of your child is connected to the beginning of your child
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[0]].after, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # Plus start connects to his son's start
                self.movement_record.append(AFN_tran("E",self.binary_tree[node].former, self.binary_tree[child_node(node, self.binary_tree)[0]].former))

                # The end of his son connects to the end of Pluss
                self.movement_record.append(AFN_tran("E",self.binary_tree[child_node(node, self.binary_tree)[0]].after,self.binary_tree[node].after))

                #The child is already analyzed
                self.binary_tree[child_node(node, self.binary_tree)[0]].analyzed = True

        # We finally eliminate from que the states identified in a concatenation
        for elemento in self.estados_borrar:
            if elemento in self.que:
                self.que.remove(elemento)

        # Temporary alphabet
        for x in self.postfix:
            if x not in self.operators:
                self.sigma.append(x)
        self.sigma.append('E')

        # Reads movements from movement_record and stores them in self.delta
        for x in self.que:
            self.delta[x] = {}
        for x in self.delta:
            for letra in self.sigma:
                self.delta[x][letra] = []
        for x in self.delta:
            for letra in self.sigma:
                for tran in self.movement_record:
                    if x == tran.inicio and tran.dato == letra:
                        self.delta[x][letra].append(tran.fin)

        # We register the final state
        self.F.append(self.binary_tree[-1].after)

        # And the initial state
        self.q_o = self.binary_tree[-1].former

        # Self.delta and self.sigma cleaning
        while True:
            duplicado = False
            for elemento in self.sigma:
                if self.sigma.count(elemento) > 1:
                    self.sigma.remove(elemento)
                    duplicado = True
            if not duplicado:
                break
        for clave, valor in self.delta.items():
            for clave2, valor2 in valor.items():
                valor[clave2] = list(set(valor2))

        self.sigma.remove('E')

        """AFN FINAL RESULTS"""

        banner(' AFN final results ')


        """ Fancy prints with tabulate"""

        finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta)

        """ Final prints without tabulate"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta,False)


""" AFN_node is a class that allow us to have a
summary of the properties of each characther
in the postfix expression"""

class AFN_node:
    def __init__(self, value, former, after):

        self.after = after
        self.value = value
        self.former = former
        self.analyzed = False

    # Easy print of AFN_node
    def __str__(self):
        return f'Value -> {self.value}  Antes -> {self.former}  Despues -> {self.after}'

# AFN_tran allow us to save a transition in our
# movement_record that later will be our
# summary of transitions (delta)
class AFN_tran:
    def __init__(self, dato, inicio, fin):

        self.dato = dato
        self.inicio = inicio
        self.fin = fin

    # Easy print on AFN_tran
    def __str__(self):
        return f'{self.inicio}  --> {self.dato} --> {self.fin}'