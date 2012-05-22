#!/usr/bin/env python

"""
hackdiet.py: Weight, Body-fat, and Wakeup-time plotting inspired by the
Hacker's Diet online by John Walker.

:author: Robert David Grant <robert.david.grant@gmail.com>

:copyright:
    Copyright 2012 Robert David Grant

    Licensed under the Apache License, Version 2.0 (the "License"); you
    may not use this file except in compliance with the License.  You
    may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.  See the License for the specific language governing
    permissions and limitations under the License.
"""

from __future__ import division

import sys
import matplotlib.pyplot as plt
from numpy import NaN, arange, zeros
from pandas import *


DATAPATH = './data.tsv'


def convert_time_string(timestring):
    """Take a time string from the Wake column, return number of hours since
    midnight as a float.
    """
    hour, minute = map(int, timestring.split(':'))
    rval = hour + minute/60
    return rval


def convert_time_col(timestrings):
    """Convert the Wake column (strings) to number of hours since midnight
    (floats).
    """
    idx = timestrings.notnull()
    timestrings[idx] = timestrings[idx].apply(convert_time_string)
    return timestrings


def read_data(path=DATAPATH):
    """Parse the data."""
    dta = read_table(path, header=1, index_col=0, parse_dates=True,
            skiprows=[0])
    dta.Wake = convert_time_col(dta.Wake)
    return dta.convert_objects()


def show_data(start=0, path=DATAPATH, floaters=True, floatstyle='.',
        nofloatstyle='k,'):
    """Plot the data.

    `start`   : Integer offset from beginning of data (in days) to allow
                plotting only recent data.  If negative, works as an offset
                from end of data.
    `path`    : Path to the tab-separated value file containing the data.
    `floaters`: Boolean indicating whether you want 'floaters and sinkers'
                plotted like in the original Hacker's Diet online.
    `floatstyle`: If floaters are used, pass this style parameter to
                matplotlib.
    `nofloatstyle`: If floaters are not used, pass this style parameter to
                matplotlib.
    """
    wakeup_goal = 7  # reference line in Wakeup-time plot
    window = 20 # ndays in exponentially-weighted moving average
    fig, axs = plt.subplots(nrows=3, sharex=True)

    data = read_data(path)

    # Wakeup-time plot
    wake_delta = data.Wake - wakeup_goal
    if floaters:
        axs[2].errorbar(data.index[start:], data.Wake[start:],
                [wake_delta[start:], zeros(len(data.index))[start:]],
                ecolor='g', capsize=0, fmt=floatstyle)
        axs[2].axhline(7, color='r')
    else:
        data.Wake[start:].plot(ax=axs[2], style=nofloatstyle)
        axs[2].axhline(8, color='r')
        axs[2].axhline(5, color='r')
    axs[2].set_ylim((0,24))
    axs[2].set_yticks(arange(1,24,3))
    axs[2].set_yticklabels(map(lambda t: '%02d'%(t,), arange(1,24,3)))
    axs[2].set_ylabel('Wake Time')
    axs[2].grid(axis='both')

    # Weight plot
    weight_avg = ewma(data.Weight, window)
    weight_delta = data.Weight - weight_avg
    if floaters:
        axs[0].errorbar(data.index[start:], data.Weight[start:],
                [weight_delta[start:], zeros(len(data.index))[start:]],
                ecolor='g', capsize=0, fmt=floatstyle)
    else:
        data.Weight[start:].plot(ax=axs[0], style=nofloatstyle)
    weight_avg[start:].plot(ax=axs[0])
    axs[0].set_ylabel('Weight')

    # Body fat plot
    bf_avg = ewma(data.BF, window)
    bf_delta = data.BF - bf_avg
    if floaters:
        axs[1].errorbar(data.index[start:], data.BF[start:],
                [bf_delta[start:], zeros(len(data.index))[start:]],
                ecolor='g', capsize=0, fmt=floatstyle)
    else:
        data.BF[start:].plot(ax=axs[1], style=nofloatstyle)
    bf_avg[start:].plot(ax=axs[1])
    axs[1].set_ylabel('% Body Fat')

    axs[0].set_title('Life Data')
    fig.text(0.5, 0.05, 'wt: %.1f    bf: %.1f'%(weight_avg[-1], bf_avg[-1]),
            horizontalalignment='center', verticalalignment='bottom')
    #print "Weight est: %4.1f lbs"%(weight_avg[-1],)
    #print "    BF est: %4.1f%%"%(bf_avg[-1],)

    for ax in axs:
        ax.tick_params(axis='y', labelleft='on', labelright='on')

    plt.show()


def summarize(start=0):
    """Return the pandas summary of the data."""
    data = read_data()
    return data[start:].describe()


def cli(argv):
    """
    Simple command-line interface.  Interprets a single command-line
    argument as an offset for the range of data to be plotted.  E.g.

    >>> ./hackdiet.py -30

    plots data for the last 30 days.

    >>> ./hackdiet.py 360

    plots all data except for the first 360 days.  If plotting all the
    data it doesn't put points on the floaters (it looks too cluttered).
    Else, it does.

    TODO: Rewrite with argparse
    """
    if len(argv) > 1:
        start = int(argv[1])
    else:
        start = 0

    if start is 0:
        floatstyle = None
    else:
        floatstyle = '.'

    show_data(start, floatstyle=floatstyle)


if __name__ == '__main__':
    cli(sys.argv)
