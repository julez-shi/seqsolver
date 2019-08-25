# -*- coding: utf-8 -*-
"""
Main function for creating plots from data-files

@author: Ruben
"""
import numpy as np
import matplotlib.pyplot as plt


def importdata(directory):
    '''Function, which creates six arrays from potential.dat, energies.dat,
    wavefunc.dat and expvalues.dat files.

    Args:
        directory: Argument containing the directory of input .dat files.

    Returns:
        energies_data: Array with energie data (eigenvalues).
        potential_xdata: Array with potential x-data.
        potential_ydata: Array with potential y-data.
        wavefuncs_xdata: Array with wavefunction x-data.
        wavefuncs_ydata: Array with wavefunction y-data
                         [[y1(x1), y2(x1), ...], ..., [y1(xn), y2(xn), ...]].
        expvalues_xdata: Array with expvalues x-data.
        expvalues_ydata: Array with expvalues y-data.
        '''
    energiesdir = ".\\" + directory + "\energies.dat"
    potentialdir = ".\\" + directory + "\potential.dat"
    wavefuncsdir = ".\\" + directory + "\wavefuncs.dat"
    expvaluesdir = ".\\" + directory + "\expvalues.dat"

    with open(str(energiesdir), "r"):
        energies_data = np.loadtxt(str(energiesdir))

    with open(str(potentialdir), "r"):
        potential_rawdata = np.loadtxt(str(potentialdir))

        potential_xdata = np.zeros(len(potential_rawdata), dtype=float)
        potential_ydata = np.zeros(len(potential_rawdata), dtype=float)
        for i in range(0, len(potential_rawdata)):
            potential_xdata[i] = potential_rawdata[i, 0]
            potential_ydata[i] = potential_rawdata[i, 1]

    with open(str(wavefuncsdir), "r"):
        wavefuncs_rawdata = np.loadtxt(str(wavefuncsdir))

        wavefuncs_xdata = np.zeros(len(wavefuncs_rawdata), dtype=float)
        for k in range(0, len(wavefuncs_rawdata)):
            wavefuncs_xdata[k] = wavefuncs_rawdata[k, 0]

        wavefuncs_ydata = np.zeros((len(wavefuncs_rawdata),
                                    len(wavefuncs_rawdata[0])-1), dtype=float)
        for n in range(0, len(wavefuncs_rawdata)):
            for m in range(0, len(wavefuncs_rawdata[0])-1):
                wavefuncs_ydata[n, m] = wavefuncs_rawdata[n, m+1]

    with open(str(expvaluesdir), "r"):
        expvalues_rawdata = np.loadtxt(str(expvaluesdir))

        expvalues_xdata = np.zeros(len(expvalues_rawdata), dtype=float)
        expvalues_ydata = np.zeros(len(expvalues_rawdata), dtype=float)
        for j in range(0, len(expvalues_rawdata)):
            expvalues_xdata[j] = expvalues_rawdata[j, 0]
            expvalues_ydata[j] = expvalues_rawdata[j, 1]

    return(energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
           wavefuncs_ydata, expvalues_xdata, expvalues_ydata)


def make_plot(energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
              wavefuncs_ydata, expvalues_xdata, expvalues_ydata):
    '''Trying to make two plots from data createn by importdata-function.

    Args:
        energies_data: Array with energie data (eigenvalues).
        potential_xdata: Array with potential x-data.
        potential_ydata: Array with potential y-data.
        wavefuncs_xdata: Array with wavefunction x-data.
        wavefuncs_ydata: Array with wavefunction y-data
                         [[y1(x1), y2(x1), ...], ..., [y1(xn), y2(xn), ...]].
        expvalues_xdata: Array with expvalues x-data.
        expvalues_ydata: Array with expvalues y-data.

    Returns:
        Plot saved as pdf or png file.
    '''
    plt.figure(figsize=(10, 10), dpi=80)

    plt.subplot(1, 2, 1)  # plotting wavefunctions, energies and potential

    # energy levels
    for i in range(0, len(energies_data)):
        x_energy = [wavefuncs_xdata[0], wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [energies_data[i], energies_data[i]]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # wavefunctions
    y_wave = np.zeros(len(wavefuncs_xdata), dtype=float)
    for j in range(0, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="red")

    for j in range(1, len(energies_data), 2):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] + energies_data[j]
        plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="blue")
    # potential
    plt.plot(potential_xdata, potential_ydata, linestyle="-", color="black")

    # format
    plt.ylim(min(potential_ydata), energies_data[len(energies_data)-1] + 1)



    #plt.savefig('test.pdf', format='pdf')

directory = str()

def plot(directory):

    (energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
 wavefuncs_ydata, expvalues_xdata, expvalues_ydata) = importdata(directory)

    make_plot(energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
          wavefuncs_ydata, expvalues_xdata, expvalues_ydata)