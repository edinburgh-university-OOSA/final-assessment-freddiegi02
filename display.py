import rasterio
import matplotlib.pyplot as plt

# Open the raster file
filename = 'OutputRaster/MergedFILL.tif'  # Replace with your raster file path
with rasterio.open(filename) as src:
    # Read the data (this reads all bands by default)
    band1 = src.read(1)  # Read the first band (e.g., grayscale)
    
    # Display the raster data using matplotlib
    plt.imshow(band1, cmap='gray')
    plt.colorbar()  # Optionally add a color bar
    plt.title('Raster Display')
    plt.show()


