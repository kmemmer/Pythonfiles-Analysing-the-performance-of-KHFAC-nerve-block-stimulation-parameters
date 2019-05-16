# Import Python libraries
import pylab as plt
import numpy as np
# Import for BrainFrame
import matplotlib
# Import custom function libraries
from MRG_Model import *             # Interface with Neuron MRG Model
from configoptions import *
from waveforms import *             # Waveform functions for Neuron
from plottingfunctions import *     # Plotting functions
from plottingfunctions_justification import *
from blockdetection import *
if not os.path.exists('reportplots'):
    os.makedirs('reportplots')
if not os.path.exists('reportplots/background'):
    os.makedirs('reportplots/background')
if not os.path.exists('reportplots/method'):
    os.makedirs('reportplots/method')
if not os.path.exists('reportplots/implementation'):
    os.makedirs('reportplots/implementation')
import time
from matplotlib.pyplot import figure

plt.rcParams.update({'font.size': 12})

##############################################################
# PLOT 'JUSTIFICATION OF MODEL' PLOTS
##############################################################
def justificationplots(select):
    if(select == "square"):
        result_classic = np.load("justification_files/results_squarewave_classicmethod.npy", encoding="ASCII").item()
        result_proposed = np.load("justification_files/results_squarewave_proposedmethod.npy", encoding="ASCII").item()
        plotjustification2D(result_classic, result_proposed)
        plt.show()
    elif(select == "sine"):
        result_classic = np.load("justification_files/results_sinewave_classicmethod.npy", encoding="ASCII").item()
        result_proposed = np.load("justification_files/results_sinewave_proposedmethod20190226_171930.npy", encoding="ASCII").item()
        plotjustification2Dcpp(result_classic, result_proposed)
        plt.savefig("reportplots/method/performance_sine_cpp.eps", format='eps', dpi=300)
        plt.show()
        plotjustification2D(result_classic, result_proposed)
        plt.savefig("reportplots/method/performance_sine.eps", format='eps', dpi=300)
        plt.show()
    elif(select == "squareCB"):
        result_classic = np.load("justification_files/results_squarewave_CB_classicmethod.npy", encoding="ASCII").item()
        result_proposed = np.load("justification_files/results_squarewave_CB_proposedmethod.npy", encoding="ASCII").item()
        # result_proposed = np.load("results_monopolar/results_monopolar_assymmetricalwave_allfrequencies.npy").item()
        plotjustification3Dcpp(result_classic, result_proposed, "singleCB", 0.1)#, freqname = "frequency", chargename = "chargeperphase")#"subplots")
        plt.show()
        plotjustification3Dcpp(result_classic, result_proposed, "singleCB", 0.5)#, freqname = "frequency", chargename = "chargeperphase")
        plt.show()
        plotjustification3Dcpp(result_classic, result_proposed, "singleCB", 0.8)#, freqname = "frequency", chargename = "chargeperphase")
        plt.show()
        plotjustification3Dcpp(result_classic, result_proposed, "singleCB", 0.9)#, freqname = "frequency", chargename = "chargeperphase")
        plt.show()
    else:
        print "Type non-existent!"


##########################################################
# VISUALIZATION OF SINGLE SIMULATION 2D
##########################################################
def plotsquareWave():
    return None
#     t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], 4, 0.5)
#     runandplotsignal(par, recpar, t_signal, i_signal, config)


