import markdown as render
from xml.sax import saxutils


whiteList = [
            ('<code>', '{[(HACKERCODESTART)]}'),
            ('</code>', '{[(HACKERCODEEND)]}'),
            ('<pre>', '{[(HACKERPRESTART)]}'),
            ('</pre>', '{[(HACKERPREEND)]}'),
]


def markdown(md):
    for i in whiteList:
        if i[0] in md:
            md = md.replace(i[0], i[1])
    md2 = saxutils.escape(md)
    data = render.markdown(md2, extensions=['markdown.extensions.extra'])
    for i in whiteList:
        if i[1] in data:
            data = data.replace(i[1], i[0])
    return data
