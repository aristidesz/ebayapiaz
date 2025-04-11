import numpy as np
from mayavi.mlab import *
import matplotlib.pyplot as plt
from scipy import interpolate
from sklearn.preprocessing import StandardScaler,MinMaxScaler


minlat = -30
maxlat = 30
minlon = 75
maxlon = 165
mindepth = 1.5
maxdepth = -1600

r=30
l=40
lo=60

dicingNS = 20
dicingEW = 20

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

fDInterface = open('./data/gridint1.z','r')
linesID = fDInterface.readlines()



idcounter = 0
interfaceDepthDicing = {}
arrMlab = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1),dtype=float)
for j in xrange(0,(lo-1)*dicingEW+1):
	reallon = (j)*rlon/dicingEW+minlon
	for i in xrange(0,(l-1)*dicingNS+1):
		reallat = (i)*rlat/dicingNS+minlat
		azrdepth = float(linesID[idcounter])
		arrMlab[i][j] = azrdepth*-5
		interfaceDepthDicing[str(round(reallat,1))+","+str(round(reallon,1))] = azrdepth
		idcounter += 1

interfaceDepth = interfaceDepthDicing


world = []
allworld = []
with open('./coastlines/world100.txt','rb') as csvfile:
	for line in csvfile:
		if line !="\n":
			lon, lat = line.split()	
			lat = float(lat)
			lon = float(lon)
			
			if lon > minlon and lon < maxlon and lat > minlat and lat < maxlat:
				world.append([lat,lon])
				allworld.append([lat,lon])
		else:
			import numpy as np
			if world:
				world = np.array(world)
				lat, long = world.T
				alt = [0 for x in range(len(lat))]


				m = np.divide((l-1)*dicingNS+1,len(lat))
				# len(lat)
				# lat = lat * 11
	
				# import pdb;pdb.set_trace()
				# div2 = np.divide((l-1)*dicingNS+1,2)
				# data = lat
				# # scaler = MinMaxScaler(feature_range = (-29.461043796508527, 29.832520453403149))
				# # scaler = MinMaxScaler(feature_range = (-1*div2, div2))
				
				# scaler.fit(data)
				# scaler.data_max_
				# lat = scaler.transform(data)


				# div3 = np.divide((lo-1)*dicingEW+1,2)
				# data = long
				# # scaler = MinMaxScaler(feature_range = (75.396101108709587, 164.82981530177568))
				# # scaler = MinMaxScaler(feature_range = (-1*div3, div3))
				# scaler.fit(data)
				# scaler.data_max_
				# long = scaler.transform(data)
				

				# plot3d(lat,long,alt,color=(0,0,0),tube_radius=None,opacity=0.6)
				world = []


# import pdb;pdb.set_trace()
azsurf = surf(arrMlab)

show()