##########################################################
# DEMO SINGLE SIMULATION TIME-SPATIAL
##########################################################
def plot_square_classic(f = 10, a = 0.47, tstop = 40.0, intrinsic = 0):
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency']    = f    # kHz
    par['HFSamp']          = a  # mA
    par['tstop'] = tstop
    if intrinsic == 0:
        par['intrinsicStim'] = 0
    else:
        par['intrinsicStim'] = 1
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_sine_classic(f = 10, a = 0.47, tstop = 40.0, intrinsic = 0):
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency']    = f    # kHz
    par['HFSamp']          = a  # mA
    par['tstop'] = tstop
    if intrinsic == 0:
        par['intrinsicStim'] = 0
    else:
        par['intrinsicStim'] = 1
    HFSsamplesize   = 1000  # Number of samples per period
    t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], HFSsamplesize)
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_assymmetric_classic(f = 10, a = 0.47, tstop = 40.0, chargebalance=0.5, intrinsic = 0):
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency'] = f  # kHz
    par['HFSamp'] = a  # mA
    par['tstop'] = tstop
    if intrinsic == 0:
        par['intrinsicStim'] = 0
    else:
        par['intrinsicStim'] = 1
    chargeperphase = par['HFSamp'] / (2 * par['HFSfrequency'])
    t_signal, i_signal = chargebalanced_asymmetrical(par['HFSdelay'], par['tstop'], par['HFSfrequency'], chargeperphase, chargebalance)
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_square_proposed(f, a):
    config = "ProposedModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency']    = f    # kHz
    par['HFSamp']          = a  # mA
    par['tstop'] = 20.0
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_sine_proposed(f,a):
    config = "ProposedModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency']    = f    # kHz
    par['HFSamp']          = a  # mA
    par['tstop'] = 20.0
    HFSsamplesize   = 1000  # Number of samples per period
    t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], HFSsamplesize)
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_assymmetric_proposed(f, a, chargebalance):
    config = "ProposedModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency'] = f  # kHz
    par['HFSamp'] = a  # mA
    par['tstop'] = 20.0
    chargeperphase = par['HFSamp'] / (2 * par['HFSfrequency'])
    t_signal, i_signal = chargebalanced_asymmetrical(par['HFSdelay'], par['tstop'], par['HFSfrequency'], chargeperphase, chargebalance)
    runandplotsignal(par, recpar, t_signal, i_signal, config)


def plot_square_proposed_bipolar(f, a):
    config = "ProposedModel_Bipolar"
    par, recpar = selectConfig(config)
    par['HFSfrequency']    = f    # kHz
    par['HFSamp']          = a  # mA
    par['tstop'] = 20.0
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
    runandplotsignal(par, recpar, t_signal, i_signal, config)


##########################################################
# BACKGROUND CHAPTER
##########################################################
def plotAP():
    config = "singleAPdemo"
    par, recpar = selectConfig(config)
    a = 0
    par['HFSreferenceNode'] = 2.0
    par['HFSamp'] = a
    par['tstop'] = 150.0
    par['dt'] = 0.005
    t_signal, i_signal = [0],[0]
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    plotMRGgatessinglenodeAP(plt, rec, 10)
    plt.savefig("reportplots/background/normalAP.eps", format='eps', dpi=1200)
    plt.show()

    par['tstop'] = 10.0
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    plotMRGgatessinglenodeAP(plt, rec, 10)
    plt.savefig("reportplots/background/normalAP_zoom.eps", format='eps', dpi=1200)
    plt.show()


def plotKHFACdemogates():
    config = "HFSdemo"
    par, recpar = selectConfig(config)
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    plotMRGgatessingletime(plt,rec,20)
    plt.savefig("reportplots/background/HFSexample_gatesallnodes_T20ms.eps", format='eps', dpi=1200)
    plt.show()
    plotMRGgatessinglenode(plt,rec,26)
    plt.savefig("reportplots/background/HFSexample_virtualanodes.eps", format='eps', dpi=1200)
    plt.show()
    plotMRGgatessinglenode(plt, rec, 10)
    plt.savefig("reportplots/background/HFSexample_onsetresponse.eps", format='eps', dpi=1200)
    plt.show()


