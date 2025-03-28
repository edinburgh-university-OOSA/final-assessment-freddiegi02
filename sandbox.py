
'''
Plotting a singular plot
'''


from tiffExample import writeTiff # Import function to write GeoTIFF files
from processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 



def getCmdArgs():
  '''
  Get commandline arguments
  '''
  # Create an argparse paser object with a description
  ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  # Add a positional argument for the input filename (string)
  ap.add_argument("filename",type=str,help=("Input filename"))
  # Add a positional argument for the resolution (integer)
  ap.add_argument("res", type=int,help=("Spec Res"))
  # Parse command-line arguments
  args = ap.parse_args()
  # return that object from this function
  return args

##########################################S

class plotLVIS(lvisGround):
  """
  A class inheriting from lvisGround and adding additional methods 
  for reprojecting geolocation data and writing DEM files.
  """

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
  
def norm_lon(lon):
    #Normalise longitude to ensure values remain within a valid range (0-360 degrees)
    return (lon) % 360

if __name__=="__main__":
  '''Main block'''

# read the command line
args = getCmdArgs()
filename = args.filename #Store input filename
res = args.res #Store spatial resolution


x0 = norm_lon(-102.00) # set min x coord
y0 = -75.4 # set min y coord
x1 = norm_lon(-99.00) #set max x coord
y1 = -74.6 #set max y coord

#read in all data within our spatial subset
lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)


lvis.reprojectLVIS(3031) # Reproject the data to the Antarctic Polar Stereographic projection (EPSG 3031)
lvis.estimateGround()    # Estimate ground elevation from LVIS data
outName="DEM.tif" # Set the output filename for the DEM
lvis.writeDEM(res, outName) # Write the DEM data to a GeoTIFF file with the specified resolution
