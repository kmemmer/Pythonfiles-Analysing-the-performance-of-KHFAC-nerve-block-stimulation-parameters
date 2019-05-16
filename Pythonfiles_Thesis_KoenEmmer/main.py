##############################################################
# This main file contains an overview of functions that were
# run to do simulations in the thesis of Koen Emmer
# Uncomment functions to run them
# For questions, contact me via LinkedIn
# https://www.linkedin.com/in/koenemmer/
##############################################################

##############################################################
# Import Modules
##############################################################
# Import Python libraries
# Import for BrainFrame
# import matplotlib

from configoptions import *
from reportplots import *
from datasetproposedmethod import *
from datasetsformodeldesign import *
from monopolar_simulations import *
from bipolar_simulations import *

##############################################################
# Build datasets for
##############################################################
# runwave("ClassicModel", "square", "complete", "saveall")
# runwave("ClassicModel", "sine", "complete", "saveall")
# runsquarewaveCB("ClassicModel", "complete", "saveall")
# runwave("ProposedModel", "square", "complete", "saveall")
# runwave("ProposedModel", "sine", "complete", "saveall")
# runsquarewaveCB("ProposedModel", "complete", "saveall")

##############################################################
# Find blocking amplitudes via proposed method
##############################################################
# squarewaveresults()
# sineresults()
# assymmetricalresults()

##############################################################
# Plot single KHFAC simulation
##############################################################
# plot_square_classic(tstop=20)
# plot_sine_classic()
# plot_assymmetric_classic(f=10, a=0.2, tstop = 50.0, chargebalance=0.1, intrinsic=1)
# plot_square_proposed(f=10, a=0.47)
# plot_sine_proposed(f=10, a=0.52)
# plot_assymmetric_classic(f=10, a=0.55, tstop = 51.0, chargebalance=0.8, intrinsic=1)
# plot_assymmetric_classic(f=10, a=0.6, tstop = 51.0, chargebalance=0.9, intrinsic=1)
# plot_assymmetric_proposed(f=10, a=0.19, chargebalance=0.1)
# plot_assymmetric_proposed(f=10, a=0.2, chargebalance=0.1)
# plot_assymmetric_proposed(f=10, a=0.6, chargebalance=0.9)
# plot_sine_proposed(10,0.52)
# plot_sine_proposed(10,0.45)
# plot_sine_proposed(40,0.66)
# plot_sine_proposed(40,0.60)
# plot_square_proposed_bipolar(10,1.0)


##############################################################
# Plot and test waveforms (uncomment one of the lines together with the last two lines to produce a picture
##############################################################
# t_signal, i_signal = sinewave(0, 0.1, 10, 1, 1000)
# t_signal, i_signal = chargebalanced_asymmetrical(0, 2.0, 1, 0.06, 0.8, 0.1, 0.1)
# t_signal, i_signal = chargebalanced_asymmetrical(0, 0.1, 10, 0.05, 0.9)
# t_signal, i_signal = trianglewave(0, 0.1, 10, 1)
# t_signal, i_signal = squarewave_ip(0, 0.2, 10, 1, 0.1, 0.1)
# t_signal, i_signal = squarewave(0, 0.2, 10, 1)
# t_signal, i_signal = stepwave(0, 0.1, 10, 2, 3)
# t_signal, i_signal = stepwave_sine(0, 0.1, 10, 1, 20)
# plot_signal(plt, t_signal, i_signal)
# plt.show()

##############################################################
# Monopolar simulations -> create result files
##############################################################
# monopolar_triangularwave_results()
# monopolar_sinewave_results()
# monopolar_squarewave_results()
# monopolar_step("triangular")
# monopolar_step("sine")
# monopolar_assymmetricalwave_results()
# squarewave_ipd_results()
# monopolar_squarewave_realdistance_results()
# squarewave_ipd_results("validation")

##############################################################
# Bipolar simulations -> create result files
##############################################################
# bipolar_squarewave_ETAdistance_IECdistance_parallel_results()
# bipolar_squarewave_ETAdistance_IECdistance_parallel_results(zoom=True)
# bipolar_squarewave_IECdistance_results('parallel')
# bipolar_squarewave_IECdistance_results('perpendicular')
# bipolar_squarewave_orientation_results('x')
# bipolar_squarewave_orientation_results('z')

##############################################################
# Build report plots
##############################################################
## Background chapter
# plotAP()
# plotKHFACdemogates()
# plothminftau()

## Method chapter
# plot_2D_blockdescription()
# plot_3D_blockdescription()
# plot_gates_proposedmethodsetup()
# plot_asymmetrical_waveform()
# justificationplots("sine")
# justificationplots("square")
# justificationplots("squareCB")

## Results Chapter
# Monopolar plots
# plot_monopolar("monopolar_basic_waveforms", "amplitude")
# plot_monopolar("monopolar_basic_waveforms", "cpp")
# plot_monopolar("stepfunctions", "amplitude")
# plot_monopolar("stepfunctions", "cpp")
# plot_monopolar("asymmetrical", "amplitude", "colour")
# plot_monopolar("asymmetrical", "cpp", "colour")
# plot_monopolar("asymmetrical", "amplitude", "3D")
# plot_monopolar("asymmetrical", "cpp", "3D")
# plot_monopolar("asymmetrical", "amplitude", "singlefrequency", 10)
# plot_monopolar("squarewave_ipd", "amplitude", "lines")
# plot_monopolar("squarewave_ipd", "cpp", "lines")
# plot_monopolar("squarewave_ipd", "amplitude", "colour")
# plot_monopolar("squarewave_ipd", "cpp", "colour")
# plot_monopolar("squarewave_ipd", "amplitude", "3D")
# plot_monopolar("squarewave_ipd", "cpp", "3D")
# plot_monopolar("squarewave_ipd_validation", "amplitude", "lines")
# plot_monopolar("squarewave_ipd_validation", "cpp", "lines")
# plot_monopolar("squarewave_ipd_validation", "amplitude", "colour")
# plot_monopolar("squarewave_ipd_validation", "cpp", "colour")
# plot_monopolar("realdistance", "amplitude")
# plot_monopolar("realdistance", "cpp")
# Bipolar plots
# plot_bipolar("ETA_IEC_parallel", "amplitude", "lines")
# plot_bipolar("ETA_IEC_parallel", "cpp", "lines")
# plot_bipolar("ETA_IEC_parallel", "amplitude", "colour")
# plot_bipolar("ETA_IEC_parallel", "cpp", "colour")
# plot_bipolar("ETA_IEC_parallel", "amplitude", "3D")
# plot_bipolar("ETA_IEC_parallel", "cpp", "3D")
# plot_bipolar("ETA_IEC_parallel", "amplitude", "optimal")
# plot_bipolar("ETA_IEC_parallel", "amplitude", "lines", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "cpp", "lines", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "amplitude", "colour", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "cpp", "colour", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "amplitude", "3D", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "cpp", "3D", zoom=True)
# plot_bipolar("ETA_IEC_parallel", "amplitude", "optimal", zoom=True)
# plot_bipolar("IEC_parallelperpendicular", "amplitude")
# plot_bipolar("IEC_parallelperpendicular", "cpp")
# plot_bipolar("orientation", "amplitude")

## Discussion plots
# plot_asymmetrical_bipolar(0.001)
# plot_ipdbasicimplementation(0.25,0.25)
# plot_ipdbasicimplementation(0,0.5)
# plot_ipdcompleximplementation()
# plot_ipd_validation(0.4,0,0)

##############################################################
## Build presentation plots
##############################################################
# buildKHFACgif()


quitNeuron()