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
from scipy import interpolate
from traits.api import List
from tvtk.api import tvtk
from fractions import Fraction
from decimal import *


minlat = -30
maxlat = 30
minlon = 75
maxlon = 165
mindepth = 1.5
maxdepth = -1600

r=60
l=60
lo=60


ri=30
li=40
loi=60

dicingNS = 20
dicingEW = 20

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

modelMaxDepth = 500

velocity3d = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1,modelMaxDepth),dtype=float)

for xx in range(0,modelMaxDepth):
	print "Reading depth (km):",xx
	fDInterface = open('/home/rpgsbs/r02az15/Documents/aris/ResultsMaxwell2/p-wave/p-wave606060xyzttWeighting/d10_s5/gmtplotPython/grid2dvd'+str(xx)+'.z','r')
	linesID = fDInterface.readlines()
	idcounter = 0
	velocity2d = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1),dtype=float)
	for i in xrange(0,(l-1)*dicingNS+1):
		reallat = (i)*rlat/dicingNS+minlat
		for j in xrange(0,(lo-1)*dicingEW+1):
			reallon = (j)*rlon/dicingEW+minlon
			azrdepth = float(linesID[idcounter])
			velocity2d[i][j] = azrdepth
			idcounter += 1
	velocity3d[:,:,xx] = velocity2d


velocity3dInterp = np.zeros((100,66,modelMaxDepth),dtype=float)
nx,ny,nz = velocity3d.shape
x = np.linspace(0, (lo-1)*dicingEW+1,(lo-1)*dicingEW+1)
y = np.linspace(0, (l-1)*dicingNS+1, (l-1)*dicingNS+1)
xnew = np.linspace(0, (lo-1)*dicingEW+1, 100)
ynew = np.linspace(0, (l-1)*dicingNS+1, 66)


try:
	azstep = 10
	counter = 0
	for i in xrange(0,modelMaxDepth):
		z = velocity3d[:,:,counter]
		f = interpolate.interp2d(x, y, z, kind='linear')
		znew = f(ynew, xnew)
		velocity3dInterp[:,:,counter] = znew
		# import pdb;pdb.set_trace()
		# plt.plot(x, z[0, :], 'ro-', ynew, znew[0, :], 'b-')
		# plt.show()
		counter+=1
except Exception as e:
	print e
	import pdb;pdb.set_trace()

# import pdb;pdb.set_trace()
velocity3dInterpN = np.zeros((100,66,20),dtype=float)
nx1,ny1,nz1 = velocity3dInterpN.shape

try:
	for i in range(nx1):
		for j in range(ny1):
			x = np.array([x for x in range(len(velocity3dInterp[i][j]))])
			y = velocity3dInterp[i][j]
			f = interpolate.interp1d(x, y)
			# float(Decimal(20) / Decimal(modelMaxDepth))
			xnew = np.arange(0, modelMaxDepth, modelMaxDepth/20)
			ynew = f(xnew)   # use interpolation function returned by `interp1d`
			# plt.plot(x, y, 'o', xnew, ynew, '-')
			# plt.show()
			# import pdb;pdb.set_trace()
			velocity3dInterpN[i][j] = ynew
except Exception as e:
	print e
	import pdb;pdb.set_trace()










velocity3dInterpNI = velocity3dInterpN[::-1]
m = velocity3dInterpNI
m1 = np.rot90(m, axes=(1,0))





rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

fDInterface = open('./data/gridint1.z','r')
linesID = fDInterface.readlines()



idcounter = 0
interfaceDepthDicing = {}
azcolordepth = []
arrMlab = np.zeros(((li-1)*dicingNS+1,(loi-1)*dicingEW+1),dtype=float)
for j in xrange(0,(loi-1)*dicingEW+1):
	reallon = (j)*rlon/dicingEW+minlon
	for i in xrange(0,(li-1)*dicingNS+1):
		reallat = (i)*rlat/dicingNS+minlat
		azrdepth = float(linesID[idcounter])
		arrMlab[i][j] = azrdepth*-1
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


				m = np.divide((li-1)*dicingNS+1,len(lat))
				len(lat)
				# lat = lat * 11
	
				
				div2 = np.divide(66,2)
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


				div3 = np.divide(100,2)
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
				
				# import pdb;pdb.set_trace()
				# normals = azsurf.parent.parent
				line = mlab.plot3d(lat,long,alt,color=(0,0,0),tube_radius=None,opacity=1,line_width=4,extent=[lat.min()+33,lat.max()+33,long.min()+50,long.max()+50,0,0])
				
				world = []





try:
	nx,ny = arrMlab.shape
	x = np.linspace(0, (li-1)*dicingNS+1, (li-1)*dicingNS+1)
	y = np.linspace(0, (loi-1)*dicingEW+1,(loi-1)*dicingEW+1)
	xnew = np.linspace(0, (loi-1)*dicingEW+1, 100)
	ynew = np.linspace(0, (li-1)*dicingNS+1, 66)


	f = interpolate.interp2d(y, x, arrMlab, kind='linear')
	znew = f(xnew, ynew)
	
except Exception as e:
	print e
	import pdb;pdb.set_trace()

mlab.axes(xlabel='Latitude', ylabel='Longitude', zlabel='Depth',ranges=(-30,30,75,165,10,500),nb_labels=5,extent=[0,66,0,100,0,20])

import pdb;pdb.set_trace()

azsurf = mlab.surf(znew,extent=[0,66,0,100,0,3],colormap="gist_earth")
src = mlab.pipeline.scalar_field(m1)
# vol = mlab.pipeline.volume(src)
yplane = mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes',slice_index=10,colormap='RdBu',vmin=-0.4,vmax=0.4)
xplane = mlab.pipeline.image_plane_widget(src,plane_orientation='x_axes',slice_index=10,colormap='RdBu',vmin=-0.4,vmax=0.4)
contours = mlab.pipeline.iso_surface(src, contours=[velocity3d.min()+0.5*velocity3d.ptp(), ], opacity=0.2)
contours = mlab.pipeline.iso_surface(src, contours=[velocity3d.max()-0.1*velocity3d.ptp(), ],)
# mlab.pipeline.iso_surface(src, contours=0,)

# mlab.view(azimuth=0, elevation=0, distance=3000)
# mlab.show()
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