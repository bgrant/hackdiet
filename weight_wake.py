from __future__ import division

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

def plot_data(start=0, floaters=True):
    plt.close('all')
    data = read_data()

    wakeup_goal = 7
    window = 20 # days
    fig, axs = plt.subplots(nrows=3, sharex=True)
    axs[0].set_title('Life Data')

    # Wakeup-time plot
    wake_delta = data.Wake - wakeup_goal
    wake_errs = [wake_delta, zeros(len(wake_delta))]
    if floaters:
        axs[2].errorbar(data.index[start:], data.Wake[start:],
                wake_errs[start:],
                ecolor='g', capsize=0, fmt=None)
        axs[2].axhline(7, color='r')
    else:
        data.Wake[start:].plot(ax=axs[2], style='k,')
        axs[2].axhline(8, color='r')
        axs[2].axhline(5, color='r')
    axs[2].set_ylim((0,24))
    axs[2].set_yticks(arange(1,24,3))
    axs[2].set_yticklabels(map(lambda t: '%02d'%(t,), arange(1,24,3)))
    axs[2].set_ylabel('Wake Time')

    # Weight plot
    weight_avg = ewma(data.Weight, window)
    weight_delta = data.Weight - weight_avg
    weight_errs = [weight_delta, zeros(len(weight_delta))]
    if floaters:
        axs[0].errorbar(data.index[start:], data.Weight[start:],
                weight_errs[start:],
                ecolor='g', capsize=0, fmt=None)
    else:
        data.Weight[start:].plot(ax=axs[0], style='k,')
    weight_avg[start:].plot(ax=axs[0])
    axs[0].set_ylabel('Weight')
    
    # Body fat plot
    bf_avg = ewma(data.BF, window)
    bf_delta = data.BF - bf_avg
    bf_errs = [bf_delta, zeros(len(bf_delta))]
    if floaters:
        axs[1].errorbar(data.index[start:], data.BF[start:], bf_errs[start:],
                ecolor='g', capsize=0, fmt=None)
    else:
        data.BF[start:].plot(ax=axs[1], style='k,')
    bf_avg[start:].plot(ax=axs[1])
    axs[1].set_ylabel('% Body Fat')

    for ax in axs:
        ax.tick_params(axis='y', labelleft='on', labelright='on')

    plt.show()


def summarize(start=0):
    data = read_data()
    return data[start:].describe()
