# -*- coding: utf-8 -*-
import os, sys
from PyQt4.QtGui import QDialog, QMessageBox
from http import callRestSync
import json
import datetime

if 'APPDATA' in os.environ:
    settingDir = os.path.join(os.environ['APPDATA'], 'stockii')
else:
    settingDir = '.'
if not os.path.exists(settingDir):
    os.makedirs(settingDir)
serverType = None#'web'
serverAddr = None
dealDays = []
id2name = {}
id2area = {}
id2industry = {}
area2ids = {}
industry2ids = {}

typeUnitTable = {
"growth_ratio": u"%", 
"current_price": u"元", 
"daily_up_down": u"元", 
"bought_price": u"元", 
"sold_price": u"元", 
"growth_speed": u"%", 
"turnover_ratio": u"%", 
"today_begin_price": u"元", 
"ytd_end_price": u"元", 
"max": u"元", 
"min": u"元", 
"total_money": u"亿元", 
"cir_of_cap_stock": u"亿股", 
"avg_price": u"元", 
"num1_buy_price": u"元", 
"num1_sell_price": u"元", 
"num2_buy_price": u"元", 
"num2_sell_price": u"元", 
"num3_buy_price": u"元", 
"num3_sell_price": u"元", 
"circulation_value": u"亿元", 
"total_value": u"亿元", 
"bbi_balance": u"元", 
"bull_profit": u"元", 
"bull_stop_losses": u"元", 
"total_stock": u"亿股", 
"max_circulation_value": u"亿元", 
"current_circulation_value": u"亿元", 
"min_circulation_value": u"亿元", 
"avg_circulation_value": u"亿元", 

"growth": u"%", 
"turn": u"%", 
"total": u"亿元", 
}

reCalcTable = {
"total_money": 100000000, 
"total": 100000000, 
"cir_of_cap_stock": 10000, 
"total_stock": 10000
}

def initDealDays():
    ret = callRestSync('listtradedate',  {'response': 'json'})
    if ret[0] == False:
        QMessageBox.warning(None,'warning', ret[1])
        sys.exit(1)
    try:
        decodedJson = json.loads(ret[1])
        response = decodedJson['listtradedateresponse']
        valuelist = response['tradedate']
        for value in valuelist:
            tmpDate = None
            try:
                tmpDate = datetime.datetime.strptime(value['listdate'],"%Y-%m-%dT%H:%M:%S")
            except:
                tmpDate = datetime.datetime.strptime(value['listdate'],"%Y-%m-%dT%H:%M:%S+0800")
            if tmpDate is not None:
                dealDays.append(tmpDate.date())
        
        dealDays.sort()
    except:
        import traceback 
        traceback.print_exc()
        QMessageBox.warning(None,'warning', u"通信错误")
        sys.exit(1)
        
def init():
    
#    ret = callRestSync('listStockBasicInfo',  {'response': 'json'})
    ret = callRestSync('liststockclassification',  {'response': 'json'})
    if ret[0] == False:
        QMessageBox.warning(None,'warning', ret[1])
        sys.exit(1)
    try:
        decodedJson = json.loads(ret[1])
        response = decodedJson['liststockclassificationresponse']
        valuelist = response['stockclassification']
        for value in valuelist:
            id2name[value['stockid']] = value['stockname']
            
            if 'areaname' in value and value['areaname'] != '':
                id2area[value['stockid']] = value['areaname']
                if value['areaname'] not in area2ids:
                    area2ids[value['areaname']] = [value['stockid']]
                elif value['stockid'] not in area2ids[value['areaname']]:
                    area2ids[value['areaname']].append(value['stockid'])
            if 'industryname' in value and value['industryname'] != '':
                id2industry[value['stockid']] = value['industryname']
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
