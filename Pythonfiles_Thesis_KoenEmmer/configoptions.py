# This file stores different standard configurations
# By Koen Emmer
import numpy as np
import math

def selectConfig(config):
    # STANDARDIZED PARAMETERS
    par = {
        # [MRGnode]
        # ENVIRONMENTAL PARAMETERS
        'celsius'		    :  37.0,    # Temperature
        'v_init'			: -80.0,    # Initial membrane voltage
        'axonnodes'			: 51,       # Amount of Nodes of Ranvier on the axon
        'fiberD'			: 10.0,     # Diameter of the axonfiber, choose from 5.7, 7.3, 8.7, 10.0, 11.5, 12.8, 14.0, 15.0, 16.0
        # SIMULATION PARAMETERS
        'dt'			    : 0.005,    # Simulation timestep (in ms)
        'tstop'				: 10,       # Total simulation time (in ms)
        # HFS PARAMETERS
        'HFSreferenceNode'  : 2,  # Node of Ranvier where KHFAC stimulation is applied
        'HFSamp'		    : 0.0,      # Amplitude of KHFAC waveform (mA)
        'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
        'HFSdelay'			: 5.0,      # Time when KHFAC waveform starts (ms)
        'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis
        'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis
        'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis
        'tonset'			: 10,		# Duration of onset response
        'bipolar'           :  0,       # Set to 1 for bipolar electrode
        # PARAMETERS FOR INTRACELLULAR STIMULUS
        'intrinsicStim'     : 0,  # Change to 1 to add intrinsic pulse(train)
    }

    if config=='singleAPdemo':
        # Create single AP
        par.update({
            # ENVIRONMENTAL PARAMETERS
            'celsius'		    :  37.0,    # Temperature
            'v_init'			: -80.0,    # Initial membrane voltage
            'axonnodes'			: 21,       # Amount of Nodes of Ranvier on the axon
            # SIMULATION PARAMETERS
            'tstop'				: 10,       # Total simulation time (in ms)
            # PARAMETERS FOR INTRACELLULAR STIMULUS
            'intrinsicStim'     : 1,        # Change to 1 to add intrinsic pulse(train)
            'intrinsicType'		: 0,        # 0 is single pulse, 1 is pulsetrain
            'intrinsicNode'		: 10.0,      # Node where intracellular stimulus starts
            'intrinsicAmp'		: 1.0,      # Amplitude of intracellular stimulus (nA)
            'intrinsicDel'		: 3.0,      # Time when intracellular stimulus starts (ms)
            'intrinsicDur'		: 1.0,      # Duration of intracellular stimulus (ms)           # ONLY SINGLE PULSE
            'intrinsicTON'		: 1.0,      # Duration of ON phase intracellular stimulus (ms)  # ONLY PULSE TRAIN
            'intrinsicTOFF'		: 1.0,      # Duration of OFF phase intracellular stimulus (ms) # ONLY PULSE TRAIN
            'intrinsicNum'		: None      # Number of intrinsic pulses (when doing a pulsetrain)
        })

    elif config=='HFSdemo':
        par.update({
            # [MRGnode]
            # ENVIRONMENTAL PARAMETERS
            'axonnodes'		: 51.0,     # Amount of Nodes of Ranvier on the axon
            # SIMULATION PARAMETERS
            'tstop'				: 20,       # Total simulation time (in ms)
            # HFS PARAMETERS
            'HFSreferenceNode'	: 25,       # Node of Ranvier where KHFAC stimulation is applied (First node is 0)
            'HFSamp'			: 1.0,      # Amplitude of KHFAC waveform (mA)
            'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
            'HFSdelay'			: 2.0,      # Time when KHFAC waveform starts (ms)
            'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis ()
            'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis ()
            'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis ()
        })

    elif config=="ClassicModel":
        par.update({
            # [MRGnode]
            # ENVIRONMENTAL PARAMETERS
            'axonnodes'		: 51.0,     # Amount of Nodes of Ranvier on the axon
            # SIMULATION PARAMETERS
            'tstop'				: 51,       # Total simulation time (in ms)
            'dt'			    : 0.001,    # Simulation timestep (in ms)
            # HFS PARAMETERS
            'HFSreferenceNode'	: 25,       # Node of Ranvier where KHFAC stimulation is applied (First node is 0)
            # 'HFSamp'			: 1.5,      # Amplitude of KHFAC waveform (mA)
            # 'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
            'HFSdelay'			: 0.0,      # Time when KHFAC waveform starts (ms)
            'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis (um)
            'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis (um)
            'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis (um)
            # PARAMETERS FOR INTRACELLULAR STIMULUS
            'intrinsicStim'		: 1,        # Change to 1 to add intrinsic pulse(train)
            'intrinsicType'		: 1,        # 0 is single pulse, 1 is pulsetrain
            'intrinsicNode'		: 0,        # Node where intracellular stimulus starts
            'intrinsicAmp'		: 2.0,      # Amplitude of intracellular stimulus (nA)
            'intrinsicDel'		: 10.0,      # Time when intracellular stimulus starts (ms)
            'intrinsicDur'		: 0.1,      # Duration of intracellular stimulus (ms)           # ONLY SINGLE PULSE
            'intrinsicTON'		: 0.5,      # Duration of ON phase intracellular stimulus (ms)  # ONLY PULSE TRAIN
            'intrinsicTOFF'		: 1.5,      # Duration of OFF phase intracellular stimulus (ms) # ONLY PULSE TRAIN
            'intrinsicNum'		: None      # Number of intrinsic pulses (when doing a pulsetrain)
        })
    elif config=="ClassicModel_Bipolar":
        par.update({
            # [MRGnode]
            # ENVIRONMENTAL PARAMETERS
            'axonnodes'		: 51.0,     # Amount of Nodes of Ranvier on the axon
            # SIMULATION PARAMETERS
            'tstop'				: 51,       # Total simulation time (in ms)
            'dt'			    : 0.001,    # Simulation timestep (in ms)
            # HFS PARAMETERS
            'HFSreferenceNode'	: 25,       # Node of Ranvier where KHFAC stimulation is applied (First node is 0)
            # 'HFSamp'			: 1.5,      # Amplitude of KHFAC waveform (mA)
            # 'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
            'HFSdelay'			: 0.0,      # Time when KHFAC waveform starts (ms)
            'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis (um)
            'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis (um)
            'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis (um)
            'bipolar'			: 1,  # Set to 1 for bipolar stimulation
            'HFSx2'				: 0.0,      # Location of the KHFAC electrode on the x-axis (um)
            'HFSy2'				: 0.0,      # Location of the KHFAC electrode on the y-axis (um)
            'HFSz2'			    : 1000.0,   # Location of the KHFAC electrode on the z-axis (um)
            # PARAMETERS FOR INTRACELLULAR STIMULUS
            'intrinsicStim'		: 1,        # Change to 1 to add intrinsic pulse(train)
            'intrinsicType'		: 1,        # 0 is single pulse, 1 is pulsetrain
            'intrinsicNode'		: 0,        # Node where intracellular stimulus starts
            'intrinsicAmp'		: 2.0,      # Amplitude of intracellular stimulus (nA)
            'intrinsicDel'		: 10.0,      # Time when intracellular stimulus starts (ms)
            'intrinsicDur'		: 0.1,      # Duration of intracellular stimulus (ms)           # ONLY SINGLE PULSE
            'intrinsicTON'		: 0.5,      # Duration of ON phase intracellular stimulus (ms)  # ONLY PULSE TRAIN
            'intrinsicTOFF'		: 1.5,      # Duration of OFF phase intracellular stimulus (ms) # ONLY PULSE TRAIN
            'intrinsicNum'		: None      # Number of intrinsic pulses (when doing a pulsetrain)
        })
    elif config=="ProposedModel":
        # Create simplified Model
        par.update({
            # [MRGnode]
            # ENVIRONMENTAL PARAMETERS
            'axonnodes'			: 5,       # Amount of Nodes of Ranvier on the axon (standard 5)
            # SIMULATION PARAMETERS
            'dt'				: 0.001,    # Simulation timestep (in ms)
            'tstop'				: 20.0,     # Total simulation time (in ms) (standard 2)
            # HFS PARAMETERS
            # 'HFSamp'			: 0.5,      # Amplitude of KHFAC waveform (mA)
            # 'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
            'HFSdelay'			: 0.0,      # Time when KHFAC waveform starts (ms)
            'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis ()
            'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis ()
            'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis ()
            'tonset'			: 18,		# Duration of onset response (standard 2)
        })
    elif config == "ProposedModel_Bipolar":
        # Create simplified Model
        par.update({
            # [MRGnode]
            # ENVIRONMENTAL PARAMETERS
            'axonnodes'		: 5,       # Amount of Nodes of Ranvier on the axon (standard 5)
            # SIMULATION PARAMETERS
            'dt'				: 0.001,    # Simulation timestep (in ms)
            'tstop'				: 20.0,     # Total simulation time (in ms) (standard 2)
            # HFS PARAMETERS
            # 'HFSamp'			: 0.5,      # Amplitude of KHFAC waveform (mA)
            # 'HFSfrequency'		: 10.0,     # Frequency of KHFAC waveform (kHz)
            'HFSdelay'			: 0.0,      # Time when KHFAC waveform starts (ms)
            'HFSx'				: 0.0,      # Location of the KHFAC electrode on the x-axis ()
            'HFSy'				: 0.0,      # Location of the KHFAC electrode on the y-axis ()
            'HFSz'				: 1000.0,   # Location of the KHFAC electrode on the z-axis ()
            'tonset'			: 18,		# Duration of onset response (standard 2)
            'bipolar'           : 1,        # Set to 1 for bipolar stimulation
            'HFSx2'				: 0.0,      # Location of the KHFAC electrode on the x-axis
            'HFSy2'				: 0.0,      # Location of the KHFAC electrode on the y-axis
            'HFSz2'			    : 1000.0,   # Location of the KHFAC electrode on the z-axis ()
        })
        par['HFSreferenceNode'] = int(math.floor(par['axonnodes']/2))  # Node of Ranvier where KHFAC stimulation is applied (first node = 0)


    if par['intrinsicStim'] == 1:
        par['intrinsicNum'] = int(par['tstop'] / (par['intrinsicTON'] + par['intrinsicTOFF']))

    recpar = {  # Parameters used for recording
        # 'record'			: True,
        # 'plot'				: False,
        'nodes'			    : np.array(range(0, int(par['axonnodes']))  ), # Nodes that are to be recorded
        'recordVoltage'		: True,     # Switch to allow recording of voltages
    }

    return par, recpar
