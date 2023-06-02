# # # # # # # # # # original_list = ['(', 'ws', '|', 'id', '|', "'+'", '|', "'*'", '|', "'('", '|', "')'", ')']
# # # # # # # # # # new_list = []

# # # # # # # # # # for position, item in enumerate(original_list):
# # # # # # # # # #     if (position+1)%2  == 0:
# # # # # # # # # #         new_list.append(item)
# # # # # # # # # #         new_list.append('#')
# # # # # # # # # #     else:
# # # # # # # # # #         new_list.append(item)

# # # # # # # # # # print(new_list)

# # # # # # # # # with open("./src/ScannerTests/prueba_1.txt", "r") as file:
# # # # # # # # #     # content = file.read().replace('\n', '"\n"')
# # # # # # # # #     content = file.read()
# # # # # # # # #     print(repr(content))

# # # # # # # cadena1 = "'0'"
# # # # # # # cadena2 = '0'

# # # # # # # if eval(cadena1) == eval(repr(cadena2)):
# # # # # # #     print("Las cadenas son iguales")
# # # # # # # else:
# # # # # # #     print("Las cadenas son diferentes")
# # # # # # # # mi_lista = ['manzana', 'banana', 'naranja']
# # # # # # # # nueva_lista = ["'{}'".format(elemento) for elemento in mi_lista]
# # # # # # # # print(nueva_lista)

# # # # # # mi_lista = ['Hola', 'Mundo', '!']
# # # # # # mi_string = ''.join(mi_lista)

# # # # # # print(mi_string)
# # # # # # diccionario = {'A': {"#'+'": [], '3': ['B'], "'+'": ['F'], '1': ['B'], "'('": ['D'], '5': ['B'], '#ws': [], "#'('": [], '0': ['B'], "'\\n'": ['E'], '9':
# # # # # # ['B'], '4': ['B'], "' '": ['E'], "'\\t'": ['E'], "#'*'": [], "'-'": [], '2': ['B'], '6': ['B'], "')'": ['G'], '7': ['B'], '#number': [], '8': ['B'], "#')'": [], "'*'": ['C']}, 'B': {"#'+'": [], '3': ['B'], "'+'": ['H'], '1': ['B'], "'('": [], '5': ['B'], '#ws': [], "#'('": [],
# # # # # # '0': ['B'], "'\\n'": [], '9': ['B'], '4': ['B'], "' '": [], "'\\t'": [], "#'*'": [], "'-'": ['H'], '2': ['B'], '6': ['B'], "')'": [], '7':
# # # # # # ['B'], '#number': [], '8': ['B'], "#')'": [], "'*'": []}, 'C': {"#'+'": [], '3': [], "'+'": [], '1': [], "'('": [], '5': [], '#ws': [], "#'('": [], '0': [], "'\\n'": [], '9': [], '4': [], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': [], '6': [], "')'": [], '7': [], '#number': [], '8': [], "#')'": [], "'*'": []}, 'D': {"#'+'": [], '3': [], "'+'": [], '1': [], "'('": [], '5': [], '#ws': [], "#'('": [], '0': [], "'\\n'": [], '9': [], '4': [], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': [], '6': [], "')'": [], '7': [], '#number': [], '8':
# # # # # # [], "#')'": [], "'*'": []}, 'E': {"#'+'": [], '3': [], "'+'": [], '1': [], "'('": [], '5': [], '#ws': [], "#'('": [], '0': [], "'\\n'": ['E'], '9': [], '4': [], "' '": ['E'], "'\\t'": ['E'], "#'*'": [], "'-'": [], '2': [], '6': [], "')'": [], '7': [], '#number': [], '8': [], "#')'": [], "'*'": []}, 'F': {"#'+'": [], '3': [], "'+'": [], '1': [], "'('": [], '5': [], '#ws': [], "#'('": [], '0': [], "'\\n'": [], '9':
# # # # # # [], '4': [], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': [], '6': [], "')'": [], '7': [], '#number': [], '8': [], "#')'": [], "'*'": []}, 'G': {"#'+'": [], '3': [], "'+'": [], '1': [], "'('": [], '5': [], '#ws': [], "#'('": [], '0': [], "'\\n'": [], '9': [], '4': [], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': [], '6': [], "')'": [], '7': [], '#number': [], '8': [], "#')'": [], "'*'": []}, 'H': {"#'+'": [], '3': ['I'], "'+'": [], '1': ['I'], "'('": [], '5': ['I'], '#ws': [], "#'('": [], '0': ['I'], "'\\n'": [], '9': ['I'], '4': ['I'], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': ['I'], '6': ['I'], "')'": [], '7': ['I'], '#number': [], '8': ['I'], "#')'": [], "'*'": []}, 'I': {"#'+'": [], '3': ['I'], "'+'": [], '1': ['I'], "'('": [], '5': ['I'], '#ws': [], "#'('": [], '0': ['I'], "'\\n'": [], '9': ['I'], '4': ['I'], "' '": [], "'\\t'": [], "#'*'": [], "'-'": [], '2': ['I'], '6': ['I'], "')'": [], '7': ['I'], '#number': [], '8': ['I'], "#')'": [], "'*'": []}}
# # # # # # print(diccionario)

