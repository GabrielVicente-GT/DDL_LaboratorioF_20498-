"""
Clase que permite realizar la minimización de un AFD a partir de obtener su quintupla
Referencia: https://users.exa.unicen.edu.ar/catedras/ccomp1/ClaseAFNDMinimizacion.pdf
"""
# utils is usefull to rename the sets and prints
from Tools.utils import *

class AFD_min(object):
    def __init__(self, AFD, name):

        self.AFD = AFD
        self.delta_minimizated = []
        self.partition_existence = []
        self.delta_transformation = []
        self.length_part = 0

        ''' AFD min consist of:'''
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

        if self.AFD.postfix == 'ERROR':
            banner(' Min AFD not available ', False)
        else:
            self.transform_afd_to_afd_min()
            finite_automaton_graph(self.F, self.q_o, self.delta,str('AFD_min_' + name))

    def transform_afd_to_afd_min(self):

        # The sigmas are equal for AFD and AFD minimized
        self.sigma = self.AFD.sigma

        # We stater the proces to minimize an AFD until the partition is no longer valid
        self.delta_transformation = [[key1, key2, val] for key1, value1 in self.AFD.delta.items() for key2, value2 in value1.items() for val in value2]

        # We made de initial partition separation between acceptance states and not acceptances states
        self.partition_existence.append(self.AFD.F)
        self.partition_existence.append([state for state in self.AFD.que if state not in self.AFD.F])

        # Minimiza algorith by reference

        self.purificacion = True

        while (self.purificacion):

            if self.length_part == len(self.partition_existence):
                self.purificacion = False
            else:
                self.length_part = len(self.partition_existence)
                for partition in range(len(self.partition_existence)):
                    self.tran_register = []
                    if len(self.partition_existence[partition]) >= 2:
                        for state in self.partition_existence[partition]:
                            self.cohorte_state = [state]
                            for delta_row in self.delta_transformation:
                                for symbol in self.sigma:
                                    if (symbol, delta_row[0]) == (delta_row[1], state):
                                        self.transition_goes_to = [symbol]
                                        for w, partition_value in enumerate(self.partition_existence):
                                            if delta_row[2] in partition_value:
                                                self.transition_goes_to.append(w)
                                                self.cohorte_state.append(self.transition_goes_to)
                            self.tran_register.append(self.cohorte_state) if self.cohorte_state not in self.tran_register else None
                        self.state_align = {}
                        [self.state_align.setdefault(tuple(sorted([str(new_tran_state_symbol[0])+str(new_tran_state_symbol[1]) for new_tran_state_symbol in tran_row_new[1:]])), []).append(tran_row_new[0]) for tran_row_new in self.tran_register]
                        self.partition_existence[partition:partition+1] = self.state_align.values()

                self.partition_existence = [partition_value for partition_value in self.partition_existence if partition_value != []]

        self.delta_minimizated = cleaning_process(self.sigma, self.partition_existence,self.delta_transformation,self.delta_minimizated)

        # Filling AF variables
        # Acceptances state and final state

        for transition in self.delta_minimizated:
            self.que.extend([state for state in transition[::2] if state not in self.que])

        # Final delta
        for clave1, clave2, valor in self.delta_minimizated:
            self.delta.setdefault(clave1, {})[clave2] = [valor]

        for letra in self.sigma:
            for key, value in self.delta.items():
                value.setdefault(letra, [])

        for state in self.que:
            if state not in self.delta:
                self.delta[state] = {}
        for state in self.delta:
            if self.delta[state] == {}:
                for letter in self.sigma:
                    self.delta[state][letter] = []
        self.F = [item[0] for item in self.partition_existence if any(x in self.AFD.F for x in item)]
        self.q_o = [item[0] for item in self.partition_existence if any(x == self.AFD.q_o for x in item)][0]
        self.delta = dict(sorted(self.delta.items(), key=lambda x: x[0]))


        """AFD minimized FINAL RESULTS"""

        banner(' AFD minimized results ')

        """ Fancy prints with tabulate"""

        finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta)

        """ Final prints without tabulate"""

        # finite_automaton_results(self.que, self.sigma, self.F, self.q_o, self.delta, False)
