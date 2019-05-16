##############################################################
# Bipolar simulation functions
##############################################################
import csv
from configoptions import *
import time
import datetime
from MRG_Model import *             # Interface with Neuron MRG Model
from blockdetection import *
from waveforms import *             # Waveform functions for Neuron
from plottingfunctions_results import *
# from simulationfunctions_proposedmodel import *


import os
if not os.path.exists('results_bipolar'):
    os.makedirs('results_bipolar')          # Ensure that brainframe makes justification folder
if not os.path.exists('reportplots'):
    os.makedirs('reportplots')
if not os.path.exists('reportplots/bipolar_results'):
    os.makedirs('reportplots/bipolar_results')

##############################################################
# Build dataset bipolar square wave simulation, changing electrode to axon distance and inter electrode contact distance
##############################################################
def bipolar_squarewave_ETAdistance_IECdistance_parallel_results(zoom=False): #ETA = Electrode To Axon, IEC = Inter Electrode Contact
    print("--- RUN BIPOLAR SIMULATION SQUAREWAVE WITH CHANGING ELECTRODE TO AXON DISTANCE AND INTER ELECTRODE CONTACT DISTANCE, ELECTRODE PARALLEL TO AXON ---")
    config = 'ProposedModel_Bipolar'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    perpdistance_list = []
    for i in range(1000, 6001, 500):
        perpdistance_list.append(i)

    poledistance_list = []
    count = {}
    if zoom:
        for i in range (1000, 10000, 100):
            poledistance_list.append(i)
    else:
        for i in range(1000, 60001, 1000):
            poledistance_list.append(i)
    for i in poledistance_list:
        count[i] = 0
    amplitudelist = []
    for i in range(200):
        amplitudelist.append(round(0.01 * i, 2))
    for i in range(280):
        amplitudelist.append(round(2.0 + 0.1 * i, 2))
    starttime = time.time()
    createMRGaxon(par)
    result = {}
    for ETAdist in perpdistance_list:
        result[ETAdist] = {}
        par['HFSz'] = ETAdist
        par['HFSz2'] = ETAdist
        for IECdist in poledistance_list:
            result[ETAdist][IECdist] = {}
            par['HFSy2'] = -IECdist
            for a in amplitudelist[count[IECdist]:]:
                rec = recordMRGaxon(recpar)
                par['HFSamp'] = a
                t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
                updateMRGaxon(par)
                print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s um el-to-ax distance, %s um interelectrodecontact distance) ---" % (frequency, a, ETAdist, IECdist))
                runMRGaxon(rec, t_signal, i_signal)
                if is_blocked(rec, par):
                    cpp = (1.0)/(2*(1000*frequency))*a
                    result[ETAdist][IECdist]["frequency"] = frequency
                    result[ETAdist][IECdist]["electrodetoaxondistance"] = ETAdist
                    result[ETAdist][IECdist]["interelectrodecontactdistance"] = IECdist
                    result[ETAdist][IECdist]["amplitude"] = a
                    result[ETAdist][IECdist]["chargeperphase"] = cpp
                    count[IECdist] = max(0, count[IECdist] - 10)
                    break
                count[IECdist] += 1
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename_end = ""
    if zoom:
        filename_end = "_zoom"
    filename = 'results_bipolar/results_squarewave_ETAdist_IECdist_parallel'+filename_end
    np.save(filename, result)


##############################################################
# Build dataset for square wave with interphase delay tested with Proposed Model
##############################################################
def bipolar_squarewave_IECdistance_results(mode): #ETA = Electrode To Axon, IEC = Inter Electrode Contact
    print("--- RUN BIPOLAR SIMULATION SQUAREWAVE WITH CHANGING ELECTRODE TO AXON DISTANCE AND INTER ELECTRODE CONTACT DISTANCE, ELECTRODE %s TO AXON ---" % mode)
    config = 'ProposedModel_Bipolar'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    poledistance_list = []
    count = {}
    for i in range(1000, 60001, 500):
        poledistance_list.append(i)
    amplitudelist = []
    for i in range(200):
        amplitudelist.append(round(0.01 * i, 2))
    starttime = time.time()
    createMRGaxon(par)
    result = {}
    for dist in poledistance_list:
        result[dist] = {}
        if mode == 'parallel':
            par['HFSy2'] = -dist
        elif mode == 'perpendicular':
            par['HFSx2'] = -dist
        for a in amplitudelist:
            rec = recordMRGaxon(recpar)
            par['HFSamp'] = a
            t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
            updateMRGaxon(par)
            print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s um interelectrodecontact distance) ---" % (frequency, a, dist))
            runMRGaxon(rec, t_signal, i_signal)
            if is_blocked(rec, par):
                cpp = (1.0)/(2*(1000*frequency))*a
                result[dist]["frequency"] = frequency
                result[dist]["interelectrodecontactdistance"] = dist
                result[dist]["amplitude"] = a
                result[dist]["chargeperphase"] = cpp
                break
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename = 'results_bipolar/results_squarewave_IECdist_' + mode
    np.save(filename, result)


