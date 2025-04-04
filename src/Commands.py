  
import argparse
import rasterio
from rasterio.merge import merge #Import for merging GeoTIFF files
import matplotlib.pyplot as plt
import os


def getCmdArgs():
    '''
    Get commandline arguments
    '''
    # Create an argparse paser object with a description
    ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
    # Add a positional argument for the input filename (string)
    ap.add_argument("--filename",type=str,help=("Input filename"))
    # Add a positional argument for the resolution (integer)
    ap.add_argument("--res", type=int,help=("Spec Res"))
    # Add a postioal argument to specify the year of the data
    ap.add_argument('--year', type=str,help=("2009 or 2015"))
    ap.add_argument("--waveform",type=int,help=("Input Number"))
    ap.add_argument("--folder",type=str,help=("Input folder"))
    # Parse command-line arguments
    args = ap.parse_args()
    # return that object from this function
    return args


def norm_lon(lon):
    """
    SFixes negetive CRS issues
    
    Paramters:
      lon (float): Longitide Value

    Returns:
      float: Normalised longitude within the range of 0-360 degrees"
      """
    return (lon) % 360 #Normalise longitude to ensure it stays within a valid range (0-360 degrees)

def mergeDEM( year, dirpath, out_fp):
    """A function to merge all of the tiles of the raster together 
    
    Parameters: 
      year (int): File year
      dirpath (string): Input file location 
      out_fp (string): Output file location


    Returns:
      merged file (geotiff)
    """
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

    plt.clf()
    plt.imshow(mosaic[0], cmap='viridis')  # You can adjust the colormap as needed
    plt.colorbar(label="Elevation(m)")  # Add a color bar for reference


    folder_path = f'LVIS{year}/Datasets'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


