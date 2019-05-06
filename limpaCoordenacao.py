import os


def listaPOScu(i, j, originalLines):
    contaParenteses = 1
    passouCu = False
    listaPOS = []

    for k in range(i, len(originalLines)):
        linha = originalLines[k]
        u = 0
        if k == i:
            u = j

        for w in range(u, len(linha)):
            if linha[w] != '(' or linha[w] != ')':
                continue
            if linha[w] == '(':
                novaLinha = linha.split(' ')
                if not passouCu and novaLinha.index('cu') > -1:
                    passouCu = True
                elif passouCu:
                    contaParenteses += 1
            if passouCu and linha[w] == ')':
                contaParenteses -= 1
            if contaParenteses == 2:
                novaLinha[w:] = linha.split(' ')
                listaPOS.append(novaLinha[0][1:])

    return listaPOS


def traduzCu(i, j, originalLines):

    listaPOS = listaPOScu(i, j, originalLines)

    return '_CU_'

endereco = '.'
tagCoord = '_CU_'
diretorio = os.fsdecode(endereco)
os.chdir('bosque_anotado_separado_limpo_traduzido')


for nomeArquivo in os.listdir(diretorio):
    arquivo = open(nomeArquivo, 'r', encoding='utf-8')
    linhas = arquivo.readlines()

    for i in range(len(linhas)):
        if i >= len(linhas):
            break
        linha = linhas[i]

        indice = linha.find(tagCoord)

        if(indice < 0):
            continue