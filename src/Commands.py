  
import argparse
import rasterio
from rasterio.merge import merge #Import for merging GeoTIFF files
import matplotlib.pyplot as plt
import os
from rasterio.fill import fillnodata
from glob import glob


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

def mergeDEM( year, out_fp, x0, y0, x1, y1):
    """A function to merge all of the tiles of the raster together 
    
    Parameters: 
      year (int): File year
      dirpath (string): Input file location 
      out_fp (string): Output file location


    Returns:
      merged file (geotiff)
    """
    dirpath = glob(f"LVIS{year}/Datasets/*.tif")
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
    plt.title(f"PIG Elevation for the {year}")
    # Save the figure as a PNG with the specified DPI and tight bounding box
    plt.savefig(f"Output_Images/PIG_{year}_{x0:.2f}_{x1:.2f}_{y0:.2f}_{y1:.2f}.png", dpi=75, bbox_inches='tight')



    folder_path = f'LVIS{year}/Datasets'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def interpolation( year, fit_file, out_interfile, x0, y0, x1, y1):
  """A function to merge all of the tiles of the raster together 
  
  Parameters: 
    year (int): File year
    fit_file (string): Input file location 
    out_interfile (string): Output file location


  Returns:
    Interpolated file (geotiff)
  """

  # Read the first band of the raster file
  raster = fit_file.read(1)

  # Create a boolean mask where raster values are not equal to -999 (considered as no-data)
  mask_boolean = (raster !=-999)

  # Use fillnodata function to fill missing data in the raster
  # Nax Search Distance defines the window size for the fill algorithm
  filled_raster = fillnodata(raster, mask = mask_boolean, max_search_distance =1000)


  #Copy the output metadata
  out_meta = fit_file.meta.copy()
  out_meta.update({
      "driver": "GTiff", #Set the driver
      "height": filled_raster.shape[0], #Set the height
      "width": filled_raster.shape[1], #Set the width
      "transform": fit_file.transform, #Transform the CRS
      "dtype": filled_raster.dtype, # Set the data type of the array
  })

  #Open the file using rasterio and write hte file name to it 
  with rasterio.open(out_interfile, "w", **out_meta) as dest:
      dest.write(filled_raster, 1)

      # Plot the filled raster
  plt.clf()
  plt.imshow(filled_raster, cmap='viridis')  # You can adjust the colormap as needed
  plt.colorbar(label="Elevation (m)")  # Add a color bar for reference
  plt.title(f"PIG Elevation for Year {year}")

  # Save the figure as a PNG with the specified DPI and tight bounding box
  plt.savefig(f"Output_Images/PIG_Elevation_{year}_{x0:.2f}_{x1:.2f}_{y0:.2f}_{y1:.2f}.png", dpi=75, bbox_inches='tight')