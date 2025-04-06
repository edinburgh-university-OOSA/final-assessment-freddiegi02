
'''
A class to hold LVIS data
with methods to read
'''

###################################
import numpy as np
import h5py
from pyproj import Proj, transform #Importing Proj and transform to change the CRS
###################################

class lvisData(object):
  '''
  LVIS data handler
  '''  

  

  def __init__(self,filename,setElev=False,minX=-100000000,maxX=100000000,minY=-1000000000,maxY=100000000,onlyBounds=False):
    '''
    Class initialiser. Calls a function to read LVIS data within bounds minX,minY and maxX,maxY etElev=1 converts LVIS's stop and start
    elevations to arrays of elevation. OnlyBounds sets "bounds" to the corner of the area of interest
    '''
    # call the file reader and load in to the self
    self.readLVIS(filename,minX,minY,maxX,maxY,onlyBounds)
    if(setElev):     # to save time, only read elev if wanted
      self.setElevations()



############################################################################


  # def mergeDEM(self, year, dirpath, out_fp):
  #   """A function to merge all of the tiles of the raster together 
    
  #   Parameters: 
  #     year (int): File year
  #     dirpath (string): Input file location 
  #     out_fp (string): Output file location


  #   Returns:
  #     merged file (geotiff)
  #   """
  #   mosacic_files = []

  #   # Loop through files in the folder
  #   for files in dirpath:
  #       src = rasterio.open(files) #Open the files
  #       mosacic_files.append(src) #Append the files to the list 

  #   # Merge the tiles to a mosaic
  #   mosaic, out_trans = merge(mosacic_files)


  #   # Copy the metadata
  #   out_meta = src.meta.copy()


  #   #Set the output parameters
  #   out_meta.update({
  #       "driver": "GTiff", #set file type
  #       "height": mosaic.shape[1], # Set the height 
  #       "width": mosaic.shape[2], # Define the width
  #       "transform": out_trans, # Transform the mosaic
  #       "count": mosaic.shape[0], #Set the number of layers and bands
  #       "dtype": mosaic.dtype, #Set the datatype of the array
  #   })

  #   #Open a raster and read the files to it
  #   with rasterio.open(out_fp, "w", **out_meta) as dest:
  #       dest.write(mosaic)

  #   plt.clf()
  #   plt.imshow(mosaic[0], cmap='viridis')  # You can adjust the colormap as needed
  #   plt.colorbar(label="Elevation(m)")  # Add a color bar for reference


  #   folder_path = f'LVIS{year}/Datasets'

  #   for filename in os.listdir(folder_path):
  #       file_path = os.path.join(folder_path, filename)
  #       if os.path.isfile(file_path):
  #           os.remove(file_path)


  # def interpolation(self, year, fit_file, out_interfile):
  #   """A function to merge all of the tiles of the raster together 
    
  #   Parameters: 
  #     year (int): File year
  #     fit_file (string): Input file location 
  #     out_interfile (string): Output file location


  #   Returns:
  #     Interpolated file (geotiff)
  #   """

  #   # Read the first band of the raster file
  #   raster = fit_file.read(1)

  #   # Create a boolean mask where raster values are not equal to -999 (considered as no-data)
  #   mask_boolean = (raster !=-999)

  #   # Use fillnodata function to fill missing data in the raster
  #   # Nax Search Distance defines the window size for the fill algorithm
  #   filled_raster = fillnodata(raster, mask = mask_boolean, max_search_distance = 250)


  #   #Copy the output metadata
  #   out_meta = fit_file.meta.copy()
  #   out_meta.update({
  #       "driver": "GTiff", #Set the driver
  #       "height": filled_raster.shape[0], #Set the height
  #       "width": filled_raster.shape[1], #Set the width
  #       "transform": fit_file.transform, #Transform the CRS
  #       "dtype": filled_raster.dtype, # Set the data type of the array
  #   })

  #   #Open the file using rasterio and write hte file name to it 
  #   with rasterio.open(out_interfile, "w", **out_meta) as dest:
  #       dest.write(filled_raster, 1)

  #       # Plot the filled raster
  #   plt.clf()
  #   plt.imshow(filled_raster, cmap='viridis')  # You can adjust the colormap as needed
  #   plt.colorbar(label="Elevation (m)")  # Add a color bar for reference
  #   plt.title(f"PIG Elevation for Year {year}")

  #   # Save the figure as a PNG with the specified DPI and tight bounding box
  #   plt.savefig(f"Output_Images/PIG{year}.png", dpi=75, bbox_inches='tight')

  #############

  def reprojectLVIS(self, outEPSG):
    '''A method to reproject the geolocation data
    
    Parameters:

    Outputs:
      new CRS
    
    
    '''
    inProj=Proj("epsg:4326")
    outProj=Proj("epsg:"+str(outEPSG))
    self.long, self.lat=transform(inProj, outProj,self.lat,self.lon)

    

  ###########################################

  def readLVIS(self,filename,minX,minY,maxX,maxY,onlyBounds):
    '''
    Read LVIS data from file
    '''
    # open file for reading
    f=h5py.File(filename,'r')
    # determine how many bins
    self.nBins=f['RXWAVE'].shape[1]
    # read coordinates for subsetting
    lon0=np.array(f['LON0'])       # longitude of waveform top
    lat0=np.array(f['LAT0'])       # lattitude of waveform top
    lonN=np.array(f['LON'+str(self.nBins-1)]) # longitude of waveform bottom
    latN=np.array(f['LAT'+str(self.nBins-1)]) # lattitude of waveform bottom
    # find a single coordinate per footprint
    tempLon=(lon0+lonN)/2.0
    tempLat=(lat0+latN)/2.0

    # write out bounds and leave if needed
    if(onlyBounds):
      self.lon=tempLon
      self.lat=tempLat
      self.bounds=self.dumpBounds()
      return

    # dertermine which are in region of interest
    useInd=np.where((tempLon>=minX)&(tempLon<maxX)&(tempLat>=minY)&(tempLat<maxY))
    if(len(useInd)>0):
      useInd=useInd[0]

    if(len(useInd)==0):
      print("No data contained in that region")
      self.nWaves=0
      return

    # save the subset of all data
    self.nWaves=len(useInd)
    self.lon=tempLon[useInd]
    self.lat=tempLat[useInd]

    # load sliced arrays, to save RAM
    self.lfid=np.array(f['LFID'][useInd])          # LVIS flight ID number
    self.lShot=np.array(f['SHOTNUMBER'][useInd])   # the LVIS shot number, a label
    self.waves=np.array(f['RXWAVE'][useInd])       # the recieved waveforms. The data
    self.nBins=self.waves.shape[1]
    # these variables will be converted to easier variables
    self.lZN=np.array(f['Z'+str(self.nBins-1)][useInd])       # The elevation of the waveform bottom
    self.lZ0=np.array(f['Z0'][useInd])          # The elevation of the waveform top
    # close file
    f.close()
    # return to initialiser
    return


  ###########################################

  def setElevations(self):
    '''
    Decodes LVIS's RAM efficient elevation
    format and produces an array of
    elevations per waveform bin
    '''
    self.z=np.empty((self.nWaves,self.nBins))
    for i in range(0,self.nWaves):    # loop over waves
      self.z[i]=np.linspace(self.lZ0[i],self.lZN[i],self.nBins)   # returns an array of floats


  ###########################################

  def getOneWave(self,ind):
    '''
    Return a single waveform
    '''
    return(self.z[ind],self.waves[ind])


  ###########################################

  def dumpCoords(self):
     '''
     Dump coordinates
     '''
     return(self.lon,self.lat)

  ###########################################

  def dumpBounds(self):
     '''
     Dump bounds
     '''
     return[np.min(self.lon),np.min(self.lat),np.max(self.lon),np.max(self.lat)]  # this returns a list
                                                                                  # rather than a tuple ()

###########################################

