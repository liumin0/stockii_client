# -*- coding: utf-8 -*-
import os, crypt, datetime
import myGlobal

collectInfo = True

configPath = os.path.join(myGlobal.settingDir, 'data.dat')
infoPath = os.path.join(myGlobal.settingDir, 'info.dat')
datasPath = os.path.join(myGlobal.settingDir, 'datas.dat')

def readSetting():
    """
    读取配置文件，配置文件是加密的，所以需要执行解密操作
    """
    ret = {}
    
    if os.path.exists(configPath):
        f = open(configPath,  'rb')
        c = f.read()
        f.close()
        dStr = crypt.decrypt(c)
        try:
            ret = eval(dStr)
        except:
            ret = {}
    return ret;

def writeSetting(key,  value):
    """
    写配置文件，并加密
    """
    dStruct = readSetting()
    dStruct[key] = value
    f = open(configPath,  'wb')
    f.write(crypt.encrypt(str(dStruct)))
    #f.write(str(dStruct))
    f.close()


def collect(tag, message):
    if collectInfo:
        if tag == 'info':
            f = open(infoPath,  'ab')
            t = str(datetime.datetime.today())
            try:
                message = message.encode('gbk')
            except:
                pass
            f.write(t+':\t'+str(message)+'\r\n')
            f.close()
        elif tag == 'data':
            f = open(datasPath,  'ab')
            t = str(datetime.datetime.today())
            f.write(t+':\t'+str(message) + '\r\n')
            f.close()
            
    
