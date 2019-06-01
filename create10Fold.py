import os
import sys
import math

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
listFiles = os.listdir(diretorio)
listFiles.sort()
testName = 'testFold'
trainingName = 'trainingFold'

folder = 'fold'
qntFolds = 10
qntFiles = len(listFiles)

for fold in range(qntFolds):
    diretorio = '{0}{1}'.format(folder, fold+1)
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
    foldsFraction = len(listFiles)/qntFolds
    start = math.floor(foldsFraction*fold)
    end = math.floor(foldsFraction*(fold+1))

    testFile = open('{0}{1}'.format(testName, fold),
                    'w', encoding='ISO-8859-1')
    trainingFile = open('{0}{1}'.format(
        trainingName, fold), 'w', encoding='ISO-8859-1')

    listTestFiles = listFiles[start:end]
    listTrainigFiles = listFiles[:start] + listFiles[end:]
    os.chdir(diretorio)

    for fileName in listTestFiles:
        openedFile = open(fileName, 'r', encoding='ISO-8859-1')
        lines = openedFile.readlines()
        for line in lines:
            testFile.write(line)

    for fileName in listTrainigFiles:
        openedFile = open(fileName, 'r', encoding='ISO-8859-1')
        lines = openedFile.readlines()
        for line in lines:
            trainingFile.write(line)

    testFile.close()
    trainingFile.close()

    os.chdir('../')
