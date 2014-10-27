# -*- coding: utf-8 -*-
import os, sys
from PyQt4.QtGui import QDialog, QMessageBox
from http import callRestSync
import json

serverType = None #'web'
serverAddr = None
id2name = {}
id2area = {}
id2industry = {}
area2ids = {}
industry2ids = {}

typeUnitTable = {
"avg_price": u"元", 
"growth_ratio": u"%", 
"total_stock": u"万", 
"total_value": u"万", 
"avg_circulation_value": u"亿", 
"cir_of_cap_stock": u"万", 
"current_price": u"元"
}

def init():
    
    pass
#    ret = callRestSync('listStockBasicInfo',  {'response': 'json'})
    ret = callRestSync('liststockclassfication',  {'response': 'json'})
    if ret[0] == False:
        QMessageBox.warning(None,'warning', ret[1])
        sys.exit(1)
    try:
        decodedJson = json.loads(ret[1])
        response = decodedJson['liststockclassficationresponse']
        valuelist = response['stockclassification']
        for value in valuelist:
            id2name[value['stockid']] = value['stockname']
            id2area[value['stockid']] = value['areaname']
            id2industry[value['stockid']] = value['industryname']
            if value['areaname'] not in area2ids:
                area2ids[value['areaname']] = [value['stockid']]
            elif value['stockid'] not in area2ids[value['areaname']]:
                area2ids[value['areaname']].append(value['stockid'])
            if value['industryname'] not in industry2ids:
                industry2ids[value['industryname']] = [value['stockid']]
            elif value['stockid'] not in industry2ids[value['industryname']]:
                industry2ids[value['industryname']].append(value['stockid'])
    except:
#        import traceback 
#        traceback.print_exc()
        QMessageBox.warning(None,'warning', u"通信错误")
        sys.exit(1)

def init2():
    path = 'stock_basic_info.txt'
    if os.path.exists(path):
        f = open(path, 'rb')
        c = f.readlines()
        f.close()
        for line in c:
            splitL = line.strip().split()
            try:
                id2name[splitL[0]] = splitL[1].decode('utf-8')
            except:
                pass
