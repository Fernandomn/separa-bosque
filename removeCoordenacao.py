import os
import sys

#  arquivos problemáticos
# brasil: 102

tagCoord = '_CU_'
tagConjCoord = 'CC'

# dicionario com unico objetivo de devolver o sintagma equivalente À cordenação de partes de mesma POS
dicSintagma = {
    'NN': 'NP',
    'VBP': 'VP',  # verbos finitos - Verbo "normal". conferir inflexão da 3ª pessoa do inglês
    'VBG': 'VP',  # verbos gerúndios
    'VBN': 'VP',  # verbos particípios
    'VB': 'VP',
    'JJ': 'ADJP',  # Sintagma adjectivais
    'RB': 'ADVP',  # Sintagma adverbiais
    'IN': 'PP',  # não deve se aplicar
}

# def descobreSintagma(lista):


def reconstroiProf(frase, indice, lista):
    i = 0
    while i < len(frase):
        caracter = frase[i]
        if caracter == '(':
            novoIndice, listaProv = reconstroiProf(frase[i+1:], i+1, [])
            i = novoIndice+1
            lista.append(listaProv)
        elif caracter == ')':
            if(frase[:i].find(' ') >= 0):
                classe = ''.join(c for c in frase.split(
                    ' ')[0] if c.isalpha() or c == '_')
                palavra = frase[:i].split(' ')[1]
            else:
                palavra = frase[:i]
                classe = palavra
            if len(lista) > 0:
                return i+indice, [classe, lista]
            else:
                return i+indice, [classe, palavra]
        else:
            i += 1
    return i, lista[0]


def classesIguais(lista):
    controle = lista[0]
    for i in range(len(lista)):
        if lista[i] != controle:
            return False
    return True


def verificaCasosCU(arvore):
    numFilhos = 0
    global tagConjCoord
    if type(arvore[1]) is list:
        numFilhos = len(arvore[1])

    if arvore[0] == tagCoord:
        listaClasses = []

        wordLevel = True
        for filho in arvore[1]:
            if type(filho[1]) is list:
                wordLevel = False
            # TODO verificar AQUI se os filhos da coordenação são todos folha (ou seja, coordenação word level)
            if filho[0] != '.' and filho[0] != ',' and filho[0] != tagConjCoord:
                listaClasses.append(filho[0])
            # if filho[0] == 'CC':
            #     indice = arvore[1].index(filho)
            #     palavra = filho[1]
            #     arvore[1].remove(filho)
            #     arvore[1].insert(indice, palavra)

        # TODO: Verificar se as classes são puramente POS. Se forem, a classe tem que ter o sintagma apropriado
        if not wordLevel:
            classeCoord = listaClasses[0] if classesIguais(
                listaClasses) else "UCP"
        else:
            # TODO Verificar se são sempre iguais
            if classesIguais(listaClasses):
                classeCoord = 'WL_'+dicSintagma[listaClasses[0]]
            else:
                print('classes diferentes em wordlevel')
            #     classeCoord = descobreSintagma(listaClasses)
        arvore[0] = classeCoord

    if numFilhos > 0:
        for i in range(numFilhos):
            verificaCasosCU(arvore[1][i])
    else:
        return


def imprimeArvore(arvore, nivel):
    numFilhos = 0
    classe = arvore[0]
    espacoEsquerda = ''.join('  ' for n in range(nivel))

    if type(arvore[1]) is list:
        if 'WL_' in classe:
            # stringRetorno = '{0}{1}'.format(espacoEsquerda, arvore[1])
            lPalavras = ' '.join(filho[1] for filho in arvore[1])

            stringRetorno = '{0}({1} {2})\n'.format(
                espacoEsquerda, classe[3:], lPalavras)
        else:
            stringRetorno = '{0}({1} \n'.format(espacoEsquerda, classe)

            filhos = ''.join(imprimeArvore(filho, nivel+1)
                             for filho in arvore[1])
            stringRetorno += filhos

            stringRetorno += '{0})\n'.format(espacoEsquerda)
    else:
        if classe.isalpha():
            # else:
            stringRetorno = '{0}({1} {2})\n'.format(
                espacoEsquerda, classe, arvore[1])
        else:
            stringRetorno = '{0}({1})\n'.format(espacoEsquerda, classe)
    return stringRetorno


