import d
import fileManager
import setbox

log=None
root=None
def printl(text):
    log.insert('end',text+'\n')
    log.see('end')

def setConfig(data):
    d.Email=data['user']
    d.Password=data['password']
    d.Proxy=data['proxy']
    d.Image_quality=data['quality']

def getConfigByFile():
    setConfig(fileManager.readConfig())

def printConfig():
    printl("----------------------")
    printl("用户名："+d.Email)
    printl("图片质量："+d.Image_quality)
    printl("代理设置："+d.Proxy)
    printl("----------------------")

def openfolder():
    fileManager.openFile(".\\comic")

def openMenu():
    setbox.setbox(root)

def checkConfig():
    if fileManager.isExist(".\\data\\config.json"):
        printl("读取配置文件")
        getConfigByFile()
        printConfig()
    else:
        printl("初次配置")
        openMenu()
        printConfig()

