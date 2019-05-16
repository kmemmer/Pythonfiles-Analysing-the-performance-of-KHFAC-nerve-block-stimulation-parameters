import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
# plt.style.use('seaborn-dark-palette')

###########################################
# MONOPOLAR SIMULATIONS
###########################################
def plot_results_monopolar_ipd(data, type, plottype, validation=False):
    datascalar = 1
    if type == "amplitude":
        datatype = 'amplitude'
        datalabel = "Block threshold (mA)"
        ylim = 1.0
    elif type == "cpp":
        datatype = 'chargeperphase'
        datascalar = 1000
        datalabel = "Block threshold charge per phase ($\mu$C)"
        ylim = 0.02

    if plottype == "lines":
        count = 0
        colmulti = 1
        if validation:
            colmulti = 2
        for i in sorted(data.keys()):
            if 20*i %2 == 0 and i != 0.9:
                x = sorted(data[i].keys())
                x = [n / 10 for n in x]
                y = []
                for j in sorted(data[i].keys()):
                    if data[i][j] != {}:
                        y = np.append(y, data[i][j][datatype]*datascalar)
                    else:
                        y = np.append(y, np.nan)
                line, = plt.plot(x,y,label=str(i/10) + "ms", color="C"+str(count*colmulti))
                count+=1
        plt.xlabel("Cathodal interphase delay (ms)")
        plt.ylabel(datalabel)
        plt.ylim(bottom=0, top=ylim)
        plt.xlim(0,0.09)
        if type == "amplitude":
            plt.yticks(np.arange(0, 1.1, step=0.1))
        plt.xticks(np.arange(0, 0.09, step=0.01))
        plt.grid(True)
        plt.legend(title = "Anodal interphase delay")

    elif plottype == "colour" or plottype == "3D":
        ipd1 = []
        ipd2 = []
        for i in sorted(data.keys()):
            ipd1 = np.append(ipd1, i)
            for j in sorted(data[i].keys()):
                if j not in ipd2:
                    ipd2=np.append(ipd2, j)
        matrix = np.zeros((len(ipd1), len(ipd2)))
        for i in range(len(ipd1)):
            for j in range(len(ipd2)):
                if data[ipd1[i]][ipd2[j]] != {}:
                    matrix[i][j] = data[ipd1[i]][ipd2[j]][datatype]*datascalar
                else:
                    matrix[i, j] = np.nan

        # Set up a regular grid of interpolation points
        ipd1 = [x / 10 for x in ipd1]
        ipd2 = [x / 10 for x in ipd2]
        X, Y = np.meshgrid(ipd1, ipd2)

        if plottype == "colour":
            plt.pcolormesh(X, Y, matrix.T, cmap=cm.viridis_r)
            clb = plt.colorbar()
            clb.set_label(datalabel)
            # clb.ax.set_title(datalabel)
            plt.xlabel("Anodal interphase delay (ms)")
            plt.ylabel("Cathodal interphase delay (ms)")
        elif plottype == "3D":
            ax = plt.gca(projection='3d')
            ax.plot_surface(X, Y, matrix.T, cmap=cm.viridis_r, linewidth=0, antialiased=False, vmin=np.nanmin(matrix), vmax=np.nanmax(matrix))
            ax.set_xlabel("Anodal interphase delay (ms)")
            ax.set_ylabel("Cathodal interphase delay(ms)")
            ax.set_zlabel(datalabel)
            ax.view_init(15, -160)
    title = ""
    for i in data:
        for j in data[i]:
            if data[i][j] != {}:
                title = "Frequency = " + str(data[i][j]["frequency"]) + "kHz"
                break
        if title != "":
            break
    plt.title(title)
    plt.tight_layout()
    return plt


def plot_results_monopolar_basicwaveforms(squareres, sineres, triangularres, type):
    frequencies = []
    amps_square = []
    amps_sine = []
    amps_triangle = []
    resvar = ""
    xlabelvar = ""
    if type == "amplitude":
        resvar = "Amplitude"
        ylabelvar = "Block threshold (mA)"
        ylim = 1.0
    elif type == "cpp":
        resvar = "Chargeperphas"
        ylabelvar = "Block threshold charge per phase ($\mu$C)"
        ylim = 0.05
    else:
        print "Incorrect type"
        return
    for i in sorted(squareres):
        frequencies.append(i)
        amps_square.append(squareres[i][resvar])
    for i in sorted(sineres):
        amps_sine.append(sineres[i][resvar])
    for i in sorted(triangularres):
        amps_triangle.append(triangularres[i][resvar])
    plt.plot(frequencies,amps_square, label="Square")
    plt.plot(frequencies,amps_sine, label="Sine")
    plt.plot(frequencies,amps_triangle, label="Triangular")
    plt.xlabel("KHFAC frequency (kHz)")
    plt.ylabel(ylabelvar)
    plt.legend(title="Waveform type")
    plt.ylim(0, ylim)
    plt.yticks(np.arange(0,ylim+ylim/10,ylim/10))
    plt.xlim(left=0, right=max(frequencies)+5)
    plt.xticks(np.arange(0,max(frequencies)+5,5))
    plt.grid()
    plt.tight_layout()
    return plt