def plothminftau():
    Vm = np.arange(-150,50,1)
    Vm = np.delete(Vm, np.where(Vm == -114))
    alpha_h = [(0.34 * (-(v + 114))) / (1.0 - np.exp((v + 114) / 11.0)) for v in Vm]
    beta_h = [12.6 / (1.0 + np.exp(-(v + 31.8) / 13.4)) for v in Vm]
    print alpha_h
    h_inf = [a / (a + b) for a,b in zip(alpha_h, beta_h)]
    tau_h = [1.0 / (a + b) for a,b in zip(alpha_h, beta_h)]

    alpha_m = [(6.57 * (v + 20.4)) / (1 - np.exp(-(v + 20.4) / 10.3)) for v in Vm]
    beta_m = [(0.304 * (-(v + 25.7))) / (1 - np.exp((v + 25.7) / 9.16)) for v in Vm]
    m_inf = [a / (a + b) for a,b in zip(alpha_m, beta_m)]
    tau_m = [1.0 / (a + b) for a,b in zip(alpha_m, beta_m)]

    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=[15,5])
    plt.plot(Vm, h_inf, label='$h_\infty$')
    plt.plot(Vm, m_inf, label='$m_\infty$')
    plt.ylabel('State value')
    plt.xlabel('Membrane voltage (mV)')
    plt.legend()
    plt.xlim(-150,50)
    plt.xticks(np.arange(-150,60,20))
    plt.grid()
    plt.tight_layout()
    plt.savefig("reportplots/background/vm_gatevaluedependence_infty.eps", format='eps', dpi=1200)
    plt.show()

    plt.figure(figsize=[15, 5])
    plt.plot(Vm, tau_h, label='$\\tau_h$')
    plt.plot(Vm, tau_m, label='$\\tau_m$')
    plt.ylabel('Time constant (ms)')
    plt.xlabel('Membrane voltage (mV)')
    plt.legend()
    plt.xlim(-150, 50)
    plt.yticks(np.arange(0,1.2,0.2))
    plt.xticks(np.arange(-150, 60, 20))
    plt.grid()
    plt.tight_layout()
    plt.savefig("reportplots/background/vm_gatevaluedependence_tau.eps", format='eps', dpi=1200)
    plt.show()


##########################################################
# CHAPTER DETERMINING THE EFFECTIVENESS OF A BLOCK
##########################################################
def plot_2D_blockdescription():
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    f = 10
    a = 0.6
    HFSsamplesize = 1000
    par['HFSfrequency'] = f  # kHz
    par['HFSamp'] = a  # mA
    par['tstop'] = 20.0
    par['intrinsicDel'] = 15.0
    par['intrinsicDur'] = 0.1
    par['intrinsicType'] = 0
    t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], HFSsamplesize)
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    # plotMRGaxon(rec)
    dt = par['dt']
    t = [15.0, 15.2, 15.4, 15.6, 15.8, 16.0]
    for i in t:
        figure(num=None, figsize=(15, 3), dpi=1200, facecolor='w', edgecolor='k')
        plotnodeVoltagessingletime(rec, int(i/dt), plt)
        plt.tight_layout()
        plt.savefig("reportplots/method/KHFACdemo_" + str(i) + ".eps", format='eps', dpi=1200)
    return plt


def plot_3D_blockdescription():
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    f = 20
    HFSsamplesize = 1000
    par['HFSfrequency'] = f  # kHz
    par['tstop'] = 40.0
    par['intrinsicDel'] = 20.0

    a = [0.53, 0.6]
    intrinsictype = [0, 1]
    createMRGaxon(par)
    for i in intrinsictype:
        for j in a:
            par['intrinsicType'] = i
            par['HFSamp'] = j  # mA
            t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], HFSsamplesize)
            rec = recordMRGaxon(recpar)
            updateMRGaxon(par)
            runMRGaxon(rec, t_signal, i_signal)
            fig = plotMRGaxon(rec)
            plt.tight_layout()
            plt.savefig("reportplots/method/KHFACdemo3D_pulse_" + str(i) + "_amp_" + str(j) + ".eps", format='eps', dpi=1200)
    return plt


