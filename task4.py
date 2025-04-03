import geopandas as gpd
from shapely.geometry import Point

# Sample function to normalize longitude (assuming simple normalization between -180 and 180)
def norm_lon(lon):
    # Normalize longitude to be between -180 and 180 (just as an example)
    return ((lon + 180) % 360) - 180

# Given points

x0 = norm_lon(-100.20) # set min x coord
y0 = -75.195 # set min y coord
x1 = norm_lon(-99.0) #set max x coord
y1 = -75.185 #set max y coord


# Create Point geometries for each coordinate pair
point0 = Point(x0, y0)
point1 = Point(x1, y1)

# Create a GeoDataFrame to hold the points
gdf = gpd.GeoDataFrame({'geometry': [point0, point1]})

# Set a coordinate reference system (CRS) for the shapefile (WGS 84)
gdf.set_crs("EPSG:4326", inplace=True)

# Save the GeoDataFrame to a shapefile
gdf.to_file("points.shp")

print("Shapefile created successfully.")
