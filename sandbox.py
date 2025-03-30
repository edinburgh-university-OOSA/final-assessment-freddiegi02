import tracemalloc
from src.tiffExample import writeTiff # Import function to write GeoTIFF files
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
from matplotlib import pyplot as plt #Import for plotting
import numpy as np #Import for numerical operations 
import argparse #Import for handling command-line arguments 
import os #Import for file and directory handling
from rasterio.merge import merge #Import for merging GeoTIFF files
import rasterio #Import to help with Raster Data
from glob import glob #Import to help with multiple files and folders 
from rasterio.fill import fillnodata
year = '2009'
current_dir = os.getcwd()
dirpath = glob(f"{current_dir}/LVIS{year}/Datasets/T2*tif")
print(dirpath)