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

for clave, valor in TerminalDict.items():
    TerminalDict[clave] = valor.replace('return ', '')


NumeracionGrammar = {}
NumeracionGrammarNew = {}

for indice, elemento in enumerate(AugmentedGrammar):
    NumeracionGrammar[str(elemento)] = indice+1
    NumeracionGrammarNew[str(indice+1)] = elemento

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

CONFLICTS = []

# Reduce movement
for key, value in AsignacionReversed.items():
    if key != str(Aceptacion):
        for production in value:
            if production[-1] == '.':

                """Removiendo el punto"""
                production.pop()

                FollowToDo = production[0]
                # print(FollowToDo)
                # print(AugmentedGrammar)
                # print(AugmentedGrammar[0][0])
                # print(Terminals)
                Simbolos_reduce = FOLLOW2(FollowToDo, AugmentedGrammar, AugmentedGrammar[0][0], Terminals)
                for simbol in Simbolos_reduce:
                    if len(InitialDelta[key][simbol])>0:
                        CONFLICTS.append(f"CONFLICT in [{key},{simbol}] = ({InitialDelta[key][simbol][0]},R{NumeracionGrammar[str(production)]})")
                    else:
                        InitialDelta[key][simbol].append(f'R{NumeracionGrammar[str(production)]}')
                # print("Estado", key, "Followtd", FollowToDo, "FOLLLOW: ", Simbolos_reduce)

if len(CONFLICTS) > 0:
    banner(" "+CONFLICTS[0]+ " ", False)
else:
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
    print()

    """Simulacion"""

    with open('./src/output.json') as f:
        tokenizacion_test = json.load(f)

    INPUT = []
    STACK = ['0']
    ACTION = None

    for key, value in tokenizacion_test.items():
        if value in TerminalDict:
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

    RegistroSimulacion = [['Linea','Pila', 'Simbolos', 'Entrada', 'Accion']]

    while(Simulacion):

        if ACTION == 'ACC':
            Simulacion = False

        # print(STACK, " ", INPUT, " ", ACTION)

        RegistroSimulacion.append(
            [
                len(RegistroSimulacion),
                ' '.join([elemento for elemento in STACK if elemento not in Alfabeto]),
                ' '.join([elemento for elemento in STACK if elemento in Alfabeto]),
                ' '.join(INPUT),
                ACTION_EXP(ACTION, NumeracionGrammarNew)
            ]
        )

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

    # for x in RegistroSimulacion:
    #     print(x)
    encabezados = RegistroSimulacion.pop(0)
    print(tabulate(RegistroSimulacion, headers=encabezados, tablefmt="fancy_grid"))

    if Acepta:
        print()
        banner(' ¿Se acepta segun la simulacion? YES ', False)
    else:
        print()
        banner(' ¿Se acepta segun la simulacion? NO ', False)
