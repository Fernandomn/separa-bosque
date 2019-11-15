import settings
import os
import re
from sintagma import Sintagma

listaBrackets = ['(', ')', '[', ']', '{', '}']


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
    # tag.replace('-', '')
    return settings.tabela[tag]


def tradutorFuncao(func_tag, form_tag):
    # form_tag = tradutor(form_tag)
    if not settings.tabelaFuncoes:
        settings.tabelaFuncoes = {
            # Enunciados - Todos Enunciados são considerados inicios de Sentenças -> S
            'UTT': 'S',  # enunciados -
            'STA': 'S',  # declarativo -
            'QUE': 'S',  # interrogativo
            'CMD': 'S',  # imperativo -
            'EXC': 'S',  # exclamativo -

            # Orações
            'SUBJ': tradutor(form_tag),
            # sujeito - marcador de sentenças. A tag de forma costuma dizer o tipo de sintagma.
            # obj. directo - similar a sujeito, a tag forma informa o tipo de sintagma.
            'ACC': tradutor(form_tag) if form_tag != 'cu' else 'NP',
            'ACC-PASS': 'NP',
            # part. apassivante - ok, inglês não tem nenhuma particula de voz passiva. é obj+to be + verbo participio + compl. seguindo o proprio BOSQUE, é um NP
            'DAT': 'NP',  # obj. ind. pronominal - sempre NP.
            'PIV': 'PP',  # obj. ind. preposicional
            'PASS': 'PP',
            # agente passiva - por def (https://www.normaculta.com.br/agente-da-passiva/), "é um termo preposicionado). Logo, PP
            # adj. adverbiais do sujeito - poderia ser cu, pp, advp e np (referente ao BOSQUE), mas pp ocorre muito mais vezes
            'SA': 'IN',
            'OA': tradutor(form_tag),  # adj. adverbiais do objecto - formTag informa o sintagma
            # adj. adverbiais  - a form_tag informa o sintagma. em caso de ACL, é advp.
            'ADVL': 'ADVP' if form_tag == 'acl' else tradutor(form_tag),
            # predicativos do sujeito - O Predicativo do Sujeito, representado pela etiqueta SC estabelece uma relação de
            # predicação com o sujeito por meio de verbos copulativos ou verbos que, não sendo copulativos, exibem um
            # comportamento semelhante em termos semânticos (Biblia). Logo, VP
            'SC': 'VP',
            # predicativos do objecto - a tag form costuma dizer o sintagma.
            'OC': 'NP' if form_tag == 'acl' else tradutor(form_tag),
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
            'H': tradutor(form_tag),  # núcleo
            # 'MV': 'VBP',  # verbo principal - maioria v-fin
            # 'PMV': 'VBP',  # verbo principal - maioria são verbos finitos. Inflexões verbais do portugues muito diferentes da do inglês
            # verbo auxiliar (pra que por duas tags pramsm função? tnc). Maioria v-fin
            'AUX': 'VBP',
            # Por 11.1.1. Particípios com argumentos coordenados, com partilha de auxiliar, considerado VP
            'AUX<': 'VP',
            # 'PAUX': 'VBP',  # verbo auxiliar
            # 'PRT-AUX': 'IN',  # part. lig. verbal - MAIOR PARTE DISPARADA PRP
            # 'SUB': 'IN',  # subordinador - sempre conj-s
            # 'CO': 'CC',  # coordenador - CONJ-C maioria
            # elemento conjunto - P/ cjt, maioria np (maioria nao absoluta)
            'CJT': settings.tagCJT,
            # 11.2. Coordenação de constituintes com funções diferentes
            'CJT&ACC': 'NP',
            'CJT&PRED': 'ADJP',
            'CJT&ADVL': 'PP',
            'CJT&PASS': 'PP',
            # 'PCJT': 'IN',  # elemento conjunto - p/ pcjt, maioria pp
            # # 'x': 'VB',  # Tomar no cu essa tag. TODO
            # 'COM': 'RB',  # compl. comparação - maioria adv

            # Adjuntos
            '>N': 'NP',  # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
            'N<': 'NP',  # Adjuntos adnominais - pela teoria X', ocorre uma dobra do XP origem. (Mioto, p 68)
            '>A': '>A',  # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
            'A<': 'A<',  # Adjuntos adverbiais/adjectivais - PRECISA VERIFICAR O NUCLEO (irmão) TODO
            '>P': 'PP',  # Adjuntos preposicionais - Adjunto de PP, pela X'
            'P<': 'PP',  # Adjuntos preposicionais - Adjunto de PP, pela X'
            'KOMP<': settings.kompTag,  # Comparativos - Comp. é o cap. 22 inteiro do bracketing guidelines. TODO
        }

    # func_tag.replace('-', '')
    return settings.tabelaFuncoes[func_tag]