portugues = 'br'
# portugues = 'pt'

try:
    portugues = sys.argv[sys.argv.index('-l')+1]
except:
    portugues = 'br'

dirBrasil = 'bosque_br_limpo_traduzido'
dirPortugal = 'bosque_pt_limpo_traduzido'
pasta = dirPortugal if portugues == 'pt' else dirBrasil
os.chdir(pasta)

endereco = '.'
diretorio = os.fsdecode(endereco)

for nomeArquivo in os.listdir(diretorio):
    arquivo = open(nomeArquivo, 'r', encoding='ISO-8859-1')
    linhas = arquivo.readlines()
    anotacoes = []
    # for l in range(len(linhas)-1, 0, -1):
    for l in range(len(linhas)):
        linha = linhas[l]
        if linha[0] == '#':
            anotacoes.append(linha)
            # linhas.remove(linha)
    for anotacao in anotacoes:
        linhas.remove(anotacao)

    # nota: anteriormente, era feito um loop pelo arquivo para verificar a existencia da Tag.
    # Porém, notou-se que uma vez que a verificação de sua existencia já é feita em "verificaCasosCU()",
    # e também que, na verdade, é interessante reformatar todas as arvores (em "imprimeArvore()"),
    # preferiu-se por remover o loop / verificação
    frase = ''.join(linha for linha in linhas)
    i, arvore = reconstroiProf(frase, 0, [])
    verificaCasosCU(arvore)
    novaArvore = imprimeArvore(arvore, 0)
    arquivo = open(nomeArquivo, 'w', encoding='ISO-8859-1')
    # for anotacao in anotacoes:
    #     arquivo.write(anotacao)
    arquivo.write(novaArvore)
    arquivo.close()

    # for indiceLinha in range(len(linhas)):

    #     if indiceLinha >= len(linhas):
    #         break

    #     linha = linhas[indiceLinha]

    #     indice = linha.find(tagCoord)

    #     if(indice < 0):
    #         continue
    #     print('nomeArquivo:', nomeArquivo)
    #     frase = ''.join(linha for linha in linhas)
    #     i, arvore = reconstroiProf(frase, 0, [])
    #     verificaCasosCU(arvore)
    #     novaArvore = imprimeArvore(arvore, 0)
    #     arquivo = open(nomeArquivo, 'w', encoding='ISO-8859-1')
    #     arquivo.write(novaArvore)
    #     arquivo.close()
    #     break


# frase = '(S (_CU_ (VP (NP (PRP Alguns))(ADVP (RB at�))(ADVP (RB j�))(VP (VBP desapareceram))(,)(NP (ADVP (RB como)(NP (PRP o)(PP (IN de)(NP (NNP Castro_Verde)))))))(,)(CC e)(VP (NP (PRP outros))(VP (VBP t�m)(VBN vindo)(IN a)(VB perder))(NP (NN quadros)))(.)))'
# # frase = '(S (VP (_CU_ (CC Nem)(NP (NNP Lula))(CC nem)(NP (DT o)(NN partido)))(ADVP (RB ainda))(VP (VBP encontraram))(NP (DT um)(NN discurso))(PP (IN para)(VP (NP (PRP se))(VP (VB diferenciar))))(.)))'

# a = []

# i, b = reconstroiProf(frase, 0, a)
# print('arvore reconstruida:')
# print(b)

# verificaCasosCU(b)
# print('arvore sem coordenação:')
# print(b)

# c = imprimeArvore(b, 0)
# print('Arvore reconstruida:')
# print(c)
