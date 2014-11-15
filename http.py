# -*- coding: utf-8 -*-

"""
Module implementing ChooseId.
"""

import urllib, urllib2
import json
from log import log

import datetime
import threading
from loading import Loading
from PyQt4.QtCore import SIGNAL
import customRest
import myGlobal
import traceback
baseUrl = 'http://192.168.1.220:8080/client/api?command=%s'
#baseUrl = 'http://localhost:8080/client/api?command=%s'
#baseUrl = 'http://stockii-gf.oicp.net/client/api?command=%s'

def callRestSync(apiName,  args):
    log(args)
    try:
        if myGlobal.serverType == 'web':
            url = baseUrl %apiName
            data = urllib.urlencode(args)
            req = urllib2.Request(url,  data)
            ret = (True,  urllib2.urlopen(req).read())
        else:
            
            myUrllib = customRest.myurllib()
            ret = (True,  myUrllib.request(apiName, args))
    except Exception, e:
#        import traceback
#        traceback.print_exc()
        ret = (False,  u"无法连接服务器")
    
    return ret

def callRestAsync(parent,  apiName,  args,  callBack):
    load = Loading(parent)
    if myGlobal.serverType == 'web':
        targetFunc = callRestWithCallBack
    else:
        targetFunc = callCustomRestWithCallBack
    thread = threading.Thread(target = targetFunc,  args=(apiName,  args,  callBack,  load))
    thread.setDaemon(True)
    thread.start()
    load.exec_()

def callRestWithCallBack(apiName,  args,  callBack,  load):
    log(args)
    try:
        url = baseUrl %apiName

        data = urllib.urlencode(args)
        req = urllib2.Request(url,  data)
        #import time
        #time.sleep(5)
        ret = (True,  urllib2.urlopen(req).read())
    except Exception, e:
        ret = (False,  e)
    
#    return callBack((False,  "lalala"))
#    load.emit(SIGNAL("finished()"))
    callBack.emit(SIGNAL("callBack(QVariant, QDialog*)"),  ret,  load)
    #callBack(ret)

def callCustomRestWithCallBack(apiName,  args,  callBack,  load):
    log(args)
    try:
        myUrllib = customRest.myurllib()
        #import time
        #time.sleep(5)
        ret = (True,  myUrllib.request(apiName, args))
    except Exception, e:
        ret = (False,  e)
    
#    return callBack((False,  "lalala"))
#    load.emit(SIGNAL("finished()"))
    callBack.emit(SIGNAL("callBack(QVariant, QDialog*)"),  ret,  load)
    #callBack(ret)
    

if __name__ == '__main__':
    url = r'http://localhost:8080/client/api?command=listStockDayInfo'
    data = urllib.urlencode({
                        'response':'json', 
                        'page':0, 
                        'pagesize':20, 
                        'stockid':'000001,000002,000003,000004,000005', 
                        'starttime':'2008-09-24', 
                        'sortname':'turnover_ratio'})
                        
    
    url = 'http://192.168.1.211:8080/client/api?command=listStockDayInfo'
    #url = 'http://192.168.1.211:8080/client/api?command=listDaySum&sumtype=all&sumname=avg_price&stockid=000001&starttime=2008-04-01&endtime=2008-09-01&page=1&pagesize=10&days=3,13,5&sortname=threeSum&asc=false'
    data = urllib.urlencode({'stockid': '000001,000002,000004', 'pagesize': 2000, 'response': 'json', 'starttime': datetime.date(2000, 1, 1), 'endtime': datetime.date(2014, 12, 30), 'page': 1})
    req = urllib2.Request(url,  data)
    try:
        r = urllib2.urlopen(req).read()
        decodedJson = json.loads(r)
        response = decodedJson['liststockdayinforesponse']
        totalCount  = response['count']
        valuelist = response['stockdayinfo']
        print valuelist
    except Exception, e:
        print e
