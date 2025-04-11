import pandas as pd
import numpy as np

data = pd.read_csv('AZF-P-SAllSta.dat')

fwrite = open('azStaNLL.csv','w')
az = data[['station','stalat','stalong','staelev']]
arr = az.as_matrix()
uniquearr = np.unique(["{},{},{},{}".format(i[0],i[1],i[2],i[3]) for i in arr])

azlong = []
for azl in uniquearr:
	long2 = azl.split(",")[2]
	if float(long2) > 180:
		long1=np.mod((float(long2)+180),360)-180
		# import pdb;pdb.set_trace()
		azlong.append(str(long1))

	else:
		azlong.append(azl.split(",")[2])

elev = [str(float(x.split(",")[3])*1/1000) for x in uniquearr]

for item,e,azlo in zip(uniquearr,elev,azlong):
	item = item.split(",")
	# print 'LOCSRCE {:<15} LATLON {:<15}{:<15}{:<15} 0'.format(item[0],item[1],item[2],e)
	print 'LOCSRCE {:>6}   LATLON{:>9}{:>10}{:>9}     0'.format(item[0],item[1],azlo,e)
	fwrite.write('LOCSRCE {:>6}   LATLON{:>9}{:>10}{:>9}     0\n'.format(item[0],item[1],azlo,e))

import pdb;pdb.set_trace()

