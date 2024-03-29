#!/usr/bin/env python3
"""
Main routines for creating plots from output-files.
"""

import os.path
import numpy as np
import matplotlib.pyplot as plt


def main():
    '''
    Creates plot from given directory as .pdf file with optional scaling
    adjustments for xy-boundries and amplitudes. Plot contains wavefunctions,
    potential and expvalues. Searches for .dat input files in home directory
    or asks for an input directory if not all of them are there.
    '''

    # set directory
    directory = _check_directory()

    # import data:
    (energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
     wavefuncs_ydata, expvalues_data) = _importdata(directory)

    _auto_make_plot(energies_data, potential_xdata, potential_ydata,
                    wavefuncs_xdata, wavefuncs_ydata, expvalues_data)

    # manually adjust scale or amplitude:
    adjust_limits = input("Manually adjust limits and amplitude? [y/n]")
    if str(adjust_limits) == "y":
        _manual_make_plot(energies_data, potential_xdata, potential_ydata,
                          wavefuncs_xdata, wavefuncs_ydata, expvalues_data)


def _importdata(directory):

    energiesdir = os.path.join(directory, "energies.dat")
    potentialdir = os.path.join(directory, "potential.dat")
    wavefuncsdir = os.path.join(directory, "wavefuncs.dat")
    expvaluesdir = os.path.join(directory, "expvalues.dat")

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
        expvalues_data = np.loadtxt(str(expvaluesdir))

    return(energies_data, potential_xdata, potential_ydata, wavefuncs_xdata,
           wavefuncs_ydata, expvalues_data)


def _auto_make_plot(energies_data, potential_xdata, potential_ydata,
                    wavefuncs_xdata, wavefuncs_ydata, expvalues_data):

    plt.figure(figsize=(10, 10), dpi=80)

    # plot 1:
    plt.subplot(1, 2, 1)  # plotting wavefunctions, energies and potential

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # wavefunctions
    y_wave = np.zeros(len(wavefuncs_xdata), dtype=float)

    for j in range(0, len(energies_data)):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] + energies_data[j]
        if j % 2 == 0:
            plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="red")
        else:
            plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="blue")

    # potential
    plt.plot(potential_xdata, potential_ydata, linestyle="-", color="black")

    # expected values x
    for o in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[o, 0], energies_data[o], 'x', markersize=10,
                 color="purple")

    # formatting
    lim_wave = [min(potential_xdata),
                max(potential_xdata),
                min(potential_ydata) - abs(min(potential_ydata)-0.5) * 0.1,
                (energies_data[len(energies_data)-1] +
                 energies_data[len(energies_data)-1] * 0.1)]
    if abs(lim_wave[3]) <= 0.5:
        lim_wave[3] = lim_wave[3] + 0.25

    plt.xlabel("x [Bohr]", size=16)
    plt.ylabel("Energies [Hartree]", size=16)
    plt.title("Potential, Eigenstates", size=20)
    _format(lim_wave)

    # plot 2:
    plt.subplot(1, 2, 2)  # plotting energy levels and exp-values

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # expvalues
    for m in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[m, 1], energies_data[m], 'x', markersize=10,
                 color="purple")

    # formatting
    x_max_exp = np.zeros(len(expvalues_data), dtype=float)
    for i in range(len(expvalues_data)):
        x_max_exp[i] = expvalues_data[i, 1]

    lim_exp = [0,
               max(x_max_exp) + max(x_max_exp) * 0.1,
               lim_wave[2],
               lim_wave[3]]

    plt.xlabel("x [Bohr]", size=16)
    plt.title(r'$\sigma_x$', size=20)
    _format(lim_exp)

    # saving plot
    plt.savefig('plots.pdf', format='pdf')
    print("Plot image saved as plots.pdf")