# # # # # # for key, value in diccionario.items():
# # # # # #     copy_value = value.copy()  # hacemos una copia del diccionario interno antes de recorrerlo y modificarlo
# # # # # #     for k, v in copy_value.items():
# # # # # #         if not v:
# # # # # #             del value[k]

# # # # # # print(diccionario)

# # # # # # import json

# # # # # # # Diccionario a guardar
# # # # # # diccionario = {'A': {'3': ['B'], "'+'": ['F'], '1': ['B'], "'('": ['D'], '5': ['B'], '0': ['B'], "'\\n'": ['E'], '9': ['B'], '4': ['B'], "' '": ['E'], "'\\t'": ['E'], '2': ['B'], '6': ['B'], "')'": ['G'], '7': ['B'], '8': ['B'], "'*'": ['C']}, 'B': {'3': ['B'], "'+'": ['H'], '1': ['B'], '5': ['B'], '0': ['B'], '9': ['B'], '4': ['B'], "'-'": ['H'], '2': ['B'], '6': ['B'], '7': ['B'], '8': ['B']}, 'C': {}, 'D': {}, 'E': {"'\\n'": ['E'], "' '": ['E'], "'\\t'": ['E']}, 'F': {}, 'G': {}, 'H': {'3': ['I'], '1': ['I'], '5': ['I'], '0': ['I'], '9': ['I'], '4': ['I'], '2': ['I'], '6': ['I'], '7': ['I'], '8': ['I']}, 'I': {'3': ['I'], '1': ['I'], '5': ['I'], '0': ['I'], '9': ['I'], '4': ['I'], '2': ['I'], '6': ['I'], '7': ['I'], '8': ['I']}}

# # # # # # # Guardar diccionario como archivo JSON
# # # # # # with open("diccionario.json", "w") as f:
# # # # # #     json.dump(diccionario, f)
# # # # # import json

# # # # # # Crear la lista que deseas guardar
# # # # # mi_lista = ["manzana", "banana", "naranja"]

# # # # # # Escribir la lista en un archivo JSON
# # # # # with open("mi_lista.json", "w") as f:
# # # # #     json.dump(mi_lista, f)

# # # # import json

# # # # # Definir una cadena
# # # # my_string = "¡Hola, mundo!"

# # # # # Definir un diccionario
# # # # my_dict = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}

# # # # # Definir tres listas
# # # # my_list1 = [1, 2, 3, 4, 5]
# # # # my_list2 = ["a", "b", "c", "d", "e"]
# # # # my_list3 = [True, False, True, False, True]

# # # # # Crear un diccionario para almacenar los datos
# # # # data = {"string": my_string, "diccionario": my_dict, "lista1": my_list1, "lista2": my_list2, "lista3": my_list3}

# # # # # Guardar los datos en un archivo JSON
# # # # with open("datos.json", "w") as json_file:
# # # #     json.dump(data, json_file)

# # # # # Cargar los datos desde el archivo JSON
# # # # with open("datos.json", "r") as json_file:
# # # #     data = json.load(json_file)

# # # # # Recuperar los datos
# # # # my_string = data["string"]
# # # # my_dict = data["diccionario"]
# # # # my_list1 = data["lista1"]
# # # # my_list2 = data["lista2"]
# # # # my_list3 = data["lista3"]

# # # # print(my_string)
# # # # print(my_dict)
# # # # print(my_list1)
# # # # print(my_list2)
# # # # print(my_list3)

# # # with open('probando_creacion.py', 'w') as f:
# # #     f.write('''
# # # from tabulate import tabulate
# # # from Tools.utils import *
# # # import json

# # # Str_token = {"key1": "value1", "key2": "value2", "key3": "value3"}

