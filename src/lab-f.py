

from tabulate import tabulate
from Tools.utils import *
import json

with open("./src/AFD_Properties/data.json", "r") as json_file:
    data = json.load(json_file)

funcion_transicion  = data["Transition_Function"]
initial_state       = data["Initial_state"]
designation         = data["Tokens"]
current_state       = initial_state
        
with open("./src/YaparTests/test_file.txt", "r") as file:
    #Limpiando el texto
    content = file.read()
    content = repr(content)
    w = list(content)

    temp_w = []
    for position, caracter in enumerate(w):
        if caracter == "\\":
            if w[position+1] == 'n' or w[position+1] == 't' or w[position+1] == 's':
                temp_w.append(str("\\"+w[position+1]))
        elif caracter == 'n' or caracter == 't' or caracter == 's':
            if w[position-1] != '\\':
                temp_w.append(caracter)
        elif caracter == '=':
            if '=' == ''.join(w[position:(position+1)]):
                temp_w.append(''.join(w[position:(position+1)]))
                w[position:(position+1)] = [''] * len(w[position:(position+1)])
        
        elif caracter == '*':
            if '*' == ''.join(w[position:(position+1)]):
                temp_w.append(''.join(w[position:(position+1)]))
                w[position:(position+1)] = [''] * len(w[position:(position+1)])
        
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
        
        elif eval(character) in funcion_transicion[current_state]:
            str_read.append(eval(character))
            current_state = funcion_transicion[current_state][eval(character)][0]
            character = w.pop(0)
        
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
    print(tabulate(table, headers=["Obtained Value", "Token"],  tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')

        
    with open("./src/output.json", "w") as json_file:
        json.dump(Str_token, json_file)