##############################################################
# Build dataset for square wave with bipolar electrode of changing orientation
##############################################################
def bipolar_squarewave_orientation_results(mode = 'x'): #ETA = Electrode To Axon, IEC = Inter Electrode Contact
    print("--- RUN BIPOLAR SIMULATION SQUAREWAVE WITH CHANGING ELECTRODE ORIENTATION OVER %s-AXIS---" % mode)
    config = 'ProposedModel_Bipolar'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    orientation_list = []
    count = {}
    poledistance_list = []
    for i in range(45, 91, 5):
        orientation_list.append(i)
    for i in range(1000, 5001, 200):
        poledistance_list.append(i)
    amplitudelist = []
    for i in range(20,200):
        amplitudelist.append(round(0.01 * i, 2))
    starttime = time.time()
    createMRGaxon(par)
    result = {}
    for angle in orientation_list:
        result[angle] = {}
        for dist in poledistance_list:
            result[angle][dist]= {}
            par['HFSy2'] = -np.cos(np.deg2rad(angle))*dist
            if mode == 'x':
                par['HFSx2'] = -np.sin(np.deg2rad(angle))*dist
            if mode == 'z':
                par['HFSz2'] = par['HFSz'] + np.sin(np.deg2rad(angle))*dist
                print par['HFSz2']
                print par['HFSy2']
                print par['HFSx2']
            for a in amplitudelist:
                rec = recordMRGaxon(recpar)
                par['HFSamp'] = a
                t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
                updateMRGaxon(par)
                print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s degree angle, %s um interpolar distance) ---" % (frequency, a, angle, dist))
                runMRGaxon(rec, t_signal, i_signal)
                if is_blocked(rec, par):
                    cpp = (1.0)/(2*(1000*frequency))*a
                    result[angle][dist]["frequency"] = frequency
                    result[angle][dist]["electrodeangle"] = angle
                    result[angle][dist]["interelectrodecontactdistance"] = dist
                    result[angle][dist]["amplitude"] = a
                    result[angle][dist]["chargeperphase"] = cpp
                    break
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename = 'results_bipolar/results_squarewave_orientation_' + mode
    np.save(filename, result)


##############################################################
# Plot results of  square wave with interphase delay
##############################################################
def plot_bipolar(type, restype="amplitude", plottype="lines", zoom=False):
    if type == "ETA_IEC_parallel":
        zoomtext = ""
        if zoom:
            zoomtext = "_zoom"
        result = np.load("results_bipolar/results_squarewave_ETAdist_IECdist_parallel" + zoomtext + ".npy", encoding="ASCII").item()
        plot_results_bipolar_ETA_IEC_parallel(result, restype, plottype)
        filename = "results_bipolar_ETA_IEC_parallel" + zoomtext + "_"+plottype+"_"+restype
    elif type == "IEC_parallelperpendicular":
        result_parallel = np.load("results_bipolar/results_squarewave_IECdist_parallel.npy", encoding="ASCII").item()
        result_perpendicular = np.load("results_bipolar/results_squarewave_IECdist_perpendicular.npy", encoding="ASCII").item()
        plot_results_bipolar_IEC_parallelperp(result_parallel, result_perpendicular, restype)
        filename = "results_bipolar_IEC_parvsperp_"+restype
    elif type == "orientation":
        result_x =  np.load("results_bipolar/results_squarewave_orientation_x.npy", encoding="ASCII").item()
        result_z = np.load("results_bipolar/results_squarewave_orientation_z.npy", encoding="ASCII").item()
        filename = "results_bipolar_orientation_"+restype
        plot_results_bipolar_orientation(restype, result_x, result_z)
    plt.savefig("reportplots/bipolar_results/" + filename + ".pdf", format='pdf', dpi=1200)
    plt.show()
