from __init__ import *
import collections
from config import BRAND_CONFIG_DEST

def load_poster_config():
    fp = open(BRAND_CONFIG_DEST, 'r')
    brand_info = collections.OrderedDict()
    for line in fp.readlines():
        tmp = line.split(' ')
        if len(tmp) != 2:
            continue
        brand_info[tmp[0]] = tmp[1]
    fp.close()
    return brand_info

def save_poster_config(brand_info):
    fp = open(BRAND_CONFIG_DEST, 'w')
    for key in brand_info:
        line = "{0} {1}.;;.;".format(key, brand_info[key])
        fp.write(line)
    fp.close()


class Poster(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            origin = super(Poster, cls)
            cls._instance = origin.__new__(cls, *args)
        return cls._instance

    def __init__(self):
        self.config = load_poster_config()

    def save_config(self):
        save_poster_config(self.config)

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def set(self, key, value):
        self.config[key] = value

    def delete(self, key, value=None):
        self.config.__delitem__(key)

    def items(self):
        return self.config.items()

poster = Poster()






