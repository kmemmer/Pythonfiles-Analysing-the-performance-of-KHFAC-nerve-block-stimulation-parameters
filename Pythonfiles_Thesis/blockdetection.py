##############################################################
# This file contains the functions that detect a successful block
##############################################################
import numpy as np


##############################################################
# This functions returns values that can be used to determine
# the thresholds that categorize a block as successful or
# non-successful
##############################################################
def conductionBlock (rec, par, node):
    dt = par['dt']
    tstart = int((par['HFSdelay'] + par['tonset']) / dt) # Start measuring 1 ms after initiating the KHFAC signal, divide by dt to get listindex (2)

    gatevalues = rec['gates']
    # Neuron hocObjects need to be converted to arrays via np.array()!
    blockingnode_h = np.array(gatevalues['h_node' + str(node)])  # The node where the block occurs (a virtual anode of the HFS node)


    h_max = np.max(blockingnode_h[tstart:])
    h_min = np.min(blockingnode_h[tstart:])


    voltages = rec['voltage']
    blockingnode_voltage = np.array(voltages['v_node' + str(node)])
    V_max = np.max(blockingnode_voltage[tstart:])
    V_min = np.min(blockingnode_voltage[tstart:])

    blockingnode_m = np.array(gatevalues['m_node' + str(node)])
    m_max = np.max(blockingnode_m[tstart:])
    m_min = np.min(blockingnode_m[tstart:])

    currents = rec['current']
    blockingnode_h_inf = np.array(currents['h_inf_node' + str(node)])

    blockingnode_h_dist = [a - b for a, b in zip(blockingnode_h_inf, blockingnode_h)]
    h_dist_max = np.max(blockingnode_h_dist)
    h_dist_min = np.min(blockingnode_h_dist)


    return h_max, h_min, V_max, V_min, m_max, m_min, h_dist_max, h_dist_min


########################################
# Proposed block detection method
########################################
def is_blocked(rec, par):
    dt = par['dt']
    tstart = int((par['HFSdelay'] + par['tonset']) / dt)

    gatevalues = rec['gates']
    blocking_anode_hmax = np.max(np.array(gatevalues['h_node' + str(par['HFSreferenceNode'] + 1)])[tstart:])  # The node where the block occurs (a virtual anode of the HFS node)

    voltages = rec['voltage']
    blocking_node_Vmax = np.max(np.array(voltages['v_node' + str(par['HFSreferenceNode'])])[tstart:])
    blocking_node_Vmin = np.min(np.array(voltages['v_node' + str(par['HFSreferenceNode'])])[tstart:])

    blocking_anode_Vmax = np.max(np.array(voltages['v_node' + str(par['HFSreferenceNode']+1)])[tstart:])
    blocking_anode_Vmin = np.min(np.array(voltages['v_node' + str(par['HFSreferenceNode'] + 1)])[tstart:])

    if blocking_anode_hmax < 0.04 and (blocking_anode_Vmax > -22 or blocking_anode_Vmin > -51.5 or blocking_node_Vmin < -90):
        return True
    else:
        return False


########################################
# Classic block detection method as %
########################################
def blockeffectiveness(rec, par):

    spikesfirstnode = np.array(rec['spiketimes']['spk' + str(0)])
    # spikesfirstnode = (par['tstop'] - par['HFSdelay']) / (par['intrinsicTON'] + par['intrinsicTOFF'])
    spikeslastnode = np.array(rec['spiketimes']['spk' + str(int(par['axonnodes'])-1)])

    effectiveness = min(1, max(1.0 - float(len(spikeslastnode[(spikeslastnode > 10.0)])) / float(len(spikesfirstnode[(spikesfirstnode > 10.0)])), 0))
    return effectiveness