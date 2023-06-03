"""
Autor: Gabriel Vicente (20498)
Proyecto: Laboratorio E

Descripción:
Laboratorio E para la clase Diseño de Lenguajes
* Correcta interpretación de un archivo de especificación YAPar (extensión
.yalp), siguiendo todos los lineamientos del archivo Consideraciones de
YAPar.

* Validación de tokens provistos en archivo de especificación de YAPar con el
output generado por YALex (validar que los tokens escritos en YAPar si se
encuentren presentes como parte de la lectura de un archivo YALex).

* Cálculo de funciones asociadas sobre la gramática provista: FIRST, FOLLOW
y CLOSURE.

* Generación de elementos de nodos de autómata LR(0) y construcción del
autómata LR(0) con sus transiciones y elementos asociados, generado a
partir de la gramática provista, incluyendo una representación visual del
mismo.



Tomando en cuenta operaciones y abreviaturas
[* , + , . , ? , |]

Al igual que la jerarquia de los parentesis
"""
#Persistance data
import json

#Imports needed for lab C
from Tools.utils import *
from Tools.ReadingYal import *
from FiniteAutomata.AFD import *
from FiniteAutomata.AFN import *
from Tools.InfixToPostfixV2 import *
from FiniteAutomata.AFD_minimization import *

# Descripction
Description()

# File request
# string = input('Enter a file name from which to generate the Expression tree: ')
string = 'slr-yapar'
# string = 'lab-f'
# string = 'slr-1'

# Postfix from the .yal by shunting yard method
# yal_postfix = InfixToPostfix(Reader(file_name).yal_final_regex).postfix

print(Reader(string+'.yal').yal_final_regex)

yal_postfix = InfixToPostfix(Reader(string+'.yal').yal_final_regex).postfix

bracket_programation = Reader(string+'.yal').bracket_programation
# We graph the Expression tree if possible
if yal_postfix[0] != 'ERROR':
    three_graph(yal_postfix,"ArbolExpresiones_yal_0")


# Automata Finito Determinista del .yal
DDFA = Direct_AFD(yal_postfix, 'LabD')

"""DFA Properties persitance"""

# Cleaning delta function
funcion_transicion = DDFA.delta

for key, value in funcion_transicion.items():
    copy_value = value.copy()
    for k, v in copy_value.items():
        if not v:
            del value[k]

# Crear un diccionario para almacenar los datos
data = {"Initial_state": DDFA.q_o, "Transition_Function": funcion_transicion, "Alphabet": DDFA.sigma, "States": DDFA.que, "Acceptance_states": DDFA.F, "Tokens": DDFA.F_designation}


# Guardar los datos en un archivo JSON
with open("./src/AFD_Properties/data.json", "w") as json_file:
    json.dump(data, json_file)

# Creating scanner:
print(bracket_programation)
print(type(bracket_programation))
CreatingScanner(string, 'slr-1.yalp', bracket_programation, Reader(string+'.yal').part_2,False)
# CreatingScanner(string, 'lab-f.yalp', bracket_programation, Reader(string+'.yal').part_2,False)
# CreatingScanner(string, 'test_file.txt', bracket_programation, Reader(string+'.yal').part_2,False)

