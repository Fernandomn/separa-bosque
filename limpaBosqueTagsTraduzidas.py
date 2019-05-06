import os

# Referencias:
# https://www.linguateca.pt/floresta/BibliaFlorestal/anexo1.html
# https://www.linguateca.pt/floresta/BibliaFlorestal/anexo4.html
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://www.clips.uantwerpen.be/pages/mbsp-tags
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/a-definicao-de-oracao-nao-finita/17097
# https://educacao.uol.com.br/disciplinas/portugues/nocoes-de-morfossintaxe-nomes-e-pronomes.htm
# https://www.todamateria.com.br/passive-voice/
# https://www.infoescola.com/portugues/funcoes-do-se/
# https://www.linguateca.pt/floresta/BibliaFlorestal/sec09.html
# https://catalog.ldc.upenn.edu/LDC99T42
# https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/as-formas-finitas-e-nao-finitas-dos-verbos/32776

#  IDEIA DE NOME:
# Como treinar seu parser??
# Comentar como foi uma merda remover varias tags, como tem tags que foi um cu
# pra descobrir a tradução, e como levou muito tempo até eu fazer a
# substituição de FRASE
# Salientar, na escrita final, que palavras com hifem tiveram sua estrutura
# modificada para seguir o padrão do PTB.
# Algumas árvores tem mais de uma forma. Descobrir como gerar arquivos tipo 0, a, b
# Citar o StyleGuide oficial (trabalho da porra de achar:
#  https://catalog.ldc.upenn.edu/LDC99T42)
# Arquivos que precisaram ser modificados:
# 0002,0067,0261,0262,0275,0293,0349,0409,0501,0560,0666,0747,0791,0998,1403,
# 1482,1502,1517,1573,1607,1794,1798,1807,1887,1893,1925,1938,2033,2035,2381,
# 2489,2505,2668,2748,2780,2830,2907,3056,3082,3138,3168,3236,3331,3478,3547,
# 3581,3583,3592,3820,3833,3853,3881,3882,3898,3898,3976,4028,4096,4117,4160,
# 4300,4320,4338,4426,4517,4519,4553,4565,4580,4622,4710,4856,4973,5086,5099,
# 5101,5113,5139

tabela = {}


def tradutor(tag, i, originalLines):
    global tabela
    if not tabela:
        tabela = {
            # Formas Oracionais
            'fcl': 'VP',  # Forma Oracional Finita -> usa verbos não no infinitivo -> sintagma verbal
            'icl': 'VP',  # Forma Oracional não finita
            'acl': 'ADVP',  # Forma Oracional adverbial

            # Sintagmas
            'np': 'NP',  # Sintagma nominais
            'adjp': 'ADJP',  # Sintagma adjectivais
            'advp': 'ADVP',  # Sintagma adverbiais
            'vp': 'VP',  # Sintagma verbais
            'pp': 'PP',  # Sintagma preposicionais
            # Sintagma evidenciador coordenação
            'cu': '_CU_',
            # Sintagma sequências discursivas - (pnc dessa tag). Substituir por NP, por ser a tag filha imediata desta
            'sq': 'NP',

            # Classes de palavras
            'n': 'NN',  # substantivos
            'n-adj': 'NN',  # substantivos/adjectivos - pesquisar mostrou que são todos substantivos
            'adj': 'JJ',  # adjectivos
            'prop': 'NNP',  # nomes próprios
            'adv': 'RB',  # advérbios
            'num': 'CD',
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
            'adv': 'RB',  # advérbios
            'prp': 'IN',  # preposições
            'intj': 'UH',  # interjeições
            'conj-s': 'IN',  # conjunções subordinativa
            'conj-c': 'CC',  # conjunções coordenativa
            'ec': '_EC_',  # prefixos - ativei o modo Elza e let it go

            # Enunciados
            'UTT': 'NP',  # enunciados - não tem muito o que fazer aqui...
            'STA': 'NP',  # declarativo - outra tag aleatória
            'QUE': 'NP',  # interrogativo
            'CMD': 'VP',  # imperativo - caraio, não tem tag pra isso.
            'EXC': 'NP',  # exclamativo - pode ser literalmente qualquer um

            # Orações
            'SUBJ': '-SBJ',  # sujeito
            'ACC': '-OBJ',  # obj. directo
            'ACC-PASS': 'NP',  # part. apassivante - ok, inglês não tem nenhuma particula de voz passiva. é obj+to be + verbo participio + compl. seguindo o proprio BOSQUE, é um NP
            'DAT': '-OBJ',  # obj. ind. pronominal - não tem a inflexão dativa no inglês, e não tem tag no ptb para objeto indireto
            'PIV': 'IN',  # obj. ind. preposicional
            'PASS': 'IN',  # agente passiva - de acordo com o bosque, é pp
            # adj. adverbiais do sujeito SUB:conj-s poderia ser cu, pp, advp e np (referente ao BOSQUE), mas pp ocorre muito mais vezes
            'SA': 'IN',
            'OA': 'IN',  # adj. adverbiaiSUB:conj-s do objecto
            'ADVL': 'IN',  # adj. adverbiSUB:conj-sis livres - pode ser pp, advp, flc, icl, np, cu. principalmente pp ou advp. esses dois ultimos quase em igual proporção. vou chutar pp
            'SC': 'NP',  # predicativosSUB:conj-sdo sujeito - mais um caso múltiplo. pode ser np, advp, pp, icl, adjp, cu. np e advp com grandes chances. deliberadamente vou escolher np
            'OC': 'ADVP',  # predicativosSUB:conj-sdo objecto - pode ser adjp, advp, acl, cu, v-pcp, np, pp, icl. maior parte noa amostra foi acl
            # predicativos verbo-nominaisSUB:conj-s- podem ser icl, np, pp, adjp, cu, adj, pron-det. icl maioria.
            'PRED': 'VP',
            'VOC': 'NP',  # vocativo - toSUB:conj-so vocativo do bosque é um NP
            'APP': 'NP',  # apostos normaSUB:conj-s - pode ser fcl, np, adjp, cu, advp. np maioria
            'N<PRED': 'NP',  # apostos epit. predicativo - pode ser fcl, np, pp, cu. É bem distribuido, mas a priori, a maior parte é NP
            '>S': 'JJ',  # apostos da oração - se for >S, é sempre adj.
            'S<': 'NP',  # apostos da oração - se for S<, pode ser fcl ou np. Mais seguro ir no np
            # 'N<ARG.*': '_',  # compl. nominais - não existe
            'N<ARGS': 'IN',  # compl. nominais do sujeito - só tem pp, ufa
            'N<ARGO': 'IN',  # compl. nominais do objecto - só tem pp
            'N<ARG': 'IN',  # compl. nominais outros - só pp
            'P': 'VB',  # predicador - maior parte disparado é vp
            'FOC': 'RB',  # foco - maioria é advp
            # tópico - poucos casos. todos envolvem ou np, ou pronome.
            'TOP': 'NP',

            # Palavra
            'H': 'NN',  # núcleo - pqp. maior parte é n (substantivo)
            'MV': 'VBP',  # verbo principal - maioria v-fin
            'PMV': 'VBP',  # verbo principal - maioria são verbos finitos. Inflexões verbais do portugues muito diferentes da do inglês
            # verbo auxiliar (pra que por duas tags pramsm função? tnc). Maioria v-fin
            'AUX': 'VBP',
            'PAUX': 'VBP',  # verbo auxiliar
            'PRT-AUX': 'IN',  # part. lig. verbal - MAIOR PARTE DISPARADA PRP
            'SUB': 'IN',  # subordinador - sempre conj-s
            'CO': 'CC',  # coordenador - CONJ-C maioria
            # elemento conjunto - P/ cjt, maioria np (maioria nao absoluta)
            'CJT': 'NP',
            'PCJT': 'IN',  # elemento conjunto - p/ pcjt, maioria pp
            'x': 'VB',  # Tomar no cu essa tag. TODO
            'COM': 'RB',  # compl. comparação - maioria adv

            # Adjuntos
            '>N': 'DT',  # Adjuntos adnominais - maioria art
            'N<': 'IN',  # Adjuntos adnominais - maioria absoluta pp
            '>A': 'RB',  # Adjuntos adverbiais/adjectivais - maioria adv
            'A<': 'IN',  # Adjuntos adverbiais/adjectivais - maioria pp
            '>P': 'RB',  # Adjuntos preposicionais - maioria adv
            'P<': 'NP'  # Adjuntos preposicionais - maioria np
        }

    # remove o travessão da tag
    if tag[0] == '-':
        tag = tag[1:]
    if tag[-1] == '-':
        tag = tag[:-1]
    # print(tag)

    return tabela[tag]

