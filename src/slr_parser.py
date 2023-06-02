from tabulate import tabulate
from Tools.utils import *
import json

with open("./src/LR(0)_Properties/data.json", "r") as json_file:
    data = json.load(json_file)

Alfabeto            = data["Alfabeto"]
Terminals           = data["Terminals"]
DotGrammar          = data["DotGrammar"]
AugmentedGrammar    = data["AugmentedGrammar"]
InitialDelta        = data["Transiciones"]
Asignacion          = data["Asignacion"]
AsignacionReversed  = data["Asignacion_2"]
Aceptacion          = data["Acceptance"]
TerminalDict          = data["TerminalsInner"]


print()
banner(" Terminals DICT ", False)
for clave, valor in TerminalDict.items():
    TerminalDict[clave] = valor.replace('return ', '')

print(TerminalDict)

print()
banner(" Augmented grammar ", False)

print(AugmentedGrammar)

NumeracionGrammar = {}
NumeracionGrammarNew = {}

for indice, elemento in enumerate(AugmentedGrammar):
    NumeracionGrammar[str(elemento)] = indice+1
    NumeracionGrammarNew[str(indice+1)] = elemento

print()
banner(" Gramar Numeration ", False)

print(NumeracionGrammar)

print()
banner(" Gramar Numeration Renuved", False)

print(NumeracionGrammarNew)


print()
banner(" Estados ", False)
for key, value in AsignacionReversed.items():
    print(f"Estado: {key}")
    for sublist in value:
        print(f"  - {sublist}")
    print()

# Renamining
InitialDelta = {Asignacion[str(conjunto)]: {k: [Asignacion[s] if s in Asignacion else s for s in v] for k, v in valores.items()} for conjunto, valores in InitialDelta.items()}

# Aplicar la concatenación "S" al string si se cumple la condición
for inner_dict in InitialDelta.values():
    for key, value in inner_dict.items():
        if key in Terminals and len(value) != 0:
            inner_dict[key] = [f"S{val}" for val in value]

# Estado de aceptacion

InitialDelta[str(Aceptacion)]['$'].append('ACC')

# Reduce movement
for key, value in AsignacionReversed.items():
    if key != str(Aceptacion):
        for production in value:
            if production[-1] == '.':

                """Removiendo el punto"""
                production.pop()

                FollowToDo = production[0]

                Simbolos_reduce = FOLLOW(FollowToDo, AugmentedGrammar, AugmentedGrammar[0][0], Terminals)
                for simbol in Simbolos_reduce:
                    InitialDelta[key][simbol].append(f'R{NumeracionGrammar[str(production)]}')
                # print("Estado", key, "Followtd", FollowToDo, "FOLLLOW: ", Simbolos_reduce)

"""Impresion de tabla"""

# Obtener las claves únicas para las columnas
columns = sorted(set(key for inner_dict in InitialDelta.values() for key in inner_dict.keys()))
moving = columns.pop(0)
columns.insert(len(Terminals), moving)
# print(columns)
# Crear una lista de listas con los datos para la tabla
table_data = [[key] + [inner_dict.get(col, []) for col in columns] for key, inner_dict in InitialDelta.items()]

# Imprimir la tabla utilizando tabulate
banner(" Tabla SLR ", False)
print(tabulate(table_data, headers=['Estado'] + columns, tablefmt="fancy_grid"))


"""Simulacion"""

with open('./src/output.json') as f:
    tokenizacion_test = json.load(f)

INPUT = []
STACK = ['0']
ACTION = None

for key, value in tokenizacion_test.items():
    INPUT.append(TerminalDict[value])

while '' in INPUT:
    INPUT.remove('')

INPUT.append('$')

Simulacion = True
Acepta = True

if len(InitialDelta[STACK[-1]][INPUT[0]]) > 0:
    ACTION = InitialDelta[STACK[-1]][INPUT[0]][0]
else:
    Simulacion = False
    Acepta = False

while(Simulacion):

    if ACTION == 'ACC':
        Simulacion = False

    print(STACK, " ", INPUT, " ", ACTION)

    if ACTION[0] == 'S':
        STACK.append(INPUT.pop(0))
        STACK.append(ACTION[1:])

    if ACTION[0] == 'R':
        for _ in range((len(NumeracionGrammarNew[ACTION[1:]]) - 2)*2):
            STACK.pop()
        STACK.append(NumeracionGrammarNew[ACTION[1:]][0])
        STACK.append(InitialDelta[STACK[-2]][STACK[-1]][0])

    if len(InitialDelta[STACK[-1]][INPUT[0]]) >0:
        ACTION = InitialDelta[STACK[-1]][INPUT[0]][0]
    else:
        Simulacion = False
        Acepta = False

if Acepta:
    print("Pertenece")
else:
    print("No pertenece")

# Delta = []
# for key, value in InitialDelta.items():
#     subtable = []
#     for subkey, subvalue in value.items():
#         subtable.append([subkey, subvalue])
#     Delta.append([key, tabulate(subtable, tablefmt="plain", numalign="center", stralign="left")])

# print(tabulate(Delta, headers=['Estado             ', 'Transicion'], tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

# print(InitialDelta)