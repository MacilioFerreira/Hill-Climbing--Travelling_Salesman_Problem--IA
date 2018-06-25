# -*- coding: utf-8 -*-

import random as rn

'''for i in xrange(0,20):
    print str((i, for x in xrange(0,8)))
    print '_' * 20
'''
cidades = []
l = 0
while l <= 10:
    a = (float(rn.randint(0,l)), float(rn.randint(0,l)))
    if not a in cidades:
        cidades.append(a)
    l += 1

#for city in cidades:
#    print city[0], city[1]
print [cidade[0] for cidade in cidades]
print [cidade[1] for cidade in cidades]