# Verifica se o o nó aliado é uma folha ou não


def ehFolha(linha, inicio):
    for i in range(inicio, len(linha)):
        if linha[i] == ')':
            # print('folha')
            return True
        elif linha[i] == '(' or linha[i] == '\n':
            # print('no')
            return False
        else:
            continue

# trata o numero para fazer o nome do arquivo bonitinho


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


endereco = "~/stanford-parser/BOSQUE/"
nomeArquivo = "Bosque_CP_8.0.PennTreebank.txt"

a = []
nomeArquivoAbertoAtual = ''
# originalFile = open(nomeArquivo, 'r')
originalFile = open(nomeArquivo, 'r', encoding='utf-8')

originalLines = originalFile.readlines()
os.chdir('bosque_anotado_separado_limpo_traduzido')

with open('Bosque_0001', 'w') as finalFile:
    # eu quero declarar a variavel de arquivo aqui
    for i in range(len(originalLines)):
        line = originalLines[i]

        if line[0] == '#':
            numero = line[1:].split(' ')[0]
            if numero.isdigit():
                numeroTratado = tratarNumero(numero)
                nomeArquivoAbertoAtual = 'Bosque_'+numeroTratado
                finalFile = open(nomeArquivoAbertoAtual, 'w', encoding='utf-8')

        elif line.strip() == '':
            if not finalFile.closed:
                finalFile.close()

        else:
            if finalFile.closed:
                continue

            # remove a tag FRASE
            tagRemover = '(FRASE'
            tamTagRemover = len(tagRemover)

            if(line.find(tagRemover) >= 0):
                # o 2 é uma correção de quantidade de caracteres
                aSubstituir = line[tamTagRemover +
                                   1:].index(' ')+tamTagRemover+2
                line = line.replace(line[:aSubstituir], '(S ')

            for j in range(len(line)-1, 0, -1):
                if(j >= len(line)):
                    break

                char = line[j]
                if(char != '('):
                    continue

                inicio = j

                try:
                    final = inicio + line[inicio:].index(' ')
                    listaClasse = line[inicio+1:final].split(':')
                    if len(listaClasse) > 1:
                        funcao = listaClasse[0]
                        classe = listaClasse[1]
                        if classe == 'x' or funcao == 'X':
                            finalFile.close()
                            os.remove(finalFile.name)
                            break

                        newLine = line.replace(
                            line[inicio:final], '(' + tradutor(classe, i, j, originalLines))

                        line = newLine
                except ValueError:
                    continue
            if not finalFile.closed:
                finalFile.write(line)
