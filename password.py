import hmac
import hashlib
import d

def sha256(string):
        sha256 = hashlib.sha256()
        sha256.update(string.encode('utf-8'))
        res = sha256.hexdigest()
        return res

def hmacsha256(key,string):
        signature = hmac.new(
                bytes(key.encode('utf-8')),
                msg=string.encode('utf-8'),
                digestmod=hashlib.sha256
        ).hexdigest()
        return signature

def password(url,method,time,nonce):
        key=d.Key
        str=url+time+nonce+method+key
        str=str.lower()
        mi=d.Key2
        return hmacsha256(mi,str)

def readtxt(url,content):
        with open(url,'a') as file_handle:
              print(content)
              file_handle.write(content)

