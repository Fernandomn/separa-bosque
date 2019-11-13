import settings
import os
import sys
import tradutor


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
# Erro nos arquivos (CF):
# 498: Possuia uma tag P.vp -> converti pra P:vp
# 593: tem um PRP 'tipo' mal formatado. O prp não estava numa folha.
# 922: tinha um espaço em N>ARGS :pp, que tava zoando o rolê
# 1031: um artigo não fechado, que nem no 593
# 1183: palavra "tiro" não fechada. Como em 593
# 3013: Artigo não fechado. "o mais bonito". como em 593
# 3159: Artigo não fechado. Descobrir porque tem tantos artigos abertos.


#####################################

def main():
    settings.init()

    portugues = 'br'

    try:
        portugues = sys.argv[sys.argv.index('-l') + 1]
    except:
        portugues = 'br'

    endereco = "~/stanford-parser/BOSQUE/"
    # CENTEMPublico (portugues de portugual)
    arquivoPortugal = "Bosque_CP_8.0.PennTreebank.txt"
    # CENTEMFolha (portugues brasileiro)
    arquivoBrasil = "Bosque_CF_8.0.PennTreebank.txt"
    # NOTA: dentro do arquivo, a indicação está invertida: Aponta o CP como sendo
    # centemFolha, e viceversa. ignorar.

    nomeArquivo = arquivoPortugal if portugues == 'pt' else arquivoBrasil

    originalFile = open(nomeArquivo, 'r')

    originalLines = originalFile.readlines()

    dirBrasil = 'bosque_br_limpo_traduzido'
    dirPortugal = 'bosque_pt_limpo_traduzido'
    diretorio = dirPortugal if portugues == 'pt' else dirBrasil

    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
    os.chdir(diretorio)

    tradutor.createTransFile(originalLines)


if __name__ == '__main__':
    main()
