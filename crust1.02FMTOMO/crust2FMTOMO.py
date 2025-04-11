from __future__ import division
import json
import numpy as np
from scipy import interpolate
import matplotlib.pylab as plt
from math import floor
def round_of_rating(number):
	# import pdb;pdb.set_trace()
	return floor(number)+0.5
#7x32x42 = 6000 entries
#5 Depth = nvr
#30 Lat = nvt
#40 Lon = nvp

#i=j=k=1 -> -30Lat 75Lon 
fak135 = open('./ak135true.vel','r')

fwrites = open("./crust1.0_S_FMTOMO.vel", 'w')

fwrite = open("./crust1.0_P_FMTOMO.vel", 'w')

fwriteI = open("./crust1.0InterfaceFMTOMO.in", 'w')

# crust1 = open('azcrust1.0v2.txt', 'r').read()
# az = eval(crust1)
d2 = json.load(open("azcrust1.0v3.txt"))
crust1 = d2['crust1.0']
dd = json.load(open("azcrust1.0Depthv3.txt"))
crust1d = dd['crust1.0']
# import pdb;pdb.set_trace()

minlat = -30
maxlat = 30
minlon = 75
maxlon = 165
mindepth = 10
maxdepth = -1600

r=120
l=160
lo=200

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

r = r+2
l = l+2
lo = lo+2




depth_lst = []
vpref_lst = []
vsref_lst = []
for line in fak135:
	print line
	sline = line.strip().split()
	depth = float(sline[0])
	vpref = float(sline[1])
	vsref = float(sline[2])
	depth_lst.append(depth)
	vpref_lst.append(vpref)
	vsref_lst.append(vsref)


x = depth_lst
y = vpref_lst
f = interpolate.interp1d(x, y,kind='linear')
depthak135 = np.arange(-100, 6372, 1)
vpak135 = f(depthak135)   # use interpolation function returned by `interp1d`

y = vsref_lst
f = interpolate.interp1d(x, y,kind='linear')
vsak135 = f(depthak135)
depthak135 = list(depthak135)


counter = 0
for i in xrange(0,r):
	realdepth = maxdepth*-1+rdepth-i*rdepth
	
	lat_lst = []
	for j in xrange(0,l):
		reallat = (j)*rlat-rlat+minlat
		lon_lst = []
		for z in xrange(0,lo):
			reallon = (z)*rlon-rlon+minlon

			
			
			
			try:		
				mylatlot = str(int(realdepth))+","+str(round_of_rating(reallat))+","+str(round_of_rating(reallon))
				vp,vs = crust1[mylatlot]
			except:
				idx = depthak135.index(int(realdepth))
				vp = vpak135[idx] 
				vs = vsak135[idx]

			# print "Lat:", str(reallat),"Lon:",str(reallon),"Depth:",str(realdepth), "Vel:", str(vp)
			# print "Lat:", str(reallat),"Lon:",str(reallon),"Depth:",str(realdepth), "Vel:", str(vs)
			lon_lst.append(vp)
			fwrite.write(str(vp)+'\n')
			fwrites.write(str(vs)+'\n')
			counter += 1

		lat_lst.append(lon_lst)
	print realdepth,reallat,reallon
	# if realdepth<100:
	# 	idx = depthak135.index(int(realdepth))
	# 	vp = vpak135[idx]
	# 	# plt.imshow(lat_lst[::-1],vmin=vp-0.6, vmax=vp+0.6)
	# 	plt.imshow(lat_lst[::-1])
	# 	# for (j,i),label in np.ndenumerate(lat_lst[::-1]):
	# 	#     plt.text(i,j,label,ha='center',va='center')
	# 	#     plt.text(i,j,label,ha='center',va='center')
	# 	plt.colorbar()
	# 	import pdb;pdb.set_trace()
	# 	plt.close('all') 

#Producing Interface

	
lat_lst = []
for j in xrange(0,l):
	reallat = (j)*rlat-rlat+minlat
	lon_lst = []
	for z in xrange(0,lo):
		reallon = (z)*rlon-rlon+minlon
		mylatlot = str(round_of_rating(reallat))+","+str(round_of_rating(reallon))
		# import pdb;pdb.set_trace() 
		mohoD = crust1d[mylatlot]

		fwriteI.write(str(mohoD)+'\n')
	print "Moho Depth at:","Lat",str(reallat),"Lon",str(reallon),"is",str(mohoD)
		