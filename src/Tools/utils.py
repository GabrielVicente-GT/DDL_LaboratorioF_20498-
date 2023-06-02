# graphviz allow us to do an AFN grahp
import graphviz


# tabulate allow us to print the properties in a fancy way (it is not elementary)
from tabulate import tabulate

def Description():
    print(f'\n{"─"*117}\n{"─"*50}WELCOME TO LAB D!{"─"*50}\n{"─"*85} Auth. Gabriel Vicente 20498 UVG\n')
    print(' --> Note that')
    print('\t*\tThe tree is only available for .yal files')
    print('\t*\tEpsilon is represented by our \"E\" character ')
    print('\t*\tIf the path is not available the process will end')
    print('\t*\tThe tree will be generated only if .yal is valid\n')


def banner(header, row_jumps = True):
    value   = 120
    banner = "{:─^120}".format(header)

    print(f'{"─"*value}')

    if row_jumps:
        print(f'\n{banner}\n')
    else:
        print(f'{banner}')
    print(f'{"─"*value}\n')

def child_node(father_position, arbol):

    # Space to save the children position
    children = []

    # Position where the analysis begin
    to_analize = father_position - 1

    # While we are not out the array the process continues
    while (to_analize != -1):

        # If the analyzed property is False it represents a child
        # we appende this position to our result
        if arbol[to_analize].analyzed == False and len(children) < 2:
            children.append(to_analize)

        # We substract a position until the while es False
        to_analize -= 1

    # We return the children
    return children


class Tree_node(object):

    def __init__(self, value, id = None):

        self.id         = id
        self.value      = value
        self.analyzed   = False

    def __str__(self):
        return f"id:{self.id} valor: {self.value} analizado: {self.analyzed}"

def three_graph(postfix, titulo):
    f= graphviz.Digraph(name=titulo)
    f.attr(rankdir='TB')

    arbol = []
    for indice, valor in enumerate(postfix):
        arbol.append(Tree_node(valor,indice ))

    for nodo in arbol:
        f.node(str(nodo.id), label=str(nodo.value), shape = "circle", style = 'filled', fillcolor = 'white')

    for position, leaf in enumerate(arbol):
        if leaf.value == '*':
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[0]].id), arrowhead='vee')
            arbol[child_node(position, arbol)[0]].analyzed = True
        elif leaf.value == '+':
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[0]].id), arrowhead='vee')
            arbol[child_node(position, arbol)[0]].analyzed = True
        elif leaf.value == '?':
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[0]].id), arrowhead='vee')
            arbol[child_node(position, arbol)[0]].analyzed = True
        elif leaf.value == '|':
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[1]].id), arrowhead='vee')
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[0]].id), arrowhead='vee')
            arbol[child_node(position, arbol)[1]].analyzed = True
            arbol[child_node(position, arbol)[0]].analyzed = True

        elif leaf.value == '.':
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[1]].id), arrowhead='vee')
            f.edge(str(leaf.id),str(arbol[child_node(position, arbol)[0]].id), arrowhead='vee')
            arbol[child_node(position, arbol)[1]].analyzed = True
            arbol[child_node(position, arbol)[0]].analyzed = True

    render = "./src/GraphedBinaryTree/"+titulo
    f.render(render, format="png", view="True")

def flatten(arr):
    result = []
    for elem in arr:
        if isinstance(elem, list):
            result.extend(flatten(elem))
        else:
            result.append(elem)
    return result

def finite_automaton_graph(F,q_o,delta, titulo):
    f= graphviz.Digraph(name=titulo)
    f.attr(rankdir='LR')


    for x, y in delta.items():
        if x in F:
            f.node(str(x), shape = "doublecircle", style = 'filled', fillcolor = 'lightblue')
        elif x == q_o:
            f.node(str(x), shape = "circle", style = 'filled', fillcolor = 'lightgreen')
        else:
            f.node(str(x), shape = "circle")

    for x in delta:
        for y in delta[x]:
                if len(delta[x][y]) != 0:
                    for w in delta[x][y]:
                        f.edge(x,w, label = repr(y), arrowhead='vee')

    f.node("", height = "0",width = "0", shape = "box")
    f.edge("",q_o, arrowhead='vee')
    render = "./src/GraphedFiniteAutomata/"+titulo
    f.render(render, format="png", view="True")

def dictionary_results(d, tabulation = True):
    print('')
    if tabulation:
        my_dict = d

        # Crear una lista de tuplas (fruta, valor) a partir del diccionario
        table = [(fruit, ''.join(map(str, value))) for fruit, value in my_dict.items()]

        # Imprimir la tabla utilizando tabulate
        print(tabulate(table, headers=['Production Name', 'Is equal to..'], tablefmt="fancy_grid", numalign="center", stralign="left"))
    else:
        for key, value in d.items():
            print(f"{key} = {value} ")
    print('')

