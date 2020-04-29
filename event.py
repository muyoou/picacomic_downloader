import d
import fileManager
import setbox

log=None
root=None
page=None
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

def setDownloaded():
    d.Downloaded=fileManager.readDownloaded()

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
        printl("加载配置文件")
        getConfigByFile()
        printConfig()
    else:
        printl("初次配置")
        openMenu()
        printConfig()
    printl("加载日志")
    if fileManager.isExist('.\\data\\downloaded.json'):
        setDownloaded()
    else:
        fileManager.createJsonFile([],'downloaded.json')

def isDownloaded(input):
    if input in d.Downloaded:
        return True
    else: return False

def setPage(nowp,allp):
    d.nowPage=nowp
    d.AllPage=allp
    page.set("第%d页，共%d页"%(nowp,allp))

def getNowPage():
    return d.nowPage

def getAllPage():
    return d.AllPage

def setNowPage(nowp):
    d.nowPage=nowp
    page.set("第%d页，共%d页"%(nowp,d.AllPage))
