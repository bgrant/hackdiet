#!/usr/bin/env python

#   Copyright 2015 Robert David Grant
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Weight, body-fat, wakeup-time, waist-size plotting inspired by the Hacker's
Diet online by John Walker.
"""

from __future__ import print_function, division

import sys
import matplotlib.pyplot as plt
from numpy import zeros, NaN
from pandas import read_csv, ewma, Series


def timestring_to_timefloat(timestring):
    """Take a time string from the Wake column, return number of hours since
    midnight as a float.
    """
    try:
        hour, minute = map(int, timestring.split(':'))
        rval = hour + minute / 60
    except ValueError:
        rval = NaN
    return rval


def timefloat_to_timestring(timefloat):
    """Take a 24-hr time represented as a float and return the HH:MM time."""
    try:
        hour = int(abs(timefloat))
        minute = int((abs(timefloat) - hour) * 60.0)
        sgn = '-' if timefloat < 0 else ''
        rval = "{}{:02d}:{:02d}".format(sgn, hour, minute)
    except ValueError:
        rval = NaN
    return rval


def read_data(path):
    """Parse the data."""
    return read_csv(path, index_col=0, parse_dates=True,
                    converters={'Wake': timestring_to_timefloat})


def plot_lollipops(index, points, line, ax, ecolor='g', capsize=0, fmt='none'):
    """Make a floaters-and-sinkers plot.

    `points` : The data points as a dataframe.
    """
    delta = points - line
    ax.errorbar(index, points, [delta, zeros(len(index))],
                ecolor='g', capsize=0, fmt=fmt, linewidth=0.5)


def first_finite(timeseries):
    return timeseries[timeseries.notnull()][0]


def plot_data(data, start=None, end=None, floatstyle='g+', window=20,
              lollipops=True, interp_na=True):
    """Plot the data.

    Parameters
    ----------
    start : date or str
        Start date
    end : date or str
        End date
    floatstyle : str
        Style of floaters.  Probably '.' or None is what you want.
    window : int
        Number of days to average over.
    lollipops : bool
        turn lollipops on or off
    interp_na : bool
        linearly interpolate to replace NA values
    """
    cols = ['Weight', 'BF', 'Wake', 'Waist']
    if interp_na:
        processed_data = data[cols].apply(Series.interpolate)
    else:
        processed_data = data[cols]
    averages = ewma(processed_data, span=window)
    averages = averages[start:end]
    data = data[start:end]

    plot_kwargs = {'style': floatstyle}
    avg_kwargs = {'style': 'k-'}

    fig = plt.figure()

    ax0 = fig.add_subplot(4, 1, 1)
    data.Weight.plot(ax=ax0, **plot_kwargs)
    averages.Weight.plot(ax=ax0, **avg_kwargs)
    if lollipops:
        plot_lollipops(data.index, data.Weight, averages.Weight, ax0)
    ax0.set_ylabel('Weight')
    plt.setp(ax0.get_xticklabels(), visible=False)

    ax1 = fig.add_subplot(4, 1, 2, sharex=ax0)
    data.BF.plot(ax=ax1, **plot_kwargs)
    averages.BF.plot(ax=ax1, **avg_kwargs)
    if lollipops:
        plot_lollipops(data.index, data.BF, averages.BF, ax1)
    ax1.set_ylabel('% Body Fat')
    ax1.set_yticks(ax1.get_yticks()[:-1])
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = fig.add_subplot(4, 1, 3, sharex=ax0)
    data.Wake.plot(ax=ax2, **plot_kwargs)
    averages.Wake.plot(ax=ax2, **avg_kwargs)
    if lollipops:
        plot_lollipops(data.index, data.Wake, averages.Wake, ax2)
    ax2.set_ylabel('Wake Time')
    ax2.set_yticks(ax2.get_yticks()[:-1])

    ax3 = fig.add_subplot(4, 1, 4, sharex=ax0)
    data.Waist.plot(ax=ax3, **plot_kwargs)
    averages.Waist.plot(ax=ax3, **avg_kwargs)
    if lollipops:
        plot_lollipops(data.index, data.Waist, averages.Waist, ax3)
    ax3.set_ylabel('Waist (in)')
    ax3.set_yticks(ax3.get_yticks()[:-1])

    # Plot annotations
    axs = ax0, ax1, ax2, ax3
    for ax in axs:
        ax.tick_params(axis='y', labelleft='on', labelright='on')

    # Axis for annotations
    ax4 = ax0.twiny()
    ax4.set_xlim(ax2.get_xlim())
    ax4.xaxis_date()
    ax4.set_xticks(data.index[data.Notes.notnull()])
    ax4.set_xticklabels(data.Notes[data.Notes.notnull()],
                        rotation='vertical', size='small')

    # Put a little space on the right so we can see the latest point
    xlims = axs[-1].get_xlim()
    axs[-1].set_xlim((xlims[0], xlims[1] + 1))

    # Analysis
    weight_change = averages.Weight[-1] - first_finite(averages.Weight)
    bf_change = averages.BF[-1] - first_finite(averages.BF)
    wake_change = averages.Wake[-1] - first_finite(averages.Wake)

    fmt_string = ('weight: {:.1f} ({:.1f}), '
                  'bf: {:.1f} ({:.1f}), '
                  'wake: {:s} ({:s})')

    ax0.set_xlabel('')
    ax1.set_xlabel('')
    ax2.set_xlabel(fmt_string.format(averages.Weight[-1], weight_change,
                                     averages.BF[-1], bf_change,
                                     timefloat_to_timestring(averages.Wake[-1]),
                                     timefloat_to_timestring(wake_change)))

    plt.subplots_adjust(hspace=0.00, top=0.85, bottom=0.10, left=0.10, right=0.90)
    plt.show()


def summarize(start='1900-01-01', end=''):
    """Return the pandas summary of the data."""
    data = read_data()
    data = data[start:end]
    return data.describe()


def cli():
    """Simple command-line interface."""
    argv = sys.argv
    kwargs = {}
    datapath = argv[1]
    if len(argv) >= 3:
        kwargs['start'] = argv[2]
    if len(argv) >= 4:
        kwargs['end'] = argv[3]

    dta = read_data(datapath)
    plot_data(dta, **kwargs)


if __name__ == '__main__':
    cli()
