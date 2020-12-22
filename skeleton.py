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
    # Parameters
    Kb = 8  # Symbol width in samples
    fs = 16000  # Sampling frequency in Hz
    # ...

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

    # Encode baseband signal
    xb = wcs.encode_baseband_signal(bs, Kb)

    # Optional plotting of the baseband signal
    """fig, ax = plt.subplots()
    ax.plot(np.arange(0, 30, 1), xb[0:30])
    ax.grid()
    plt.xticks(np.arange(0, 30, 1))
    plt.show()"""

    # TODO: Put your transmitter code here (feel free to modify any other parts
    # too, of course)

    # Carrier signal
    k = np.arange(0, len(xb), 1)  # TODO: Range of k?
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

    # Filtered signal (band-limited signal)  # TODO
    # xt = ...

    # Channel simulation
    # TODO: Enable channel simulation.
    # N.B.: Requires the sampling frequency fs as an input
    # yr = wcs.simulate_channel(xt, fs)

    # TODO: Put your receiver code here. Feel free to modify any
    # other parts of the code as you see fit, of course.

    # Filtered signal (band-limited signal)  # TODO
    # ym = ...

    # Demodulated signal # TODO: Uncomment when filtered signal is done
    # yId = ym*np.cos(Wc*k)
    # yQd = -ym*np.sin(Wc*k)

    # Low-pass filtered IQ-signals (pure IQ baseband signals)  # TODO
    # yIb = ...
    # yQb = ...
    # yb = yIb + 1j*yQb

    # TODO: Replace the three lines below, they are only there for
    #  illustration and as an MWE.
    yb = xb * np.exp(1j * np.pi / 5) + 0.1 * np.random.randn(xb.shape[0])  #
    # Should be removed
    ybm = np.abs(yb)  # Should be: ybm = np.abs(yb) (already correct)
    ybp = np.angle(yb)

    # Baseband and string decoding
    br = wcs.decode_baseband_signal(ybm, ybp, Kb)
    data_rx = wcs.decode_string(br)
    print('Received: ' + data_rx)


if __name__ == "__main__":
    main()
