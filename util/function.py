#
# public function used by CUIT web site
#

def user_rank_color(score):
    if score in xrange(0,1000):
        return "#0000FF"
    elif score in xrange(1000,1500):
        return "#0000FF"
    else :
        return "#0000FF"