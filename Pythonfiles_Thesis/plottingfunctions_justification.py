import pylab as plt
import numpy as np

##########################################################
# VISUALIZATION OF PROPOSED METHOD RESULTS VERSUS CLASSIC METHOD RESULTS
##########################################################
# Plots '2 dimensional' results
def plotjustification2D(classicres, proposedres):
    amplitudes  = {}
    for i in classicres:
        for j in classicres[i]:
            for k in classicres[i][j]:
                if classicres[i][j][k] != {}:
                    if classicres[i][j][k]["Frequency"] in amplitudes:
                        if classicres[i][j][k]["Amplitude"] > amplitudes[classicres[i][j][k]["Frequency"]]:
                            amplitudes[classicres[i][j][k]["Frequency"]] = classicres[i][j][k]["Amplitude"]
                    else:
                        amplitudes[classicres[i][j][k]["Frequency"]] = classicres[i][j][k]["Amplitude"]

    lists = sorted(amplitudes.items())
    fc, ac = zip(*lists)
    plt.plot(fc, ac, color= 'darkgrey', linestyle='-', label='Classic Method')

    amplitudes_prop = {}
    for i in proposedres:
        if proposedres[i] != {}:
            if proposedres[i]["Frequency"] in amplitudes_prop:
                if proposedres[i]["Amplitude"] > amplitudes_prop[proposedres[i]["Frequency"]]:
                    amplitudes_prop[proposedres[i]["Frequency"]] = proposedres[i]["Amplitude"]
            else:
                amplitudes_prop[proposedres[i]["Frequency"]] = proposedres[i]["Amplitude"]

    lists = sorted(amplitudes_prop.items())
    fp, ap = zip(*lists)
    plt.plot(fp, ap, 'b-', label='Proposed Method')

    plt.xlabel("Frequency (kHz)")
    plt.xticks(np.arange(0,45,5))
    plt.xlim(left=0,right=45)
    plt.ylabel("Minimal blocking amplitude (mA)")
    plt.ylim([0, 1])
    plt.grid()
    plt.legend()
    plt.tight_layout()

    return plt


def plotjustification2Dcpp(classicres, proposedres):
    amplitudes  = {}
    for i in classicres:
        for j in classicres[i]:
            for k in classicres[i][j]:
                if classicres[i][j][k] != {}:
                    cpp = classicres[i][j][k]["Amplitude"] / (np.pi * classicres[i][j][k]["Frequency"])
                    if classicres[i][j][k]["Frequency"] in amplitudes:
                        if cpp > amplitudes[classicres[i][j][k]["Frequency"]]:
                            amplitudes[classicres[i][j][k]["Frequency"]] = cpp
                    else:
                        amplitudes[classicres[i][j][k]["Frequency"]] = cpp

    lists = sorted(amplitudes.items())
    fc, ac = zip(*lists)
    plt.plot(fc, ac, color= 'darkgrey', linestyle='-', label='Classic Method')

    amplitudes_prop = {}
    for i in proposedres:
        if proposedres[i] != {}:
            cpp = proposedres[i]["Amplitude"] / (np.pi * proposedres[i]["Frequency"])
            if proposedres[i]["Frequency"] in amplitudes_prop:
                if cpp > amplitudes_prop[proposedres[i]["Frequency"]]:
                    amplitudes_prop[proposedres[i]["Frequency"]] = cpp
            else:
                amplitudes_prop[proposedres[i]["Frequency"]] = cpp

    lists = sorted(amplitudes_prop.items())
    fp, ap = zip(*lists)
    plt.plot(fp, ap, 'b-', label='Proposed Method')

    plt.xlabel("Frequency (kHz)")
    plt.xticks(np.arange(0,45,5))
    plt.xlim(left=0,right=45)

    plt.ylabel("Threshold charge per phase ($\mu C$)")
    plt.ylim([0, 0.05])

    plt.grid()
    plt.legend()
    plt.tight_layout()
    return plt


