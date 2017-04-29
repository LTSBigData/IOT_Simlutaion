from os import path

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
from sklearn import metrics
from sklearn.cluster import DBSCAN, MiniBatchKMeans

from extractShapeFile import *

project_dir = path.dirname(path.dirname(os.getcwd()))

san_jose_shape_file = project_dir + '/resources/shapefiles/san_jose_shape'
san_jose_shape = 'san_jose_shape'
fignum = 1


def initMapBase():
    llcrnrlon = -122.018
    llcrnrlat = 37.2888
    urcrnrlon = -121.836
    urcrnrlat = 37.3793

    map = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, epsg=4326,
                  resolution='c')
    map.readshapefile(san_jose_shape_file, san_jose_shape)
    return map

###########################################################################

user_data_file = project_dir + '/output/user_history_2017-04-27 21:18:01.843562.csv'

shapeFileName = os.path.basename(user_data_file).split('.')[0]

# print shapeFileName

user_history_dataframe = pd.read_csv(user_data_file, sep=',',
                                     names=["datetime", "user_id", "latitude", "longitude", "pulse", "temp", "age",
                                            "bpCat"],
                                     header=None,
                                     usecols=["datetime", "user_id", "latitude", "longitude"],
                                     # skipfooter=1,
                                     parse_dates=['datetime'],
                                     infer_datetime_format=True)  # ,
# nrows=10)


min_time = min(user_history_dataframe['datetime'])
max_time = max(user_history_dataframe['datetime'])
total_diff = max_time - min_time
total_diff = (total_diff.days * 24 * 60 * 60) + (total_diff.seconds)

# print total_diff

user_history_dataframe['diff_time'] = user_history_dataframe['datetime'] - min_time
user_history_dataframe['rel_diff_seconds'] = user_history_dataframe['diff_time'].dt.total_seconds() / total_diff
user_history_dataframe = user_history_dataframe.round({'rel_diff_seconds': 2})

user_history_dataframe = user_history_dataframe[['datetime', 'user_id', 'latitude', 'longitude', 'rel_diff_seconds']]

# print user_history_dataframe.head()

##############################################################################
###################_______INITIAL PLOTS_______________########################
# Unsorted lat and lon initial plot
lat = user_history_dataframe['latitude']
lon = user_history_dataframe['longitude']

plt.figure(fignum)
plt.clf()
map1 = initMapBase()
x1, y1 = map1(lon, lat)
map1.scatter(x1, y1, latlon=True, marker='v', color='#EC2727', s=1, alpha=0.01)
save_location = project_dir + '/output/images/' + str(fignum) + '_' + shapeFileName + '_allpoints.png'
plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
# plt.show()
##############################################################################

fignum += 1

# Sorting dataframe by time and plotting --> for better visualising the data
user_history_dataframe = user_history_dataframe.sort_values(by=['datetime'], ascending=False)

# print user_history_dataframe.head()

##############################################################################
groups = user_history_dataframe.groupby(by=['rel_diff_seconds'])

plt.figure(fignum)
plt.clf()
map1 = initMapBase()
for name, group in groups:
    if name == 1.0:
        lat = group['latitude']
        lon = group['longitude']
        x, y = map1(lon, lat)
        map1.scatter(x, y, latlon=True, marker='d', color='#2789EC', s=3, alpha=name)
    else:
        lat = group['latitude']
        lon = group['longitude']
        x, y = map1(lon, lat)
        map1.scatter(x, y, latlon=True, marker='v', color='#EC2727', s=.5, alpha=name / 10)

save_location = project_dir + '/output/images/' + str(fignum) + '_' + shapeFileName + '_grouped.png'
plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
# plt.show()
##############################################################################

fignum += 1
##############################################################################
##################__________DBSCAN CLUSTERING_________########################

# Initializing new dataframe with only the latest_location of each user
latest_loc = user_history_dataframe.groupby(by=['user_id']).first()

