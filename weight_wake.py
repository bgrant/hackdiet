#!/usr/bin/env python

from __future__ import division

import sys
import matplotlib.pyplot as plt
from numpy import NaN, arange, zeros
from pandas import *


def convert_time_string(timestring):
    if timestring == 'NA':
        rval = NaN
    else:
        hour, minute = map(int, timestring.split(':'))
        rval = hour + minute/60
    return rval


def read_data(filename='weight.tsv'):
    return read_table(filename, header=1, index_col=0, parse_dates=True,
            converters={'Wake': convert_time_string})


def show_data(start=0, floatstyle='.', nofloatstyle='k,', floaters=True,
        path='/Users/bgrant/documents/life/data/weight-wake/weight.tsv'):
    plt.close('all')
    data = read_data(path)

    wakeup_goal = 7
    window = 20 # days
    fig, axs = plt.subplots(nrows=3, sharex=True)

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
    data = read_data()
    return data[start:].describe()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        start = int(sys.argv[1])
    else:
        start = 0

    if start is 0:
        floatstyle = None
    else:
        floatstyle = '.'

    show_data(start, floatstyle=floatstyle)
