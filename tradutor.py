import settings
import os
import re
from sintagma import Sintagma

listaBrackets = ['(', ')', '[', ']', '{', '}']

dictBrackets = {'(': '-LRB-',
                ')': '-RRB-',
                '[': '-LSB-',
                ']': '-RSB-',
                '{': '-LCB-',
                '}': '-RCB-'}


# def tradutor(tag, i, originalLines):
def tradutor(tag):
    if not settings.tabela:
        settings.tabela = {
            'S': 'S',  # Marcador de Sentença

            # bracketing
            '(': '-LRB-',
            ')': '-RRB-',
            '[': '-LSB-',
            ']': '-RSB-',
            '{': '-LCB-',
            '}': '-RCB-',

            # Formas Oracionais
            'fcl': 'VP',  # Forma Oracional Finita -> usa verbos não no infinitivo -> sintagma verbal
            'icl': 'VP',  # Forma Oracional não finita
            'acl': 'ADVP',  # Forma Oracional averbal TODO

            # Sintagmas
            'np': 'NP',  # Sintagma nominais
            'adjp': 'ADJP',  # Sintagma adjectivais
            'advp': 'ADVP',  # Sintagma adverbiais
            'vp': 'VP',  # Sintagma verbais
            'pp': 'PP',  # Sintagma preposicionais
            # Sintagma evidenciador coordenação
            'cu': settings.tagCoord,
            # Sintagma sequências discursivas - (pnc dessa tag). Substituir por NP, por ser a tag filha imediata desta
            'sq': 'S',

            # Classes de palavras
            'n': 'NN',  # substantivos
            'n-adj': 'NN',  # substantivos/adjectivos - pesquisar mostrou que são todos substantivos
            'adj': 'JJ',  # adjectivos
            'prop': 'NNP',  # nomes próprios
            'adv': 'RB',  # advérbios
            'num': 'CD',  # numeral
            'v-fin': 'VBP',  # verbos finitos - Verbo "normal". conferir inflexão da 3ª pessoa do inglês
            'v-ger': 'VBG',  # verbos gerúndios
            'v-pcp': 'VBN',  # verbos particípios
            'v-inf': 'VB',  # verbos infinitivos
            'art': 'DT',  # artigos
            # pronomes determinativos - essa distinção não parece se aplicar propriamente àos pronomes em inglês. pesquisar mais. Notar que DEterminante não é Determiner (Artigo)
            'pron-det': 'PRP',
            # pronomes independentes - não achei essa classificação, independentes.
            'pron-rel': 'PRP',
            # pronomes independentes (tag nao está no dicionario oficial da linguateca)
            'pron-indp': 'PRP',
            'pron-pess': 'PRP',  # pronomes pessoais
            # pronomes pessoais (tag nao está no dicionario oficial da linguateca)
            'pron-pers': 'PRP',
            'prp': 'IN',  # preposições
            'intj': 'UH',  # interjeições
            'conj-s': 'IN',  # conjunções subordinativa
            'conj-c': settings.tagFlat,  # conjunções coordenativa
            'ec': settings.tagHifem,  # prefixos - ativei o modo Elza e let it go
        }

    if tag == '':
        return tag

    # remove o travessão da tag
    if tag[0] == '-':
        tag = tag[1:]
    if tag[-1] == '-':
        tag = tag[:-1]

    return settings.tabela[tag]


