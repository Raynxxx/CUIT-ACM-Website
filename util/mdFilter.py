import markdown as render
from bs4 import BeautifulSoup
import re

regex_cache = {}

def search(text, regex):
    if regex == '':
        return True
    regexcmp = regex_cache.get(regex)
    if not regexcmp:
        regexcmp = re.compile(regex)
        regex_cache[regex] = regexcmp
    return regexcmp.search(text)

VALID_TAGS = {'h1':{}, 'h2':{}, 'h3':{}, 'h4':{}, 'h5':{}, 'h6':{},'sup':{},
              'strong':{}, 'em':{}, 'pre':{},'code':{}, 'i':{'class':''},
              'table':{},'th':{},'tr':{},'td':{},'blockquote':{},'kbd':{},'dl':{},'dt':{},'dd':{},
              'p':{},'ol':{}, 'ul':{}, 'li':{}, 'br':{}, 'a':{'href':'^(/|http?|ftp|#)', 'title':'.*', 'class':''},
              'img':{'src':'^(/|http?|ftp|#)', 'alt':'.*'}}

VALID_ATTR = {'id':''}

def parsehtml(html):
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True
        else:
            attr_rules = dict(VALID_TAGS[tag.name], **VALID_ATTR)
            for attr in tag.attrs.keys():
                if attr not in attr_rules:
                    del tag[attr]
                    continue
                if not search(tag.attrs[attr], attr_rules[attr]):
                    del tag[attr]
    return soup.renderContents()


def markdown(md):
    data = render.markdown(md, extensions=['markdown.extensions.extra','markdown.extensions.toc'])
    #return data
    return parsehtml(data).decode('utf-8')
