##############################################################
# This file contains simulation functions.
##############################################################
# Import Python libraries
import datetime
import csv
import pylab as plt
import os
if not os.path.exists('results'):
    os.makedirs('results')          # Ensure that brainframe makes result folder
# Import custom function libraries
from MRG_Model import *             # Interface with Neuron MRG Model
from plottingfunctions import *     # Plotting functions
from blockdetection import *
from waveforms import *             # Waveform functions for Neuron
import time


##############################################################
# Functions to save data to CSV
##############################################################
def savetocsv(result, now = datetime.datetime.now()):
    with open('results/results_' + now.strftime("%Y%m%d_%H%M%S") + '.csv', mode='w') as csv_file:
        fieldnames = ["Node", "Frequency (kHz)", "Amplitude (mA)", "Block %",
                      "h_max", "h_min", "V_max", "V_min", "m_max", "m_min", "h_dist_max", "h_dist_min"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore', delimiter='|')
        writer.writeheader()

        for i in result:
            for j in result[i]:
                for k in result[i][j]:
                    if result[i][j][k] != {}:                                                   # Empty dicts should be ignored
                        result[i][j][k]["Frequency (kHz)"] = result[i][j][k].pop("Frequency")   # Needed to make compliant to fieldnames of CSV
                        result[i][j][k]["Amplitude (mA)"] = result[i][j][k].pop("Amplitude")    # Needed to make compliant to fieldnames of CSV
                        writer.writerow(result[i][j][k])


# Asymmetrical waves csv-save function
def savetocsv2(result, now = datetime.datetime.now()):

    with open('results/results_' + now.strftime("%Y%m%d_%H%M%S") + '.csv', mode='w') as csv_file:
        fieldnames = ["Node", "Frequency (kHz)", "Chargebalance", "Charge per Phase (uC)", "Amplitude (mA)", "Block %",
                      "h_max", "h_min", "V_max", "V_min", "m_max", "m_min", "h_dist_max", "h_dist_min"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore', delimiter='|')
        writer.writeheader()

        for i in result:
            for j in result[i]:
                for k in result[i][j]:
                    for l in result[i][j][k]:
                            if result[i][j][k][l] != {}:
                                result[i][j][k][l]["Frequency (kHz)"] = result[i][j][k][l].pop("Frequency")             # Needed to make compliant to fieldnames of CSV
                                result[i][j][k][l]["Charge per Phase (uC)"] = result[i][j][k][l].pop("Chargeperphase")  # Needed to make compliant to fieldnames of CSV
                                result[i][j][k][l]["Amplitude (mA)"] = result[i][j][k][l].pop("Amplitude")              # Needed to make compliant to fieldnames of CSV
                                writer.writerow(result[i][j][k][l])


##############################################################
# This functions runs simulations and returns the results as a dataset
# Find blockingamplitudes, sweep over frequency
##############################################################
def run_and_save_FreqAmp(par, recpar, nodes, frequencylist, amplitudelist, waveform="square", config="ClassicModel", runtype="fast", savetype = "saveall"):
    # Run simulations for all frequencies and amplitudes and save data of nodes specified
    # Time Process
    starttime = time.time()

    # Create the axon
    createMRGaxon(par)  # , verbose)
    intervaltime = time.time() - starttime
    print("--- CREATEAXON: %s seconds ---" % (intervaltime))
    intervaltime = time.time()

    amplitude_counter = 0        # Needed for fast simulations
    # INITIALIZE RESULT ARRAY
    result = {}
    for f in frequencylist:
        result[f] = {}
        par['HFSfrequency'] = f
        for a in amplitudelist[amplitude_counter:]:
            rec = recordMRGaxon(recpar)
            # RUN SIMULATION
            par['HFSamp'] = a

            if waveform == "sine":
                t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], 1000)
            elif waveform == "square":
                t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
            else:
                print "Incompatible waveform selected!"
                return None

            intervaltime = time.time() - intervaltime
            print("--- BUILD AND RUN HFS-SIGNAL (%s kHz, %s mA) : %s seconds ---" % (f, a, intervaltime))
            intervaltime = time.time()

            updateMRGaxon(par)  # , verbose)
            runMRGaxon(rec, t_signal, i_signal)

            if config == "ClassicModel":
                effectiveness = blockeffectiveness(rec, par)
            elif is_blocked(rec, par):
                effectiveness = 1.0
            else:
                effectiveness = 0.0


            # STORE RESULTS
            if (effectiveness >= 0.90 and savetype == "saveblock") or savetype == "saveall":
                result[f][a] = {}
                for n in nodes:
                    result[f][a][n] = {}
                    h_max, h_min, V_max, V_min, m_max, m_min, h_dist_max, h_dist_min = conductionBlock(rec, par, n)

                    result[n][f][a]["Node"] = n
                    result[n][f][a]["Frequency"] = f
                    result[n][f][a]["Amplitude"] = a
                    result[n][f][a]["Block %"] = effectiveness

                    result[n][f][a]["h_max"] = h_max
                    result[n][f][a]["h_min"] = h_min
                    result[n][f][a]["V_max"] = V_max
                    result[n][f][a]["V_min"] = V_min
                    result[n][f][a]["m_max"] = m_max
                    result[n][f][a]["m_min"] = m_min
                    result[n][f][a]["h_dist_max"] = h_dist_max
                    result[n][f][a]["h_dist_min"] = h_dist_min
                    # result[n][f][a]["rec"] = rec

            # Code for fast runtype (skips amplitudes of which is known that they are not effective)
            if runtype == "fast":
                if effectiveness >= 0.90:
                    amplitude_counter = max(0, amplitude_counter - 5)  # Optional
                    break

                elif amplitude_counter >= len(amplitudelist) - 1:
                    amplitude_counter = 0
                    break

                amplitude_counter += 1

    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))

    return result


