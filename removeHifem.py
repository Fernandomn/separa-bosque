import os

tagHifem = '_EC_'
# os.chdir('bosque_anotado_separado_limpo_traduzido')

portugues = 'br'
# portugues = 'pt'
dirBrasil = 'bosque_br_limpo_traduzido'
dirPortugal = 'bosque_pt_limpo_traduzido'
pasta = dirPortugal if portugues == 'pt' else dirBrasil
os.chdir(pasta)

endereco = '.'
diretorio = os.fsdecode(endereco)

for nomeArquivo in os.listdir(diretorio):
    arquivo = open(nomeArquivo, 'r', encoding='utf-8')
    linhas = arquivo.readlines()
    for indiceLinha in range(len(linhas)):
        if indiceLinha >= len(linhas):
            break
        linha = linhas[indiceLinha]

        indice = linha.find(tagHifem)

        if(indice < 0):
            continue
        # print(nomeArquivo)
        # print('próxima linha: '+linhas[indiceLinha+1])

        indAbreParenteses = indice-1
        indFechaParenteses = 0
        # print('linha[indAbreParenteses:]'+linha[indAbreParenteses:])
        for indCaracter in range(len(linha[indAbreParenteses:])):
            caracter = linha[indAbreParenteses:][indCaracter]
            if caracter == ')':
                indFechaParenteses = indCaracter + indAbreParenteses
                break
        # print(indAbreParenteses)
        # print(indFechaParenteses)
        folhaEc = linha[indAbreParenteses:indFechaParenteses+1]
        proximaLinha = linhas[indiceLinha+1]
        # print('folhaEc' + folhaEc)
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

        # print('linha: '+linha)
        # print('proximaLinha'+proximaLinha)
        novaTag = '%s(NP %s%s)%s' % (
            linha[:indAbreParenteses], primeiraPalavra, segundaPalavra, proximaLinha[indFechaParProxLinha:])
        # print(novaTag)
        linhas.insert(indiceLinha, novaTag)
        linhas.remove(proximaLinha)
        linhas.remove(linha)
    arquivo.close()
    arquivo = open(nomeArquivo, 'w', encoding='utf-8')
    arquivo.writelines(linhas)
    arquivo.close()
