####################################################################
####################################################################
#### 	The Awesome Simulator, 3D Simulation Module		####
####    						    	####
####	Author: Abhejit Rajagopal,  abhejit@ucla.edu	    	####
####    Date: 09/01/2014				    	####
####    		   				    	####
####    (3D.py) is part of the AwSimLib software package   	####
####	module 3D.py: /sim/3D.py		    		####
####    		    				    	####
####    This software is free to use, subjct to terms and   	####
####    	conditions in the AwSimLib license (LGPLv3).	####
####    AwSimLib license: ../_LICENSE.TXT		    	####
####################################################################
####################################################################

####################################################################
####	 Version History					####
####################################################################
####  0.5	09/02/2013 - interpPG new			####
####    		    				    	####
####  Part of the AwSimLib software package.			####
####  Copyright (C) 2014 Abhejit Rajagopal			####
####################################################################
####################################################################

####################################################################
####	Helper Functions: --> Debug				####
####################################################################
#### LUMERICAL
def interpPG(lumerical_csv, FEM_data, FEM_scaling):
	import numpy as np
	import scipy as sp
	from scipy.interpolate import griddata

	print ('')
	print ('~~~~~~~~~~~~~~~~~~~~')
	print ('AwSimLib interpPG(FDTD,FEM)')
	print ('~~~~~~~~~~~~~~~~~~~~')

	to_return_PG = [] 	# to_return will be a list of lists. 
					#	each item is a list of PG values for given region

	## read PG data
	print "--> Reading PG data"
	FDTD_data = np.float64(np.genfromtxt(lumerical_csv, delimiter=',')) # stored in rows
	FDTD_x = FDTD_data[:,0]
	FDTD_y = FDTD_data[:,1]
	FDTD_z = FDTD_data[:,2]
	FDTD_pg = FDTD_data[:,3]
	TensorGrid = FDTD_data[:,0:3]
	TensorGrid = TensorGrid#*(1/FEM_scaling)

	print ("--> fetching FEM results")
	i=0
	for item in FEM_data:
		## gather data
		FEM_vertices = np.asarray(np.float64(item[:,0:3])) #x,y,z
		FEM_vertices = FEM_vertices*FEM_scaling
		FEM_x = FEM_vertices[:,0] #x
		FEM_y = FEM_vertices[:,1] #x
		FEM_z = FEM_vertices[:,2] #x

		## interpolate
		#FEM_pg = griddata( TensorGrid, FDTD_pg, FEM_vertices, method='cubic')
		#FEM_pg = griddata( TensorGrid, FDTD_pg, FEM_vertices, method='linear')
		FEM_pg = griddata( TensorGrid, FDTD_pg, FEM_vertices, method='nearest')
		FEM_pg = np.asmatrix(FEM_pg).transpose()
		to_return_PG.append(FEM_pg)
	
		## print info
		print('~~~')
		print ('Reg'+str(i)+'	'+'MIN'	+'	'+ 'MAX' +'	'+ 'avg')
		print ('')
		print 'FDTD_x:	' + str(np.min(FDTD_x)) + '	' + str(np.max(FDTD_x))
		print 'FEM_x:	' + str(np.min(FEM_x)) + '	' + str(np.max(FEM_x))
		print ('')
		print 'FDTD_y:	' + str(np.min(FDTD_y)) + '	' + str(np.max(FDTD_y))
		print 'FEM_y:	' + str(np.min(FEM_y)) + '	' + str(np.max(FEM_y))
		print ('')
		print 'FDTD_z:	' + str(np.min(FDTD_z)) + '	' + str(np.max(FDTD_z))
		print 'FEM_z	' + str(np.min(FEM_z)) + '	' + str(np.max(FEM_z))
		print ('')
		print 'FDTD_pg:' + str(np.min(FDTD_pg)) + '	' + str(np.max(FDTD_pg)) + '	avg:' + str(np.mean(FDTD_pg))
		print 'FEM_pg:	' + str(np.min(FEM_pg)) + '	' + str(np.max(FEM_pg)) + '	avg:' + str(np.mean(FEM_pg))
		print ('')
	
		i=i+1
	#end
	print ('~~~~~~~~~~~~~~~~~~~~')

	return to_return_PG
## END FUNCTION
