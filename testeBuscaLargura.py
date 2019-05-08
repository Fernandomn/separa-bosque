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
    return i, lista


def verificaCasosCU(arvore):
    numFilhos = len(arvore[0][1])
    if arvore[0] != '_CU_':
        if numFilhos > 0:
            for i in range(numFilhos):
                verificaCasosCU(arvore[0][1][i])
        else:
            return
    else:
        listaClasses = []
        for filho in arvore[1]:
            listaClasses.append(filho[0])
        a = listaClasses[0]
        print(listaClasses)


# frase = '012345'
# frase = 'a vida é bela'
frase = '(S (_CU_ (VP (NP (PRP Alguns))(ADVP (RB at�))(ADVP (RB j�))(VP (VBP desapareceram))(,)(NP (ADVP (RB como)(NP (PRP o)(PP (IN de)(NP (NNP Castro_Verde)))))))(,)(CC e)(VP (NP (PRP outros))(VP (VBP t�m)(VBN vindo)(IN a)(VB perder))(NP (NN quadros)))(.)))'

a = []

i, b = reconstroiProf(frase, 0, a)
verificaCasosCU(b)
print(b)
