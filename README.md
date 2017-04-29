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


A link to a detailed documentation is provided in the repository. 

-------------------


## Analysis

We start off first by analysing the whole set of points first.

##### Stage 1
![Initial Plot - Before data cleaning](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/1_user_history_2017-04-27%2021:18:01_allpoints%20copy.png)

There are 1455581 latitude-longitude pairs. The data points can be found in this 
[archive](https://drive.google.com/open?id=0By71xL1Nx_SfR0hTekFXSGJPckk) under the filename 
*user_history_2017-04-27 21:18:01.843562.csv*. The files will be generated with current 
date-time stamp. The file generated contains 1 days worth of data for 5076 users taken at an interval
of every 5 minutes. Due to the sheer number of data points an *alpha = 0.01* has been used while
plotting to make it more readable.

##### Stage 2
![Second Plot - Plotting user paths and latest location](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/2_user_history_2017-04-27%2021:18:01_grouped%20copy.png)

Only the user's final location data are of interest to us. The *blue dots* represent the latest
locaiton while the *red dots* shows the path of the users (although it can't be figured out from
this plot due to to sheer number). At next stages we'll be dealing with only the latest location.

##### Stage 3
![Third Plot - DBSCAN with noise](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/3_user_history_2017-04-27%2021:18:01_DBSCAN%20copy.png)

The data has been cleaned and only the latest location for all users are taken into consideration.
[DBSCAN](https://en.wikipedia.org/wiki/DBSCAN) has been performed on the data set to get a 'feel'
of the possible 'dense' cluster locations. We see that there are about 9 dense clusters.
The *blue dots* that are spread out in the plot are 'noisy data points'. Let's observe the data
once the noise has been removed from the dataset.

![Fourth Plot - DBSCAN without noise](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/4_user_history_2017-04-27%2021:18:01_DBSCAN_without_noise%20copy.png)

Now we can clearly see the 9 dense clusters with a *__silhouette factor ~ 0.3__*. It should be noted that the 'noisy' data in this 
case are of importance to us as well. DBSCAN provides us with the insight of 'dense' clusters 
only.

##### Stage 4

The next plots are results of K-Means clustering taking different number of cluster points.

###### k = 2
![Fifth Plot - KMeans with two clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/8_user_history_2017-04-27%2021:18:01_k_means_2%20copy.png)

###### k = 4
![Sixth Plot - KMeans with four clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/9_user_history_2017-04-27%2021:18:01_k_means_4%20copy.png)

###### k = 6
![Seventh Plot - KMeans with six clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/10_user_history_2017-04-27%2021:18:01_k_means_6%20copy.png)

###### k = 8
![Eighth Plot - KMeans with eight clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/11_user_history_2017-04-27%2021:18:01_k_means_8%20copy.png)

###### k = 10
![Ninth Plot - KMeans with ten clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/6_user_history_2017-04-27%2021:18:01_k_means_10%20copy.png)

###### k = 12
![Tenth Plot - KMeans with twelve clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/7_user_history_2017-04-27%2021:18:01_k_means_12%20copy.png)

###### k = 14
![Eleventh Plot - KMeans with fourteen clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/5_user_history_2017-04-27%2021:18:01_k_means_14%20copy.png)

The analysis and decision making for KMeans will be based solely on the *silhouette value*. 
We stop at *number_of_clusters = 14* and take a look whether there is a significant amount of
change in the *silhouette value* as we increase the number of clusters.

![Twelve Plot - Silhouette Value vs Cluster Numbers](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/sill_coeff_vs_clusters.png)

A rapid decrease in *sill_coeff* is observed w.r.t to *number_of_clusters*. From
*number_of_clusters = 20* it is observed that the deviation of the *sill_coeff* is actually 
quite small.

![Thirteen Plot - Zooming in on sill_coeff vs. n_clusters](https://github.com/sarkaraj/IOT_Simlutaion/blob/master/output/images/cluster_2_to_20.png)

Zooming in on our previous figure, we observe that from *n_cluster = 14* onwards, 
the *sill_coeff* reaches a *pseudo-saturation state*.
Therefore, our choice of stopping KMeans at *n_clusters = 14* was infact a correct one.

## Report

For our current use case, based on [DBSCAN](https://en.wikipedia.org/wiki/DBSCAN), we obtained 
the *dense* cluster centers. On the contrary using [K-Means](https://en.wikipedia.org/wiki/K-means_clustering)
 all points were *classified* into different clusters. It should be mentioned here that 
 DBSCAN and K-Means are used for very different purpose with different applications.
As far as our dataset is concerned, in terms of clustering our 'users', the choices boils down 
 *n_cluster = 10* or *n_cluster = 6*, based on the *silhouette score*.
 
