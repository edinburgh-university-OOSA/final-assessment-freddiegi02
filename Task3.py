'''
A script to run multiple scripts and join them together 
This script processes LVIS data, creates Digital Elevation Models (DEMs) 
and merges them into one output file.
'''
import tracemalloc #Import for memory tracking
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from src.WriteExtent import extent #Import the function of bouding box
from src.Commands import getCmdArgs, norm_lon, mergeDEM, interpolation
from Task2 import file_loop #Importing the function to loop through files
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import os #Import for file and directory handling
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders 
from pyproj import Transformer

tracemalloc.start() # Start memory tracking

##########################################S

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method, merge and write function'''


  def writeDEM(self,res,outName):
    '''Write LVIS ground elevation data to a geotiff
    
    Paramters:
      res (int): Resolution of the output raster
      outname (str): Output file name
    '''
    # call function from tiffExample.py
    writeTiff(self.zG,self.long,self.lat,res,filename=outName,epsg=3031)
    return


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

  step_x = (x1 - x0) / 6 # Divide the x-range into 6 tiles
  step_y = (y1 - y0) / 6  # Divide the y-range into 6 tiles
  file_count = 1 #Initialise a counter
  # Loop through each file in the folder
  for filename in os.listdir(folder):
    if filename.endswith(".h5"): #Process files that end with '.hf'
      filepath = os.path.join(folder, filename) #Get the full file path

      try: 
          print(f"File Processed {filepath}") #Print files being processed
          file_count = file_loop(filepath, x0, x1, y0, y1, step_x, step_y, res, year, file_count)

      except AttributeError as e:
          #Print error in file
          print(f"{filepath} Skipped")

  #Call the merge function
  out_fp = f"LVIS{year}/GeoTIFF/T3_Merged{year}.tif"
  mergeDEM(year, out_fp, x0, y0, x1, y1) 

  #Transform the coordinates to EPSG:3031
  transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", always_xy=True)
  min_x, min_y = transformer.transform(x0, y0)  # Transform minimum coordinates
  max_x, max_y = transformer.transform(x1, y1)  # Transform maximum coordinates
  bounding_box = (max_x, min_y, min_x, max_y)  # Define the bounding box

  input_raster = f'LVIS{year}/GeoTIFF/T3_Merged{year}.tif'
  output_raster = f'LVIS{year}/GeoTIFF/T3_Merged{year}_FIT.tif'
  extent(input_raster, output_raster, bounding_box) #call the function to standarise the shape of the raster


  # Open the GeoTIFF file for the specfied year 
  fit_file = rasterio.open(f'LVIS{year}/GeoTIFF/T3_Merged{year}_FIT.tif')
  #Define the output file path for the filled raster
  out_interfile = f'LVIS{year}/GeoTIFF/T3_Merged{year}_FILL.tif'
  interpolation(year, fit_file, out_interfile, x0, y0, x1, y1)
      

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