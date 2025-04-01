import rasterio
import matplotlib.pyplot as plt
filename = 'Merged2009.tif' 
# Open the raster file
#filename = 'LVIS2015/GeoTIFF/Merged2015.tif'  # Replace with your raster file path
#filename = 'LVIS2015/GeoTIFF/Merged2015_FILL.tif'
#   # Replace with your raster file path
with rasterio.open(filename) as src:
    # Read the data (this reads all bands by default)
    band1 = src.read(1)  # Read the first band (e.g., grayscale)
    
    # Get the shape of the raster (rows, columns)
    raster_shape = band1.shape
    print(f"Raster shape: {raster_shape}")
    
    # Display the raster data using matplotlib
    plt.imshow(band1, cmap='gray')
    plt.colorbar()  # Optionally add a color bar
    plt.title('Raster Display')
    plt.show()
