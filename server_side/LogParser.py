import numpy as np

LOG_FILE_PATH = "logFile.txt"


def parseLog():
    address2name = {}
    file = open(LOG_FILE_PATH, 'r')
    lines = file.readlines()
    for line in lines[1:]:
        tokens = line.split(',')
        address = tokens[1].split('@')[0]
        predictedName = tokens[3]
        if not (predictedName == ""):
            address2name[address] = predictedName
    return address2name



if __name__ == '__main__':
    for pair in parseLog().items():
        # print(pair)
        print(f'{pair[0]} - {pair[1]}')

