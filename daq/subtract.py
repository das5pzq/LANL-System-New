import numpy as np

def pedastals(data):
    left_max = 0.3
    right_max = 0.7
    left_index = np.argmax(data[:left_max])
    right_index = np.argmax(data[right_max:]) + right_max
    left_baseline = np.mean(data[:left_index])
    right_baseline = np.mean(data[right_index:])
    pedastals = left_baseline - right_baseline
    ped_offset = (left_baseline + right_baseline) / 2
    return pedastals, ped_offset #### what the hell is this??????

def subtract(data, qcurve, invert_polarity, if_log_delay, substract_pedastals):
    if invert_polarity or if_log_delay: 
        data += qcurve
    else:
        data -= qcurve
    if substract_pedastals:
        pedastals, ped_offset = pedastals(data)
        data -= ped_offset
    return data