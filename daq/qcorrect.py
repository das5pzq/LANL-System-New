import numpy as np

def qcorrect(max_gain_bool, subtract_q_curve, amp, center_freq, step_width, nsteps):
    if not subtract_q_curve:
        ### make no correction to qcurve
        return np.zeros(nsteps)
    fmin = center_freq - step_width * (nsteps / 2)
    f = np.array([fmin + x * step_width for x in range(nsteps)])
    if max_gain_bool:
        return amp*(f-center_freq)**2
    else:
        return 0.1*amp*(f-center_freq)**2