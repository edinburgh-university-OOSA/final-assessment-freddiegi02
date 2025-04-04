import rasterio
import matplotlib.pyplot as plt
import numpy as np

def calculate_ice_loss(LVIS2009, LVIS2015, output_image="Output_Images/Elevation_Change.png", dpi=75):

    with rasterio.open(LVIS2009) as LVIS2009, rasterio.open(LVIS2015) as LVIS2015:
        LVIS2009_5 = LVIS2009.read(1)
        LVIS2015_5 = LVIS2015.read(1)

    Elevation_Change = LVIS2015_5-LVIS2009_5

    Ice_Loss = Elevation_Change[Elevation_Change < 0]

    pixel_width = abs(LVIS2009.meta['transform'][0])  # Pixel width (in meters)
    pixel_height = abs(LVIS2009.meta['transform'][4])  # Pixel height (in meters)
    pixel_area = pixel_width * pixel_height  # Area of one pixel in square meters

    Total_Ice_Loss = np.sum(Ice_Loss)

    total_ice_loss_volume = Total_Ice_Loss * pixel_area

    total_ice_loss_volume_km3 = total_ice_loss_volume / 1000000000  

    print(f"Total Ice Loss Volume: {total_ice_loss_volume_km3:.3f} km³")

    abs_max = np.abs(Elevation_Change).max()
    plt.imshow(Elevation_Change, cmap='coolwarm', vmin=-abs_max, vmax=abs_max)
    plt.colorbar(label="Elevation Change (m)")
    plt.title("Ice Elevation Change (2015 - 2009)")
    plt.savefig(output_image, dpi=75, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    calculate_ice_loss("LVIS2009/GeoTIFF/T3_Merged2009_FILL.tif", "LVIS2015/GeoTIFF/T3_Merged2015_FILL.tif")