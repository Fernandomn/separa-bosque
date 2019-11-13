import sys
import os

global tagRemover
global tagHifem
global tagCoord
global tagConjCoord


tagRemover = '(FRASE'
tagHifem = '_EC_'
tagCoord = '_CU_'
tagConjCoord = 'CC'


def init():
    global tabela
    tabela = {}

# Verifica se o o nó aliado é uma folha ou não


def ehFolha(linha, inicio):
    for i in range(inicio, len(linha)):
        if linha[i] == ')':
            return True
        elif linha[i] == '(' or linha[i] == '\n':
            return False
        else:
            continue


# trata o numero para fazer o nome do arquivo bonitinho
def tratarNumero(numero):
    if numero.isdigit():
        stringNumero = str(numero)
        tamString = len(stringNumero)
        if tamString == 1:
            return '000' + stringNumero
        elif tamString == 2:
            return '00' + stringNumero
        elif tamString == 3:
            return '0' + stringNumero
        elif tamString >= 4:
            return stringNumero
    else:
        return '0000'
