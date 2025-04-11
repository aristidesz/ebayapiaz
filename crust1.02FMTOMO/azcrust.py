import numpy as np
from math import floor
import json
import matplotlib.pyplot as plt
from scipy import interpolate


fvp = open("crust1.vp",'r')
fvs = open("crust1.vs",'r')
fdepth = open("crust1.bnds",'r')

# -179.5  89.5 -> 179.5 -89.5

if __name__ == '__main__':
	# lat  = int(raw_input('Lat: '))
	# lon = int(raw_input('Lon: '))
	latlon = []
	azcrust = {}
	azcrustdepth = {}
	for lat in xrange(90,-90,-1):
		lat = lat - 0.5
		for lon in xrange(-180,180):
			lon = lon + 0.5
			latlon.append([lat,lon])

	counter = 0
	for depth,vp,vs in zip(fdepth,fvp,fvs):	
		vp_lst = []
		vs_lst = []
		depth_lst = []
		
		lat = latlon[counter][0]
		lon = latlon[counter][1]
		print lat,lon
		# import pdb;pdb.set_trace()
		azcrustdepth[str(lat)+","+str(lon)] = str(round(float(depth.strip().split()[-1]),4))
		dl = [float(dq) for dq in depth.split()]
		v = np.diff(dl)
		for d,p,s,dd in zip(depth.split(),vp.split(),vs.split(),v):
			# print d,p,s
			# depth = 0
			# import pdb;pdb.set_trace()
			if np.absolute(dd) < 0.1:
				continue
			
			
			depth_lst.append(float(d)*-1)
			vp_lst.append(float(p))
			vs_lst.append(float(s))

		
		
		x = depth_lst
		f = interpolate.interp1d(x, vp_lst,kind='linear',bounds_error=False,fill_value=(vp_lst[0],vp_lst[-1]))
		fs = interpolate.interp1d(x, vs_lst,kind='linear',bounds_error=False,fill_value=(vs_lst[0],vs_lst[-1]))
		xnew = np.arange(0, 65, 1)
		vpnew = f(xnew)   # use interpolation function returned by `interp1d`
		
		vsnew = fs(xnew)
		# import pdb;pdb.set_trace()
		# plt.plot(x, vp_lst, 'o', xnew, vpnew, '-')
		for depths,vpd,vsd in zip(xnew,vpnew,vsnew):
			azcrust[str(int(depths))+","+str(lat)+","+str(lon)] = [vpd,vsd]
			
			# import pdb;pdb.set_trace()
			
		counter += 1
	# as requested in comment
	exDict = {'crust1.0': azcrust}
	with open('azcrust1.0v3.txt', 'w') as file:
		 file.write(json.dumps(exDict)) # use `json.loads` to do the reverse

	exDict1 = {'crust1.0': azcrustdepth}
	with open('azcrust1.0Depthv3.txt', 'w') as file:
		 file.write(json.dumps(exDict1)) # use `json.loads` to do the reverse