# Plots '3 dimensional' results (e.g. chargebalance)
def plotjustification3D(classicres, proposedres, type):     # If type is subplots, build all results in smaller subplots
    amplitudes  = {}

    for i in classicres:
        for j in classicres[i]:
            for k in classicres[i][j]:
                for l in classicres[i][j][k]:
                    if classicres[i][j][k][l] != {}:
                        if k not in amplitudes:
                            amplitudes[k] = {}

                        if classicres[i][j][k][l]["Frequency"] in amplitudes[k]:
                            if classicres[i][j][k][l]["Amplitude"] > amplitudes[k][classicres[i][j][k][l]["Frequency"]]:
                                amplitudes[k][j][classicres[i][j][k][l]["Frequency"]] = classicres[i][j][k][l]["Amplitude"]
                        else:
                            amplitudes[k][classicres[i][j][k][l]["Frequency"]] = classicres[i][j][k][l]["Amplitude"]


    amplitudes_prop = {}
    for i in proposedres:
        if i not in amplitudes_prop:
            amplitudes_prop[i] = {}
        for j in proposedres[i]:
            if proposedres[i][j] != {}:
                if proposedres[i][j]["Frequency"] in amplitudes_prop[i]:
                    if proposedres[i][j]["Amplitude"] > amplitudes_prop[i][proposedres[i][j]["Frequency"]]:
                        amplitudes_prop[i][proposedres[i][j]["Frequency"]] = proposedres[i][j]["Amplitude"]
                else:
                    # frequencies.append(proposedres[i][j]["Frequency"])
                    amplitudes_prop[i][proposedres[i][j]["Frequency"]] = proposedres[i][j]["Amplitude"]

    if type == "largeplot":
        lists = {}
        for i in sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            plt.plot(fc, ac, 'k-', label='Classic Method CB=' + str(i))

        lists = {}
        for i in sorted(amplitudes_prop):
            lists[i] = sorted(amplitudes_prop[i].items())
            fc, ac = zip(*lists[i])
            plt.plot(fc, ac, 'b-', label='Proposed Method CB=' + str(i))


    elif type == "subplots":
        figheight = 3
        figwidth = 4
        fig, axarr = plt.subplots(figheight, figwidth)

        lists = {}
        lists_prop = {}
        plotnum = 0
        for i in sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            subplt.plot(fc, ac, 'k-', label='Classic Method CB=' + str(i))
            subplt.set_title('Chargebalance = ' + str(i))

            lists_prop[i] = sorted(amplitudes_prop[i].items())
            fc_prop, ac_prop = zip(*lists_prop[i])
            subplt.plot(fc_prop, ac_prop, 'b-', label='Proposed Method CB=' + str(i))

            plotnum += 1
            subplt.set_ylim([0, 1])
            subplt.legend()

        for i in range(plotnum, figheight*figwidth):
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            fig.delaxes(subplt)
            plotnum +=1

    else :
        print "No type selected! Choose 'largeplot' or 'subplots'"
        return None

    return plt


# Plots '3 dimensional' results  Chargeperphase(e.g. chargebalance)
def plotjustification3Dcpp(classicres, proposedres, type, balance = 0.5, freqname = "Frequency", chargename = "Chargeperphase"):     # If type is subplots, build all results in smaller subplots
    amplitudes = {}

    for i in classicres:
        for j in classicres[i]:
            for k in classicres[i][j]:
                for l in classicres[i][j][k]:
                    if classicres[i][j][k][l] != {}:
                        if k not in amplitudes:
                            amplitudes[k] = {}

                        if classicres[i][j][k][l]["Frequency"] in amplitudes[k]:
                            if classicres[i][j][k][l]["Chargeperphase"] > amplitudes[k][classicres[i][j][k][l]["Frequency"]]:
                                amplitudes[k][j][classicres[i][j][k][l]["Frequency"]] = classicres[i][j][k][l]["Chargeperphase"]
                        else:
                            amplitudes[k][classicres[i][j][k][l]["Frequency"]] = classicres[i][j][k][l]["Chargeperphase"]


    amplitudes_prop = {}



    for i in proposedres:
        if i not in amplitudes_prop:
            amplitudes_prop[i] = {}
        for j in proposedres[i]:
            if proposedres[i][j] != {}:
                if proposedres[i][j][freqname] in amplitudes_prop[i]:
                    if proposedres[i][j][chargename] > amplitudes_prop[i][proposedres[i][j][freqname]]:
                        amplitudes_prop[i][proposedres[i][j][freqname]] = proposedres[i][j][chargename]
                else:
                    # frequencies.append(proposedres[i][j]["Frequency"])
                    amplitudes_prop[i][proposedres[i][j][freqname]] = proposedres[i][j][chargename]

    if type == "largeplot" or type == "singleCB":
        lists = {}
        for i in sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            if type == "largeplot" or (type == "singleCB" and i == balance):
                plt.plot(fc, ac, color='darkgrey', linestyle='-', label='Classic Method')

        lists = {}
        for i in sorted(amplitudes_prop):
            lists[i] = sorted(amplitudes_prop[i].items())
            fc, ac = zip(*lists[i])
            if type == "largeplot" or (type == "singleCB" and i == balance):
                plt.plot(fc, ac, color='b', linestyle='-', label='Proposed Method')
                if type == "singleCB":
                    plt.title('$T_{anode}$ = ' + str(i) + '$T_{signal}$', y=0.7)
        plt.ylim([0, 0.04])
        plt.xlabel("Frequency (kHz)")
        plt.ylabel("Threshold charge per phase ($\mu C$)")
        plt.legend()
        plt.grid()
        plt.xlim(left=0, right=45)
        plt.tight_layout()

    elif type == "subplots":
        figheight = 3
        figwidth = 4
        fig, axarr = plt.subplots(figheight, figwidth)

        lists = {}
        lists_prop = {}
        plotnum = 0
        for i in sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            ac = [1000 * a for a in ac]
            l1 = subplt.plot(fc, ac, 'k-')
            subplt.set_title('$T_{anode}$ = ' + str(i) + '$T$', y=0.8)

            lists_prop[i] = sorted(amplitudes_prop[i].items())
            fc_prop, ac_prop = zip(*lists_prop[i])
            ac_prop = [1000 * a for a in ac_prop]
            l2 = subplt.plot(fc_prop, ac_prop, 'b-')

            plotnum += 1
            subplt.set_ylim([0, 30])
            subplt.set_xlabel("Frequency (kHz)")
            subplt.set_ylabel("Charge per phase ($nC$)")
            # subplt.legend()

        for i in range(plotnum, figheight*figwidth):
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            fig.delaxes(subplt)
            plotnum +=1

        fig.legend([l1, l2], labels=["Classical Method", "Proposed Method"])#, loc='lower right')#, bbox_to_anchor=(0.6, 0.3))
        # plt.tight_layout()


    else :
        print "No type selected! Choose 'largeplot' or 'subplots'"
        return None

    return plt