def fatia_arvore(frase):
    frase_split = re.findall('[\(\)]|[\wÀ-ú\,\.\'\"\!\*\,-\/\:\;\?\`\<\>\{\}\%\+\[\]\&]*', frase)
    frase_split = [c.strip() for c in frase_split]
    frase_split = [i for i in frase_split if i != '']
    return frase_split


def createTransFile(originalLines, dir):
    # tamTagRemover = len(settings.tagRemover)
    tree_text = ''
    here = os.path.dirname(os.path.realpath(__file__))

    with open('Bosque_0001', 'w') as finalFile:
        # eu quero declarar a variavel de arquivo aqui
        for i in range(len(originalLines)):
            line = originalLines[i]

            if line[0] == '#':
                numero = line[1:].split(' ')[0]
                if numero.isdigit():
                    # frase = line[line.index(' ') + 1:]
                    numero_tratado = settings.tratarNumero(numero)
                    print(numero_tratado)
                    file_name = 'Bosque_' + numero_tratado

                    filepath = os.path.join(here, dir, file_name)

                    finalFile = open(filepath, 'w')

            elif line.strip() == '':
                if not finalFile.closed:
                    tree_split = fatia_arvore(tree_text)
                    tree_translate = translateTags(tree_split)
                    finalFile.write(tree_translate)
                    finalFile.close()
                    tree_text = ''

            else:
                if finalFile.closed:
                    continue
                tree_text += '' + line.strip()


def gera_tag_rels(func, form):
    if func not in settings.rel_func_tag:
        settings.rel_func_tag[func] = 1
    else:
        settings.rel_func_tag[func] += 1
    if form not in settings.rel_form_tag:
        settings.rel_form_tag[form] = 1
    else:
        settings.rel_form_tag[form] += 1
    par = '{0}:{1}'.format(func, form)
    if par not in settings.rel_func_form_tag:
        settings.rel_func_form_tag[par] = 1
    else:
        settings.rel_func_form_tag[par] += 1


def gera_point_rel(point):
    if point not in settings.rel_point:
        settings.rel_point[point] = 1
    else:
        settings.rel_point[point] += 1


def removeHifens(tag):
    if tag[0] == '-':
        tag = tag[1:]
    if tag[-1] == '-':
        tag = tag[:-1]
    return tag


# reconstroi a estrutura da sentença classificada em árvores lógicas
def reconstroiArvore(frase_split, indice, arvore):
    i = 0

    while i < len(frase_split):
        item = frase_split[i]
        if item == '(':
            # começo da sentença
            if 'FRASE' in frase_split[i + 1]:
                frase_split.remove(frase_split[i + 2])
                frase_split.remove(frase_split[i + 1])
                frase_split.insert(i + 1, 'S')

                classe = frase_split[i + 1]

            # caso padrão. cabeçalho do bosque tem muitos valores
            elif ':' in frase_split[i + 1]:
                split_temp = frase_split[i + 1].split(':')
                # func = split_temp[0]
                # form = split_temp[1]
                func = removeHifens(split_temp[0])
                form = removeHifens(split_temp[1])

                # form = split_temp[1].replace('-', '')

                gera_tag_rels(func, form)

                if form not in settings.posTagsProb:
                    frase_split[i + 1] = tradutor(form)
                else:
                    frase_split[i + 1] = tradutorFuncao(func, form)
                classe = frase_split[i + 1]

            # pontuações. são SEMPRE um problema.
            elif re.match('\W', frase_split[i + 1]):
                classe = settings.tagPoint

            # se a árvore precisar ser corrigida no futuro.
            if '_' in classe and not settings.tagProblematica:
                settings.tagProblematica = True

            nova_arvore = Sintagma(classe, [], arvore.classe, '')
            novo_indice, subarvore = reconstroiArvore(frase_split[i + 1:], i + 1, nova_arvore)
            i = novo_indice + 1
            arvore.filhos.append(subarvore)
        elif item == ')':

            palavra = frase_split[i - 1]
            classe = frase_split[0]

            # porcentagem é considerada uma palavra, logo, um nó. será necessário marcá-lo, para transformar o símbolo,
            # e o numero anterior, numa \textit{flat structure}
            if palavra == '%':
                classe = settings.percentTag

            #     palavra == classe quando é um sinal
            if re.match('\W', palavra) and palavra == classe:
                gera_point_rel(palavra)
                if palavra in settings.dictBrackets:
                    palavra = settings.dictBrackets[palavra]
                classe = settings.tagPoint

            if len(arvore.filhos):
                subarvore = Sintagma(classe, arvore.filhos, arvore.classe_pai, '')
            else:
                subarvore = Sintagma(classe, [], arvore.classe_pai, palavra)
            return i + indice, subarvore
        else:
            i += 1
    return i, arvore


