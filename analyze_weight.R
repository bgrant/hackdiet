require(ggplot2)
setwd("~/documents/life/data")


######### data conversion functions ##########

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


######### interactive functions ##########

read.data <- function(file="weight.tsv") {
    wt <- read.delim(file, header=TRUE, 
                     colClasses=c('Date', 'numeric', 'numeric', 'character'))
    wt$Day.Length <- c(NA, diff(convert.datetime(wt$Date, wt$Wake)))
    wt$Wake <- convert.time(wt$Wake)
    return(wt)
}

get.mydata <- function(since="1900-01-01", data=wt) {
    sub.wt <- subset(data, Date > as.Date(since))
    melt(sub.wt, id.vars='Date', measure.vars=c('Weight', 'BF', 'Wake'))
    #melt(sub.wt, id.vars='Date', measure.vars=c('Weight', 'BF'))
}

plot.mydata <- function(since="1900-01-01", data=wt, span=1) {
    melt.wt <- get.mydata(since=since, data)
    p1 <- ggplot(data=melt.wt, 
            mapping=aes(Date, value))
    p1 + geom_point(na.rm=T) + 
         geom_smooth(na.rm=T, span=span) +
         facet_grid(variable ~ ., scales="free_y") +
         opts(title="Life Data")
}


# other possible plots... probably not functional right now
plot.mywake <- function(since="1900-01-01", data=wt) {
    wt <- read.data(file="weight.tsv")
    sub.wt <- subset(data, Date > as.Date(since))
#    wake.time.plot <- qplot(Date, Wake, data=wt, geom="point")
    qplot(Date, Wake, data=sub.wt, geom="point")
#    day.length.dplot <- qplot(Day.Length[1:length(Day.Length)-1], data=wt,
#                             geom=c("density"), xlab="Day Length (h)")
#    day.length.boxplot <- 
#        qplot(factor(1),Day.Length[1:length(Day.Length)-1], 
#            data=wt, geom="boxplot", scale_x_discrete("")) + coord_flip()
}

plot.daylength <- function(since="1900-01-01", data=wt) {
    wt <- read.data(file="weight.tsv")
    sub.wt <- subset(data, Date > as.Date(since))
    qplot(Day.Length[1:length(Day.Length)-1], data=sub.wt,
                             geom=c("density"), xlab="Day Length (h)", na.rm=T)
}

# one function to rule them all
show.data <- function(since="1900-01-01", span=0.3) {
    wt <- read.data(file="weight.tsv")
    plot.mydata(since, wt, span)
}