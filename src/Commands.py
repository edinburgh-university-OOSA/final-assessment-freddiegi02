  
import argparse


def getCmdArgs():
    '''
    Get commandline arguments
    '''
    # Create an argparse paser object with a description
    ap = argparse.ArgumentParser(description=("An illustration of a command line parser"))
    # Add a positional argument for the input filename (string)
    ap.add_argument("--filename",type=str,help=("Input filename"))
    # Add a positional argument for the resolution (integer)
    ap.add_argument("--res", type=int,help=("Spec Res"))
    # Add a postioal argument to specify the year of the data
    ap.add_argument('--year', type=str,help=("2009 or 2015"))
    ap.add_argument("--waveform",type=int,help=("Input Number"))
    ap.add_argument("--folder",type=str,help=("Input folder"))
    # Parse command-line arguments
    args = ap.parse_args()
    # return that object from this function
    return args


def norm_lon(lon):
    """
    SFixes negetive CRS issues
    
    Paramters:
      lon (float): Longitide Value

    Returns:
      float: Normalised longitude within the range of 0-360 degrees"
      """
    return (lon) % 360 #Normalise longitude to ensure it stays within a valid range (0-360 degrees)