# # # with open("./src/AFD_Properties/data.json", "r") as json_file:
# # #     data = json.load(json_file)

# # # funcion_transicion  = data["Transition_Function"]
# # # initial_state       = data["Initial_state"]
# # # designation         = data["Tokens"]
# # # current_state       = initial_state

# # # with open("./src/ScannerTests/prueba_1.txt", "r") as file:

# # #     #Limpiando el texto
# # #     content = file.read()
# # #     content = repr(content)
# # #     w = list(content)

# # #     temp_w = []
# # #     for position, caracter in enumerate(w):
# # #         if caracter == "\\\\":
# # #             temp_w.append(str("\\\\"+w[position+1]))
# # #         elif caracter == 'n' or caracter == 't':
# # #             if w[position-1] != '\\\\':
# # #                 temp_w.append(caracter)
# # #         else:
# # #             temp_w.append(caracter)

# # #     w = temp_w
# # #     w = ["'{}'".format(elemento) for elemento in w]

# # #     del w[0]
# # #     original_len = len(w)

# # #     Str_token = {}
# # #     str_read = []
# # #     character = w.pop(0)

# # #     while (len(w) != 0):

# # #         if eval(repr(character)) in funcion_transicion[current_state]:
# # #             str_read.append(eval(repr(character)))
# # #             current_state = funcion_transicion[current_state][eval(repr(character))][0]
# # #             character = w.pop(0)

# # #         elif eval(character) in funcion_transicion[current_state]:
# # #             str_read.append(eval(character))
# # #             current_state = funcion_transicion[current_state][eval(character)][0]
# # #             character = w.pop(0)

# # #         else:
# # #             if current_state in designation:
# # #                 Str_token[''.join(str_read)] = designation[current_state]
# # #                 str_read.clear()
# # #                 current_state = initial_state
# # #             else:
# # #                 Str_token[character+' EIP ->'+str(original_len - len(w))] = 'INVALID TOKEN'
# # #                 str_read.clear()
# # #                 character = w.pop(0)
# # #                 current_state = initial_state

# # #     table = [(k, v) for k, v in Str_token.items()]
# # #     print()
# # #     banner("Tokens encontrados", False)
# # #     print(tabulate(table, headers=["Obtained Value", "Token"],  tablefmt="fancy_grid", numalign="center", stralign="left"),'\\n')

# # # ''')

# # # Crear la lista con espacios en blanco
# # mi_lista = ['Hola ', "' '", 'Mundo ', '  ', 'en', '  ', 'Python']

# # # Usar comprensión de lista para eliminar espacios en blanco
# # mi_lista_sin_espacios = [elemento.strip() for elemento in mi_lista if elemento.strip()]

# # # Imprimir la lista sin espacios en blanco
# # print(mi_lista_sin_espacios)

# texto = "Este es un [ejemplo asdfadsfa ] de [texto] con [varios] bloques [entre] brackets."

# bloques = []
# i = 0
# while i < len(texto):
#     if texto[i] == '[':
#         j = i
#         while j < len(texto) and texto[j] != ']':
#             j += 1
#         bloques.append(texto[i+1:j])
#         i = j + 1
#     else:
#         i += 1

# print(bloques)

# cadena = "rule tokens =ws| id        { return ID }        | '+'       { return PLUS }| '*'       { return TIMES }| '('      "
cadena = " tokens =     ws        { return WHITESPACE = }                 | number    { return NUMBER }  | '+'       { return PLUS }  | '*'       { return TIMES }  | '('       { return LPAREN }  | ')'       { return RPAREN }"

diccionario = {}

# Separar la cadena por el carácter de igualdad
clave, valor = cadena.split("=", maxsplit=1)

# Separar el valor por el carácter "|"
opciones = valor.split("|")

# Para cada opción, extraer la clave y el valor
for opcion in opciones:
    # Extraer la clave que está antes del carácter "{"
    clave_opcion = opcion.split("{")[0].strip()

    # Verificar que la opción tiene un valor entre los caracteres "{" y "}"
    if "{" in opcion and "}" in opcion:
        # Extraer el valor que está entre los caracteres "{" y "}"
        valor_opcion = opcion.split("{")[1].split("}")[0].strip()
    else:
        # Si la opción no tiene un valor válido, asignar un valor vacío
        valor_opcion = ""

    # Agregar la clave y el valor al diccionario
    diccionario[clave_opcion] = valor_opcion

print(diccionario)