def tradutorFuncao(func_tag, form_tag):
    if not settings.tabelaFuncoes:
        pass
    settings.tabelaFuncoes = {
        # Enunciados
        'UTT': 'NP',  # enunciados -
        'STA': 'NP',  # declarativo -
        'QUE': 'NP',  # interrogativo
        'CMD': 'VP',  # imperativo -
        'EXC': 'NP',  # exclamativo -

        # Orações
        'SUBJ': '-SBJ',  # sujeito
        'ACC': '-OBJ',  # obj. directo
        'ACC-PASS': 'NP',
        # part. apassivante - ok, inglês não tem nenhuma particula de voz passiva. é obj+to be + verbo participio + compl. seguindo o proprio BOSQUE, é um NP
        'DAT': 'NP',  # obj. ind. pronominal - sempre NP.
        'PIV': 'PP',  # obj. ind. preposicional
        'PASS': 'PP',
        # agente passiva - por def (https://www.normaculta.com.br/agente-da-passiva/), "é um termo preposicionado). Logo, PP
        # adj. adverbiais do sujeito - poderia ser cu, pp, advp e np (referente ao BOSQUE), mas pp ocorre muito mais vezes
        'SA': 'IN',
        'OA': 'IN',  # adj. adverbiais do objecto
        'ADVL': 'IN',
        # adj. adverbiais livres - pode ser pp, advp, flc, icl, np, cu. principalmente pp ou advp. esses dois ultimos quase em igual proporção. vou chutar pp
        'SC': 'NP',
        # predicativos do sujeito - mais um caso múltiplo. pode ser np, advp, pp, icl, adjp, cu. np e advp com grandes chances. deliberadamente vou escolher np
        'OC': 'ADVP',
        # predicativos do objecto - pode ser adjp, advp, acl, cu, v-pcp, np, pp, icl. maior parte noa amostra foi acl
        # predicativos verbo-nominais - podem ser icl, np, pp, adjp, cu, adj, pron-det. icl maioria.
        'PRED': 'VP',
        'VOC': 'NP',  # vocativo - todo vocativo do bosque é um NP
        'APP': 'NP',  # apostos normal - pode ser fcl, np, adjp, cu, advp. np maioria
        'N<PRED': 'NP',
        # apostos epit. predicativo - pode ser fcl, np, pp, cu. É bem distribuido, mas a priori, a maior parte é NP
        '>S': 'JJ',  # apostos da oração - se for >S, é sempre adj.
        'S<': 'NP',  # apostos da oração - se for S<, pode ser fcl ou np. Mais seguro ir no np
        'N<ARGS': 'IN',  # compl. nominais do sujeito - só tem pp, ufa
        'N<ARGO': 'IN',  # compl. nominais do objecto - só tem pp
        'N<ARG': 'IN',  # compl. nominais outros - só pp
        'P': 'VB',  # predicador - maior parte disparado é vp
        'FOC': 'RB',  # foco - maioria é advp
        # tópico - poucos casos. todos envolvem ou np, ou pronome.
        'TOP': 'NP',
        'X': settings.tagX,

        # Palavra
        'H': form_tag,  # núcleo
        # 'MV': 'VBP',  # verbo principal - maioria v-fin
        # 'PMV': 'VBP',  # verbo principal - maioria são verbos finitos. Inflexões verbais do portugues muito diferentes da do inglês
        # verbo auxiliar (pra que por duas tags pramsm função? tnc). Maioria v-fin
        # 'AUX': 'VBP',
        # 'PAUX': 'VBP',  # verbo auxiliar
        # 'PRT-AUX': 'IN',  # part. lig. verbal - MAIOR PARTE DISPARADA PRP
        # 'SUB': 'IN',  # subordinador - sempre conj-s
        # 'CO': 'CC',  # coordenador - CONJ-C maioria
        # elemento conjunto - P/ cjt, maioria np (maioria nao absoluta)
        'CJT': settings.tagCJT,
        # 'PCJT': 'IN',  # elemento conjunto - p/ pcjt, maioria pp
        # # 'x': 'VB',  # Tomar no cu essa tag. TODO
        # 'COM': 'RB',  # compl. comparação - maioria adv

        # Adjuntos
        '>N': 'NP',  # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
        'N<': 'NP',  # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
        # '>A': 'ADVP',  # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
        # 'A<': 'ADVP',  # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
        '>P': 'PP',  # Adjuntos preposicionais - Adjunto de PP, pela X'
        'P<': 'PP'  # Adjuntos preposicionais - Adjunto de PP, pela X'
    }

    return settings.tabelaFuncoes[func_tag]


def fatia_arvore(frase):
    frase_split = re.findall('[\(\)]|[\wÀ-ú\,\.\'\"\!\*\,-\/\:\;\?\`\<\>\{\}\%\+\[\]]*', frase)
    frase_split = [c.strip() for c in frase_split]
    frase_split = [i for i in frase_split if i != '']
    return frase_split


