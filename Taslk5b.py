import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
import matplotlib.pyplot as plt

with rasterio.open("LVIS2009/GeoTIFF/Merged2009_FILL.tif") as src1, \
     rasterio.open("LVIS2015/GeoTIFF/Merged2015_FILL.tif") as src2:
    
    LVIS2015_5 = src2.read(1)
    print(LVIS2015_5[3])


    # Read metadata from the 2009 raster
    out_meta = src1.meta.copy()

    # Create an empty array to store the resampled 2015 raster
    resampled_2015 = np.zeros(src1.shape, dtype=src1.dtypes[0])
    print(resampled_2015)

    # Reproject the 2015 raster to match the 2009 raster
    reproject(
        source=src2.read(1),  # Read data from 2015 raster
        destination=resampled_2015,  # Store resampled data here
        src_transform=src2.transform,
        src_crs=src2.crs,
        dst_transform=src1.transform,
        dst_crs=src1.crs,
        resampling=Resampling.bilinear
    )

    # Read the 2009 raster
    LVIS2009_5 = src1.read(1)
    

# Compute the elevation change (2015 - 2009)
elevation_change = resampled_2015 - LVIS2009_5
print(elevation_change)

# Filter negative changes (ice loss)
ice_loss = elevation_change[elevation_change < 0]
print(f'Ice Lost: {ice_loss}')



# Pixel area (in square meters) based on the raster's metadata
pixel_width = abs(src1.meta['transform'][0])  # Pixel width (in meters)
pixel_height = abs(src1.meta['transform'][4])  # Pixel height (in meters)
pixel_area = pixel_width * pixel_height  # Area of one pixel in square meters

# Calculate total ice loss (sum of negative changes) in meters
total_ice_loss = np.sum(ice_loss)

# Calculate total ice loss volume in cubic meters
total_ice_loss_volume = total_ice_loss * pixel_area

total_ice_loss_volume_km3 = total_ice_loss_volume / 1_000_000_000  



print(f"Total Ice Loss (elevation change) in meters: {total_ice_loss} meters")
print(f"Total Ice Loss Volume: {total_ice_loss_volume:,} cubic meters")
print(f"Total Ice Loss Volume: {total_ice_loss_volume_km3:.3f} km³")




# # Plot the elevation change to visualize the ice loss
# plt.imshow(elevation_change, cmap='coolwarm', vmin=-np.abs(elevation_change).max(), vmax=np.abs(elevation_change).max())
# plt.colorbar(label="Elevation Change (m)")
# plt.title("Ice Elevation Change (2015 - 2009)")
# plt.show()