# -*- coding: utf-8 -*-
import os,  hashlib,  zlib

def encrypt(srcStr):
    try:
        srcStr = srcStr.encode('utf-8')
    except:
        srcStr = srcStr
    md5 = hashlib.md5()
    md5.update(srcStr)
    key = bytearray(md5.hexdigest())
    #print key
    keyLen = len(key)
    zipStr = bytearray(zlib.compress(srcStr))
    for i in range(len(zipStr)):
        zipStr[i] = zipStr[i] ^ key[i%keyLen]
    return str(zipStr + key)

def decrypt(srcStr):
    try:
        srcStr = srcStr.encode('utf-8')
    except:
        srcStr = srcStr
    key = bytearray(srcStr[-32:])
    keyLen = len(key)
    zipStr = bytearray(srcStr[:-32])
    for i in range(len(zipStr)):
        zipStr[i] = zipStr[i] ^ key[i%keyLen]
    try:
        returnValue = zlib.decompress(str(zipStr))
    except:
        returnValue = ''
    return returnValue
    

if __name__ == '__main__':
    myStr = "Hello world!"
    for i in myStr:
        print "%02x " %ord(i) , 
    
    print '\n'
    enStr = encrypt(myStr)
    for i in enStr:
        print "%02x " %ord(i),  
    print '\n'
#    import urllib2
#    f = urllib2.Request(
#        url     = 'http://localhost:8080/post.php',
#        headers = {'Content-Type' : 'text/xml','charset':'UTF-8'},
#        data    = enStr
#    )
#    fd = urllib2.urlopen(f)
#    acc = fd.read()
#    print decrypt(acc)
    
