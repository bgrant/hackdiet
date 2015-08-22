hackdiet
========


Summary
-------

This project contains some fairly simple data plotting functions inspired by
the Hacker's Diet online by John Walker:

http://www.fourmilab.ch/hackdiet/online/hdo.html

The idea is to keep track of your weight (and other daily variables) over time,
look at trends, and get frequent feedback to see if you are making progress
toward your goals.  These files are mostly for my own use and do not have a
super-streamlined interface.  That said, they're simple and hackable, and if
people are actually interested in using them I will make them more
user-friendly.  If you want something very user-friendly, just use Walker's
online tool.

Why recreate the functionality of Walker's online tool?  His tool is nice, but
it only tracks the specific variables he had in mind, namely Weight and the
'Rung' you're on in his workout program.  I happened to want to track different
variables, and I wanted to be able to play around with the data analysis
myself.

The main output is a three-paneled plot, showing Weight, % Body Fat, and
Wakeup-time by Date.  You can optionally provide a "Note" for each data point
that will be displayed at the top.  I duplicate Walker's
exponentially-weighted-moving-average and floaters-and-sinkers plotting
techniques.


Requirements
------------

* numpy
* matplotlib
* pandas


Input
-----

Assumes a CSV file of the form:

```
Date,Weight,BF,Wake,Note
2009-07-18,169.8,22.6,09:01
2009-07-19,172.4,23.5,14:31
2009-07-20,170.2,23.2,14:38
2009-07-21,,,
2009-07-22,170.6,23.5,12:00
2009-07-23,,22.3,11:45
2009-07-24,165.8,22.1,11:20
```

The first line is not parsed.  Each column is separated by tabs.  If
you're missing a data point, put an 'NA' in that spot, and pandas and
ggplot2 will generally handle it.
