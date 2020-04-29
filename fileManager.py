import os
import json

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

def createJsonFile(input,name):
    mkdir(".\\data")
    with open('.\\data\\'+name,'w',encoding='utf-8') as f:
        json.dump(input,f,ensure_ascii=False)

def openFile(input):
    os.startfile(input)

def isExist(input):
    return os.path.exists(input)

def readConfig():
    with open('.\\data\\config.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
        return data

def creatTokenFile(input):
    with open('.\\data\\token.dat', 'w') as f:
        f.write(input)

def readToken():
    return open(".\\data\\token.dat", "r+").readline()

def readDownloaded():
    with open('.\\data\\downloaded.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
        return data

def createNewFile(filename):
    fd = open(filename, mode="w", encoding="utf-8")
    fd.close()