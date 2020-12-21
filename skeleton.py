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
#from scipy import signal
#import matplotlib.pyplot as plt
import wcslib as wcs

"""
Main
"""


def main():
    # Parameters
    Kb = 8     # Symbol width in samples
    fs = 16000   # Sampling frequency in Hz
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

    # TODO: Put your transmitter code here (feel free to modify any other parts
    # too, of course)

    # Carrier signal
    Wc = np.pi/2
    A = np.sqrt(2)
    xc = A*np.sin(Wc)

    # Channel simulation
    # TODO: Enable channel simulation.
    # N.B.: Requires the sampling frequency fs as an input
    yr = wcs.simulate_channel(xm, fs)

    # TODO: Put your receiver code here. Replace the three lines below, they
    # are only there for illustration and as an MWE. Feel free to modify any
    # other parts of the code as you see fit, of course.
    yb = xb*np.exp(1j*np.pi/5) + 0.1*np.random.randn(xb.shape[0])
    ybm = np.abs(yb)
    ybp = np.angle(yb)

    # Baseband and string decoding
    br = wcs.decode_baseband_signal(ybm, ybp, Kb)
    data_rx = wcs.decode_string(br)
    print('Received: ' + data_rx)


if __name__ == "__main__":
    main()
