from dataclasses import dataclass
from enum import StrEnum

@dataclass
class Config:

    ### RF Generator + IF Settings
    center_freq: float = 213 # MHz
    freq_span: float = 0.8 
    step_width: float = 0.02
    tank_rf: bool = False
    if_attenuation: float = 7.0 #dB
    rf_okay: bool = True



    ### DAC Settings

    tune_mode: StrEnum = StrEnum("Operating", "Phase", "Diode")

    tune_voltage: float = 0.1850 # V
    phase_voltage: float = 2.5660 # V

    log_offset: float = 0.0 # V
    if_offset: float = 4.4757 # V

    ### implement later, but check rf bool if if offset > 7.5 V
    if if_offset < 7.5:
        rf_okay = False
    else:
        rf_okay = True

    if_log_digitizer: bool = False

    ### ADC Settings

    sample_per_step: int = 20

    invert_polarity: bool = False

    gain: StrEnum = StrEnum("MAX", "HIGH", "LOW")

    ### Data Analysis

    num_sweeps: int = 500
    quality_cuts: bool = True
    autotune: bool = False
    remove_pedestals: bool = True
    gaussian_fit: bool = True
    subtract_qcurve: bool = True
    qcurve_amplitude: float = 0.8
    autofreq: bool = False

    calibration_constant: float = 1.0

    ### Save data

    save_data: bool = True
    save_folder: str = "data.csv"
    
    def set_tune(self, mode, *args):
        if mode == "Operating":
            self.invert_polarity = True
            self.if_log_digitizer = False
            self.autotune = True
            self.gain = "HIGH"
        elif mode == "Phase":
            self.phase_voltage = args[0]
            self.invert_polarity = True
            self.if_log_digitizer = False
            self.autotune = False
            self.gain = "LOW"
        elif mode == "Diode":
            self.tune_voltage = args[0]
            self.invert_polarity = False
            self.if_log_digitizer = True
            self.autotune = False
            self.gain = "LOW"


