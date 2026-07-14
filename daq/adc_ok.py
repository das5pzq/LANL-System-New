import numpy as np

def check_adc(data, is_pedastal_okay):
    vmax = np.max(data)
    vmin = np.min(data)

    vlim = 4.9

    ### maxmimum design voltage seems to b 5V, lanl uses ceiling of 4.9V for checking

    if not (vmax < vlim and vmin > -vlim) or is_pedastal_okay:
        return True #### ADC is OK
    else:
        return False #### ADC is not OK