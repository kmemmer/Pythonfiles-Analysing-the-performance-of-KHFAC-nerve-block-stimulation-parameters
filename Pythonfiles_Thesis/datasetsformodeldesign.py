##############################################################
# This file contains functions that create large datasets which
# can be used to determine the threshold conditions for the proposed model.
##############################################################
from configoptions import *
from simulationfunctions import *


# Helper function
def revertFreqAmpFields3D(result):
    for i in result:
        for j in result[i]:
            for k in result[i][j]:
                if result[i][j][k] != {}:  # Empty dicts should be ignored
                    result[i][j][k]["Frequency"] = result[i][j][k].pop("Frequency (kHz)")  # Needed to make compliant to fieldnames of CSV
                    result[i][j][k]["Amplitude"] = result[i][j][k].pop("Amplitude (mA)")  # Needed to make compliant to fieldnames of CSV
    return result


##############################################################
# Run symmetrical waveforms and find values related to blocking
# config should be 'ProposedModel' or 'ClassicModel'
# runtype should be
#   - 'complete' to plot and save all amplitudes
#   - 'fast' to plot until minimal blocking amplitude is found
# savetype should be
#   - 'saveall' to save all amplitudes that are plotted
#   - 'saveblock' to only save data at blocking amplitude
# waveform should be
#   - 'square' for square waveforms
#   - 'sine' for sine waveforms
##############################################################
def runwave(config, waveform, runtype, savetype):
    par, recpar = selectConfig(config)

    nodes = {par['HFSreferenceNode']: {}, par['HFSreferenceNode'] + 1: {}}
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i+2)*2)
    amplitudelist = []
    for i in range(90):
        amplitudelist.append(round(0.1+0.01*i,2))

    result = run_and_save_FreqAmp(par, recpar, nodes, frequencylist, amplitudelist, waveform=waveform, config=config, runtype=runtype, savetype=savetype)

    now = datetime.datetime.now()
    np.save("results/results_" + now.strftime("%Y%m%d_%H%M%S"), result)
    savetocsv(result, now)


##############################################################
# Run asymmetrical waveforms and find values related to blocking
# config should be 'ProposedModel' or 'ClassicModel'
# runtype should be
#   - 'complete' to plot and save all amplitudes
#   - 'fast' to plot until minimal blocking amplitude is found
# savetype should be
#   - 'saveall' to save all amplitudes that are plotted
#   - 'saveblock' to only save data at blocking amplitude
# A combination of runtype fast and savetype saveall should result in all data being saved up to the blocking amplitude
##############################################################
def runsquarewaveCB(config, runtype, savetype):
    par, recpar = selectConfig(config)

    nodes = {par['HFSreferenceNode']: {}, par['HFSreferenceNode'] + 1: {}}
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    amplitudelist = []
    for i in range(90):
        amplitudelist.append(round(0.1 + 0.01 * i, 2))
    chargebalancelist = []
    for i in range(9):
        chargebalancelist.append(round(0.1 + 0.1 * i, 1))

    result = run_and_save_assymmetrical(par, recpar, nodes, frequencylist, amplitudelist, chargebalancelist, config=config, runtype=runtype, savetype=savetype)

    now = datetime.datetime.now()
    np.save("results/results_" + now.strftime("%Y%m%d_%H%M%S"), result)
    savetocsv2(result, now)