# revisa e corrige tags que precisem de tratamentos especiais
def tagFilhosCoord(filhos):
    # classe_base = filhos[0].classe
    filhos_iguais = True
    tag_comp = ''
    for filho in filhos:
        if filho.classe == settings.tagFlat:
            continue
        if tag_comp == '':
            tag_comp = filho.classe
        if filho.classe != tag_comp:
            filhos_iguais = False
            break
    return tag_comp if filhos_iguais else 'UCP'


def revisaTags(arvore):
    classe = arvore.classe

    if classe == settings.tagCoord:
        # pro futuro: colocar function tags no UCP.
        arvore.classe = tagFilhosCoord(arvore.filhos)
        arvore.atualizaClasseFilhos()

    # if classe == settings.pointTag:
    #     return
    # if classe in settings.tagsProblematicas:
    #     arvore = consertaTagProbObj(arvore)

    if len(arvore.filhos) > 0:
        for i in range(len(arvore.filhos)):
            # como vários nós serão removidos, restrição para não travar o loop
            if i >= len(arvore.filhos):
                break
            filho = arvore.filhos[i]
            revisaTags(filho)
            if filho.classe == settings.tagHifem:
                irmao_direita = arvore.filhos[i + 1]
                novo_filho = Sintagma('NP', [], arvore.classe, '{0}{1}'.format(filho.valor, irmao_direita.valor))
                arvore.filhos.insert(i, novo_filho)
                arvore.removeFilho(filho)
                arvore.removeFilho(irmao_direita)
            # if settings.removeTag == filho.classe:
            #     arvore.removeFilho(filho)
        # setRemoveTagsObj(arvore)
    else:
        return


# imprime a árvore no padrão PTB
def imprimeArvore(arvore, nivel):
    espaco_esquerda = ''.join(' ' for n in range(nivel))

    # raiz
    if arvore.classe == '':
        return '(\n{0})'.format(imprimeArvore(arvore.filhos[0], nivel + 1))

    # nao-terminal
    if len(arvore.filhos) > 0:

        string_filhos = ''
        if arvore.classe in settings.wordLevelTags and arvore.valor != '':
            for filho in arvore.filhos:
                string_filhos += filho.valor + ' '

            string_retorno = '{0}{1}\n'.format(espaco_esquerda, string_filhos.strip())
            # string_retorno = '{0}({1} {2})\n'.format(espaco_esquerda, arvore.classe, string_filhos.strip())
        else:
            for filho in arvore.filhos:
                string_filhos += imprimeArvore(filho, nivel + 1)

            string_retorno = '{0}({1} \n{2}{0})\n'.format(espaco_esquerda, arvore.classe, string_filhos)
    # terminal
    else:
        if arvore.classe == settings.tagPoint:
            string_retorno = '{0}{1}\n'.format(espaco_esquerda, arvore.valor)
            # string_retorno = ''
        else:
            string_retorno = '{0}({1} {2})\n'.format(espaco_esquerda, arvore.classe, arvore.valor)

    return string_retorno


def translateTags(tree_split):
    raiz = Sintagma('', [], '', '')
    i, arvore = reconstroiArvore(tree_split, 0, raiz)
    # print(arvore)
    if settings.tagProblematica:
        revisaTags(arvore)
        settings.tagProblematica = False
    tree_text = imprimeArvore(arvore, 0)
    return tree_text
