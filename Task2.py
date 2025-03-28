
'''
Plotting a singular plot
'''

import tracemalloc
from tiffExample import writeTiff # Import function to write GeoTIFF files
from processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 



tracemalloc.start()
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

  file_count = 1

  step_x = (x1 - x0) / 4 # Divide the x-range into 6 tiles
  step_y = (y1 - y0) / 4  # Divide the y-range into 6 tiles

  for tile_x0 in np.arange(x0,x1, step_x):
    tile_x1=tile_x0+step_x
    for tile_y0 in np.arange(y0, y1, step_y):
      tile_y1=tile_y0+step_y
      
      try:
          #read in all data within our spatial subset
        lvis=plotLVIS(filename,minX=tile_x0,minY=tile_y0,maxX=tile_x1,maxY=tile_y1,setElev=True)


        lvis.reprojectLVIS(3031) # Reproject the data to the Antarctic Polar Stereographic projection (EPSG 3031)
        lvis.estimateGround()  
        outName = f"lvisDEM2009{file_count}.tif"  # Estimate ground elevation from LVIS data
        file_count +=1 #Increase the file size by one each time
        lvis.writeDEM(res, outName) # Write the DEM data to a GeoTIFF file with the specified resolution
      
      except AttributeError as e:
        print(f"{filename} Skipped")
  

print("Memory peak usage:", tracemalloc.get_traced_memory())
tracemalloc.stop()