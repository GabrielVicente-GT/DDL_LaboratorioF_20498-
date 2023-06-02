# Just used to see if the path is available
import os
# utils is usefull to rename the sets and prints
from Tools.utils import *

# This class allow us to read the file if is possible and do the math for the Expression Tree
class Reader(object):
    def __init__(self, path, impresiones = True):

        # Proccess variables
        self.path               = "./src/YalexTests/"+path
        self.yal_regex          = []
        self.productions        = []
        self.yal_final_regex    = []
        self.regex_operators_ni     = ['(',')','|','*','?','+']
        self.bracket_programation = None
        self.part_2 = None
        # If is a valid path for the filename
        if os.path.exists(self.path):

            # We read the file
            with open(self.path, 'r') as file:

                # We convert the multiple file rows in one row
                linea = file.read().replace('\n', '')

                # And we split it be the str rule
                linea = linea.split('rule')

                # print(linea)
                """Part 1 asignations"""

                # Comments delete from part 1
                i = 0
                while i < len(linea[0]):
                    if linea[0][i:i+2] == '(*':
                        j = linea[0].find('*)', i+2)
                        if j == -1:
                            break
                        linea[0] = linea[0][:i] + linea[0][j+2:]
                    else:
                        i += 1

                # Commets delete from part 2
                i = 0
                while i < len(linea[1]):
                    if linea[1][i:i+2] == '(*':
                        j = linea[1].find('*)', i+2)
                        if j == -1:
                            break
                        linea[1] = linea[1][:i] + linea[1][j+2:]
                    else:
                        i += 1

                #Simple sustitutions
                linea[0] = linea[0].replace('\n','\\n')
                linea[0] = linea[0].replace('\t','\\t')
                linea[0] = linea[0].replace('\s','\\s')
                linea[0] = linea[0].replace('"\\s\\t\\n"',"['\\s''\\t''\\n']")
                linea[0] = linea[0].replace('"0123456789"',"'0'-'9'")

                # Original dictionary (just strings withot error handling)
                diccionario = {}
                pares = linea[0].split("let ")[1:]
                for par in pares:
                    clave, valor = par.split("=")
                    diccionario[clave.replace(' ', '')] = valor.split("let ")[0]

                for clave in diccionario:
                    diccionario[clave] = diccionario[clave].strip()

                # Fixin dictionary

                # Or between tight elements
                for clave, valor in diccionario.items():
                    diccionario[clave] = valor.replace("''", "','")

                # We remove the extra breackets and split by commas
                for key, value in diccionario.items():
                    diccionario[key] = value.strip("[]").split(",")


                # We add or betweens splits made by the commas
                for key, value in diccionario.items():
                    lista_original_1 = diccionario[key]
                    lista_nueva_1 = []

                    for elemento in lista_original_1:
                        lista_nueva_1.append(elemento)
                        if elemento != lista_original_1[-1]:
                            lista_nueva_1.append('|')

                    diccionario[key] = lista_nueva_1

                # We remove the extra commas
                for key, value in diccionario.items():
                    if key != 'delim':
                        for x in range(len(value)):
                            value[x] = value[x].replace("'","")

                # We have have a register about the productions name
                for key, value in diccionario.items():
                    self.productions.append(key)
                self.productions.reverse()
                self.productions.append('E')

                # We made an array with the production names

                # Every time we fulfill the name of a production or we pass al
                # we append an element to the position

                for key, value in diccionario.items():
                    if key != 'delim':
                        for x in range(len(value)):
                            string = value[x]
                            tokens = []
                            i = 0
                            while i < len(string):
                                for word in self.productions:
                                    if string.startswith(word, i):
                                        tokens.append(string[i:i+len(word)])
                                        i += len(word)
                                        break
                                else:
                                    tokens.append(string[i])
                                    i += 1
                            value[x] = tokens

                # Suporting the logic with ascci, every time we found a '-' that is not an str
                # from the productions, we add ever element int that list
                for key, value in diccionario.items():
                    if key != 'delim':
                        for x in range(len(value)):
                            if '-' in value[x]:
                                if value[x].index('-') != 0:
                                    arreglo = value[x]
                                    aux = []
                                    for i in range(len(arreglo)):
                                        if arreglo[i] == '-':
                                            aux += [chr(j) for j in range(ord(arreglo[i-1])+1, ord(arreglo[i+1]))]
                                            # print(aux)
                                        else:
                                            aux.append(arreglo[i])
                                    temp = []
                                    for elemento in aux:
                                        temp.append(elemento)
                                        if elemento != aux[-1]:
                                            temp.append('|')
                                    aux = temp
                                    value[x] = aux


                # There is no more sub arrays
                for key, value in diccionario.items():
                    diccionario[key] = ['('] + flatten(value) + [')']

                for key, value in diccionario.items():
                    diccionario[key] = [elemento.strip() for elemento in diccionario[key] if elemento.strip()]

                if impresiones == True:
                    banner(" Productions ", False)
                    # Impresion de producciones
                    dictionary_results(diccionario)
                    # for x, y in diccionario.items():
                    #     print(x,y)
                    print('')

                #STR exception
                for key, value in diccionario.items():
                    if key == 'number':
                        value[value.index('+')] = "'+'"
                        value[value.index('-')] = "'-'"

                """Part 2 (Substitute the productions inside the final expression)"""

                """Creating bracket info"""
                cadena = repr(linea[1])
                brackets_programation = {}

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
                    brackets_programation[clave_opcion] = valor_opcion
                self.bracket_programation = brackets_programation

                # print(brackets_programation)

                table = [(k, v) for k, v in brackets_programation.items()]
                if impresiones == True:
                    print()
                    banner("Programming Inside Brackets", False)
                    print(tabulate(table, headers=["ID", "Bracket content"],  tablefmt="fancy_grid", numalign="center", stralign="left"),'\n')


                """Substitute the productions"""

                # Cleaning returns

                i = 0
                while i < len(linea[1]):
                    if linea[1][i] == '{':
                        j = i
                        while j < len(linea[1]) and linea[1][j] != '}':
                            j += 1
                        linea[1] = linea[1][:i] + linea[1][j+1:]
                    else:
                        i += 1

                # Obtening the cleanes STR
                linea[1] = linea[1][linea[1].find("=")+1:].strip()
                linea[1] = linea[1].split("|")
                linea[1] = [elemento.strip() for elemento in linea[1]]
                linea[1] = [f'"{elemento}"' if " " in elemento else elemento for elemento in linea[1]]
                temp = []
                self.part_2 = [elemento for elemento in linea[1] if elemento not in diccionario.keys()]
                self.part_2 = [elemento.replace("'", "") for elemento in self.part_2]
                for elemento in linea[1]:
                    temp.append(elemento)
                    if elemento != linea[1][-1]:
                        temp.append('|')
                linea[1] = temp
                linea[1] = ['('] + linea[1] + [')']
                if impresiones == True:
                    banner(f" Expresion tree from rule ", False)
                    banner(f" {''.join(linea[1])} ", False)

                """Agregando valores terminales"""
                linea_temporal = []
                for position, item in enumerate(linea[1]):
                    if (position+1)%2  == 0:
                        linea_temporal.append(item)
                        linea_temporal.append('#'+str(item))
                    else:
                        linea_temporal.append(item)

                linea[1] = linea_temporal

                # Finally we Substitute the productions inside the final expression

                while True:
                    sustitucion_hecha = False
                    for i in range(len(linea[1])):
                        if linea[1][i] in diccionario:
                            valor_diccionario = diccionario[linea[1][i]]
                            if isinstance(valor_diccionario, list):
                                linea[1][i] = valor_diccionario[0]
                                if len(valor_diccionario) > 1:
                                    linea[1][i+1:i+1] = valor_diccionario[1:]
                                sustitucion_hecha = True
                            else:
                                linea[1][i] = valor_diccionario
                                sustitucion_hecha = True
                    if not sustitucion_hecha:
                        break

                #Cleaning brackets that we miss
                for i in range(len(linea[1])):
                    if linea[1][i] == '[':
                        linea[1][i] = '('
                    if linea[1][i] == ']':
                        linea[1][i] = ')'

                #Final or
                for i in range(len(linea[1])):
                    if linea[1][i] == '-' and linea[1][i-2] != '+':
                        linea[1][i] = '|'

                # Reviewing the possible concatenations
                yal_concat_regex = []
                for letra in linea[1]:
                    yal_concat_regex.append(letra)
                    yal_concat_regex.append('.')
                yal_concat_regex.pop()

                # Clean the concatenations
                for symbol, char in enumerate(yal_concat_regex):
                    if char == '.' and 0 < symbol < len(yal_concat_regex) - 1:
                        prev_char = yal_concat_regex[symbol - 1]
                        next_char = yal_concat_regex[symbol + 1]
                        if prev_char not in self.regex_operators_ni and next_char not in self.regex_operators_ni:
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '*' and next_char not in self.regex_operators_ni:
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '*' and next_char == '(':
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '+' and next_char not in self.regex_operators_ni:
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '+' and next_char == '(':
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == ')' and next_char not in self.regex_operators_ni:
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '?' and next_char not in self.regex_operators_ni:
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == '?' and next_char == '(':
                            yal_concat_regex[symbol] = '.'
                        elif prev_char not in self.regex_operators_ni and next_char == '(':
                            yal_concat_regex[symbol] = '.'
                        elif prev_char == ')' and next_char == '(':
                            yal_concat_regex[symbol] = '.'
                        else:
                            yal_concat_regex[symbol] = ''
                for elemento in yal_concat_regex:
                    if elemento != '':
                        self.yal_regex.append(elemento)

                # We look for doble concatenatons in the expresion
                for symbol, char in enumerate(self.yal_regex):
                    if char == '.' and 0 < symbol < len(self.yal_regex) - 1:
                        prev_char = self.yal_regex[symbol - 1]
                        next_char = self.yal_regex[symbol + 1]
                        if prev_char == '.':
                            self.yal_regex[symbol] = '.'
                            self.yal_regex[symbol-1] = "'.'"
                        elif next_char == '.':
                            self.yal_regex[symbol] = "'.'"
                            self.yal_regex[symbol+1] = '.'

                # We finally clean the sem yal regex to the final regex
                for elemento in self.yal_regex:
                    if elemento != '':
                        self.yal_final_regex.append(elemento)
                if impresiones == True:
                    banner(f" Regex from {self.path} ", False)
                    print(f"{str(''.join(self.yal_final_regex))} \n")
                # print(f"\n{self.yal_final_regex}")
        else:
            # We add an error to the yal regex that we need to review
            self.yal_final_regex.append('ERROR')
