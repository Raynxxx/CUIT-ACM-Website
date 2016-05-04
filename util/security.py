import pyDes
import base64
from secret import security

key = security.key
iv = security.iv

def encrypt(data):
    k = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return base64.b64encode(k.encrypt(data))

def decrypt(data):
    k = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(base64.b64decode(data))