import csv
from configoptions import *
import time
import datetime
from MRG_Model import *             # Interface with Neuron MRG Model
from blockdetection import *
from waveforms import *             # Waveform functions for Neuron

##############################################################
# Functions to save data to CSV
##############################################################
def CSVsave_blockingamplitudes_2D(result, dim1name, dim1newname, filename, now = datetime.datetime.now()):
    amplitudefield = "Blocking Threshold Amplitude (mA)"
    with open(filename + '.csv', mode='w') as csv_file:
        fieldnames = [dim1newname, amplitudefield]#, 'h_max']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore', delimiter='|')
        writer.writeheader()

        for i in sorted(result):
            if result[i] != {}:  # Empty dicts should be ignored
                result[i][dim1newname] = result[i].pop(dim1name)  # Needed to make compliant to fieldnames of CSV
                result[i][amplitudefield] = result[i].pop("Amplitude")  # Needed to make compliant to fieldnames of CSV
                writer.writerow(result[i])


def CSVsave_blockingamplitudes_3D(result, dim1name, dim1newname, dim2name, dim2newname, filename, now = datetime.datetime.now()):
    amplitudefield = "Blocking Threshold Amplitude (mA)"
    with open(filename + '.csv', mode='w') as csv_file:
        fieldnames = ["Chargebalance", dim1newname, amplitudefield, dim2newname]#, 'h_max']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore', delimiter='|')
        writer.writeheader()

        for i in sorted(result):
            for j in sorted(result[i]):
                if result[i][j] != {}:  # Empty dicts should be ignored
                    result[i][j][dim1newname] = result[i][j].pop(dim1name)  # Needed to make compliant to fieldnames of CSV
                    result[i][j][dim2newname] = result[i][j].pop(dim2name)  # Needed to make compliant to fieldnames of CSV
                    result[i][j][amplitudefield] = result[i][j].pop("Amplitude")  # Needed to make compliant to fieldnames of CSV
                    writer.writerow(result[i][j])


##############################################################
# Find blockingamplitudes, sweep over frequency
##############################################################
def find_blockingamplitudes_Freq(frequencylist, waveform):
    config = 'ProposedModel'
    par, recpar = selectConfig(config)

    starttime = time.time()

    amplitudelist = []
    for i in range(100):
        amplitudelist.append(round(0.1 + 0.01 * i, 2))

    createMRGaxon(par)

    result = {}
    for f in frequencylist:
        par['HFSfrequency'] = f
        result[f] = {}
        for a in amplitudelist:
            rec = recordMRGaxon(recpar)
            par['HFSamp'] = a

            if waveform == "sine":
                t_signal, i_signal = sinewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'], 1000)
                cpp = a / (np.pi * f)
            elif waveform == "square":
                t_signal, i_signal = squarewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
                cpp = a / (2*f)
            elif waveform == "triangular":
                t_signal, i_signal = trianglewave(par['HFSdelay'], par['tstop'], par['HFSfrequency'], par['HFSamp'])
                cpp = a / (4 * f)
            else:
                print "Incompatible waveform selected!"
                return None

            updateMRGaxon(par)

            print("--- RUN HFS-SIGNAL (%s kHz, %s mA) ---" % (f, a))
            runMRGaxon(rec, t_signal, i_signal)

            if is_blocked(rec, par):
                result[f]["frequency"] = f
                result[f]["amplitude"] = a
                result[f]["chargeperphase"] = cpp
                break

    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))

    return result


##############################################################
# Find blockingamplitudes, sweep over frequency and chargebalance
##############################################################
def find_blockingamplitudes_CB(frequencylist, chargebalancelist):
    config = 'ProposedModel'
    par, recpar = selectConfig(config)

    starttime = time.time()

    amplitudelist = []
    for i in range(200):
        amplitudelist.append(round(0.1 + 0.01 * i, 2))

    createMRGaxon(par)

    result = {}
    for b in chargebalancelist:
        result[b] = {}
        for f in frequencylist:
            par['HFSfrequency'] = f
            result[b][f] = {}
            for a in amplitudelist:
                rec = recordMRGaxon(recpar)
                par['HFSamp'] = a
                cpp = a/(2*f)           # Charge per phase is amplitude times half the period
                t_signal, i_signal = chargebalanced_asymmetrical(par['HFSdelay'], par['tstop'], par['HFSfrequency'], cpp, b)
                updateMRGaxon(par)
                print("--- RUN HFS-SIGNAL (%s chargebalance, %s kHz, %s mA) ---" % (b, f, a))
                runMRGaxon(rec, t_signal, i_signal)

                if is_blocked(rec, par):
                    result[b][f]["chargebalance"] = b
                    result[b][f]["frequency"] = f
                    result[b][f]["amplitude"] = a
                    result[b][f]["chargeperphase"] = cpp
                    break

    totaltime = time.time() - starttime
    print("--- TOTAL RUNTIME: %s seconds ---" % (totaltime))

    return result