def plot_gates_proposedmethodsetup():
    config = "ProposedModel"
    par, recpar = selectConfig(config)
    f = 10
    a = 0.6
    HFSsamplesize = 1000
    par['HFSfrequency'] = f  # kHz
    par['HFSamp'] = a  # mA
    t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], HFSsamplesize)
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    # plotMRGaxon(rec)
    plotMRGgatessinglenode(plt, rec, par['HFSreferenceNode'] + 1, s=False)
    plt.savefig("reportplots/method/proposedsetupsimulation_virtualanode.eps", format='eps', dpi=1200)
    plt.show()
    return plt


def plot_asymmetrical_waveform():
    t_start = 0.0
    f = 10
    a = 1.0
    t_stop = 1.0/f
    chargebalance = [0.2, 0.5, 0.8]
    cpp = a/(2*f)
    for i in chargebalance:
        t_signal = [0]
        i_signal = [0]
        t_result, i_result = chargebalanced_asymmetrical(t_start, t_stop, f, cpp, i)
        t_signal.extend(t_result.tolist())
        t_signal.append(max(t_result))
        i_signal.extend(i_result.tolist())
        i_signal.append(0)
        plt.plot(t_signal, i_signal, label=i, linewidth=3)
        # plot_signal(plt, t_signal, i_signal, label = i)
    # plt.axhline(color='k', lw=1.0)
    plt.xlabel('Time (ms)')
    plt.ylabel('Current (mA)')
    plt.ylim(-3,3)
    plt.yticks(np.arange(-3.0,3.5,0.5))
    plt.grid()
    plt.legend(title="Anode fraction")
    plt.tight_layout()
    plt.savefig("reportplots/method/asymmetrical_waveform.eps", format='eps', dpi=300)
    plt.show()
    return plt


##########################################################
# RESULTS CHAPTER EXTRA PLOTS
##########################################################
def plot_ipdbasicimplementation(ipd1,ipd2):
    t_start = 0.0
    f = 10
    a = 1.0
    t_stop = 1.0/f
    t_result, i_result = squarewave(t_start, t_stop, f, a, ipd1, ipd2)
    t_signal = [0]
    i_signal = [0]
    t_signal.extend(t_result.tolist())
    t_signal.append(max(t_result))
    i_signal.extend(i_result.tolist())
    i_signal.append(0)
    plt.xlabel('Time (ms)')
    plt.ylabel('Current (mA)')
    plt.xticks(np.arange(0,0.11,0.01))
    plt.title("Frequency = 10 kHz")
    plt.grid()
    plt.xlim(-0.01,0.11)
    plt.plot(t_signal, i_signal, linewidth=3, color="C0")
    plt.tight_layout()
    plt.savefig("reportplots/ipdbasic_"+str(ipd1)+"_"+str(ipd2)+".eps", format='eps', dpi=300)
    plt.show()


def plot_ipdcompleximplementation():
    t_start = 0.0
    f = 10
    a = 1.0
    t_stop = 1.0/f
    ipds = [[0.2,0.3],[0.4,0.1],[0.25,0.25]]
    plt.figure(figsize=(15,4))
    for i in range(0,len(ipds)):
        ipd1, ipd2 = ipds[i]
        t_signal = [0+i*t_stop]
        i_signal = [0]
        t_result, i_result = squarewave(t_start, t_stop, f, a, ipd1, ipd2)
        t_result = [x + i*t_stop for x in t_result]
        t_signal.extend(t_result)
        i_signal.extend(i_result.tolist())
        i_signal.append(0)
        t_signal.append(max(t_result))
        plt.plot(t_signal, i_signal, linewidth=3)
    plt.xlabel('Time (ms)')
    plt.ylabel('Current (mA)')
    plt.xticks(np.arange(0,0.31,0.02))
    plt.xlim(-0.01,0.31)
    plt.title("Frequency = 10 kHz")
    plt.grid()
    plt.tight_layout()
    plt.savefig("reportplots/ipdcomplex.eps", format='eps', dpi=300)
    plt.show()


