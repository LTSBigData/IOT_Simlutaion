from os import path

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
from sklearn import metrics
from sklearn.cluster import MiniBatchKMeans

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

latest_loc = user_history_dataframe.groupby(by=['user_id']).first()

cluster_range = range(2, 20, 2)

# sill_coeff = {}
#
# for i in cluster_range:
#     kmeans = MiniBatchKMeans(n_clusters=i)
#     labels = kmeans.fit_predict(latest_loc[['latitude', 'longitude']])
#     coeff = metrics.silhouette_score(latest_loc[['latitude', 'longitude']], labels)
#     sill_coeff[i] = coeff
#
# df = pd.DataFrame(sill_coeff.items(), columns=['cluster_size', 'sill_coeff'])
#
# df.plot(x='cluster_size', y='sill_coeff')
# plt.show()




for choice in cluster_range:
    plt.figure(fignum)
    plt.clf()
    plot_title = "Plot for cluster = " + str(choice)
    map1 = initMapBase()

    kmeans = MiniBatchKMeans(n_clusters=choice).fit(latest_loc[['latitude', 'longitude']])
    centroid_lon, centroid_lat = kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1]

    kmeans_predict = kmeans.predict(latest_loc[['latitude', 'longitude']])
    column_Name = str(choice) + '_labels'
    latest_loc[column_Name] = kmeans_predict

    for name, group in latest_loc.groupby(by=[column_Name]):
        _x, _y = map1(group['longitude'], group['latitude'])
        map1.scatter(_x, _y, latlon=True, marker='d', s=3, cmap='Vega20', alpha=0.5)

    subtitle = "\nSilhouette Coefficient: " + str(
        metrics.silhouette_score(latest_loc[['longitude', 'latitude']], latest_loc[column_Name]))
    plt.title(plot_title + subtitle)
    save_location = project_dir + '/output/images/analysis_2/' + str(fignum) + '_' + shapeFileName + '_' \
                    + str(choice) + '.png'
    plt.savefig(save_location, format='png', dpi=1000, bbox_inches='tight')
    fignum += 1
