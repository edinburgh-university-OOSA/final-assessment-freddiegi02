import rasterio #Library for reading and writing raster data
import matplotlib.pyplot as plt #For plotting visulisation 
import numpy as np #Numerical Operation

def calculate_ice_loss(LVIS2009, LVIS2015, output_image="Output_Images/Elevation_Change.png", dpi=75):
    """
    Function to calculate ice loss between two elevation datasets (2009 and 2015).
    Generates an elevation change map and calculates total ice loss volume.

    Patameters:
        LVIS 2009 (str): Path to 2009 elevation data 
        LVIS 2015 (str): Path to save the output elevation change map
    """

    #Open both raster files using rasterio
    with rasterio.open(LVIS2009) as LVIS2009, rasterio.open(LVIS2015) as LVIS2015:
        LVIS2009_5 = LVIS2009.read(1)
        LVIS2015_5 = LVIS2015.read(1)

    #Calculate elevation change (2015- 2009)
    Elevation_Change = LVIS2015_5-LVIS2009_5

    #Select only negative values where ice loss has occurred
    Ice_Loss = Elevation_Change[Elevation_Change < 0]


    # Get pixel size from raster metadata
    pixel_width = abs(LVIS2009.meta['transform'][0])  # Pixel width (in meters)
    pixel_height = abs(LVIS2009.meta['transform'][4])  # Pixel height (in meters)
    pixel_area = pixel_width * pixel_height  # Area of one pixel in square meters


    #Sum of all negative elevation changes (meters)
    Total_Ice_Loss = np.sum(Ice_Loss)

    #convert total ice loss to volume (cubic meters)
    total_ice_loss_volume = Total_Ice_Loss * pixel_area

    # Convert volume from cubiuc meters to cubic kilometers
    total_ice_loss_volume_km3 = total_ice_loss_volume / 1000000000  

    #Print the total ice loss volume
    print(f"Total Ice Loss Volume: {total_ice_loss_volume_km3:.3f} km³")

    # Determine max absolute elevation change for color scaling
    abs_max = np.abs(Elevation_Change).max()
    plt.imshow(Elevation_Change, cmap='coolwarm', vmin=-abs_max, vmax=abs_max)
    plt.colorbar(label="Elevation Change (m)") # Add a legend with a colour scale
    plt.title("Ice Elevation Change (2015 - 2009)") # Add a title 
    plt.savefig(output_image, dpi=75, bbox_inches='tight') # Save the figure 
    plt.show() #Show the figure

if __name__ == '__main__':
    calculate_ice_loss("LVIS2009/GeoTIFF/T3_Merged2009_FILL.tif", "LVIS2015/GeoTIFF/T3_Merged2015_FILL.tif")