def plot_asymmetrical_bipolar(cpp):
    # par, recpar = selectConfig("ClassicModel")
    par,recpar = selectConfig("ClassicModel_Bipolar")
    par['tstop'] = 20.0
    par['intrinsicStim'] = 0
    par['HFSy2'] = 2200
    t_signal, i_signal = chargebalanced_asymmetrical(par['HFSdelay'], par['tstop'], par['HFSfrequency'], cpp, 0.7)
    # plot_signal(plt,t_signal, i_signal)
    # plt.show()
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    fig = plotMRGaxon(rec)
    plt.show()


def plot_ipd_validation(amp, ipd1,ipd2):
    par, recpar = selectConfig("ClassicModel")
    par['tstop'] = 20.0
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], amp, ipd1, ipd2)
    # plot_signal(plt,t_signal, i_signal)
    # plt.show()
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)
    fig = plotMRGaxon(rec)
    plt.tight_layout()
    plt.show()

##########################################################
# RUN AND PLOT A SINGLE SIMULATION
##########################################################
def runandplotsignal(par, recpar, t_signal, i_signal, config):
    starttime = time.time()

    createMRGaxon(par)
    intervaltime = time.time() - starttime
    print("--- CREATEAXON: %s seconds ---" % (intervaltime))
    intervaltime = time.time()

    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    intervaltime = time.time() - intervaltime
    print("--- PREPAREAXON: %s seconds ---" % (intervaltime))
    intervaltime = time.time()


    runMRGaxon(rec, t_signal, i_signal)
    intervaltime = time.time() - intervaltime
    print("--- RUNAXON: %s seconds ---" % (intervaltime))
    intervaltime = time.time()

    fig = plotMRGaxon(rec)

    # plotMRGgatessingletime(plt, rec, int(par['tstop']/par['dt']))

    # Plot single AP
    if config=='singleAPdemo':
        plotMRGgatessinglenode(plt, rec, 4)


    # # Plot single KHFAC signal
    if config=='HFSdemo':
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']))
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']) + 1)
        # Onset response
        plotMRGgatessinglenode(plt, rec, int(par['axonnodes']-1))

    if config == 'ClassicModel':
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']))
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']) + 1)

    if config == 'ProposedModel' or config == 'ProposedModel_Bipolar':
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']))
        plotMRGgatessinglenode(plt, rec, int(par['HFSreferenceNode']) + 1)
        plotMRGgatessinglenode_timeframe(plt, rec, int(par['HFSreferenceNode']), 19/par['dt'])
        plotMRGgatessinglenode_timeframe(plt, rec, int(par['HFSreferenceNode']) + 1, 19/par['dt'])


    intervaltime = time.time() - intervaltime
    print("--- PLOT: %s seconds ---" % (intervaltime))
    plt.show()


##############################################################
# Parameters for configuration of the simulation
# ##############################################################
# # config = 'singleAPdemo'
# # config = 'HFSdemo'
# # config = 'HFSModel'
# config = 'ClassicModel'
# par, recpar = selectConfig(config)
# verbose = False
#
# t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], 1000)
# testandplotsignal(par, recpar, verbose, t_signal, i_signal, config)
#
# h.quit()


##############################################################
# Presentation plots
##############################################################
def buildKHFACgif():
    config = "ClassicModel"
    par, recpar = selectConfig(config)
    par['HFSfrequency'] = 10
    par ['HFSamp'] = 0.5
    par['tstop'] = 40
    par['intrinsicDel'] = 15.0
    t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
    createMRGaxon(par)
    rec = recordMRGaxon(recpar)
    updateMRGaxon(par)
    runMRGaxon(rec, t_signal, i_signal)

    dt = par['dt']
    tstart = int((par['HFSdelay'] + par['tonset']) / dt)

    for i in range(0, par['tstop'] * 10):
        t = i/10.0
        plt.figure()
        plotnodeVoltagessingletime(rec, int(t/dt), plt)
        filename = str(int(t*10))
        plt.savefig('figures/' + filename + '.png', bbox_inches='tight')
        plt.close()