def finite_automaton_results(que,sigma,F,q_o,delta, tabulation = True):
    if tabulation == True:
        Properties = [
            ["Estados", que],
            ["Simbolos", sigma],
            ["Estados de aceptacion", F],
            ["Estado inicial", q_o],
        ]

        print(tabulate(Properties, tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

        Delta = []
        for key, value in delta.items():
            subtable = []
            for subkey, subvalue in value.items():
                subtable.append([subkey, subvalue])
            Delta.append([key, tabulate(subtable, tablefmt="plain", numalign="center", stralign="left")])

        print(tabulate(Delta, headers=['Estado             ', 'Transicion'], tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')
    elif tabulation== None:
        Properties = [
            ["Estados", que],
            ["Estados de aceptacion", F],
            ["Estado inicial", q_o],
        ]

        print(f'\nSimbolos -> {sigma}\n')

        print(tabulate(Properties, tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

        Delta = []
        for key, value in delta.items():
            subtable = []
            for subkey, subvalue in value.items():
                subtable.append([subkey, subvalue])
            Delta.append([key, tabulate(subtable, tablefmt="plain", numalign="center", stralign="left")])

        print(tabulate(Delta, headers=['Estado             ', 'Transicion'], tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

    else:
        print(f'\nEstados ->{que}')
        print(f'Transiciones ->\n')

        for x in delta:
            print(x, "", delta[x])

        print(f'\nSimbolos -> {sigma}')
        print(f'Estados de aceptacion -> {F}')
        print(f'Estado inicial-> {q_o}\n')

def letter_rename(numero):
    tabla = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I',
            '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R',
            '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z'}

    if numero > 25:
        letras = []
        for digito in str(numero):
            letras.append(tabla[digito])
        return ''.join(letras)
    else:
        letras = []
        letras.append(tabla[str(numero)])
        return ''.join(letras)

def E_closure( states, diccionario):

    reached = set()
    stack = []

    for state in states:
        stack.append(state)
        reached.add(state)

    while len(stack) != 0:
        actual_state = stack.pop()
        for state, transitions in diccionario.items():
            if actual_state == state:
                for possible_new in transitions['E']:
                    if possible_new not in reached:
                        reached.add(possible_new)
                        stack.append(possible_new)

    return reached

def move( T, symbol, diccionario):
    reached_u = set()
    stack = []

    for state in T:
        stack.append(state)

    while len(stack) != 0:
        actual_state = stack.pop()
        for state, transitions in diccionario.items():
            if actual_state == state:
                for possible_new in transitions[symbol]:
                    if possible_new not in reached_u:
                        reached_u.add(possible_new)

    return reached_u

def cleaning_process(sigma, partition_existence, delta_transformation, delta_minimizated):
    delta_minimizated.extend([[delta_row[0], delta_row[1], inside] for partition_id in partition_existence if len(partition_id) > 0 for delta_row in delta_transformation if delta_row[0] == partition_id[0] and delta_row[1] in sigma for inside_elem in partition_existence if delta_row[2] in inside_elem for inside in [inside_elem[0]]])
    return delta_minimizated


def simulation(question, AF, w):
    w = list(w)
    possible_validation = True

    for character in w:
        if character not in AF.sigma:
            possible_validation = False

    if str(type(AF)) == "<class 'FiniteAutomata.AFN.AFN'>":
        if possible_validation:
            S = E_closure([AF.q_o], AF.delta)
            for characther in w:
                S = E_closure(move(S,characther, AF.delta), AF.delta)

            proper = set(AF.F)

            if str(S&proper) != 'set()':
                print(question+"sí")
            else:
                print(question+"no")
        else:
            print(question+"no")
    else:
        current_state = AF.q_o
        for character in w:
            if possible_validation:
                if len(current_state) == 0:
                    possible_validation = False
                else:
                    if current_state[0] in AF.delta:
                        current_state = AF.delta[current_state[0]][character]
        if len(current_state) != 0:
                if current_state[0] in AF.F and possible_validation == True:
                    print(question+"sí")
                else:
                    print(question+"no")
        else:
            print(question+"no")
    print("\n")

def CreatingScanner(scanner_name, prueba_name, bp,individuals, bracket_inclusion):


    with open('./src/' + scanner_name + '.py', 'w') as f:

        f.write('''

from tabulate import tabulate
from Tools.utils import *
import json

with open("./src/AFD_Properties/data.json", "r") as json_file:
    data = json.load(json_file)

funcion_transicion  = data["Transition_Function"]
initial_state       = data["Initial_state"]
designation         = data["Tokens"]
current_state       = initial_state
        ''')
        f.write(f'''
with open("./src/YaparTests/{prueba_name}", "r") as file:''')
        f.write('''
    #Limpiando el texto
    content = file.read()
    content = repr(content)
    w = list(content)

    temp_w = []
    for position, caracter in enumerate(w):
        if caracter == "\\\\":
            if w[position+1] == 'n' or w[position+1] == 't' or w[position+1] == 's':
                temp_w.append(str("\\\\"+w[position+1]))
        elif caracter == 'n' or caracter == 't' or caracter == 's':
            if w[position-1] != '\\\\':
                temp_w.append(caracter)''')
        for identificator in individuals:
            xxx = list(identificator)
            yyy = len(xxx)
            f.write(f'''
        elif caracter == '{xxx[0]}':
            if '{identificator}' == ''.join(w[position:(position+{yyy})]):
                temp_w.append(''.join(w[position:(position+{yyy})]))
                w[position:(position+{yyy})] = [''] * len(w[position:(position+{yyy})])
        ''')
        f.write('''
        else:
            temp_w.append(caracter)

    temp_w = [elemento for elemento in temp_w if elemento != '']
    w = temp_w

    w = ["'{}'".format(elemento) for elemento in w]

    del w[0]
    original_len = len(w)

    Str_token = {}
    str_read = []
    w.pop()
    w.append("Final")
    character = w.pop(0)
    while (len(w) != 0):

        if eval(repr(character)) in funcion_transicion[current_state]:
            str_read.append(eval(repr(character)))
            current_state = funcion_transicion[current_state][eval(repr(character))][0]
            character = w.pop(0)
        ''')
        f.write('''
        elif eval(character) in funcion_transicion[current_state]:
            str_read.append(eval(character))
            current_state = funcion_transicion[current_state][eval(character)][0]
            character = w.pop(0)
        ''')
        f.write('''
        else:
            if current_state in designation:
                if current_state != initial_state:
                    Str_token[''.join(str_read)+' IN->'+str(original_len - len(w))] = designation[current_state]
                    str_read.clear()
                    current_state = initial_state
                else:
                    Str_token[character+' EIN->'+str(original_len - len(w))] = 'MT'
                    str_read.clear()
                    character = w.pop(0)
                    current_state = initial_state
            else:
                Str_token[character+' EIN->'+str(original_len - len(w))] = 'MT'
                str_read.clear()
                character = w.pop(0)
                current_state = initial_state

    table = [(k, v) for k, v in Str_token.items()]
    print()
    banner("Tokens encontrados", False)
    print(tabulate(table, headers=["Obtained Value", "Token"],  tablefmt="fancy_grid", numalign="center", stralign="left"),'\\n')

        ''')
        if bracket_inclusion == True:
            f.write('''
    # Bracket programation
    for string, token_r in Str_token.items():''')

            for llave, stringer in bp.items():
                f.write(f'''
        if token_r == "{llave}":
            {stringer}
                            ''')
        f.write('''
    with open("./src/output.json", "w") as json_file:
        json.dump(Str_token, json_file)''')
    banner('Scanner created successfully', False)



def CLOUSURE(items, dot_grammar):
    reached = []
    stack = []
    for production in items:
        stack.append(production)
        reached.append(production)

    while len(stack) != 0:
        actual_state = stack.pop()
        if actual_state.index(".") == (len(actual_state)-1):
            pass
        else:

            header = actual_state[actual_state.index(".") + 1]
            for production in dot_grammar:
                if header == production[0]:
                    if production not in reached:
                        reached.append(production)
                        stack.append(production)
    return reached

def MoveDot(arreglo_punto):
    otro = []
    for x in arreglo_punto:
        otro.append(x)

    for i in range(len(otro) -1):
        if otro[i] == ".":
            otro[i], otro[i+1] = otro[i+1], otro[i]
            return otro
    return otro


def GOTO(items, simbol, dot_grammar):

    reached_u = []
    stack = []

    for element in items:
        stack.append(element)

    while len(stack) != 0:
        actual_state = stack.pop()
        if actual_state.index(".") == (len(actual_state)-1):
            pass
        else:
            if actual_state[actual_state.index(".") + 1] == simbol:
                if actual_state not in reached_u:
                    reached_u.append(MoveDot(actual_state))

    # print("Goto I")
    reached_u = CLOUSURE(reached_u, dot_grammar)
    # for x in reached_u:
    #     print(x)
    return reached_u


def FIRST(valor, grammar, terminals):

    final = []
    stack = []
    reached = []
    stack.append(valor)
    reached.append(valor)

    if valor in terminals:
        return stack
    else:
        while len(stack) != 0:
            evaluando = stack.pop(0)
            for production in grammar:
                if production[0] == evaluando:
                    if production[2] in terminals:
                        final.append(production[2])
                    else:
                        if production[2] not in stack and production[2] not in reached:
                            stack.append(production[2])
                            reached.append(production[2])
    return final


def FOLLOW(symbol, grammar, start_symbol, terminals):
    follow_set = set()
    if symbol == start_symbol:
        follow_set.add('$')
    for production in grammar:
        # print(f"Estoy dentro de la produccion {production}")
        for i, s in enumerate(production[2:]):
            # print(s, '   ', symbol)
            # print(i)
            if s == symbol:
                if i == len(production[2:]) - 1:
                    if production[0] != symbol:
                        follow_set |= FOLLOW(production[0], grammar, start_symbol, terminals)
                else:
                    # print("NEXT SIMBOL ", i)
                    next_symbol = production[i+3]
                    # print(next_symbol)
                    if next_symbol in terminals:
                        follow_set.add(next_symbol)
                    else:
                        follow_set |= FIRST(next_symbol, grammar, terminals)
                        if '' in follow_set:
                            follow_set -= {''}
                            follow_set |= FOLLOW(production[0], grammar, start_symbol, terminals)
    return follow_set
