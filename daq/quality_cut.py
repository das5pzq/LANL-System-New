import numpy as np
from scipy.stats import sigmaclip


def cut(data, quality_cut_bool):
    if not quality_cut_bool:
        return data
    
    return sigmaclip(data, low=2.5, high=2.5)


import numpy as np

def threshold_1d_array(y_array, threshold):
    ### lanl's vi uses fractional indices to cut data???? why????
    ### we just use cut() above to explicity apply sigma cuts
    indices = np.arange(len(y_array))
    
    # Calculate fractional index by inverting the lookup
    fractional_index = np.interp(threshold, y_array, indices)
    
    return fractional_index
