import numpy as np
import nidaqmx as ni
from nidaqmx.constants import AcquisitionType, TerminalConfiguration, Signal
import time
import pyvisa  



system = ni.system.System.local()

def generate_waveform(steps_up_down, amplitude, offset, waveform_type='triangle'):
    """
    Generate waveform for frequency sweep.
    
    Parameters:
    -----------
    steps_up_down : int
        Number of steps in each direction (up/down) - will generate +1 extra to account for DC offset
    amplitude : float
        Peak-to-peak amplitude of the waveform
    offset : float
        DC offset of the waveform
    waveform_type : str
        Type of waveform: 'triangle', 'sine', or 'sawtooth'
    
    Returns:
    --------
    numpy.ndarray
        Generated waveform (with extra step at start to be discarded during acquisition)
    """
    if waveform_type.lower() == 'triangle':
        # Triangle wave: linear ramp up then linear ramp down
        # Generate +1 extra step in each direction to compensate for DC offset at start
        up_scan = np.linspace(0, 1, steps_up_down + 1, endpoint=False)
        down_scan = np.linspace(1, 0, steps_up_down + 1, endpoint=False)
        waveform = np.concatenate([up_scan, down_scan])
        waveform = amplitude * (waveform - 0.5) + offset
        
    elif waveform_type.lower() == 'sine':
        # Sine wave: smooth periodic oscillation
        # Generate +1 extra step to compensate for DC offset at start
        total_steps = (steps_up_down + 1) * 2
        t = np.linspace(0, 2*np.pi, total_steps, endpoint=False)
        waveform = amplitude * 0.5 * np.sin(t - np.pi/2) + offset
        
    elif waveform_type.lower() == 'sawtooth':
        # Sawtooth wave: linear ramp up, sharp drop
        # Generate +1 extra step to compensate for DC offset at start
        waveform = np.linspace(0, 1, steps_up_down + 1, endpoint=False)
        waveform = amplitude * (waveform - 0.5) + offset
        
    else:
        raise ValueError(f"Unknown waveform type: {waveform_type}. Must be 'triangle', 'sine', or 'sawtooth'")
    
    return waveform

def configure_rf_generator(instrument, center_freq_mhz, fm_deviation_khz, power_mv):
    """Configure RF generator for external FM modulation."""
    if instrument is None:
        return False
    
    try:
        print("\nConfiguring RF generator...")
        
        # Set center frequency
        instrument.write(f":SOURCE:FREQUENCY:CW {center_freq_mhz:.3f}MHz")
        print(f"  Center frequency: {center_freq_mhz} MHz")
        
        instrument.write(":SOURCE:FM1:SOURCE EXT1")
        instrument.write(f":SOURCE:FM1:DEVIATION {fm_deviation_khz}kHz")
        instrument.write(":SOURCE:FM1:EXTERNAL1:COUPLING DC")
        instrument.write(":SOURCE:FM1:STATE ON")
        instrument.write(":SOURCE:FM2:STATE OFF")
        print(f"  FM deviation: ±{fm_deviation_khz} kHz")
        print(f"  FM source: External (EXT1)")
        
        instrument.write(f":SOURCE:POWER:LEVEL:IMMEDIATE:AMPLITUDE {power_mv}mV")
        print(f"  Power level: {power_mv} mV")
        
        try:
            instrument.write(":OUTPUT:STATE ON")
        except:
            instrument.write(":OUTPUT ON")
        print(f"  RF output: ON")
        
        return True
        
    except Exception as e:
        print(f"Error configuring RF generator: {e}")
        return False

def sweep(
    device_name="Dev3",
    num_sweeps=100,
    scan_freq=1000.0,
    steps_up_down=500,
    amplitude=1.0,
    offset=0.0,
    ao_channel="ao0",
    ai_channel="ai1",
    rf_generator_resource="GPIB0::28::INSTR",
    rf_center_freq_mhz=213.0,
    rf_fm_deviation_khz=400,
    rf_power_mv=200,
    waveform_type='triangle',
):
    
    # Generate the selected waveform to send to RF generator FM input
    waveform = generate_waveform(steps_up_down, amplitude, offset, waveform_type=waveform_type)
    
    # Total steps for waveform (structure depends on waveform type)
    if waveform_type.lower() == 'triangle' or waveform_type.lower() == 'sine':
        total_steps_with_offset = (steps_up_down + 1) * 2
        total_steps = steps_up_down * 2  # Actual steps after removing first sample
    elif waveform_type.lower() == 'sawtooth':
        total_steps_with_offset = steps_up_down + 1
        total_steps = steps_up_down

    total_samples = num_sweeps * total_steps_with_offset
    waveform_all_sweeps = np.tile(waveform, num_sweeps)


    
    step_period = 1.0 / scan_freq

    rm = pyvisa.ResourceManager()
    rf_instrument = rm.open_resource(rf_generator_resource)
    rf_instrument.timeout = 5000

    configure_rf_generator(rf_instrument, rf_center_freq_mhz, rf_fm_deviation_khz, rf_power_mv)

    acquired_data = None

    ### Need to look at LANL system for here and see how stuff is routed

    ### Add in clock synchronization here between RF generator and DAQ/ADC system