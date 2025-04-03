'''
A script to run multiple scripts and join them together 
This script processes LVIS data, creates Digital Elevation Models (DEMs) 
and merges them into one output file.
'''
import tracemalloc
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from crs import extent
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 
import os #Import for file and directory handling
from rasterio.merge import merge #Import for merging GeoTIFF files
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders 
from rasterio.fill import fillnodata
from rasterio.windows import from_bounds
from pyproj import Proj, Transformer, transform

#from Task2 import reprojectLVIS

tracemalloc.start()

def getCmdArgs():
  '''
  Get commandline arguments
  '''
  #Create an argparse object with a decription
  ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  #Add an argument for the folder (string fo LVIS folder)
  ap.add_argument("folder",type=str,help=("Input folder"))
  #Add an argument for reading the resolution (Interger)
  ap.add_argument("res", type=int,help=("Spec Res"))
  #Parse the arguments from the command line 
  ap.add_argument('year', type=str,help=("2009 or 2015"))
  args = ap.parse_args()
  #return the argument
  return args

##########################################S

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method, merge and write function'''

  def reprojectLVIS(self, outEPSG):
    '''
    Method to reproject the geolocation data from WGS84 (EPSG:4326) 
    to the specified output EPSG coordinate system.
    '''
    inProj=Proj("epsg:4326") #Input coord
    outProj=Proj("epsg:"+str(outEPSG))
    self.long, self.lat=transform(inProj, outProj,self.lat,self.lon)


  def writeDEM(self,res,outName):
    '''Write LVIS ground elevation data to a geotiff'''
    # call function from tiffExample.py
    writeTiff(self.zG,self.long,self.lat,res,filename=outName,epsg=3031)
    return
    

  def mergeDEM(self, year):
    """A function to merge all of the tiles of the raster together """
    
    # Get the current working directory (PWD)
    current_dir = os.getcwd()

    # Use the current working directory for the input files and output file
    dirpath = glob(f"{current_dir}/LVIS{year}/Datasets/T3*tif")
    print(dirpath)
    out_fp = f"{current_dir}/LVIS{year}/GeoTIFF/Merged{year}.tif"

    #Iniate an empty list
    mosacic_files = []

    # Loop through files in the folder
    for files in dirpath:
        src = rasterio.open(files) #Open the files
        mosacic_files.append(src) #Append the files to the list 

    # Merge the tiles to a mosaic
    mosaic, out_trans = merge(mosacic_files)


    # Copy the metadata
    out_meta = src.meta.copy()


    #Set the output parameters
    out_meta.update({
        "driver": "GTiff", #set file type
        "height": mosaic.shape[1], # Set the height 
        "width": mosaic.shape[2], # Define the width
        "transform": out_trans, # Transform the mosaic
        "count": mosaic.shape[0], #Set the number of layers and bands
        "dtype": mosaic.dtype, #Set the datatype of the array
    })

    #Open a raster and read the files to it
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)


  def interpolation(self, year):
    """Function to Gap fill the arugments """

    # Open the GeoTIFF file for the specfied year 
    raster_file = rasterio.open(f'LVIS{year}/GeoTIFF/Merged{year}_FIT.tif')

    #Define the output file path for the filled raster
    out_fp = f'LVIS{year}/GeoTIFF/Merged{year}_FILL.tif'

    # Read the first band of the raster file
    raster = raster_file.read(1)

    # Create a boolean mask where raster values are not equal to -999 (considered as no-data)
    mask_boolean = (raster !=-999)

    # Use fillnodata function to fill missing data in the raster
    # Nax Search Distance defines the window size for the fill algorithm
    filled_raster = fillnodata(raster, mask = mask_boolean, max_search_distance = 250)


    #Copy the output metadata
    out_meta = raster_file.meta.copy()
    out_meta.update({
        "driver": "GTiff", #Set the driver
        "height": filled_raster.shape[0], #Set the height
        "width": filled_raster.shape[1], #Set the width
        "transform": raster_file.transform, #Transform the CRS
        "dtype": filled_raster.dtype, # Set the data type of the array
    })

    #Open the file using rasterio and write hte file name to it 
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(filled_raster, 1)


def norm_lon(lon):
    """Fixes negetive CRS issues"""
    return (lon) % 360 #Normalise longitude to ensure it stays within a valid range (0-360 degrees)

##########################################


if __name__=="__main__":
  '''Main block'''

  # read the command line arguments 
  args = getCmdArgs()
  folder = args.folder #Folder where LVIS data is stored
  res = args.res # Res for DEM file
  year = args.year

  x0 = norm_lon(-100.20) # set min x coord
  y0 = -75.233 # set min y coord
  x1 = norm_lon(-99.0) #set max x coord
  y1 = -75.152 #set max y coord

  file_count = 1 #Initialise a counter

  step_x = (x1 - x0) / 6 # Divide the x-range into 6 tiles
  step_y = (y1 - y0) / 6  # Divide the y-range into 6 tiles

  # Loop through each file in the folder
  for filename in os.listdir(folder):
    if filename.endswith(".h5"): #Process files that end with '.hf'
      filepath = os.path.join(folder, filename) #Get the full file path

      try: 
          print(f"File Processed {filepath}") #Print files being processed

          for tile_x0 in np.arange(x0,x1, step_x):
            tile_x1=tile_x0+step_x
            for tile_y0 in np.arange(y0, y1, step_y):
              tile_y1=tile_y0+step_y
              
              try:
                  #read in all data within our spatial subset
                lvis=plotLVIS(filepath,minX=tile_x0,minY=tile_y0,maxX=tile_x1,maxY=tile_y1,setElev=True)


                lvis.reprojectLVIS(3031) # Reproject the data to the Antarctic Polar Stereographic projection (EPSG 3031)
                lvis.estimateGround()  
                #outName = f"T3_DEM_{file_count}.tif"  # Estimate ground elevation from LVIS data
                outName = f"LVIS{year}/Datasets/T3_DEM_{file_count}.tif"  # Estimate ground elevation from LVIS data             
                file_count +=1 #Increase the file size by one each time
                lvis.writeDEM(res, outName) # Write the DEM data to a GeoTIFF file with the specified resolution
              
              except AttributeError as e:
                print(f"{filepath} Skipped")
          

      except AttributeError as e:
          #Print error in file
          print(f"{filepath} Skipped")

#Call the merge function
lvis.mergeDEM(year)
#Call the interpolation functon
#lvis.interpolation(year)

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", always_xy=True)
min_x, min_y = transformer.transform(x0, y0)
max_x, max_y = transformer.transform(x1, y1)
bouding_box = (max_x, min_y, min_x, max_y)

input_raster = f'LVIS{year}/GeoTIFF/Merged{year}.tif'
output_raster = f'LVIS{year}/GeoTIFF/Merged{year}_FIT.tif'
print(f"Input Raster: {input_raster}")
print(f"Output Raster: {output_raster}")
print(f"Common Bounds: {bouding_box}")

extent(input_raster, output_raster, bouding_box)
lvis.interpolation(year)
peak = tracemalloc.get_traced_memory()

# Convert bytes to MB for better readability
peak_mb = peak[0] / 10**9  # Peak memory in GB
current_mb = peak[1] / 10**9  # Current memory in GB

# Print memory usage details
print(f"Peak memory usage: {peak_mb:.2f} GB")
print(f"Current memory usage: {current_mb:.2f} GB")

# Stop tracing memory
tracemalloc.stop()