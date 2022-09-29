import os.path
import string

def isDelimiter(char):
    delimiters = ";,(){}[]"

    if char in delimiters:
        return True

    return False

def whichDelimiterToken(delimiter):
    delimiters = ";,(){}[]"

    position = delimiters.find(delimiter)

    return "TOKEN20{}".format(position)

def isLetter(char):
    letter = string.ascii_letters

    if char in letter:
        return True
    return False

def isNumber(char):
    numbers = "0123456789"

    if char in numbers:
        return True
    return False

def isOperator(char):
    operators = ". + - * / ++ -- == != > >= < <= && || =".split()

    if char in operators:
        return True
    return False

def whichOperatorToken(char):
    operators = ". + - * / ++ -- == != > >= < <= && || =".split()

    position = 0

    for operator in operators:
        if operator == char:
            break

        position += 1

        if position <= 9:
            return "TOKEN10{}".format(position)
        else:
            return "TOKEN1{}".format(position)

def isReservedWord(word):
    reserved = "begin end for do while int float double char string const array boolean if else switch case".split()

    if word in reserved:
        return True
    return False

def whichReservedToken(word):
    reserved = "begin end for do while int float double char string const array boolean if else switch case".split()

    position = 0

    for reserve in reserved:
        if reserve == word:
            break

        position += 1

        if position <= 9:
            return "TOKEN60{}".format(position)
        else:
            return "TOKEN6{}".format(position)

def isSymbol(char):
    symbols = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    if (char in symbols):
        return True
    return False

