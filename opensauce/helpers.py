"""Helper functions for OpenSauce

"""

# Licensed under Apache v2 (see LICENSE)

from __future__ import division

import math
import fileinput

import numpy as np
from scipy.io import wavfile


def wavread(fn):
    """Read in a 16-bit integer PCM WAV file for processing

    Args:
        fn - filename of WAV file [string]

    Returns:
         y_float - Audio samples in float format [NumPy vector]
         y_int - Audio samples in int format [NumPy vector]
        Fs - Sampling frequency in Hz [integer]

    Emulate the parts of the Matlab wavread function that we need.

    Matlab's wavread is used by voicesauce to read in the wav files for
    processing.  As a consequence, all the translated algorithms assume the
    data from the wav file is in matlab form, which in this case means a double
    precision float between -1 and 1.  The corresponding scipy function returns
    the actual integer PCM values from the file, which range between -32768 and
    32767.  (matlab's wavread *can* return the integers, but does not by
    default and voicesauce uses the default).  Consequently, after reading the
    data using scipy's io.wavfile, we convert to float by dividing each integer
    by 32768.

    Also, save the 16-bit integer data in another NumPy vector.

    The input WAV file is assumed to be in 16-bit integer PCM format.
    """
    # For reference, I figured this out from:
    # http://mirlab.org/jang/books/audiosignalprocessing/matlab4waveRead.asp?title=4-2%20Reading%20Wave%20Files
    # XXX: if we need to handle 8 bit files we'll need to detect them and
    # special case them here.
    try:
        Fs, y = wavfile.read(fn)
    except ValueError:
        raise
    if y.dtype != 'int16':
        raise IOError('Input WAV file must be in 16-bit integer PCM format')

    return y/np.float64(32768.0), y, Fs


def round_half_away_from_zero(x):
    """Rounds a number according to round half away from zero method

    Args:
        x - number [float]

    Returns:
        q - rounded number [integer]

    For example:
       round_half_away_from_zero(3.5) = 4
       round_half_away_from_zero(3.2) = 3
       round_half_away_from_zero(-2.7) = -3
       round_half_away_from_zero(-4.3) = -4

    The reason for writing our own rounding function is that NumPy uses the
    round-half-to-even method. There is a Python round() function, but it
    doesn't work on NumPy vectors. So we wrote our own
    round-half-away-from-zero method here.
    """
    q = np.int_(np.sign(x) * np.floor(np.abs(x) + 0.5))

    return q

def remove_empty_lines_from_file(fn):
    """ Remove empty lines from a text file

    Args:
        fn - filename [string]

    Returns: nothing

    Has side effect of removing empty lines from file specified by fn
    """
    f = fileinput.FileInput(fn, inplace=True)

    for line in f:
        stripped_line = line.rstrip()
        if stripped_line:
            print(stripped_line)

    f.close()

def convert_boolean_for_praat(b):
    """ Convert Python boolean for use in Praat

    Praat uses "yes"/"no" or 1/0 values instead of True/False.
    Convert True to "yes", False to "no"
    """
    if b == True:
        return "yes"
    elif b == False:
        return "no"
    else:
        raise ValueError('Input must be a Boolean')
