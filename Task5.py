import rasterio
import matplotlib.pyplot as plt
import numpy as np

LVIS2009 = rasterio.open("LVIS2009/GeoTIFF/Merged2009_FIT.tif")
LVIS2015 = rasterio.open("LVIS2015/GeoTIFF/Merged2015_FIT.tif")

LVIS2009_5 = LVIS2009.read(1)
LVIS2015_5 = LVIS2015.read(1)

print(LVIS2015_5)

Elevation_Change = (LVIS2015_5-LVIS2009_5)

Ice_Loss = Elevation_Change[Elevation_Change < 0]

pixel_width = abs(LVIS2009.meta['transform'][0])  # Pixel width (in meters)
pixel_height = abs(LVIS2009.meta['transform'][4])  # Pixel height (in meters)
pixel_area = pixel_width * pixel_height  # Area of one pixel in square meters

Total_Ice_Loss = np.sum(Ice_Loss)

total_ice_loss_volume = Total_Ice_Loss * pixel_area

total_ice_loss_volume_km3 = total_ice_loss_volume / 1_000_000_000  

print(f"Total Ice Loss Volume: {total_ice_loss_volume_km3:.3f} km³")


