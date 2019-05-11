tagCoordenacao = 'CC'


def reconstroiProf(frase, indice, lista):
    i = 0
    while i < len(frase):
        caracter = frase[i]
        if caracter == '(':
            novoIndice, listaProv = reconstroiProf(frase[i+1:], i+1, [])
            i = novoIndice+1
            lista.append(listaProv)
        elif caracter == ')':
            if(len(frase[:i]) > 1):
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
    global tagCoordenacao
    if type(arvore[1]) is list:
        numFilhos = len(arvore[1])

    if arvore[0] == '_CU_':
        listaClasses = []

        for filho in arvore[1]:
            if filho[0] != '.' and filho[0] != ',' and filho[0] != tagCoordenacao:
                listaClasses.append(filho[0])
            # if filho[0] == 'CC':
            #     indice = arvore[1].index(filho)
            #     palavra = filho[1]
            #     arvore[1].remove(filho)
            #     arvore[1].insert(indice, palavra)

        classeCoord = listaClasses[0] if classesIguais(listaClasses) else "UCP"
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
        stringRetorno = '{0}({1}\n'.format(espacoEsquerda, classe)

        filhos = ''.join(imprimeArvore(filho, nivel+1) for filho in arvore[1])
        stringRetorno += filhos

        stringRetorno += '{0})\n'.format(espacoEsquerda)
    else:
        stringRetorno = '{0}({1} {2})\n'.format(
            espacoEsquerda, classe, arvore[1])
    return stringRetorno


frase = '(S (_CU_ (VP (NP (PRP Alguns))(ADVP (RB at�))(ADVP (RB j�))(VP (VBP desapareceram))(,)(NP (ADVP (RB como)(NP (PRP o)(PP (IN de)(NP (NNP Castro_Verde)))))))(,)(CC e)(VP (NP (PRP outros))(VP (VBP t�m)(VBN vindo)(IN a)(VB perder))(NP (NN quadros)))(.)))'
# frase = '(S (VP (_CU_ (CC Nem)(NP (NNP Lula))(CC nem)(NP (DT o)(NN partido)))(ADVP (RB ainda))(VP (VBP encontraram))(NP (DT um)(NN discurso))(PP (IN para)(VP (NP (PRP se))(VP (VB diferenciar))))(.)))'

a = []

i, b = reconstroiProf(frase, 0, a)
print('rvore reconstruida:')
print(b)

verificaCasosCU(b)
print('arvore sem coordenação:')
print(b)

c = imprimeArvore(b, 0)
print('Arvore reconstruida:')
print(c)