##############################################################
# This functions runs asymmetrical wave simulations and returns the results as a dataset
# Find blockingamplitudes, sweep over frequency and anode fraction
##############################################################
def run_and_save_assymmetrical(par, recpar, nodes, frequencylist, amplitudelist, chargebalancelist, config="ClassicModel", runtype="fast", savetype="saveall"):
    # Run simulations for all frequencies and amplitudes and save data of nodes specified

    # Time Process
    starttime = time.time()

    # Create the axon
    createMRGaxon(par)  # , verbose)
    intervaltime = time.time() - starttime
    print("--- CREATEAXON: %s seconds ---" % (intervaltime))
    intervaltime = time.time()

    amplitude_counter = {}
    for i in chargebalancelist:
        amplitude_counter[i] = 0

    result = {}
    for b in chargebalancelist:
        result[b] = {}
        for f in frequencylist:
            result[b][f] = {}
            par['HFSfrequency'] = f
            for a in amplitudelist[amplitude_counter[b]:]:
                rec = recordMRGaxon(recpar)  # verbose)
                par['HFSamp'] = a
                # Transform amplitude into charge; amplitude is actually only the amplitude when chargebalance is 0.5
                cpp = a/(2*f)           # Charge per phase is amplitude times half the period

                intervaltime = time.time() - intervaltime
                print("--- BUILD AND RUN HFS-SIGNAL (%s kHz, %s mA, %s chargebalance): %s seconds ---" % (f, a, b, intervaltime))
                intervaltime = time.time()

                # RUN SIMULATION
                t_signal, i_signal = chargebalanced_asymmetrical(par['HFSdelay'], par['tstop'], par['HFSfrequency'], cpp, b) # Build signal
                updateMRGaxon(par)
                runMRGaxon(rec, t_signal, i_signal)

                if config == "ClassicModel":
                    effectiveness = blockeffectiveness(rec, par)
                elif is_blocked(rec, par):
                    effectiveness = 1.0
                else:
                    effectiveness = 0.0

                # STORE RESULTS
                if (effectiveness >= 0.90 and savetype == "saveblock") or savetype == "saveall":
                    result[b][f][a] = {}
                    for n in nodes:
                        result[b][f][a][n] = {}
                        h_max, h_min, V_max, V_min, m_max, m_min, h_dist_max, h_dist_min = conductionBlock(rec, par, n)

                        result[b][f][a][n]["Node"] = n
                        result[b][f][a][n]["Frequency"] = f
                        result[b][f][a][n]["Chargebalance"] = b
                        result[b][f][a][n]["Chargeperphase"] = cpp
                        result[b][f][a][n]["Amplitude"] = a
                        result[b][f][a][n]["Block %"] = effectiveness

                        result[b][f][a][n]["h_max"] = h_max
                        result[b][f][a][n]["h_min"] = h_min
                        result[b][f][a][n]["V_max"] = V_max
                        result[b][f][a][n]["V_min"] = V_min
                        result[b][f][a][n]["m_max"] = m_max
                        result[b][f][a][n]["m_min"] = m_min
                        result[b][f][a][n]["h_dist_max"] = h_dist_max
                        result[b][f][a][n]["h_dist_min"] = h_dist_min

                # Code for fast runtype (skips amplitudes of which is known that they are not effective)
                if runtype == "fast":
                    if effectiveness >= 0.90:
                        amplitude_counter[b] = max(0, amplitude_counter - 5)  # Optional
                        break

                    elif amplitude_counter[b] >= len(amplitudelist) - 1:
                        if f == min(frequencylist):
                            amplitude_counter[b] = 0
                        else:
                            amplitude_counter[b] = max(0, amplitude_counter[b] - 5)
                        break

                    amplitude_counter[b] += 1


    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))

    return result