def lexicalAnalyzer():
    file_name = "code.txt"

    file = None

    if not os.path.exists(file_name):
        print("Arquivo não encontrado!")
        return
    else:
        file = open(file_name)

    program_line = file.readline()

    line_number = 1

    while program_line:
        i = 0

        line_size = len(program_line)

        while i < line_size:
            current_character = program_line[i]
            next_character = None

            if (i + 1) < line_size:
                next_character = program_line[i + 1]

            if(isDelimiter(current_character)):
                print("<{}, {}> - {}".format(whichDelimiterToken(current_character), current_character, line_number))
            elif(current_character == "#"):
                i = line_size
            elif current_character == "#" and next_character == "#":
                cont = True

                start_line = line_number

                while cont and not (current_character == "#" and next_character == "#"):
                    if (i + 2) < line_size:
                        i += 1
                        current_character = program_line[i]
                        next_character = program_line[i + 1]
                    else:
                        program_line = file.readline()
                        line_size = len(program_line)
                        line_number += 1
                        i = -1

                        if not program_line:
                            print(
                                "Erro Léxico - Comentário de bloco não foi fechado! - Inicio do erro: {}\n".format(
                                    start_line))
                            cont = False

                i += 1

            elif next_character != None and isOperator("{}{}".format(current_character, next_character)):
                print("<{}, {}> - {}".format(whichOperatorToken("{}{}".format(current_character, next_character)),
                                                current_character, line_number))
                i += 1
            elif isOperator(current_character):
                print("<{}, {}> - {}".format(whichOperatorToken("{}".format(current_character)), current_character,
                                                 line_number))

            elif current_character == string.punctuation[6]:
                if (program_line[i + 1] == "\n") or (not (string.punctuation[6] in program_line[i + 1:])):
                    print(
                        "Erro Léxico - O caracter não foi fechado! - Número da Linha: {}\n".format(
                            line_number))
                    i = line_size

                elif isSymbol(program_line[i + 1]) and program_line[i + 1] != string.punctuation[6] and \
                        program_line[i + 2] == string.punctuation[6]:
                    print("<TOKEN400, {}> - {}".format(program_line[i + 1], line_number))
                    i += 2
                elif program_line[i + 1] == string.punctuation[6] and program_line[i + 2] == string.punctuation[
                    6]:
                    print(
                        "Erro Léxico - Caracter não pode ser em aspas simples - Número da Linha: {}\n".format(
                            line_number))
                    i += 2
                elif program_line[i + 1] == string.punctuation[6]:
                    print(
                        "Erro Léxico - Caracter não pode ser vazio - Número da Linha: {}\n".format(
                            line_number))
                    i += 1
                else:
                    print(
                        "Erro Léxico - Tamanho ou simbolo do carater inválio - Número da Linha: {}\n".format(
                            line_number))
                    i = program_line[i + 1:].find(string.punctuation[6]) + 1

            elif current_character == string.punctuation[1]:
                i += 1
                isValid = True

                if program_line[i:].find(string.punctuation[1]) == -1:
                    print(
                        "Erro Léxico - String não fechada - Número da Linha: {}\n".format(
                            line_number))
                    i = line_size
                else:
                    end_string = i + program_line[i:].find(string.punctuation[1])
                    new_string = program_line[i:end_string]

                    i = end_string

                    for char in new_string:
                        if not isSymbol(char):
                            isValid = False
                            print(
                                "Erro Léxico - String com simbolo inválido (não ASCII) - Número da Linha: {}\n".format(
                                    line_number))
                            break

                    if isValid:
                        print("<TOKEN700, {}> - {}".format(new_string, line_number))

            elif isNumber(current_character):
                temp_string = current_character
                i += 1
                j = 0
                current_character = program_line[i]

                while isNumber(current_character) and (i + 1 < line_size):
                    temp_string += current_character
                    i += 1
                    current_character = program_line[i]

                if current_character == ".":
                    if (i + 1) < line_size:
                        temp_string += current_character
                        i += 1
                        current_character = program_line[i]

                        while isNumber(current_character) and i + 1 < line_size:
                            j += 1
                            temp_string += current_character
                            i += 1
                            current_character = program_line[i]

                        if current_character == '.':
                            j = 0

                            while (i + 1 < line_size):
                                i += 1
                                current_character = program_line[i]

                                if isDelimiter(current_character) or current_character == ' ':
                                    i -= 1
                                    break
                    else:
                        print("Erro Léxico - Número mal formado - Número da Linha: {}\n".format(line_number))

                    if j > 0:
                        print("<TOKEN301, {}> - {}".format(temp_string, line_number))
                    else:
                        print("Erro Léxico - Número mal formado - Número da Linha: {}\n".format(line_number))

                else:
                    print("<TOKEN300, {}> - {}".format(temp_string, line_number))

                    if not isNumber(current_character):
                        i -= 1

            elif(isLetter(current_character)):
                temp_string = current_character
                i += 1

                error = False

                while i < line_size:
                    next_character = None
                    current_character = program_line[i]

                    if (i + 1) < line_size:
                        next_character = program_line[i + 1]
                    if isLetter(current_character) or isNumber(current_character) or current_character == "_":
                        temp_string += current_character
                    elif isDelimiter(current_character) or current_character == " " or current_character == "\t" or current_character == "\r":
                        i -= 1
                        break
                    elif next_character != None and isOperator("{}{}".format(current_character, next_character) or isOperator(current_character)):
                        i -= 1
                        break
                    elif current_character != "\n":
                        print("Erro Léxico -  Identificador do caracter inválido: '{}' - Número da Linha: {}\n".format(current_character, line_number))
                        error = True
                        break

                    i += 1

                if error:
                    while i + 1 < line_size:
                        i += 1
                        current_character = program_line[i]
                        if isDelimiter(current_character) or current_character == " " or current_character == "\t" or current_character == "\r" or current_character == "/":
                            i -= 1
                            break
                        else:
                            if isReservedWord(temp_string):
                                print("<{}, {}> - {}".format(whichReservedToken(temp_string), temp_string, line_number))
                            else:
                                print("<TOKEN500, {}> - {}".format(temp_string, line_number))

            elif current_character != '\n' and current_character != ' ' and current_character != '\t' and current_character != '\r':
                print("Erro Léxico -  Caracter inválido: '{}' - Número da Linha: {}\n".format(
                    current_character, line_number))

            i += 1

        program_line = file.readline()
        line_number += 1

    file.close()



if __name__ == '__main__':
    lexicalAnalyzer()