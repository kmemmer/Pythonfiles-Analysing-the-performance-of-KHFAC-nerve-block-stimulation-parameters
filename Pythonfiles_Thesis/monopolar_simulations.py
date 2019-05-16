##############################################################
# Monopolar simulation functions
##############################################################
import csv
from configoptions import *
import time
import datetime
from MRG_Model import *             # Interface with Neuron MRG Model
from blockdetection import *
from waveforms import *             # Waveform functions for Neuron
from plottingfunctions_results import *
from simulationfunctions_proposedmodel import *

import os
if not os.path.exists('results_monopolar'):
    os.makedirs('results_monopolar')          # Ensure that brainframe makes justification folder
if not os.path.exists('reportplots'):
    os.makedirs('reportplots')
if not os.path.exists('reportplots/monopolar_results'):
    os.makedirs('reportplots/monopolar_results')

##############################################################
# Build dataset for square wave with interphase delay tested with Proposed Model
##############################################################
def squarewave_ipd_results(type="normal"):
    print("--- RUN MONOPOLAR SIMULATION SQUAREWAVE WITH INTERPHASE DELAYS ---")
    config = 'ProposedModel'
    if type == "validation":
        config = 'ClassicModel'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    ipd_anodal_list = []
    for i in range(20):
        ipd_anodal_list.append(round(0.0 + 0.05 * i, 2))
    if type == "validation":
        ipd_anodal_list = []
        for i in range(5):
            ipd_anodal_list.append(round(0.0 + 0.20 * i, 2))
    ipd_cathodal_list = ipd_anodal_list
    starttime = time.time()
    amplitudelist = []
    for i in range(100):
        amplitudelist.append(round(0.1 + 0.01 * i, 2))
    if type == "validation":
        amplitudelist = []
        for i in range(80):
            amplitudelist.append(round(0.35 + 0.01 * i, 2))
    createMRGaxon(par)
    result = {}
    for ipd1 in ipd_anodal_list:
        result[ipd1] = {}
        for ipd2 in ipd_cathodal_list:
            result[ipd1][ipd2] = {}
            for a in amplitudelist:
                rec = recordMRGaxon(recpar)
                par['HFSamp'] = a
                if ipd1+ipd2 >= 1.0:
                    break
                t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], ipd1, ipd2)
                updateMRGaxon(par)
                print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s ipd1, %s ipd2, type = %s) ---" % (frequency, a, ipd1, ipd2, type))
                runMRGaxon(rec, t_signal, i_signal)
                block = False
                if type != "validation":
                    block = is_blocked(rec,par)
                else:
                    if blockeffectiveness(rec,par) >= 0.9:
                        block = True
                if block:
                    cpp = (1.0-ipd1-ipd2)/(2*(1000*frequency))*a
                    result[ipd1][ipd2]["frequency"] = frequency
                    result[ipd1][ipd2]["ipd1"] = ipd1
                    result[ipd1][ipd2]["ipd2"] = ipd2
                    result[ipd1][ipd2]["amplitude"] = a
                    result[ipd1][ipd2]["chargeperphase"] = cpp
                    break
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename = 'results_monopolar/results_squarewave_ipd_proposedmethod'
    if type == "validation":
        filename = 'results_monopolar/results_squarewave_ipd_validation'
    np.save(filename, result)


##############################################################
# Build dataset for step wave triangular shape
##############################################################
def monopolar_step(shape):
    print("--- RUN MONOPOLAR SIMULATION STEPWAVE (" + shape + ") WITH INCREASING STEPSIZES---")
    config = 'ProposedModel'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    step_list = []
    for i in range(1,51):
        step_list.append(i)
    starttime = time.time()
    amplitudelist = []
    for i in range(200):
        amplitudelist.append(round(0.1 + 0.01 * i, 2))
    createMRGaxon(par)
    result = {}
    for steps in step_list:
        result[steps] = {}
        for a in amplitudelist:
            rec = recordMRGaxon(recpar)
            par['HFSamp'] = a
            if shape == "triangular":
                t_signal, i_signal = stepwave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], steps)
            elif shape == "sine":
                t_signal, i_signal = stepwave_sine(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], steps)
            else:
                print "Wrong shape selected!"
                break
            updateMRGaxon(par)
            print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s steps (triangular)) ---" % (frequency, a, steps))
            runMRGaxon(rec, t_signal, i_signal)
            if is_blocked(rec, par):
                cpp = 0.0
                if shape == "triangular":
                    stepsize = a / steps
                    for i in range(steps+1):
                        cpp += (i * stepsize / (4 * frequency * steps))
                    for i in range(steps):
                        cpp += (i * stepsize / (4 * frequency * steps))
                elif shape == "sine":
                    for i in range(steps*2):
                        cpp += (a * np.sin(2 * np.pi * i / (steps * 4)) / (4 * frequency * steps))
                result[steps]["frequency"] = frequency
                result[steps]["numberofsteps"] = steps
                result[steps]["amplitude"] = a
                result[steps]["chargeperphase"] = cpp
                break
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename = 'results_monopolar/results_monopolar_stepwave_' + shape
    np.save(filename, result)


##############################################################
# Build dataset for triangular wave tested with Proposed Model
##############################################################
def monopolar_triangularwave_results():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    result = find_blockingamplitudes_Freq(frequencylist, "triangular")
    filename = 'results_monopolar/results_monopolar_triangularwave'
    np.save(filename, result)


