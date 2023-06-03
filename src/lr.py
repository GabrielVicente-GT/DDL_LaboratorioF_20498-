import json
from tabulate import tabulate
from Tools.utils import *
from Tools.ReadingYal import *
# Leyendo json

class LR_0(object):
    def __init__(self, name):
        self.name = name
        self.data = None
        self.grammar = []
        self.terminals = []
        self.clean_yapar = []
        self.dot_grammar = []
        self.augmented_grammar = []
        self.reading_comment = False
        self.continue_process = True
        self.F_identificator = None
        self.augmented_grammar_reserved = []
        self.tokens_yalex = str(Reader(self.name+".yal", False).bracket_programation)
        self.terminals_dictionari = Reader(self.name+".yal", False).bracket_programation
        self.faltantes = []
        self.asignation = {}
        self.asignation_reversed = {}
        self.final_state = None

        self.que = []
        self.delta = {}
        self.sigma = set()
        self.unmarked = []



        with open('./src/output.json') as f:
            self.data = json.load(f)

        """ Quitando comentarios """
        for llave, valor in self.data.items():
            if self.reading_comment:
                if valor == "'*/'":
                    self.reading_comment = False
            else:
                if valor == "'/*'":
                    self.reading_comment = True
                elif valor == 'ws':
                    pass
                else:
                    self.clean_yapar.append([llave, valor])

        """Tokens obtenidos del yapar"""

        for position, token in enumerate(self.clean_yapar):
            if self.clean_yapar[position][1] == "'%token'":
                for next_pos in range(position + 1, len(self.clean_yapar)):
                    if self.clean_yapar[next_pos][1] != "terminal":
                        break
                    self.terminals.append(self.clean_yapar[next_pos][0].strip("'").split(' IN')[0])

        """Verificacion con yalex"""
        for x in self.terminals:
            if x != 'IGNORE':
                if x not in self.tokens_yalex:
                    self.continue_process = False
                    self.faltantes.append(x)
            else:
                self.terminals.remove('IGNORE')

        if self.continue_process == True:

            """Terminales encontrados para corroborar en yalex"""

            print(self.clean_yapar)

            for position, token in enumerate(self.clean_yapar):
                if self.clean_yapar[position][1] == "nts":
                    # print(self.clean_yapar[position+1])
                    if position +1< len(self.clean_yapar):
                        if self.clean_yapar[position + 1][1] == "':'":
                            production = []
                            production.append(self.clean_yapar[position][0].strip("'").split(' IN')[0])
                            production.append("-->")
                            for next_pos in range(position + 2, len(self.clean_yapar)):
                                if self.clean_yapar[next_pos][1] == "';'":
                                    break
                                elif self.clean_yapar[next_pos][1] == "MT" and "|" in self.clean_yapar[next_pos][0]:
                                    production.append("|")
                                else:
                                    production.append(self.clean_yapar[next_pos][0].strip("'").split(' IN')[0])
                            self.grammar.append(production)

            """Gramatica del yapal"""

            for position, production in enumerate(self.grammar):
                head = self.grammar[position][0]
                arr = self.grammar[position][2:]
                result = []
                temp = []
                for item in arr:
                    if item == '|':
                        result.append(temp)
                        temp = []
                    else:
                        temp.append(item)
                if temp:
                    result.append(temp)
                for x in result:
                    x.insert(0, '-->')
                    x.insert(0, head)
                for x in result:
                    self.augmented_grammar.append(x)

            self.augmented_grammar.insert(0, [self.grammar[0][0] + '`', '-->',self.grammar[0][0] ])

            """Impresion de gramatica aumentada"""
            print()
            banner(f" Gramatica aumentada para LR(0) ", False)

            # print(self.augmented_grammar)

            for x in self.augmented_grammar:
                print(f"{x[0]} {' '.join(x[1:])}")

            # print('xxx')

            for x in self.augmented_grammar:
                self.augmented_grammar_reserved.append(x)
            # print(self.augmented_grammar_reserved)

            for x in self.augmented_grammar:
                y=[]
                for w in x:
                    y.append(w)
                y.insert(2,'.')
                self.dot_grammar.append(y)

            """ Creacion de la funcion de transicion para LR(0)"""
            for x in self.terminals:
                self.sigma.add(x)

            self.sigma.add("$")

            for x in self.grammar:
                self.sigma.add(x[0])


            self.que.append(CLOUSURE([self.dot_grammar[0]], self.dot_grammar))
            self.delta = {str(state): {} for state in self.que}
            self.delta = {x: {letra: [] for letra in self.sigma} for x in self.delta}

            self.unmarked.append(self.que[0])

            while len(self.unmarked) != 0:
                actual_state = self.unmarked.pop()
                for Symbol in self.sigma:
                    U = GOTO(actual_state, Symbol, self.dot_grammar)

                    if U not in self.que and str(U) != '[]':
                        # print(f"type({type(U)})")
                        # print(f"str({str(U)})")
                        self.que.append(U)
                        self.delta[str(U)] = {}
                        for letra in self.sigma:
                            self.delta[str(U)][letra] = []
                        self.unmarked.append(U)
                    if str(U) != '[]':
                        self.delta[str(actual_state)][Symbol].append(str(U))

            self.F_identificator = MoveDot(self.dot_grammar[0])
            self.F_identificator = str(self.F_identificator)

            """ Graficar LR(0)"""
            grafo = graphviz.Digraph(name="LR(0)")
            def ats(s):
                return s.replace('], [', ']\n[')

            temp_que = []

            for x in self.que:
                temp_que.append(str(x))

            contador = 0
            for x, y in self.delta.items():
                grafo.node(ats(x), label= f"I_{contador}\n\n{ats(x)}" , shape = "box")
                self.asignation_reversed[str(contador)] = self.que[temp_que.index(str(x))]
                self.asignation[str(x)] = str(contador)
                contador += 1

            for x in self.delta:
                for y in self.delta[x]:
                        if len(self.delta[x][y]) != 0:
                            for w in self.delta[x][y]:
                                grafo.edge(ats(x),ats(w), label = repr(y), arrowhead='vee')

            grafo.node("accept", label="ACCEPT", shape="box", color="white")
            for x in self.delta:
                if self.F_identificator in x:
                    self.final_state = self.asignation[str(x)]
                    grafo.edge(ats(x),"accept",label = "$" ,arrowhead='vee')

            render = "./src/LR(0)/"+"LR(0)_"+self.name
            grafo.render(render, format="png", view="True")

            print()
            banner(f" LR(0) construido ", False)
            print()
            print(self.dot_grammar)

            print()

            print(self.sigma)
            print()
            print(self.que)
            print()

            print(self.augmented_grammar_reserved)

            print()

            print(self.terminals)

            # Crear un diccionario para almacenar los datos
            data = {
                "DotGrammar": self.dot_grammar,
                "Alfabeto": list(self.sigma),
                "AugmentedGrammar": self.augmented_grammar_reserved,
                "Terminals": self.terminals,
                "Transiciones": self.delta,
                "Asignacion": self.asignation,
                "Asignacion_2": self.asignation_reversed,
                "Acceptance": self.final_state,
                "TerminalsInner": self.terminals_dictionari
            }


            # Guardar los datos en un archivo JSON
            with open("./src/LR(0)_properties/data.json", "w") as json_file:
                json.dump(data, json_file)


        else:
            print()
            banner(f" Tokens en yalp no existen en yalex ", True)

            tabla = [[elemento] for elemento in self.faltantes]
            print(tabulate(tabla, headers=["Tokens faltantes en yalex"],  tablefmt="fancy_grid", numalign="center", stralign="left"))
            print()
        # banner(f" Tokens en yalp no definidos en yalex ", False)

if __name__ == '__main__':
    LR_0("slr-1")