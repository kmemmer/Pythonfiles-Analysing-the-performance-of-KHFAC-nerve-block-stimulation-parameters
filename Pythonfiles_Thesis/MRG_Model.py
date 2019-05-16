#################################################################################################
# INTERFACE FUNCTIONS FOR PYTHON<->NEURON
# This is an adopted version from the work of Baquer Gomez (not published in thesis):
# https://repository.tudelft.nl/islandora/object/uuid%3A5c875b14-08a3-4ef0-8e90-4fc997dc19d3
# Extended by Koen Emmer to record gate variables, all other credits go to Baquer Gomez and the
# names mentioned in the code
#################################################################################################
import sys
sys.path.append("<path>")
from neuron import h
import numpy as np


#################################################################################################
# Functions that load variables into Neuron
#################################################################################################
def pass_parameters_to_nrn(parameters):#, verb=False): # USED
    '''
    Passes parameters from a dictionary to NEURON.
    If the the element is a vector it assumes that the a vector
    has been created as objref and new Vector() in the hoc code.
    Set 'verb' to True for verbose.
    '''
    for k, v in parameters.iteritems():
        if type(v) is not type(np.array([])):
            h("{" + k + " = " + str(v) + "}")
            # if verb:
            #     print(k + " = " + str(v))


#################################################################################################
# Functions that initialize the axon in Neuron
#################################################################################################
def createMRGaxon(par):#, verbose): # USED
    '''
    Initializes the model.
    Creates the axon and stimulation according to the parameters.
    '''
    h('{load_file("stdgui.hoc")}')                  # Starts the Neuron session
    pass_parameters_to_nrn(par)#, verb=verbose)       # Passes the configuration file
    h('{load_file("MRG_MODEL_edit.hoc")}')          # Loads the hoc file of the model
    h('{buildModel()}')                             # Runs the buildmodel function of the hoc file, creating the axon


#################################################################################################
# Functions that set up recording process in Neuron
#################################################################################################
def recordMRGaxon(recpar):#, verbose):
    '''
    Inserts the recorders as specified in recpar.
    '''
    k = recpar['nodes']                                         # List with al the nodes [0, 1, 2, ..., N]
    rec = {}

    if recpar['recordVoltage']:
        rec['voltage'] = record_node_voltage(k)                 # Maybe not used when looking for gating variables
    rec['gates'] = record_node_gates(k)
    rec['current'] = record_node_current(k)
    rec['spiketimes'], rec['apcount'] = record_node_spikes(k)
    # if verbose:
    #     print('Now recording from ' + str(k))
    return rec


def record_node_voltage(nodenumber, rec=None):
    '''
    Records the membrane potential of a particular set of nodes.
    '''
    segments = []
    for n in nodenumber:
        segments.append(h.node[n](0.5))
    for seg, n in zip(segments, nodenumber):
        rec = insert_nrn_recorders(seg, {'v_node' + str(n): '_ref_v'}, rec) # Another function layer; necessary?
    return rec


def record_node_gates(nodenumber, rec=None):
    segments = []
    for n in nodenumber:
        segments.append(h.node[n](0.5))
    for seg, n in zip(segments, nodenumber):
        rec = insert_nrn_recorders(seg, {'h_node' + str(n): '_ref_h_axnode'}, rec)      # Nonlinear fast sodium inactivation gate
        rec = insert_nrn_recorders(seg, {'m_node' + str(n): '_ref_m_axnode'}, rec)      # Nonlinear fast sodium activation gate
        rec = insert_nrn_recorders(seg, {'mp_node' + str(n): '_ref_mp_axnode'}, rec)    # Persistent sodium activation gate
        rec = insert_nrn_recorders(seg, {'s_node' + str(n): '_ref_s_axnode'}, rec)      # Slow potassium activation gate
    return rec


def record_node_current(nodenumber, rec=None):
    segments = []
    for n in nodenumber:
        segments.append(h.node[n](0.5))
    for seg, n in zip(segments, nodenumber):
        rec = insert_nrn_recorders(seg, {'i_Na_node' + str(n): '_ref_ina_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'i_Nap_node' + str(n): '_ref_inap_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'i_K_node' + str(n): '_ref_ik_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'i_l_node' + str(n): '_ref_il_axnode'}, rec)

        rec = insert_nrn_recorders(seg, {'m_inf_node' + str(n): '_ref_m_inf_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'tau_m_node' + str(n): '_ref_tau_m_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'h_inf_node' + str(n): '_ref_h_inf_axnode'}, rec)
        rec = insert_nrn_recorders(seg, {'tau_h_node' + str(n): '_ref_tau_h_axnode'}, rec)
    return rec


def record_node_spikes(nodenumber, rec=None,
                       apc=None, threshold = -15):
    '''
    Records the action potentials of a particular set of nodes.
    Returns a "rec" dictionary.
    '''
    if rec is None:
        rec = {}
    if apc is None:
        apc = {}
    for n in nodenumber:
        apc['apc'+str(n)] = h.APCount(h.node[int(n)](0.5))
        apc['apc'+str(n)].thresh = threshold
        rec['spk'+str(n)] = h.Vector()
        apc['apc'+str(n)].record(rec['spk'+str(n)])
    return rec,apc


def insert_nrn_recorders(segment, labels, rec=None):
    '''
    Inserts recorders for NEURON state variables.
    Use one per segment.
    "labels" is a dictionary.
    Example {'v': '_ref_v'}.
    Specify 'rec' to append to previous recorders.
    Records also time if 'rec' is 'None' (default).
    (Acknowledgements: Daniele Linaro)
    '''
    if rec is None:
        rec = {'t': h.Vector()}
        rec['t'].record(h._ref_t)
    for k, v in labels.items():
        rec[k] = h.Vector()
        rec[k].record(getattr(segment, v))
    return rec


#################################################################################################
# Functions run a simulation of the axon
#################################################################################################
def runMRGaxon(rec, ts, xs):
    h.resetModel()
    tvec = h.Vector(len(ts)) #time vector
    for i, t in enumerate(ts):
        tvec.x[i] = t
    xvec = h.Vector(len(ts)) #amplitude vector
    for i, x in enumerate(xs):
        xvec.x[i] = x
    xvec.play(h.exIClmp._ref_i, tvec, 1)
    h.run()
    rec['i_block'] = {'i': [], 't': rec['voltage']['t']}
    rec['i_block']['i'] = h.rec_electrode_block
    rec['i_stim'] = {'i': [], 't': rec['voltage']['t']}
    rec['i_stim']['i'] = h.rec_electrode_stim
    return rec


#################################################################################################
# Functions that reset values between simulations
#################################################################################################
def updateMRGaxon(par):#, verbose):
    '''
    Updates the parameters of the model.
    '''
    pass_parameters_to_nrn(par)#, verb=verbose)
    h.resetModel()

def quitNeuron():
    h.quit()

# Resets spike counter and voltages in recorder
# def resetRecorder(rec, verbose=False):
#     '''
#     Clears hoc vectors in spiketimes and voltage and resets apcounts.
#     '''
#     for k, o in rec['spiketimes'].iteritems():
#         if verbose:
#             print('Reseting ' + k)
#         o.clear()
#     if 'voltage' in rec.keys():
#         for k, o in rec['voltage'].iteritems():
#             if verbose:
#                 print('Reseting ' + k)
#             o.clear()
#     for k, o in rec['apcount'].iteritems():
#         if verbose:
#             print('Setting apcount ' + k + ' to zero.')
#         o.n = 0

