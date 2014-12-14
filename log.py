# -*- coding: utf-8 -*-

import os

DEBUG = False

def log(*s):
    if DEBUG:
        for i in s:
            print i, 
        print ''    
             
            
