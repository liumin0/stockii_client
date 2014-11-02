# -*- coding: utf-8 -*-
import os,  crypt

def readSetting():
    """
    读取配置文件，配置文件是加密的，所以需要执行解密操作
    """
    ret = {}
    if os.path.exists('data.dat'):
        f = open('data.dat',  'rb')
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
    f = open('data.dat',  'wb')
    f.write(crypt.encrypt(str(dStruct)))
    #f.write(str(dStruct))
    f.close()
