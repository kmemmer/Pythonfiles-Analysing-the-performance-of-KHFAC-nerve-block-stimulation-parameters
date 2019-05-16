##############################################################
##############################################################
# Pythoncode containing Neuron-vector descriptions of waveforms
##############################################################
##############################################################
import numpy as np
import matplotlib.pyplot as plt

##############################################################
# Transforms a standard waveform into a signal that is ready to be used by Neuron
# t_start is when the signal should start
# t_stop is when the signal should end
# t_period is the time vector of the signal
# i_period is the current amplitude vector of the signal
# f is the frequency of the signal
# amplitude is the amplitude of the signal
# The outputs are:
# t_signal: the time vector of the signal
# i_signal: the amplitude vector of the signal
# Neuron combines the two to construct a signal,
# build up by having amplitude i_signal[x] at time t_signal[x]
##############################################################
def KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude):
    f = 1000*f # Translate from KHz to Hz
    period = 1000.0/f #in milliseconds
    t_period = [x * period/max(t_period) for x in t_period] #Neuron t is in ms
    i_period = [x * amplitude for x in i_period]
    timestep = max(t_period)
    t_signal = []
    i_signal = []
    for i in range(0, int(t_stop/period)):
        t_signal = np.concatenate((t_signal, t_period))
        t_period = [x + timestep for x in t_period]
        if i < int(t_start/period):
            i_signal = np.concatenate((i_signal, [x * 0 for x in i_period]))
        else:
            i_signal = np.concatenate((i_signal, i_period))
    return t_signal, i_signal


##############################################################
# Creates a sampled sinewave-period for Neuron, consisting of:
# t_period: the time vector of one period
# i_period: the amplitude vector of one period
##############################################################
def sinewaveperiod(samplesperperiod):
    t_period = []
    i_period = []
    for i in range(0, samplesperperiod+1):
        t_period = np.concatenate((t_period, i), axis=None)
        i_period = np.concatenate((i_period, np.sin(2*np.pi*i/samplesperperiod)), axis=None)
    return t_period, i_period


##############################################################
# Creates a sampled sinewave signal for Neuron
##############################################################
def sinewave(t_start, t_stop, f, amplitude, samplesperperiod):
    t_period, i_period = sinewaveperiod(samplesperperiod)
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)


##############################################################
# Creates a sampled triangle wave signal for Neuron
##############################################################
def trianglewave(t_start, t_stop, f, amplitude):
    t_period = [0, 1, 2, 3, 4]
    i_period = [0, 1, 0, -1, 0]
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)


##############################################################
# Creates a sampled square wave signal for Neuron
# ipd1 and ipd2 represent interphase delays, as a fraction of the waveform period (e.g. ipd1=0.1 will create an interphase delay of one tenth of the signal period after the anodal pulse
##############################################################
def squarewave(t_start, t_stop, f, amplitude, ipd1 = 0, ipd2 = 0):
    period_length = 1.0
    no_ipd_length = period_length - ipd1 - ipd2
    t_period = [0, no_ipd_length / 2, no_ipd_length / 2, no_ipd_length / 2 + ipd1, no_ipd_length / 2 + ipd1, no_ipd_length + ipd1, no_ipd_length + ipd1, period_length]
    i_period = [1, 1, 0, 0, -1, -1, 0, 0]
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)


##############################################################
# Creates a sampled charge balanced asymmetrical square wave for Neuron
# chargeperphase in uC
# f in kHz
# t_start & t_stop in ms
##############################################################
def chargebalanced_asymmetrical(t_start, t_stop, f, chargeperphase, ratioHi, ipd1 = 0, ipd2 = 0):
    ratioLo = 1.0-ratioHi
    period = 1.0
    no_ipd_length = period - ipd1 - ipd2
    T_anodal = no_ipd_length * ratioHi                 # period of anodal (positive) stimulation phase
    T_cathodal = no_ipd_length * ratioLo               # period of cathodal (negative) stimulation phase
    A_anodal = 1.0                                     # Anodal pulse is reference amplitude
    A_cathodal = -1* A_anodal*T_anodal/T_cathodal      # Cathodal pulse scaled to match reference amplitude
    amplitude = f * chargeperphase / ratioHi    # Real amplitude of anodal pulse is calculated as multiplication
    t_period = [0, T_anodal, T_anodal, T_anodal + ipd1, T_anodal + ipd1, T_anodal + ipd1 + T_cathodal, T_anodal + ipd1 + T_cathodal,  T_anodal + ipd1 + T_cathodal + ipd2]
    i_period = [A_anodal, A_anodal, 0, 0, A_cathodal, A_cathodal, 0, 0]
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)


##############################################################
# Creates a sampled square wave signal with interphase delays for Neuron
# ##############################################################
# def squarewave_ip(t_start, t_stop, f, amplitude, ipd1, ipd2):
#     period_length = 1.0
#     no_ipd_length = period_length-ipd1-ipd2
#     t_period = [0, no_ipd_length/2, no_ipd_length/2, no_ipd_length/2+ipd1, no_ipd_length/2+ipd1, no_ipd_length+ipd1, no_ipd_length+ipd1, period_length]
#     i_period = [1, 1, 0, 0, -1, -1, 0, 0]
#     return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)


##############################################################
# Creates a stepwave for Neuron, consisting of:
# t_period: the time vector of one period
# i_period: the amplitude vector of one period
##############################################################
def stepwave(t_start, t_stop, f, amplitude, steps_per_quartercycle): #Trianglewave
    t_period = [0]
    i_period = [0]
    step_increment = 1.0/steps_per_quartercycle
    for i in range(0, steps_per_quartercycle*4):
        t_period = np.concatenate((t_period, [i,i+1]), axis=None)
        i_period = np.concatenate((i_period, [i_period[-1] + step_increment, i_period[-1] + step_increment]), axis = None)
        if abs(abs(i_period[-1]) - 1.0) <= 1.0/100000000:
            step_increment *= -1
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)

def stepwave_sine(t_start, t_stop, f, amplitude, steps_per_quartercycle): #Sineshape
    t_period = [0]
    i_period = [0]
    for i in range(0, steps_per_quartercycle*4):
        t_period = np.concatenate((t_period, [i,i+1]), axis=None)
        i_period = np.concatenate((i_period, [np.sin(2*np.pi*i/(steps_per_quartercycle*4)), np.sin(2*np.pi*i/(steps_per_quartercycle*4))]), axis = None)
    return KHFACblocksignal(t_start, t_stop, t_period, i_period, f, amplitude)