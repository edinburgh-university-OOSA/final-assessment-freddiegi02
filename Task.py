import rasterio
import matplotlib.pyplot as plt
from rasterio.warp import reproject, Resampling
import matplotlib.pyplot as plt

# LVIS2009 = rasterio.open("LVIS2009/GeoTIFF/Merged2009_FILL.tif")
# LVIS2015 = rasterio.open("LVIS2015/GeoTIFF/Merged2015_FILL.tif")
LVIS2009 = rasterio.open("aligned_raster3.tif")
LVIS2015 = rasterio.open("aligned_raster2.tif")




LVIS2009_5 = LVIS2009.read(1)
LVIS2015_5 = LVIS2015.read(1)
Ice_Change = (LVIS2015_5-LVIS2009_5)

plt.imshow(Ice_Change)
plt.colorbar()
plt.show()