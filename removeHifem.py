import os

tagHifem = '_EC_'

portugues = 'br'
# portugues = 'pt'
dirBrasil = 'bosque_br_limpo_traduzido'
dirPortugal = 'bosque_pt_limpo_traduzido'
pasta = dirPortugal if portugues == 'pt' else dirBrasil
os.chdir(pasta)

endereco = '.'
diretorio = os.fsdecode(endereco)

for nomeArquivo in os.listdir(diretorio):
    arquivo = open(nomeArquivo, 'r', encoding='ISO-8859-1')
    linhas = arquivo.readlines()

    for indiceLinha in range(len(linhas)):
        if indiceLinha >= len(linhas):
            break

        linha = linhas[indiceLinha]

        indice = linha.find(tagHifem)

        if(indice < 0):
            continue

        indAbreParenteses = indice-1
        indFechaParenteses = 0

        for indCaracter in range(len(linha[indAbreParenteses:])):
            caracter = linha[indAbreParenteses:][indCaracter]
            if caracter == ')':
                indFechaParenteses = indCaracter + indAbreParenteses
                break

        folhaEc = linha[indAbreParenteses:indFechaParenteses+1]
        proximaLinha = linhas[indiceLinha+1]
        indFechaParProxLinha = proximaLinha.find(')')+1

        for index in range(indFechaParProxLinha, 0, -1):
            if proximaLinha[index] == '(':
                indAbreProxLinha = index
                break

        folhaNucleo = proximaLinha[indAbreProxLinha:indFechaParProxLinha]
        primeiraPalavra = folhaEc.replace(
            '(', '').replace(')', '').split(' ')[-1]
        segundaPalavra = folhaNucleo.replace(
            '(', '').replace(')', '').split(' ')[-1]
        novaTag = '%s(NP %s%s)%s' % (
            linha[:indAbreParenteses], primeiraPalavra, segundaPalavra, proximaLinha[indFechaParProxLinha:])

        linhas.insert(indiceLinha, novaTag)
        linhas.remove(proximaLinha)
        linhas.remove(linha)
    arquivo.close()
    arquivo = open(nomeArquivo, 'w', encoding='ISO-8859-1')
    arquivo.writelines(linhas)
    arquivo.close()
