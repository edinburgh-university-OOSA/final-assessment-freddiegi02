
'''
An example of how to use the 
LVIS python scripts
'''

# import the HDF5 data handler class

from processLVIS import lvisGround

#from lvisCla import lvisData
from pyproj import Proj, transform
from matplotlib import pyplot as plt
import numpy as np
from tiffExample import writeTiff
import argparse


def getCmdArgs():
  # function description for use within python
  '''
  Get commandline arguments
  '''
  # create an argparse object with a useful help comment
  ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  # read a string
  ap.add_argument("filename",type=str,help=("Input filename"))
  ap.add_argument("res", type=int,help=("Spec Res"))
  args = ap.parse_args()
  # return that object from this function
  return args

##########################################S

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method'''

  def reprojectLVIS(self, outEPSG):
    '''A method to reproject the geolocation data'''
    inProj=Proj("epsg:4326")
    outProj=Proj("epsg:"+str(outEPSG))
    self.long, self.lat=transform(inProj, outProj,self.lat,self.lon)


  def writeDEM(self,res,outName):
    '''Write LVIS ground elevation data to a geotiff'''
    #res = float(res)
    # call function from tiffExample.py
    writeTiff(self.zG,self.long,self.lat,res,filename=outName,epsg=3031)
    return


def norm_long(lon):
    return (lon) % 360 
##########################################


if __name__=="__main__":
  '''Main block'''

# read the command line
args = getCmdArgs()
filename = args.filename
res = args.res

  # create instance of class with "onlyBounds" flag
b=plotLVIS(filename,onlyBounds=True)


# set a steo size (note that this will be in degrees)

x0 = norm_long(-102.00)
#print(x0)
y0 = -75.4
x1 = norm_long(-99.00)
#print(x1)
y1 = -74.6

# x0=b.bounds[0]
# y0=b.bounds[1]
# x1=(b.bounds[2]-b.bounds[0])/1+b.bounds[0]
# y1=(b.bounds[3]-b.bounds[1])/1+b.bounds[1]
# print(f"Bounding extent: {b.bounds}")
#read in all data within our spatial subset
lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)

#print(res)

# plot up some waveforms using your new method
#lvis.plotWave(0)
# to make a DEM as a geotiff

lvis.reprojectLVIS(3031) # reproject the data to local UTM zone
lvis.estimateGround()    # find ground elevations
outName="lvisDEMLat.tif"  # set output filename
lvis.writeDEM(res, outName)           
#               #write data to a DEM at 100 m resolution

