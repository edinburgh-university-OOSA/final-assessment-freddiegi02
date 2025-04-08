
from src.processLVIS import lvisGround #Importing lvisGround class from processLVIS
from matplotlib import pyplot as plt #Import for plotting
from src.Commands import getCmdArgs, norm_lon #Importing the command line arguments


##########################################


class plotLVIS(lvisGround):
  '''A class, ineriting from lvisData
     and add a plotting method'''


  def plotWave(self, i):
    """Plots the wavefrom for the given index
    
    Parameters:
      i (int): Index of the waveform to the plotted
    """

    # # Extract the waveform data
    wave_data = self.waves[i]
    
    # Find the first occurrence of zero and plot up to that point
    cutoff_index = len(wave_data)
    for j, value in enumerate(wave_data):
        if value == 0:
            cutoff_index = j
            break

    # Plot only up to the first zero
    plt.plot(wave_data[:cutoff_index], self.z[i][:cutoff_index])
    #plt.plot(self.waves[i], self.z[i]) #plot waveform return vs elevation 
    plt.xlabel("Waveform return") # X-axis label
    plt.ylabel("Elevation (m)") # Y-axis label
    plt.savefig("Output_Images/Waveform.png", dpi=75, bbox_inches='tight')
    plt.show() #Display the plot


##########################################


if __name__=="__main__":
  '''Main block'''
  
  args = getCmdArgs() #Get the command line arguments
  filename = args.filename   # Store the input filename 
  waveform = args.waveform   #Store the waveform index

  x0 = norm_lon(-102.00) # set min x coord
  y0 = -75.4 # set min y coord
  x1 = norm_lon(-99.00) #set max x coord
  y1 = -74.6 #set max y coord

  # read in all data within our spatial subset#
  lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1,setElev=True)

  try:
    #Plot the choosen waveform
    lvis.plotWave(waveform)
  except AttributeError as e:
    print("Try: /geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_061398.h5")
