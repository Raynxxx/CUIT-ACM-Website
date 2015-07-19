import pyDes
import base64

key = 'Y3VpdGFj'
iv = "\x22\x33\x35\x81\xBC\x38\x5A\xE7"

def encrypt(data):
    k = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return base64.b64encode(k.encrypt(data))

def decrypt(data):
    k = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(base64.b64decode(data))