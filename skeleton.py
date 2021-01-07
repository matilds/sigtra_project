#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skeleton for the wireless communication system project in Signals and
Transforms

For plain text inputs, run:
$ python3 skeleton.py "Hello World!"

For binary inputs, run:
$ python3 skeleton.py -b 010010000110100100100001

2020 -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import sys
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import wcslib as wcs

"""
Main
"""


def main():
    loop = 10

    # Detect input or set defaults
    string_data = True
    if len(sys.argv) == 2:
        data = str(sys.argv[1])

    elif len(sys.argv) == 3 and str(sys.argv[1]) == '-b':
        string_data = False
        data = str(sys.argv[2])

    else:
        print('Warning: No input arguments, using defaults.', file=sys.stderr)
        data = "Hello World!"

    # Convert string to bit sequence or string bit sequence to numeric bit
    # sequence
    if string_data:
        bs = wcs.encode_string(data)
    else:
        bs = np.array([bit for bit in map(int, data)])

    for i in range(0, loop):
        transmit(bs)


def transmit(bs):
    # Parameters
    Kb = 320  # Symbol width in samples
    fs = 16000  # Sampling frequency in Hz

    #####################
    #####TRANSMITTER#####
    #####################

    # Encode baseband signal
    xb = wcs.encode_baseband_signal(bs, Kb)

    # Optional plotting of the baseband signal
    """fig, ax = plt.subplots()
    ax.plot(np.arange(0, len(xb), 1), xb)
    ax.grid()
    plt.xticks(np.arange(0, 30, 1))
    plt.show()"""

    # Carrier signal
    k = np.arange(0, len(xb), 1)
    Wc = np.pi / 2
    A = np.sqrt(2)
    xc = A * np.sin(Wc * k)

    # Optional plotting of the carrier signal
    """fig, ax = plt.subplots()
    ax.plot(k[0:30], xc[0:30])
    ax.grid()
    plt.xticks(np.arange(0, 30, 1))
    plt.show()"""

    # Modulated signal
    xm = xc * xb

    # Optional plotting of the modulated signal
    """fig, ax = plt.subplots()
    ax.plot(np.arange(0, 30, 1), xm[0:30])
    ax.grid()
    plt.xticks(np.arange(0, 30, 1))
    plt.show()"""

    # Filtered signal (band-limited signal)
    # IIR Band pass filter
    ws = 2 * np.pi * fs
    nq = ws / 2
    wpass = [(2 * np.pi * 3900) / nq,
             (2 * np.pi * 4100) / nq]  # Normalized
    wstop = [(2 * np.pi * 3850) / nq,
             (2 * np.pi * 4150) / nq]  # Normalized
    Apass = 3
    Astop = 20
    N, wn = signal.cheb1ord(wpass, wstop, Apass, Astop)
    b, a = signal.cheby1(N, Apass, wn, btype='bandpass')

    # To check stability with poles
    # z, p, k = signal.cheby1(N, Apass, wn, btype='bandpass', output='zpk')
    # print(p)

    xt = signal.lfilter(b, a, xm)

    # Channel simulation
    # N.B.: Requires the sampling frequency fs as an input
    yr = wcs.simulate_channel(xt, fs)

    ##################
    #####RECEIVER#####
    ##################

    # Filtered signal (band-limited signal)
    # IIR Band pass filter (Reusing from the transmitter)
    ym = signal.lfilter(b, a, yr)
    # Demodulated signal
    yId = ym * np.cos(Wc * k)
    yQd = -ym * np.sin(Wc * k)

    # Low-pass filtered IQ-signals (pure IQ baseband signals)
    wpass = (2 * np.pi * 1000) / nq  # Normalized
    wstop = (2 * np.pi * 4000) / nq  # Normalized
    Apass = 1
    Astop = 50

    N, wn = signal.cheb1ord(wpass, wstop, Apass, Astop)
    b, a = signal.cheby1(N, Apass, wn, btype='lowpass')

    # To check stability with poles
    # z, p, k = signal.cheby1(N, Apass, wn, btype='lowpass', output='zpk')
    # print(p)

    yIb = signal.lfilter(b, a, yId)
    yQb = signal.lfilter(b, a, yQd)

    yb = yIb + 1j * yQb

    # Recover symbol information and transmissions
    ybp = np.angle(yb)  # Phase
    ybm = np.abs(yb)  # Magnitude

    # Baseband and string decoding
    br = wcs.decode_baseband_signal(ybm, ybp, Kb)
    data_rx = wcs.decode_string(br)
    print('Received: ' + data_rx)

    # Optional plotting of received baseband signal
    """fig, ax = plt.subplots()
    ax.plot(np.arange(0, len(br), 1), br)
    ax.grid()
    plt.show()"""


if __name__ == "__main__":
    main()
