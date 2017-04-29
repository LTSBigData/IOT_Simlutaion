# IOT_Simulation

Aim of this project was to simulate FitBit data on a large scale to for testing SparkStreaming
application and capture the latency of 3 such pipelines.

1. Real Time Pipeline
2. Near-Real Time Pipeline
3. Lambda Architecture Pipeline (Batch + Stream Processing)

This is repository is primarily meant for the simulator. Recently I have added a few of the 
data analysis methodologies as well to get an overview of the dataset as well as visualize
the plausible extent of use of this simulator.

Here I have shown only two methods of data clustering:-
1. [DBSCAN](https://en.wikipedia.org/wiki/DBSCAN)
    * ***D**ensity-**B**ased **S**patial **C**lustering of **A**pplications with **N**oise* or DBSCAN is a density-based
    clustering algorithm. The reason why I have used this is because, unlike 
    [KMeans](https://en.wikipedia.org/wiki/K-means_clustering), this methods does not require a
    pre-existing number of clusters as its argument and it has a notion of *'noise'* in data.
    This method however has one massive disadvantage - distance between points is measured as the 
    *Euclidean* distance between them. In case of higher dimensional data, this method can be 
    rendered useless. But for our test case, this method does provide meaningful insights.

2. [K-Means Clustering](https://en.wikipedia.org/wiki/K-means_clustering)
    * K-Means clustering is one of the most popular clustering algorithms. On the contrary to 
    **DBSCAN**, here the *number of clusters* the data points needs to be *'clustered'* into
    needs to be passed as an argument.

The data analysis is done based on calculating **Silhouette Score** for each of the clusters
thus formed. For more details,
[Silhouette Score](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html#sklearn.metrics.silhouette_score)
can provide with more information.


## Overview of the generator and data

The generator simulates FitBit devices or FitBit users' data, whichever is easy to comprehend.
I'll be using the term 'user' to represent a single instance of such a device for simplicity.
The program has been provided with the population statistics of a region (in this case I've chose San
Jose, but any other place can also be chosen.) I've listed below a few of the parameters that
has been used to create it.

A few of the population statistics that have been used are:-
1. *Age Distribution* -- Percentage of population in different age groups. It is based on actual
government published reports.
2. *Gender Distribution* -- Male-to-Female ratios within the population.
3. *Health Parameters* -- Indices like Body Mass Index, Body Fat Percentage, Height and Weight
distributions etc.


A link to a detailed documentation is provided at the end.

-------------------


## Analysis Report

We start off first by analysing the whole set of points first.

![Initial Plot - Before data cleaning](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/1_user_history_2017-04-27%2021:18:01_allpoints%20copy.png)

