#  hackdiet.R:  Weight, Body-fat, and Wakeup-time plotting inspired by
#  the of the Hacker's Diet online by John Walker.
#
#  :author: Robert David Grant <robert.david.grant@gmail.com>
#
#  :copyright:
#    Copyright 2012 Robert David Grant
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#    implied.  See the License for the specific language governing
#    permissions and limitations under the License.


require(ggplot2)
setwd("~/documents/life/data/hackdiet")

DATAFILE <- "data.tsv"


convert.datetime <- function(date.lst, time.lst) {
    date.with.time <- sprintf("%s %s", date.lst, time.lst)
    strptime(date.with.time, "%F %H:%M")
}

convert.time <- function(time.lst) {
    string.to.hour <- function(tm) {
        splitTime <- unlist(strsplit(tm, ':'))
        as.numeric(splitTime[1]) + as.numeric(splitTime[2])/60
    }
    sapply(time.lst, string.to.hour)
}

# Read and parse the data file
read.data <- function(file=DATAFILE) {
    data <- read.delim(file, header=TRUE, skip=1,
                     colClasses=c('Date', 'numeric', 'numeric', 'character'))
    data$Day.Length <- c(NA, diff(convert.datetime(data$Date, data$Wake)))
    data$Wake <- convert.time(data$Wake)
    return(data)
}

# Get the data since a certain date
get.datarange <- function(data, since="1900-01-01") {
    sub.data <- subset(data, Date > as.Date(since))
    melt(sub.data, id.vars='Date', measure.vars=c('Weight', 'BF', 'Wake'))
}

# Make a three-paneled plot showing weight, % body fat, and wakeup time
# vs. date.
make.plot <- function(data, since="1900-01-01", span=1) {
    melt.data <- get.datarange(data, since=since)
    p1 <- ggplot(data=melt.data,
            mapping=aes(Date, value))
    p1 + geom_point(na.rm=T) +
         geom_smooth(na.rm=T, span=span) +
         facet_grid(variable ~ ., scales="free_y") +
         opts(title="Life Data")
}


######### Top-level Functions ##########

# Read data and plot the distribution of differences between subsequent
# wakeup-times
plot.daylength <- function(since="1900-01-01") {
    data <- read.data(file=DATAFILE)
    sub.data <- subset(data, Date > as.Date(since))
    qplot(Day.Length[1:length(Day.Length)-1], data=sub.data,
                             geom=c("density"), xlab="Day Length (h)", na.rm=T)
}

# Read data and make a three-paneled plot showing weight, % body fat,
# and wakeup time vs. date
plot.data <- function(since="1900-01-01", span=0.3) {
    data <- read.data(file=DATAFILE)
    make.plot(data, since, span)
}