##############################################################
# Build dataset for square wave tested with Proposed Model
##############################################################
def monopolar_squarewave_results():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    result = find_blockingamplitudes_Freq(frequencylist, "square")
    filename = 'results_monopolar/results_monopolar_squarewave'
    np.save(filename, result)


##############################################################
# Build dataset for sine wave tested with Proposed Model
##############################################################
def monopolar_sinewave_results():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    result = find_blockingamplitudes_Freq(frequencylist, "sine")
    filename = 'results_monopolar/results_monopolar_sinewave'
    np.save(filename, result)


##############################################################
# Build dataset for assymmetricalwave tested with Proposed Model
##############################################################
def monopolar_assymmetricalwave_results():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    chargebalancelist = []
    for i in range(18):
        chargebalancelist.append(round(0.1 + 0.05*i, 2))
    result = find_blockingamplitudes_CB(frequencylist, chargebalancelist)
    filename = 'results_monopolar/results_monopolar_assymmetricalwave_allfrequencies'
    np.save(filename, result)


##############################################################
# Build dataset for assymmetricalwave tested with Proposed Model
##############################################################
def monopolar_squarewave_realdistance_results():
    print("--- RUN MONOPOLAR SIMULATION SQUAREWAVE WITH CHANGE OVER REAL PERPENDICULAR DISTANCE ---")
    config = 'ProposedModel'
    par, recpar = selectConfig(config)
    frequency = 10
    par['HFSfrequency'] = frequency
    perpdistance_list = []
    # Max nervediameter is 4.67+1.17 = 5,84. Axondiameter is 10micrometre, range is 10,585. Steps of 10 micrometre
    for i in range(100, 5850, 10):
        perpdistance_list.append(i)
    starttime = time.time()
    amplitudelist = []
    for i in range(200):
        amplitudelist.append(round(0.01 * i, 2))
    for i in range(280):
        amplitudelist.append(round(2.0 + 0.1 * i, 2))
    createMRGaxon(par)
    result = {}
    count = 0
    for dist in perpdistance_list:
        result[dist] = {}
        par['HFSz'] = dist
        for a in amplitudelist[count:]:
            rec = recordMRGaxon(recpar)
            par['HFSamp'] = a
            t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
            updateMRGaxon(par)
            print("--- RUN KHFAC-SIGNAL (%s kHz, %s mA, %s perpdistance) ---" % (frequency, a, dist))
            runMRGaxon(rec, t_signal, i_signal)
            if is_blocked(rec, par):
                cpp = a / (2*frequency)
                result[dist]["frequency"] = frequency
                result[dist]["perpendiculardistance"] = dist
                result[dist]["amplitude"] = a
                result[dist]["chargeperphase"] = cpp
                break
            count += 1
    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))
    filename = 'results_monopolar/results_monopolar_squarewave_realdistance'
    np.save(filename, result)


##############################################################
# Plot results of  square wave with interphase delay
##############################################################
def plot_monopolar(type, restype="amplitude", plottype="lines", plotfreq = 10):
    if type == "squarewave_ipd":
        result = np.load("results_monopolar/results_squarewave_ipd_proposedmethod.npy", encoding="ASCII").item()
        plot_results_monopolar_ipd(result, restype, plottype)
        filename = "results_squarewave_ipd_"+plottype+"_"+restype
    if type == "squarewave_ipd_validation":
        result = np.load("results_monopolar/results_squarewave_ipd_validation.npy", encoding="ASCII").item()
        plot_results_monopolar_ipd(result, restype, plottype, validation=True)
        filename = "results_squarewave_ipd_validation_" + plottype + "_" + restype
    if type == "monopolar_basic_waveforms":
        result_square = np.load("results_monopolar/results_monopolar_squarewave.npy").item()
        result_sine = np.load("results_monopolar/results_monopolar_sinewave.npy").item()
        result_triangular = np.load("results_monopolar/results_monopolar_triangularwave.npy").item()
        plot_results_monopolar_basicwaveforms(result_square, result_sine, result_triangular, type=restype)
        filename = "results_basicwaveforms_"+restype
    if type == "stepfunctions":
        result_stepsine = np.load("results_monopolar/results_monopolar_stepwave_sine.npy").item()
        result_steptriangular = np.load("results_monopolar/results_monopolar_stepwave_triangular.npy").item()
        plt_results_monopolar_stepwaveforms(result_stepsine, result_steptriangular, type=restype)
        filename = "results_stepfunctions_"+restype
    if type == "realdistance":
        result = np.load("results_monopolar/results_monopolar_squarewave_realdistance.npy").item()
        plt_results_monopolar_realdistance(result, type=restype)
        filename = "results_monopolar_squarewave_realdistance_"+restype
    if type == "asymmetrical":
        result = np.load("results_monopolar/results_monopolar_assymmetricalwave_allfrequencies.npy").item()
        plot_results_asymmetrical(result, restype, plottype, plotfreq)
        filename_plottype = plottype
        if plottype == "singlefrequency":
            filename_plottype = plottype + "_" + str(plotfreq) + "kHz"
        filename = "results_monopolar_asymmetricalwaves_"+filename_plottype+"_"+restype
    plt.savefig("reportplots/monopolar_results/" + filename + ".pdf", format='pdf', dpi=1200)
    plt.show()

