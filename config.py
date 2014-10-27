# -*- coding: utf-8 -*-
import os,  crypt

def readSetting():
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
    dStruct = readSetting()
    dStruct[key] = value
    f = open('data.dat',  'wb')
    f.write(crypt.encrypt(str(dStruct)))
    #f.write(str(dStruct))
    f.close()
