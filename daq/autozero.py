import numpy as np

def autozero(vmin, if_offset, max_gain_bool, invert_polarity):
    if np.abs(vmin) > 0.01:
        return None

    prefactor = 0.001 if max_gain_bool else 0.01
    pedastal_offset = prefactor * vmin
    if invert_polarity:
        return if_offset + pedastal_offset
    else:
        return if_offset - pedastal_offset
