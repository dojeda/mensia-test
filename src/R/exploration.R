require(ggplot2)
require(GGally)
require(reshape2)

## Read data from unified CSV file
dataset = read.csv('data/full_data.csv')

## Fix index column and factors
dataset$X = NULL
for (fc in c('feature','time','group'))
    dataset[[fc]] = as.factor(dataset[[fc]])

## melt with respect to electrode
dataset.wide = reshape2::melt(dataset,id.vars=c('group','subject','time','feature'))
dataset.wide$electrode = dataset.wide$variable
dataset.wide$variable = NULL

## Plot histogram of features considering each electrode
ghist.1 = ggplot(data=dataset.wide,aes(x=value)) + 
    ##geom_histogram() + 
    geom_histogram(aes(fill=group),alpha=0.5,position='identity') + 
    facet_grid(feature~electrode)
print(ghist.1)

## Histogram of features considering time
ghist.2 = ggplot(data=dataset.wide,aes(x=value)) + 
    ##geom_histogram() + 
    geom_histogram(aes(fill=group),alpha=0.5,position='identity') + 
    facet_grid(feature~time)
print(ghist.2)

## Histogram of features considering group
ghist.3 = ggplot(data=dataset.wide,aes(x=value)) + 
    ##geom_histogram() + 
    geom_histogram(aes(fill=time),alpha=0.5,position='identity') + 
    facet_grid(feature~group)
print(ghist.3)


# dataPCA = dataset.wide
# for (fc in c('group','subject','time','feature','electrode'))
#     dataPCA[[fc]] = as.integer(dataPCA[[fc]])
# 
# pc = princomp(dataPCA)

electrodes = unique(levels(dataset.wide$electrode))
testdata = dataset[dataset$feature=='Y1',]