def _manual_make_plot(energies_data, potential_xdata, potential_ydata,
                      wavefuncs_xdata, wavefuncs_ydata, expvalues_data):

    # set manual limits and amplitude factor

    # formatting
    # plot 1:
    lim_wave = [min(potential_xdata),
                max(potential_xdata),
                (min(potential_ydata) - abs(min(potential_ydata)-0.5) * 0.1),
                (energies_data[len(energies_data)-1] +
                 energies_data[len(energies_data)-1] * 0.1)]
    if abs(lim_wave[3]) <= 0.5:
        lim_wave[3] = lim_wave[3] + 0.25

    # plot 2:
    x_max_exp = np.zeros(len(expvalues_data), dtype=float)
    for i in range(len(expvalues_data)):
        x_max_exp[i] = expvalues_data[i, 1]

    # set amplitude factor for first plot
    amplitude = 1
    input_amplitude = input("set amplitude (default: 1):")
    amplitude = float(input_amplitude)

    # setting manual limits of wave plot
    manual_limits = input("Set limits of wavefunction plot (format: [x-min, "
                          "x-max, y-min, y-max], default = d):")
    manual_lim_wave = manual_limits.split(", ")

    for i in range(len(lim_wave)):  # check which limits have to be replaced
        if manual_lim_wave[i].lstrip('-').replace(".", "", 1).isdigit():
            lim_wave[i] = float(manual_lim_wave[i])

    # limits of expval plot
    lim_exp = [0,
               max(x_max_exp) + max(x_max_exp) * 0.1,
               lim_wave[2],
               lim_wave[3]]

    plt.figure(figsize=(10, 10), dpi=80)

    # plot 1
    plt.subplot(1, 2, 1)  # plotting wavefunctions, energies and potential

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # wavefunctions
    y_wave = np.zeros(len(wavefuncs_xdata), dtype=float)
    for j in range(0, len(energies_data), 1):
        for k in range(0, len(wavefuncs_xdata)):
            y_wave[k] = wavefuncs_ydata[k, j] * amplitude + energies_data[j]
        if j % 2 == 0:  # set different colors
            plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="red")
        else:
            plt.plot(wavefuncs_xdata, y_wave, linestyle="-", color="blue")

    # potential
    plt.plot(potential_xdata, potential_ydata, linestyle="-", color="black")

    # expected values
    for o in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[o, 0], energies_data[o], 'x', markersize=10,
                 color="purple")

    # setting format
    plt.xlabel("x [Bohr]", size=16)
    plt.ylabel("Energies [Hartree]", size=16)
    plt.title("Potential, Eigenstates\nAmplitude {}"
              .format(amplitude), size=20)
    _format(lim_wave)

    # plot 2:
    plt.subplot(1, 2, 2)  # plotting energy levels and expvalues

    # energy levels
    for y_energy_data in energies_data:
        x_energy = [wavefuncs_xdata[0],
                    wavefuncs_xdata[len(wavefuncs_xdata)-1]]
        y_energy = [y_energy_data, y_energy_data]
        plt.plot(x_energy, y_energy, linestyle="--", color="grey")

    # expvalues
    for m in range(0, len(expvalues_data)):
        plt.plot(expvalues_data[m, 1], energies_data[m], 'x', markersize=10,
                 color="purple")

    # setting format
    plt.xlabel("x [Bohr]", size=16)
    plt.title(r'$\sigma_x$', size=20)
    _format(lim_exp)

    # saving plot
    plt.savefig('manual_plots.pdf', format='pdf')
    print("Plot image saved as manual_plots.pdf")


def _format(array):
    plt.xlim(array[0], array[1])
    plt.ylim(array[2], array[3])


def _check_directory():
    files = ('energies.dat', 'potential.dat', 'wavefuncs.dat', 'expvalues.dat')

    for file in files:
        if os.path.exists(file) is False:
            print("Missing files in home directory.")
            directory = input("Enter new directory of data files: ")
            return directory
    print("Data found in home directory, visualizing...")
    return str(r".")


if __name__ == "__main__":
    main()
