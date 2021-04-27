hackdiet
========


Summary
-------

Simple data plotting inspired by the Hacker's Diet online by John Walker:

http://www.fourmilab.ch/hackdiet/online/hdo.html

The idea is to keep track of your weight (and other daily variables) over time,
look at trends, and get frequent feedback to see if you are making progress
toward your goals.

Why recreate the functionality of Walker's online tool?  His tool is nice, but
it only tracks the specific variables he had in mind, namely Weight and the
'Rung' you're on in his workout program.  I happened to want to track different
variables, and I wanted to be able to play around with the data analysis
myself.

The main output is a four-paneled plot, showing Weight, % Body Fat,
Wakeup-time, and Waist-size by Date.  You can optionally provide a "Note" for
each data point that will be displayed at the top.  I duplicate Walker's
exponentially-weighted-moving-averaging and implement his floaters-and-sinkers
plotting technique.


Requirements
------------

* numpy
* matplotlib
* pandas


Input
-----

Assumes a CSV file of the form:

```
Date,Weight,BF,Wake,Waist,Notes
2009-07-18,169.8,22.6,09:01,30,Birthday
2009-07-19,172.4,23.5,14:31,32,
2009-07-20,170.2,23.2,14:38,34,
2009-07-22,170.6,23.5,12:00,32
2009-07-23,,22.3,11:45,32
2009-07-24,165.8,22.1,11:20,33,Diet-start
```

Pandas will handle missing entries nicely.