# print latest_loc.head()


db = DBSCAN(eps=0.005, min_samples=30, n_jobs=-1).fit_predict(latest_loc[['longitude', 'latitude']])

latest_loc['category_DBSCAN'] = db  # Gives the categorical values for each lat-lon pair

# # print latest_loc.head()

plt.figure(fignum)
plt.clf()
map1 = initMapBase()

for name, group in latest_loc.groupby(by=['category_DBSCAN']):
    x, y = map1(group['longitude'], group['latitude'])
    map1.scatter(x, y, latlon=True, marker='d', s=3, cmap='Vega20')

save_location = project_dir + '/output/images/' + str(fignum) + '_' + shapeFileName + '_DBSCAN.png'
plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
# plt.show()

fignum += 1

# # Removing 'noise' as deduced by DBSCAN

plt.figure(fignum)
map1 = initMapBase()

dataset_clean = latest_loc[latest_loc['category_DBSCAN'] != -1]
noise_free_labels = dataset_clean['category_DBSCAN']
# Removing 'noise' points from plot
for name, group in dataset_clean.groupby(by=['category_DBSCAN']):
    x, y = map1(group['longitude'], group['latitude'])
    map1.scatter(x, y, latlon=True, marker='d', s=3, cmap='Vega20')

save_location = project_dir + '/output/images/' + str(fignum) + '_' + shapeFileName + '_DBSCAN_without_noise.png'
plot_title = "Silhouette Coefficient: " + str(
    metrics.silhouette_score(dataset_clean[['longitude', 'latitude']], noise_free_labels))
plt.title(plot_title)
plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
# plt.show()

##############################################################################

fignum += 1

##############################################################################
##################__________K-MEANS CLUSTERING_________########################

# From DBSCAN its apparent that there definitely 10 clusters. So for KMeans we are going to start from 10 to 20 with steps of 2
# We shall keep checking the sil. coefficient and try to obtain the highest plausible positive value.
# MiniBatchKmeans is used since the number of samples in the dataset is quite high. If KMeans() is just used,
# python is simply crashing.
cluster_points = {'k_means_2': MiniBatchKMeans(n_clusters=2),
                  'k_means_4': MiniBatchKMeans(n_clusters=4),
                  'k_means_6': MiniBatchKMeans(n_clusters=6),
                  'k_means_8': MiniBatchKMeans(n_clusters=8),
                  'k_means_10': MiniBatchKMeans(n_clusters=10),
                  'k_means_12': MiniBatchKMeans(n_clusters=12),
                  'k_means_14': MiniBatchKMeans(n_clusters=14)}

X = latest_loc[['longitude', 'latitude']]

for choice, estimator in cluster_points.items():
    plt.figure(fignum)
    plt.clf()
    plot_title = "Plot for " + choice
    map1 = initMapBase()

    kmeans = estimator.fit(X)
    centroid_lon, centroid_lat = kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1]

    kmeans_predict = kmeans.predict(X)
    column_Name = choice + '_labels'
    latest_loc[column_Name] = kmeans_predict

    for name, group in latest_loc.groupby(by=[column_Name]):
        _x, _y = map1(group['longitude'], group['latitude'])
        map1.scatter(_x, _y, latlon=True, marker='d', s=3, cmap='Vega20', alpha=0.5)

    # _x, _y = map1(centroid_lon, centroid_lat)
    # map1.scatter(_x, _y, latlon=True, marker='8', s=20, color='red')
    subtitle = "\nSilhouette Coefficient: " + str(
        metrics.silhouette_score(latest_loc[['longitude', 'latitude']], latest_loc[column_Name]))
    plt.title(plot_title + subtitle)
    save_location = project_dir + '/output/images/' + str(fignum) + '_' + shapeFileName + '_' + choice + '.png'
    plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
    fignum += 1

latest_loc.to_csv(project_dir + '/output/' + shapeFileName + '_final.csv')