def plt_results_monopolar_stepwaveforms(stepsineres, steptriangleres, type):
    if type == "amplitude":
        resvar = "amplitude"
        ylabelvar = "Block threshold (mA)"
        ylim = 1.0
    elif type == "cpp":
        resvar = "chargeperphase"
        ylabelvar = "Block threshold charge per phase ($\mu$C)"
        ylim = 0.05
    steps = []
    amps_sine = []
    amps_triangle = []
    for i in sorted(stepsineres):
        steps.append(i)
        amps_sine.append(stepsineres[i][resvar])
    for i in sorted(steptriangleres):
        amps_triangle.append(steptriangleres[i][resvar])
    steps = [x * 4 for x in steps]
    plt.plot(steps, amps_sine, label="Stepped sine", color="orange")
    plt.plot(steps, amps_triangle, label="Stepped triangular", color="green")
    plt.xlabel("Steps per period")
    plt.ylabel(ylabelvar)
    plt.legend(title="Waveform type")
    plt.ylim(0, ylim)
    plt.yticks(np.arange(0,ylim+ylim/10,ylim/10))
    plt.xlim(left=0, right=max(steps)+20)
    plt.xticks(np.arange(0,max(steps)+5,20))
    plt.grid()
    plt.tight_layout()
    return plt


def plt_results_monopolar_realdistance(data, type):
    if type == "amplitude":
        resvar = "amplitude"
        ylabelvar = "Block threshold (mA)"
        ylim = 30.0
    elif type == "cpp":
        resvar = "chargeperphase"
        ylabelvar = "Block threshold charge per phase ($\mu$C)"
        ylim = 1.5
    distances = []
    amps = []
    for i in sorted(data):
        distances.append(i/1000.0)
        amps.append(data[i][resvar])
    plt.plot(distances, amps)#, label="Stepped sine")
    plt.xlabel("Electrode perpendicular distance (mm)")
    plt.ylabel(ylabelvar)
    plt.title("KHFAC frequency = 10kHz")
    plt.grid(True)
    # plt.legend()
    plt.ylim(bottom = 0, top = ylim)
    plt.xlim(left = 0, right = 6)
    plt.tight_layout()
    return plt


