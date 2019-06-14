####################################################################
####################################################################
#### 	The Awesome Simulator, AwSimLib interpPG.py tester	####
####    						    	####
####	Author: Abhejit Rajagopal,  abhejit@ucla.edu	    	####
####    Date: 09/02/2014				    	####
####    						    	####
####################################################################
#### This file serves as an example how to interpolate a 3D	####
#### photogeneration profile (e.g. from Lumerical FDTD) onto	####
#### a generic, unstructured grid (e.g. Sentaurus FEM).		####
####    		   				    	####
####  (ex_interpPG.py) is part of the AwSimLib software package ####
####	module 3D.py: /sim/3D.py		    		####
####    		    				    	####
####    This software is free to use, subjct to terms and   	####
####    	conditions in the AwSimLib license (LGPLv3).	####
####    AwSimLib license: ../LICENSE.TXT		    	####
####################################################################
####################################################################
import sys
sys.path.append('../../')
from AwSimLib.fileIO import DFISE as DFISE
from AwSimLib.sim import grids as grids
import numpy as np

#######################################################################
#### READ DFISE files
filenames = ['input/grids/DFISE_init.dat', 'input/grids/PLOT_dfise.dat']
z = DFISE.readDAT(filenames)
DFISE.printDAT(z[0]) #consol output
DFISE.printDAT(z[1]) #consol output

#### DEFINE EXTraction parameters (must pass strcmp)
PMIFile = z[0] # PMIFile defines X,Y,Z coords of FEM (see README.txt)
ExtractFile = z[1] # ExtractFile contains 3D FEM data (can be == PMIFile)

## extract data from DAT to matrix
extract_file = PMIFile # given this file with data...
extract_regions = ["substrate_bot",  "cap",  "pillar", "substrate_top"] # for these regions
extract_fields = ["PMIUserField0", "PMIUserField1", "PMIUserField2", "DopingConcentration", "NDopantActiveConcentration"] # ... extract these datasets
extract_dimensions = ["1", "1", "1", "1", "1"]# ... having these dimensions
DATAfields_extract = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
#written = DFISE.write2csv(DATAfields_extract, 'output/_ASL_new_ORIG', extract_regions)
##stop
#######################################################################

#######################################################################
##### (optional) MODify matrix data
## e.g. negative X,Y,Z stored as positive, so flip Z in known regions
#i=-1
#for region in d:
#	i = i+1
#	if extract_regions[i] == "substrate" or extract_regions[i] == "mask_hole":
#		z_vals = region[:,2]
#		region[:,2] = -1.00e0*z_vals #flip z
#	else:
#		continue
#print "..-> fixed z-vals in substrate and mask_hole regions"
#######################################################################

#######################################################################
#### INTERPOLATE the photogeneration values from a CSV (refer to README.txt for how to generate)
lumerical_csv = 'input/lumerical_data/modZ3_ARexport_84941196433333.33.csv'
FEM_data = DATAfields_extract
FEM_scaling = 1.00e-6 # everything in Sentaurus is relative to 1 micron, so convert to meters

PG_data = []
i=0
PG_data = grids.interpPG(lumerical_csv, FEM_data, FEM_scaling)
for each in FEM_data:
	origLength = (FEM_data[i].shape[1])
	FEM_data[i] = np.insert(FEM_data[i], origLength, PG_data[i].transpose(), axis=1)
	newLength = (FEM_data[i].shape[1])
	if newLength == origLength+1:
		print "Sucess!",
		print FEM_data[i][:,newLength-1].mean(),
		print FEM_data[i][:,newLength-1].shape
	i=i+1
#
extract_fields.append("OpticalGeneration")
extract_dimensions.append("1")

insert_data = FEM_data
insert_filename = 'output/_ASL_interpPG.dat'
insert_regions = extract_regions
insert_dataname = [extract_fields]*len(insert_regions)
insert_function = insert_dataname
insert_type = [["scalar"]*len(extract_fields)]*len(insert_regions)
insert_dimension = [extract_dimensions]*len(insert_regions)
insert_location = [["vertex"]*len(extract_fields)]*len(insert_regions)
info = ExtractFile.INFO
newDAT = DFISE.buildDAT(insert_data, info, insert_filename, insert_regions, insert_dataname, insert_function, insert_type, insert_dimension, insert_location)
DFISE.printDAT(newDAT) #console verification

## Write DAT file
writeSucessINTERP = DFISE.writeDAT(newDAT, newDAT.filename)

#Write CSV file
[newDAT_interp] = DFISE.readDAT(newDAT.filename)
extract_file = newDAT_interp # given this file with data...
extract_regions = insert_regions
extract_fields = insert_dataname[0]
extract_dimensions = insert_dimension[0]
DATAfields_extract_interp = DFISE.extractDAT2matrix(extract_file, extract_regions, extract_fields, extract_dimensions)
written = DFISE.write2csv(DATAfields_extract_interp, 'output/_ASL_interpPG', extract_regions)
##
#######################################################################
########################################################################
########################################################################
