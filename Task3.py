'''
A script to run multiple scripts and join them together 
This script processes LVIS data, creates Digital Elevation Models (DEMs) 
and merges them into one output file.
'''

from tiffExample import writeTiff # Import function to write GeoTIFF files
from processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 
import numpy as np #Import for numerical operations 
import os #Import for file and directory handling
from rasterio.merge import merge #Import for merging GeoTIFF files
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders 

#from Task2 import reprojectLVIS

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
    #res = float(res)
    # call function from tiffExample.py
    writeTiff(self.zG,self.long,self.lat,res,filename=outName,epsg=3031)
    return
    

  def mergeDEM(self):
    
    # Get the current working directory (PWD)
    current_dir = os.getcwd()

    # Use the current working directory for the input files and output file
    dirpath = glob(f"{current_dir}/*tif")
    out_fp = f"{current_dir}/Merged2009.tif"

    mosacic_files = []

    for files in dirpath:
        src = rasterio.open(files)
        mosacic_files.append(src)

    mosaic, out_trans = merge(mosacic_files)

    out_meta = src.meta.copy()

    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "count": mosaic.shape[0],
        "dtype": mosaic.dtype,
    })

    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)


#Normalise longitude to ensure it stays within a valid range (0-360 degrees)
def norm_lon(lon):
    return (lon) % 360 

##########################################


if __name__=="__main__":
  '''Main block'''

# read the command line arguments 
args = getCmdArgs()
folder = args.folder #Folder where LVIS data is stored
res = args.res # Res for DEM file


file_count = 1 #Initialise a counter

# Loop through each file in the folder
for filename in os.listdir(folder):
  if filename.endswith(".h5"): #Process files that end with '.hf'
    filepath = os.path.join(folder, filename) #Get the full file path

    try: 
        print(f"File Processed {filepath}") #Print files being processed


        x0 = norm_lon(-102.00) # set min x coord
        y0 = -75.4 # set min y coord
        x1 = norm_lon(-99.00) #set max x coord
        y1 = -74.6 #set max y coord


        #Read in the data
        lvis=plotLVIS(filepath,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)


        lvis.reprojectLVIS(3031) # reproject the data into Polar Sterographic
        lvis.estimateGround()    # find ground elevations
        outName = f"lvisDEM2015{file_count}.tif" # Set an ouputname
        lvis.writeDEM(res, outName) #Write the DEm to a geoTIFF
        file_count +=1 #Increase the file size by one each time

    except AttributeError as e:
        #Print error in file
        print(f"{filepath} Skipped")


lvis.mergeDEM()