##########################################################
# Plots classic versus proposed method per frequency -> REWRITE!
##########################################################
def plotjustification3Dcppreverse(classicres, proposedres, type):     # If type is subplots, build all results in smaller subplots
    amplitudes  = {}

    for i in classicres:
        for j in classicres[i]:
            for k in classicres[i][j]:
                for l in classicres[i][j][k]:
                    if classicres[i][j][k][l] != {}:
                        if j not in amplitudes:
                            amplitudes[j] = {}

                        if classicres[i][j][k][l]["Chargeperphase"] in amplitudes[j]:
                            if classicres[i][j][k][l]["Chargeperphase"] > amplitudes[j][classicres[i][j][k][l]["Chargebalance"]]:
                                amplitudes[j][k][classicres[i][j][k][l]["Chargebalance"]] = classicres[i][j][k][l]["Chargeperphase"]
                        else:
                            amplitudes[j][classicres[i][j][k][l]["Chargebalance"]] = classicres[i][j][k][l]["Chargeperphase"]


    amplitudes_prop = {}
    for i in proposedres:
        for j in proposedres[i]:
            if j not in amplitudes_prop:
                amplitudes_prop[j] = {}
            if proposedres[i][j] != {}:
                if proposedres[i][j]["Frequency"] in amplitudes_prop[j]:
                    if proposedres[i][j]["Chargeperphase"] > amplitudes_prop[j][proposedres[i][j]["Chargebalance"]]:
                        amplitudes_prop[j][proposedres[i][j]["Chargebalance"]] = proposedres[i][j]["Chargeperphase"]
                else:
                    # frequencies.append(proposedres[i][j]["Frequency"])
                    amplitudes_prop[j][proposedres[i][j]["Chargebalance"]] = proposedres[i][j]["Chargeperphase"]

    if type == "largeplot":
        lists = {}
        for i in range(4,6,2):# sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            plt.plot(fc, ac, 'k-', label='Classic Method CB=' + str(i))

        lists = {}
        for i in range(4,6,2):#  sorted(amplitudes_prop):
            lists[i] = sorted(amplitudes_prop[i].items())
            fc, ac = zip(*lists[i])
            plt.plot(fc, ac, 'b-', label='Proposed Method CB=' + str(i))

        plt.ylim([0, 0.1])

    elif type == "subplots":
        figheight = 3
        figwidth = 4
        fig, axarr = plt.subplots(figheight, figwidth)

        lists = {}
        lists_prop = {}
        plotnum = 0
        for i in sorted(amplitudes):
            lists[i] = sorted(amplitudes[i].items())
            fc, ac = zip(*lists[i])
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            l1 = subplt.plot(fc, ac, 'k-', label='Classic Method')
            subplt.set_title('$T_{hi}$ = ' + str(i) + '$T$')

            lists_prop[i] = sorted(amplitudes_prop[i].items())
            fc_prop, ac_prop = zip(*lists_prop[i])
            l2 = subplt.plot(fc_prop, ac_prop, 'b-', label='Proposed Method')

            plotnum += 1
            subplt.set_ylim([0, 0.03])
            # subplt.legend()

        for i in range(plotnum, figheight*figwidth):
            subplt = axarr[int(plotnum // figwidth), int(plotnum % figwidth)]
            fig.delaxes(subplt)
            plotnum +=1

        fig.legend([l1, l2], labels=["Classical Method", "Proposed Method"], loc='lower right')#, bbox_to_anchor=(0.6, 0.3))


    else :
        print "No type selected! Choose 'largeplot' or 'subplots'"
        return None

    return plt