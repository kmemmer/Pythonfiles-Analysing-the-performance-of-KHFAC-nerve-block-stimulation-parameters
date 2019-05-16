from simulationfunctions_proposedmodel import *
import os
if not os.path.exists('justification_files'):
    os.makedirs('justification_files')          # Ensure that brainframe makes justification folder


##############################################################
# Build dataset for square wave tested with Proposed Model
##############################################################
def squarewaveresults():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)

    result = find_blockingamplitudes_Freq(frequencylist, "square")

    filename = 'justification_files/results_squarewave_proposedmethod'

    np.save(filename, result)
    CSVsave_blockingamplitudes_2D(result, "Frequency", "Frequency (kHz)", filename)


##############################################################
# Build dataset for sine wave tested with Proposed Model
##############################################################
def sineresults():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)

    result = find_blockingamplitudes_Freq(frequencylist, "sine")

    now = datetime.datetime.now()
    # filename = 'results/results_' + now.strftime("%Y%m%d_%H%M%S")
    filename = 'justification_files/results_sinewave_proposedmethod' + now.strftime("%Y%m%d_%H%M%S")

    np.save(filename, result)
    CSVsave_blockingamplitudes_2D(result, "Frequency", "Frequency (kHz)", filename)


##############################################################
# Build dataset for assymmetricalwave tested with Proposed Model
##############################################################
def assymmetricalresults():
    frequencylist = [3]
    for i in range(19):
        frequencylist.append((i + 2) * 2)
    chargebalancelist = [0.1]
    for i in range(9):
        chargebalancelist.append(round(0.1 + 0.1*i, 1))
    result = find_blockingamplitudes_CB(frequencylist, chargebalancelist)

    filename = 'justification_files/results_squarewave_CB_proposedmethod'

    np.save(filename, result)
    CSVsave_blockingamplitudes_3D(result, "Frequency", "Frequency (kHz)", "Chargeperphase", "Charge per Phase (uC)", filename)