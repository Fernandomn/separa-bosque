import os
import sys

try:
    portugues = sys.argv[sys.argv.index('-l')+1]
except:
    portugues = 'br'

# CENTEMPublico (portugues de portugual)
arquivoPortugal = "Bosque_CF_8.0.PennTreebank.txt"
# CENTEMFolha (portugues brasileiro)
arquivoBrasil = "Bosque_CP_8.0.PennTreebank.txt"

nomeArquivo = arquivoPortugal if portugues == 'pt' else arquivoBrasil

dirBrasil = 'bosque_sentencas_separado_br'
dirPortugal = 'bosque_sentencas_separado_pt'
diretorio = dirPortugal if portugues == 'pt' else dirBrasil

if not os.path.exists(diretorio):
    os.mkdir(diretorio)
os.chdir(diretorio)


def tratarNumero(numero):
    if numero.isdigit():
        stringNumero = str(numero)
        tamString = len(stringNumero)
        if tamString == 1:
            return '000'+stringNumero
        elif tamString == 2:
            return '00'+stringNumero
        elif tamString == 3:
            return '0'+stringNumero
        elif tamString >= 4:
            return stringNumero
    else:
        return '0000'


originalFile = open(nomeArquivo, 'r', encoding='ISO-8859-1')

with open('Bosque_sent_0000', 'w') as finalFile:
    for line in originalFile:
        if line[0] == '#':
            numero = line[1:].split(' ')[0]
            if numero.isdigit():
                numeroTratado = tratarNumero(numero)
                finalFile = open('Bosque_sent_'+numeroTratado,
                                 'w', encoding='ISO-8859-1')
                frase = line.split(' ')[2:]
                finalFile.write(' '.join(frase))
                finalFile.close()
