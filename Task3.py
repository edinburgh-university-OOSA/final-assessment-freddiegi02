'''
A script to run multiple scripts and join them together 
This script processes LVIS data, creates Digital Elevation Models (DEMs) 
and merges them into one output file.
'''
import tracemalloc
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from src.WriteExtent import extent
from src.Commands import getCmdArgs, norm_lon 
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import os #Import for file and directory handling
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders 
from pyproj import Transformer

tracemalloc.start()

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
current_dir = os.getcwd()
dirpath = glob(f"{current_dir}/LVIS{year}/Datasets/T3*tif")
out_fp = f"{current_dir}/LVIS{year}/GeoTIFF/T3_Merged{year}.tif"
lvis.mergeDEM(year,dirpath, out_fp)
plt.title(f"PIG Elevation for the {year}")
# Save the figure as a PNG with the specified DPI and tight bounding box
plt.savefig(f"Output_Images/PIG_Site_{year}.png", dpi=75, bbox_inches='tight')

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", always_xy=True)
min_x, min_y = transformer.transform(x0, y0)
max_x, max_y = transformer.transform(x1, y1)
bouding_box = (max_x, min_y, min_x, max_y)

input_raster = f'LVIS{year}/GeoTIFF/T3_Merged{year}.tif'
output_raster = f'LVIS{year}/GeoTIFF/T3_Merged{year}_FIT.tif'
print(f"Input Raster: {input_raster}")
print(f"Output Raster: {output_raster}")
print(f"Common Bounds: {bouding_box}")
extent(input_raster, output_raster, bouding_box)


# Open the GeoTIFF file for the specfied year 
fit_file = rasterio.open(f'LVIS{year}/GeoTIFF/T3_Merged{year}_FIT.tif')
#Define the output file path for the filled raster
out_interfile = f'LVIS{year}/GeoTIFF/T3_Merged{year}_FILL.tif'
lvis.interpolation(year, fit_file, out_interfile)
    

peak = tracemalloc.get_traced_memory()

# Convert bytes to MB for better readability
peak_mb = peak[0] / 10**9  # Peak memory in GB
current_mb = peak[1] / 10**9  # Current memory in GB

# Print memory usage details
print(f"Peak memory usage: {peak_mb:.2f} GB")
print(f"Current memory usage: {current_mb:.2f} GB")

# Stop tracing memory
tracemalloc.stop()