HACKDIET - In R and Python
========
This project contains some fairly simple data plotting functions
inspired by the Hacker's Diet online by John Walker:

http://www.fourmilab.ch/hackdiet/online/hdo.html

The idea is to keep track of your weight (and other daily variables)
over time, look at trends, and get frequent feedback to see if you are
making progress toward your goals.  These files are mostly for my own
use and do not have a super-streamlined interface.  That said, they're
simple and hackable, and if people are actually interested in using them
I will make them more user-friendly.  If you want something very
user-friendly, just use Walker's online tool.

Why recreate the functionality of Walker's online tool?  His tool is
nice, but it only tracks the specific variables he had in mind, namely
Weight and the 'Rung' you're on in his workout program.  I happened to
want to track different variables, and I wanted to be able to play
around with the data analysis myself.

This project contains two files: `hackdiet.R` and `hackdiet.py`.  They
have basically the same functionality.  The R file came first, and I
still quite like the plots produced by R and ggplot2.  However, I do
most of my programming in python, and I wanted to play with the `pandas`
package (and `statsmodels` in the future), so I rewrote it in python.

The main output of both files is a three-paneled plot, plotting Weight,
% Body Fat, and Wakeup-time by Date.  The python version duplicates
Walker's exponentially-weighted-moving-average and floaters-and-sinkers
techniques, while the R version uses plotting methods more natural to
ggplot2.  For specific functionality and usage, check out the comments
in the files or send me a message on github.

`hackdiet.py` requires `numpy`, `matplotlib`, and `pandas`, and
`hackdiet.R` requires ggplot2.

My functions assume a data file called `data.tsv` of the form::

# vim: noexpandtab : tabstop=15 : shiftwidth=10
Date	Weight	BF	Wake
2009-07-18	169.8	22.6	09:01
2009-07-19	172.4	23.5	14:31
2009-07-20	170.2	23.2	14:38
2009-07-21	169.8	22.8	08:28
2009-07-22	170.6	23.5	12:00
2009-07-23	166.4	22.3	11:45
2009-07-24	165.8	22.1	11:20


Each column is separated by tabs, and the first two lines are not
parsed.

Happy hacking.
