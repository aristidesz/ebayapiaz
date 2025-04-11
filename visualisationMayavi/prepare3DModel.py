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

dicingNS = 20
dicingEW = 20

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

modelMaxDepth = 500

velocity3d = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1,modelMaxDepth),dtype=float)

for xx in range(0,modelMaxDepth):
	print "Reading depth (km):",xx
	fDInterface = open('./data/grid2dvd'+str(xx)+'.z','r')
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





import pdb;pdb.set_trace()




velocity3dInterpNI = velocity3dInterpN[::-1]

src = mlab.pipeline.scalar_field(velocity3dInterpNI)
# vol = mlab.pipeline.volume(src)

mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes',slice_index=10,colormap='RdBu',vmin=-0.4,vmax=0.4)
mlab.pipeline.image_plane_widget(src,plane_orientation='x_axes',slice_index=10,colormap='RdBu',vmin=-0.4,vmax=0.4)
mlab.pipeline.iso_surface(src, contours=[velocity3d.min()+0.5*velocity3d.ptp(), ], opacity=0.2)
# mlab.pipeline.iso_surface(src, contours=[velocity3d.max()-0.1*velocity3d.ptp(), ],)
# mlab.pipeline.iso_surface(src, contours=0,)
import pdb;pdb.set_trace()