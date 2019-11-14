import sys
import os


def init():
    global tabela
    global tabelaFuncoes
    global tagPoint
    global tagRemover
    global tagHifem
    global tagCoord
    global tagConjCoord
    global percentTag
    global tag_x
    global tagX
    global tag_acl
    global posTagsProb
    global tagProblematica
    global tagCu
    global tagCJT
    global tagFlat
    global rel_point
    global rel_func_tag
    global rel_form_tag
    global portugues
    global kompTag

    tagProblematica = False
    tagRemover = '_TOREMOVE_'
    tagHifem = '_EC_'
    tagCu = 'cu'
    tagCoord = '_CU_'
    tagCJT = '_CJT_'
    tagConjCoord = 'CC'
    percentTag = '_PERC_'
    tag_acl = 'acl'
    tag_x = 'x'
    tagX = '_X_'
    tagFlat = '_FLAT_'
    tagPoint = 'PNT'
    kompTag = '_KOMP_'
    posTagsProb = [tag_x, tag_acl]
    tabela = {}
    tabelaFuncoes = {}
    rel_point = {}
    rel_form_tag = {}
    rel_func_tag = {}


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
