# -*- coding: utf-8 -*-
import datetime
import crypt

printLog = True
collectInfo = True

def log(*s):
    if printLog:
        print s
    

def collect(tag, message):
    if collectInfo:
        if tag == 'info':
            f = open('info.dat',  'ab')
            t = str(datetime.datetime.today())
            try:
                message = message.encode('gbk')
            except:
                pass
            f.write(t+':\t'+str(message)+'\r\n')
            f.close()
        elif tag == 'data':
            f = open('datas.dat',  'ab')
            t = str(datetime.datetime.today())
            f.write(t+':\t'+str(message) + '\r\n')
            f.close()
            



if __name__ == '__main__':
    collect('info',  'hello')
            
            