def plot_results_asymmetrical(data, type, plottype, plotfreq):
    datascalar = 1
    if type == "amplitude":
        datatype = "amplitude"
        datalabel = "Peak current amplitude at block threshold (mA)"
        # ylim = 30.0
    elif type == "cpp":
        datatype = "chargeperphase"
        datascalar = 1000
        datalabel = "Block threshold charge per phase ($\mu$C)"
        # ylim = 30.0

    if plottype == "colour" or plottype == "3D":
        cb = []
        f = []
        for i in sorted(data.keys()):
            cb.append(i)
            for j in sorted(data[i].keys()):
                if j not in f:
                    f.append(j)
        matrix = np.zeros((len(cb), len(f)))
        for i in range(len(cb)):
            for j in range(len(f)):
                if data[cb[i]][f[j]] != {}:
                    if datatype == "amplitude":
                        datascalar = 0.5 / np.min([cb[i],1.0-cb[i]])
                    matrix[i][j] = data[cb[i]][f[j]][datatype] * datascalar
                else:
                    matrix[i, j] = np.nan
        X, Y = np.meshgrid(cb, f)
        if plottype == "colour":
            plt.pcolormesh(X, Y, matrix.T, cmap=cm.viridis_r)
            clb = plt.colorbar()
            clb.set_label(datalabel)
            plt.xlabel("Anode fraction")
            plt.ylabel("Frequency (kHz)")
        elif plottype == "3D":
            ax = plt.gca(projection='3d')
            ax.plot_surface(X, Y, matrix.T, cmap=cm.viridis_r, linewidth=0, antialiased=False, vmin=np.nanmin(matrix), vmax=np.nanmax(matrix))
            ax.set_xlabel("Anode fraction")
            ax.set_ylabel("Frequency (kHz)")
            ax.set_zlabel(datalabel)
            ax.view_init(15, -160)
    elif plottype == "singlefrequency":
        cb = []
        maxamp = []
        cpp = []
        for i in sorted(data.keys()):
            cb.append(i)
            if data[i][plotfreq] != {}:
                maxamp.append(data[i][plotfreq]['amplitude']*0.5/(np.min([i, 1.0-i])))
                cpp.append(data[i][plotfreq]['chargeperphase'])
        fig, ax1 = plt.subplots(figsize=(8,5))
        cb = [n/plotfreq for n in cb]
        color = 'C0'
        ax1.set_xlabel("$T_{anode}$ (ms)")
        ax1.set_ylabel("Peak current amplitude at block threshold (mA)", color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(cb, maxamp, color=color)
        ax1.set_ylim(bottom=0, top=4.0)
        ax1.set_xlim(left=0, right=0.1)
        ax1.set_xticks(np.arange(0.01, 0.1, step=0.01))

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'r'
        ax2.set_ylabel("Block threshold charge per phase ($\mu$C)", color=color)  # we already handled the x-label with ax1
        ax2.plot(cb, cpp, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylim(bottom=0, top=0.04)
        fig.tight_layout()
        plt.grid(axis="x")
        plt.title("KHFAC frequency = " + str(plotfreq) + "kHz")
        ax1.grid()
    plt.tight_layout()
    return plt

###########################################
# BIPOLAR SIMULATIONS
###########################################
def plot_results_bipolar_ETA_IEC_parallel(data, type, plottype):
    # fig = plt.figure()
    datascalar = 1
    if type == "amplitude":
        datatype = 'amplitude'
        datalabel = "Block threshold (mA)"
    elif type == "cpp":
        datatype = 'chargeperphase'
        datascalar = 1000
        datalabel = "Block threshold charge per phase ($\mu$C)"

    if plottype == "lines":
        for i in sorted(data.keys(), reverse=True):
            x = sorted(data[i].keys())
            x = [n / 1000.0 for n in x] # convert to mm
            y = []
            for j in sorted(data[i].keys()):
                if data[i][j] != {}:
                    y = np.append(y, data[i][j][datatype]*datascalar)
                else:
                    y = np.append(y, np.nan)
            plt.plot(x,y,label=str(i) + "$\mu$m")
        plt.xlabel("Interpolar distance (mm)")
        plt.ylabel(datalabel)
        plt.legend(title = "Electrode to axon distance", loc="upper right")
        plt.grid()

    elif plottype == "colour" or plottype == "3D":
        ax1 = []
        ax2 = []
        for i in sorted(data.keys()):
            ax1.append(i)
            for j in sorted(data[i].keys()):
                if j not in ax2:
                    ax2.append(j)
        matrix = np.zeros((len(ax1), len(ax2)))
        for i in range(len(ax1)):
            for j in range(len(ax2)):
                if data[ax1[i]][ax2[j]] != {}:
                    matrix[i,j] = data[ax1[i]][ax2[j]][datatype] * datascalar
                else:
                    matrix[i,j] = np.nan
        # ax1 = [x / 1000 for x in ax1]
        ax2 = [x / 1000.0 for x in ax2]
        # Set up a regular grid of interpolation points
        X, Y = np.meshgrid(ax1, ax2)

        if plottype == "colour":
            plt.pcolormesh(Y, X, matrix.T, cmap=cm.viridis_r)
            clb = plt.colorbar()
            clb.set_label(datalabel)
            plt.xlabel("Interpolar distance (mm)")
            plt.ylabel("Electrode to axon distance ($\mu$m)")
        elif plottype == "3D":
            ax = plt.gca(projection='3d')
            ax.plot_surface(X, Y, matrix.T, cmap=cm.viridis_r, linewidth=0, antialiased=False, vmin=np.nanmin(matrix),
                            vmax=np.nanmax(matrix))
            ax.set_xlabel("Electrode to axon distance ($\mu$m)")
            ax.set_ylabel("Interpolar distance (mm)")
            ax.set_zlabel(datalabel)
            ax.view_init(15, -160)


    elif plottype == "optimal":
        x = sorted(data.keys()) # x-axis is electrode to axon distance
        bestamplitudes = []
        bestcontactdistances = []
        for i in x:
            amplitudes = []
            contactdistances = []
            for j in data[i]:
                if data[i][j] != {}:
                    amplitudes.append(data[i][j][datatype]*datascalar)
                    contactdistances.append(j)
            if amplitudes != []:
                bestamplitudes.append(np.min(amplitudes))
                bestcontactdistances.append(contactdistances[amplitudes.index(np.min(amplitudes))])
            else:
                bestamplitudes.append(np.nan)
                bestcontactdistances.append(np.nan)

        bestcontactdistances = [n / 1000.0 for n in bestcontactdistances]  # convert to mm
        fig, ax1 = plt.subplots()
        color = 'C0'
        ax1.set_xlabel("Electrode to axon distance ($\mu$m)")
        ax1.set_ylabel("Lowest block threshold (mA)", color=color)
        ax1.plot(x, bestamplitudes, color=color)
        ax1.set_ylim(bottom=0, top=12)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'r'
        ax2.set_ylabel('Optimal interpolar distance (mm)', color=color)  # we already handled the x-label with ax1
        ax2.plot(x, bestcontactdistances, color=color)
        ax2.set_ylim(bottom=0, top=6)
        ax2.tick_params(axis='y', labelcolor=color)
        ax1.set_yticks(np.arange(0, 12, step = 1))
        ax1.grid()
        ax2.set_yticks(np.arange(0, 6, step = 1))
        ax2.grid()

        fig.tight_layout()

    plt.title("KHFAC frequency = 10kHz")
    plt.tight_layout()
    return plt

def plot_results_bipolar_IEC_parallelperp(datapar, dataperp, type):
    datascalar = 1
    if type == "amplitude":
        datatype = 'amplitude'
        datalabel = "Block threshold (mA)"
        ylim = 0.8
    elif type == "cpp":
        datatype = 'chargeperphase'
        datascalar = 1000
        datalabel = "Block threshold charge per phase ($\mu$C)"
        ylim = 0.04
    x = sorted(datapar.keys())
    x = x[:x.index(25000)]

    ypar = []
    yperp = []
    for i in x:
        if datapar[i] != {}:
            ypar.append(datapar[i][datatype]*datascalar)
        else: ypar.append(np.nan)
        if dataperp[i] != {}:
            yperp.append(dataperp[i][datatype]*datascalar)
        else: ypar.append(np.nan)
    x = [n / 1000.0 for n in x]
    plt.plot(x, ypar, label = "parallel")
    plt.plot(x, yperp, label = "perpendicular")
    plt.xlabel("Interpolar distance (mm)")
    plt.ylabel(datalabel)
    plt.ylim(bottom=0, top=ylim)
    plt.xlim(0,25)
    plt.legend(title="Electrode orientation")
    plt.title("Frequency 10kHz, electrode 1000$\mu m$ above axon")
    plt.tight_layout()
    plt.grid()
    return plt


def plot_results_bipolar_orientation(type, result_x, result_z, plottype="lines", IECdist=2200):
    datascalar = 1
    if type == "amplitude":
        datatype = 'amplitude'
        datalabel = "Block threshold (mA)"
    elif type == "cpp":
        datatype = 'chargeperphase'
        datascalar = 1000
        datalabel = "Block threshold charge per phase ($\mu$C)"
    data = result_z

    if plottype == "lines":
        angles = []
        amps_x = []
        amps_z = []
        for i in sorted(result_x.keys()):
            angles.append(i)
            amps_x.append(result_x[i][IECdist][datatype])
            amps_z.append(result_z[i][IECdist][datatype])
        plt.plot(angles, amps_x, label="Electrode in $xy$-plane")
        plt.plot(angles, amps_z, label="Electrode in $yz$-plane")
        plt.xlabel("Angle (degrees)")
        plt.ylabel(datalabel)
        plt.ylim(bottom=0, top=1.0)
        plt.yticks(np.arange(0, 1, step=0.1))
        plt.xticks(np.arange(0, 90, step=10))
        plt.grid(True)
        plt.legend(title="Electrode orientation")
        plt.title("Frequency 10kHz, anode 1000$\mu m$ above axon")

    elif plottype == "colour":
        ax1 = []
        ax2 = []
        for i in sorted(data.keys()):
            ax1.append(i)
            for j in sorted(data[i].keys()):
                if j not in ax2:
                    ax2.append(j)
        matrix = np.zeros((len(ax1), len(ax2)))
        for i in range(len(ax1)):
            for j in range(len(ax2)):
                if data[ax1[i]][ax2[j]] != {}:
                    matrix[i, j] = data[ax1[i]][ax2[j]][datatype] * datascalar
                else:
                    matrix[i, j] = np.nan
        # ax1 = [x / 1000 for x in ax1]
        ax2 = [x / 1000.0 for x in ax2]
        # Set up a regular grid of interpolation points
        X, Y = np.meshgrid(ax1, ax2)

        plt.pcolormesh(Y, X, matrix.T, cmap=cm.viridis_r)
        clb = plt.colorbar()
        clb.set_label(datalabel)
        plt.xlabel("Interpolar distance (mm)")
        plt.ylabel("Angle (degrees")
    plt.tight_layout()
    return plt