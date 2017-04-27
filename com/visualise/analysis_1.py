import os
from os import path

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

project_dir = path.dirname(path.dirname(os.getcwd()))

san_jose_shape_file = project_dir + '/resources/shapefiles/san_jose_shape'
san_jose_shape = 'san_jose_shape'


llcrnrlon = -122.1257
llcrnrlat = 37.2273
urcrnrlon = -121.7536
urcrnrlat = 37.4315

map = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, epsg=4326,
              resolution='c')

map.readshapefile(san_jose_shape_file, san_jose_shape)

###########################################################################

user_data_file = project_dir + '\\output\\user_history_2017-04-27.csv'

shapeFileName = os.path.basename(user_data_file).split('.')[0]

# print shapeFileName

user_history_dataframe = pd.read_csv(user_data_file, sep=',',
                                     names=["datetime", "user_id", "latitude", "longitude", "pulse", "temp", "age",
                                            "bpCat"],
                                     header=None,
                                     usecols=["datetime", "user_id", "latitude", "longitude"],
                                     # skipfooter=1,
                                     parse_dates=[1],
                                     infer_datetime_format=True,
                                     nrows=10)

# Creating shape file for the points
# lat = user_history_dataframe['latitude']
# lon = user_history_dataframe['longitude']
# shapeFilePath = createShapeFile(lat, lon, shapeFileName, project_dir)

# map.readshapefile(shapeFilePath, shapeFileName)

# # Using ggplot
# g = ggplot(aes(x = 'latitude', y = 'latitude'), data=user_history_dataframe) +\
#     geom_line() +\
#     stat_smooth(color = 'blue', span = 0.2)
#
# print g
###########################################################################

plt.show()
