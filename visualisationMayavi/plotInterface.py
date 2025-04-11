import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt
from scipy import interpolate
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import  moviepy.editor as mpy
from tvtk.api import tvtk
from tvtk.common import configure_input_data
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from mpl_toolkits.mplot3d.axes3d import Axes3D

# import pdb;pdb.set_trace()

f = mlab.figure(1, bgcolor=(0.8,0.6,0.2), fgcolor=(0, 0, 0),size=(1200, 800))
# m = Basemap(llcrnrlon=80.,llcrnrlat=-25.,urcrnrlon=180.,urcrnrlat=25.,resolution='l')
# m.bluemarble(scale=0.5);
fig=plt.figure()
fig.set_size_inches((10, 9))
ax1=fig.add_subplot(111)
bmap=Basemap(projection='merc',llcrnrlat=-30, llcrnrlon=75,urcrnrlat=30, urcrnrlon=165,lon_0=(75+165)/2.,ax=ax1)
bmap.bluemarble(ax = ax1)
bmdata = bmap.bluemarble(ax = ax1)._A.data
mlab.imshow(bmdata[:,:,0],colormap='gist_earth')
mlab.imshow(bmdata[:,:,1],colormap='gist_earth')
mlab.imshow(bmdata[:,:,2],colormap='gist_earth')
# import pdb;pdb.set_trace()
# bmdata = np.sum(bmdata,axis=2)
# mlab.imshow(bmdata,colormap='gist_earth',vmin=0,vmax=0.5)
# import pdb;pdb.set_trace()
# bmap.drawcoastlines()
# bmdataC = bmap.drawcoastlines(ax = ax1)
# segments =  bmdataC.get_segments()
# for seg in segments:
# 	# import pdb;pdb.set_trace()
# 	mlab.plot3d(seg.T[0],seg.T[1],[0 for i in seg],color=(0,0,0),tube_radius=None,opacity=1,line_width=4)
# import pdb;pdb.set_trace()
# plt.figure(figsize=(8, 8))
# m = Basemap(projection='ortho', resolution=None, lat_0=50, lon_0=-100)
# m.bluemarble(scale=0.5);







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
azcolordepth = []
arrMlab = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1),dtype=float)
for j in xrange(0,(lo-1)*dicingEW+1):
	reallon = (j)*rlon/dicingEW+minlon
	for i in xrange(0,(l-1)*dicingNS+1):
		reallat = (i)*rlat/dicingNS+minlat
		azrdepth = float(linesID[idcounter])
		arrMlab[i][j] = azrdepth*-5
		azcolordepth.append(arrMlab[i][j])
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
				len(lat)
				# lat = lat * 11
	
				
				div2 = np.divide((l-1)*dicingNS+1,2)
				data = lat
				latma = max(lat)
				latmi = min(lat)
				lonma = max(long)
				lonmi = min(long)

				# slatmax = (latma - 29.832520453403149)*13.154884680442564
				# slatmin = (latmi - -29.461043796508527)*13.154884680442564

				# slatmax = (latma - 29.832520453403149) * np.divide(div2*2,29.832520453403149- -29.461043796508527) - div2
				# slatmin = (latmi - -29.461043796508527) * np.divide(div2*2,29.832520453403149- -29.461043796508527) - div2

				slatmax = np.divide(div2*latma,29.832520453403149)
				slatmin = np.divide(-1*div2*latmi,-29.461043796508527)

				# scaler = MinMaxScaler(feature_range = (-29.461043796508527, 29.832520453403149))
				# scaler = MinMaxScaler(feature_range = (-1*div2, div2))
				scaler = MinMaxScaler(feature_range = (slatmin, slatmax))
				
				scaler.fit(data)
				scaler.data_max_
				lat = scaler.transform(data)


				div3 = np.divide((lo-1)*dicingEW+1,2)
				data = long


				slonmax = (lonma - 164.82981530177568)*4
				slonmin = (lonmi - 75.396101108709587)*4


				slonmax = (lonma - 75.396101108709587) * np.divide(div3*2,164.82981530177568-75.396101108709587) - div3
				slonmin = (lonmi - 75.396101108709587) * np.divide(div3*2,164.82981530177568-75.396101108709587) - div3
				# slonmax = np.divide(div3*lonma,164.82981530177568)
				# slonmin = np.divide(-1*div3*lonmi,75.396101108709587)
				
				# scaler = MinMaxScaler(feature_range = (75.396101108709587, 164.82981530177568))
				# scaler = MinMaxScaler(feature_range = (-1*div3, div3))
				scaler = MinMaxScaler(feature_range = (slonmin, slonmax))
				scaler.fit(data)
				scaler.data_max_
				long = scaler.transform(data)
				
				# normals = azsurf.parent.parent
				line = mlab.plot3d(lat,long,alt,color=(0,0,0),tube_radius=None,opacity=1,line_width=4)
				world = []


azsurf = mlab.surf(arrMlab)
mlab.axes(xlabel='Latitude', ylabel='Longitude', zlabel='Depth',ranges=(-30,30,75,160,10,68.2),nb_labels=5)
# import pdb;pdb.set_trace()

# mlab.view(azimuth=0, elevation=0, distance=3000)
mlab.show()
# duration = 2
# u = np.linspace(0,2*np.pi,1000)

# def make_frame(t=1):
#     """ Generates and returns the frame for time t. """
#     y = np.sin(3*u)*(0.2+0.5*np.cos(2*np.pi*t/duration))
#     # mlab_source.set(y = y) # change y-coordinates of the mesh
#     # import pdb;pdb.set_trace()
#     # mlab.view(azimuth = 120,elevation=220-(220*t/duration), distance=3000) # camera angle
#     mlab.view(azimuth=60-60*np.sin(t), elevation=225, distance=3000)
#     return mlab.screenshot(antialiased=True) # return a RGB image

# crust = mpy.VideoClip(make_frame, duration=duration)
# # Video generation takes 10 seconds, GIF generation takes 25s
# crust.write_gif("./crust1.0.gif", fps=80)










#Isosurface

# import numpy as np
# from enthought.mayavi import mlab

# x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
# s = np.sin(x*y*z)/(x*y*z)

# src = mlab.pipeline.scalar_field(s)
# mlab.pipeline.iso_surface(src, contours=[s.min()+0.1*s.ptp(), ], opacity=0.3)
# mlab.pipeline.iso_surface(src, contours=[s.max()-0.1*s.ptp(), ],)

# mlab.show()