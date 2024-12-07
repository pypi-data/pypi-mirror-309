# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:34:27 2018

@author: danaukes
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:24:29 2018

@author: danaukes
"""

import math
ppi = 1000

# start_string = 'IN;PA;VS30;'
# end_string = 'PU;PU0,0;!PG;'

start_string = 'IN;P0;'
end_string = 'U0,0;@'

def path_string(path):
    first = True
    s=''
    for point in path:
        if first:
            s+='U{0:.0f},{1:.0f};'.format(point[0],point[1])
        else:
            s+='D{0:.0f},{1:.0f};'.format(point[0],point[1])
        first = False
    return s

def layer_string(layer):
    # layer = layer.rotate(-90)
    layer = layer.scale(ppi,ppi)
    s = start_string
    for path in layer.get_paths():
        s+=path_string(path)
    s += end_string
    return s

class Plotter(object):
    pass
