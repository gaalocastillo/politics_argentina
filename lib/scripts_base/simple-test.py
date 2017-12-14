from operator import itemgetter


from datetime import datetime

d1 = datetime(2017, 10 , 21 , 0, 0, 0)
d2 = datetime(2016, 10 , 21 , 0, 0, 0)
d3 = datetime(2018, 10 , 21 , 0, 0, 0)
d4 = datetime(2016, 8 , 21 , 0, 0, 0)

L2=['Sun Nov 12 13:08:15 +0000 2017', 'Mon Nov 13 13:08:15 +0000 2017']


d = {1:d1, 2:d2, 3:d3, 4:d4}
print d
sorted(d.items(), key=itemgetter(1))
prit
print d


#for date in d:
	#print d[date]

L = [d1, d2, d3, d4]
#print min(L2)
#print L2
#L2.sort()
#print L2
