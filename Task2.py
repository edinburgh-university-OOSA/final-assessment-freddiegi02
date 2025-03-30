
'''
Plotting a singular plot
'''

import tracemalloc
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 
from rasterio.merge import merge #Import for merging GeoTIFF files
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders
import os #Import for file and directory handling


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
  # Add a postioal argument to specify the year of the data
  ap.add_argument('year', type=str,help=("2009 or 2015"))
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
  
  def mergeDEM(self, year):
    """A function to merge all of the tiles of the raster together """
  
    # Get the current working directory (PWD)
    current_dir = os.getcwd()

    # Use the current working directory for the input files and output file
    dirpath = glob(f"{current_dir}/LVIS{year}/Datasets/T2*tif")
    #Outpaths for all of the Merged files
    out_fp = f"{current_dir}/LVIS{year}/GeoTIFF/Merged{2009}.tif"

    #Intiaties an empty list 
    mosacic_files = []

    # Loops over the folders in the directory
    for files in dirpath:
        src = rasterio.open(files)
        mosacic_files.append(src) # appends all of the files to the list

    #merge multiple rasteer files into one mosaic
    mosaic, out_trans = merge(mosacic_files)

    #Creates a copy of the meta data to retain info about the general stucture
    out_meta = src.meta.copy()

    #Update the metadata
    out_meta.update({
        "driver": "GTiff", #Set to GeoTiff format
        "height": mosaic.shape[1], #Set the height of the mosaic
        "width": mosaic.shape[2], #Set the width of the mosaic
        "transform": out_trans, # Transform the mosaic
        "count": mosaic.shape[0], #Set the number of layers/bands
        "dtype": mosaic.dtype, #Set the data type of the array
    })
    # Open a new raster file for writing using rasterio
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        # Write the mosaic data to the file
        dest.write(mosaic)

def norm_lon(lon):
    #Normalise longitude to ensure values remain within a valid range (0-360 degrees)
    return (lon) % 360

if __name__=="__main__":
  '''Main block'''

  # read the command line
  args = getCmdArgs()
  filename = args.filename #Store input filename
  res = args.res #Store spatial resolution
  year = args.res #Store the year


  x0 = norm_lon(-102.00) # set min x coord
  y0 = -75.4 # set min y coord
  x1 = norm_lon(-99.00) #set max x coord
  y1 = -74.6 #set max y coord
 

  file_count = 1 #Make the file count 1 at the start

  step_x = (x1 - x0) / 5 # Divide the x-range into 6 tiles
  step_y = (y1 - y0) / 4  # Divide the y-range into 6 tiles

  for tile_x0 in np.arange(x0,x1, step_x):
    tile_x1=tile_x0+step_x
    for tile_y0 in np.arange(y0, y1, step_y):
      tile_y1=tile_y0+step_y
      
      try:
          #read in all data within our spatial subset
        lvis=plotLVIS(filename,minX=tile_x0,minY=tile_y0,maxX=tile_x1,maxY=tile_y1,setElev=True)


        lvis.reprojectLVIS(3031) # Reproject the data to the Antarctic Polar Stereographic projection (EPSG 3031)
        lvis.estimateGround() #Call the estimate ground function
        outName = f"LVIS{year}/Datasets/T2_DEM_{file_count}.tif"  # Estimate ground elevation from LVIS data
        file_count +=1 #Increase the file size by one each time
        lvis.writeDEM(res, outName) # Write the DEM data to a GeoTIFF file with the specified resolution
      
      except AttributeError as e:
        print(f"{filename} Skipped") #Print the files which have been skipped
  
# Call the merge fuction 
lvis.mergeDEM(year) 

# Call Memory Function to get the currnet and peak memory in bytes
current, peak = tracemalloc.get_traced_memory()

# Convert bytes to GB
current_mb = current / 10**9
peak_mb = peak / 10**9

# Print memory usage details
print(f"Current memory usage: {current_mb:.2f} GB")
print(f"Peak memory usage: {peak_mb:.2f} GB")

# Stop tracing memory
tracemalloc.stop()