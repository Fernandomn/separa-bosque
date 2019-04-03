import os

endereco = "~/stanford-parser/BOSQUE/"
nomeArquivo = "Bosque_CP_8.0.PennTreebank.txt"


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


a = []
originalFile = open(nomeArquivo, 'r', encoding='latin-1')
os.chdir('bosque_anotado_separado')
with open('Bosque_0000', 'w') as finalFile:
    # eu quero declarar a variavel de arquivo aqui
    for line in originalFile:
        # print ('line: ', line)
        if line[0] == '#':
            numero = line[1:].split(' ')[0]
            if numero.isdigit():
                numeroTratado = tratarNumero(numero)
                finalFile = open('Bosque_'+numeroTratado, 'w')
                # print('Abrindo arquivo Bosque_'+numero)
        elif line.strip() == '':
            if not finalFile.closed:
                finalFile.close()
                # print('Fechou arquivo')
        else:
            if not finalFile.closed:
                # print('Escrevendo linha:', line)
                finalFile.write(line)
