#
# public function used by CUIT web site
#


def user_rank_color(score):
    if score in xrange(0,1000):
        return "#24e5bf"
    elif score in xrange(1000,1500):
        return "#f2cf2e"
    else :
        return "#fd8321"