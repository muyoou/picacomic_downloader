import os
import json

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        print(path)
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

def updataDownloaded(input):
    with open('.\\data\\downloaded.json', 'w') as f:
        json.dump(input,f,ensure_ascii=False)

def createNewFile(filename):
    fd = open(filename, mode="w", encoding="utf-8")
    fd.close()

def saveImg(img,path):
    if not isExist(path):
        open(path, 'wb').write(img)

def removeToken():
    if isExist(".\\data\\token.dat"):
        os.unlink(".\\data\\token.dat")