def createTransFile(originalLines):
    tamTagRemover = len(settings.tagRemover)
    tree_text = ''
    with open('Bosque_0001', 'w') as finalFile:
        # eu quero declarar a variavel de arquivo aqui
        for i in range(len(originalLines)):
            line = originalLines[i]

            if line[0] == '#':
                numero = line[1:].split(' ')[0]
                if numero.isdigit():
                    frase = line[line.index(' ') + 1:]
                    numeroTratado = settings.tratarNumero(numero)
                    nomeArquivoAbertoAtual = 'Bosque_' + numeroTratado
                    finalFile = open(nomeArquivoAbertoAtual, 'w')

            elif line.strip() == '':
                if not finalFile.closed:
                    tree_split = fatia_arvore(tree_text)
                    tree_translate = translateTags(tree_split)

                    finalFile.close()
                    tree_text = ''


            else:
                if finalFile.closed:
                    continue
                tree_text += '' + line.strip()
                # remove a tag FRASE
                # if settings.tagRemover in line:
                #     # o 2 é uma correção de quantidade de caracteres
                #     aSubstituir = line[tamTagRemover +
                #                        1:].index(' ') + tamTagRemover + 2
                #     line = line.replace(line[:aSubstituir], '(S ')
                #
                # for j in reversed(range(len(line))):
                #     if j >= len(line):
                #         break
                #
                #     char = line[j]
                #     if (char != '('):
                #         continue
                #
                #     inicio = j
                #
                #     if line[inicio:].find(' ') >= 0:
                #         final = inicio + line[inicio:].index(' ')
                #         listaClasse = line[inicio + 1:final].split(':')
                #         if len(listaClasse) > 1:
                #             funcao = listaClasse[0]
                #             classe = listaClasse[1]
                #             if classe == 'x' or funcao == 'X':
                #                 finalFile.close()
                #                 os.remove(finalFile.name)
                #                 finalFile = open(nomeArquivoAbertoAtual,
                #                                  'w', encoding='ISO-8859-1')
                #                 finalFile.write('# Frase com tag X\n')
                #                 finalFile.write('# ' + frase)
                #                 finalFile.write('(S)')
                #                 finalFile.close()
                #                 break
                #
                #             newLine = line.replace(
                #                 line[inicio:final], '(' + tradutor(classe, i, originalLines))
                #             line = newLine
                #
                #     elif listaBrackets.count(line[inicio:][1]) > 0:
                #         newLine = line.replace(
                #             line[inicio:][1], dictBrackets[line[inicio:][1]])
                #         line = newLine
                #
                #     else:
                #         continue
                # if not finalFile.closed:
                #     finalFile.write(line)


def reconstroiArvore(frase_split, indice, arvore):
    i = 0

    while i < len(frase_split):
        item = frase_split[i]
        if item == '(':
            if 'FRASE' in frase_split[i + 1]:
                frase_split.remove(frase_split[i + 2])
                frase_split.remove(frase_split[i + 1])
                frase_split.insert(i + 1, 'S')
                # classe = 'S'
                # print(1)

            elif ':' in frase_split[i + 1]:
                split_temp = frase_split[i + 1].split(':')
                if split_temp[1] not in settings.posTagsProb:
                    frase_split[i + 1] = split_temp[1]
                else:
                    frase_split[i + 1] = tradutorFuncao(split_temp[0], split_temp[1])

            elif re.match('\W', frase_split[i + 1]):
                # print(2)
                i += 1
                continue
            #     TODO
            classe = frase_split[i + 1]

            nova_arvore = Sintagma(classe, [], arvore.classe, '')
            novo_indice, subarvore = reconstroiArvore(frase_split[i + 1:], i + 1, nova_arvore)
            i = novo_indice + 1
            arvore.filhos.append(subarvore)
        elif item == ')':
            # classe_temp = ''.join(frase_split[:i - 1])
            palavra = frase_split[i - 1]
            classe = tradutor(frase_split[0])
            if palavra == '%':
                classe = settings.percentTag

            if len(arvore.filhos):
                subarvore = Sintagma(classe, arvore.filhos, tradutor(arvore.classe), '')
            else:
                subarvore = Sintagma(classe, [], tradutor(arvore.classe_pai), palavra)
            return i + indice, subarvore
        elif i - 1 == 0 and re.match('\W', item) and item != '%':
            # porcentagem é considerada uma palavra, logo, um nó. será necessário marcá-lo, para transformar o símbolo,
            # e o numero anterior, numa \textit{flat structure}
            # print(2)
            palavra = item if item not in dictBrackets.keys() else dictBrackets(item)
            subarvore = Sintagma('', [], arvore.classe, palavra)
            # return i+indice, subarvore
            arvore.filhos.append(subarvore)
            i += 2
            continue
        # elif item in settings.pointList: #particular do CINTIL
        #     if frase_split[i - 1] == 'NNS':
        #         frase_split[i - 1] = settings.pointTag
        #         subarvore = Sintagma(settings.pointTag, [], arvore.classe, item)
        #         # i+=1
        #         arvore.filhos.append(subarvore)
        #         # continue
        #     else:
        #         # point = item if not (item == '"' or item == "'") else item + item
        #         subarvore = Sintagma(settings.pointTag, [], arvore.classe, item)
        #         arvore.filhos.append(subarvore)
        #     i += 1
        else:
            i += 1
    return i, arvore


def translateTags(tree_split):
    raiz = Sintagma('', [], '', '')
    i, arvore = reconstroiArvore(tree_split, 0, raiz)
    print(arvore)
