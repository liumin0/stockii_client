# -*- coding: utf-8 -*-
import os,  hashlib,  zlib

def encrypt(srcStr):
    """
    加密函数，利用zlib压缩，并用原内容的md5进行异或操作，最后将md5保存在尾部
    输入：需要加密的字符串
    输出：加密后的字符串
    """
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
    """
    解密函数
    输入：需要解密的字符串
    输出：解密后的字符串
    """
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
    
