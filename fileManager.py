import os
import json

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

def createJsonFile(input):
    with open('config.json','w',encoding='utf-8') as f:
        json.dump(input,f,ensure_ascii=False)