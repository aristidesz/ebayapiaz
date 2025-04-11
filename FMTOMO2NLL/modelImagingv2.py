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

dicingNS = 10
dicingEW = 10

rdepth = (float(np.absolute(mindepth))+float(np.absolute(maxdepth)))/float(r-1)
rlat = (float(np.absolute(minlat))+float(np.absolute(maxlat)))/float(l-1)
rlon = (float(np.absolute(maxlon))-float(np.absolute(minlon)))/float(lo-1)

modelMaxDepth = 800

velocity3d = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1,modelMaxDepth),dtype=float)
fvel = open('azFMTOMOVel.p', 'w')


for xx in range(0,modelMaxDepth):
	print "Reading depth (km):",xx
	fDInterface = open('/home/rpgsbs/r02az15/Documents/aris/ResultsMaxwell2/p-wave/p-waveNLLMantle5070100/d10_s5/gmtplotPython/grid2dvd'+str(xx)+'.z','r')
	linesID = fDInterface.readlines()
	idcounter = 0
	velocity2d = np.zeros(((l-1)*dicingNS+1,(lo-1)*dicingEW+1),dtype=float)
	for i in xrange(0,(l-1)*dicingNS+1):
		reallat = (i)*rlat/dicingNS+minlat
		for j in xrange(0,(lo-1)*dicingEW+1):
			reallon = (j)*rlon/dicingEW+minlon
			azrdepth = float(linesID[idcounter])
			fvel.write('{:<15}{:<15}{:<15}{:<15}\n'.format(str(xx),str(round(reallat,3)),str(round(reallon,3)),str(round(azrdepth,4))))
			velocity2d[i][j] = azrdepth
			idcounter += 1
	velocity3d[:,:,xx] = velocity2d

