import os
from os import path

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

project_dir = path.dirname(path.dirname(os.getcwd()))

san_jose_shape_file = project_dir + '/resources/san_jose_shape'
san_jose_shape = 'san_jose_shape'


llcrnrlon = -122.1257
llcrnrlat = 37.2273
urcrnrlon = -121.7536
urcrnrlat = 37.4315

map = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, epsg=4326,
              resolution='c')

map.readshapefile(san_jose_shape_file, san_jose_shape)

###########################################################################

user_data_file = project_dir + '/output/user_history_2017-04-26 19:01:57.007305.csv'
user_history_dataframe = pd.read_csv(user_data_file, sep=',',
                                     names=["datetime", "user_id", "latitude", "longitude", "pulse", "temp", "age",
                                            "bpCat"],
                                     header=None,
                                     usecols=["datetime", "user_id", "latitude", "longitude"],
                                     # skipfooter=1,
                                     parse_dates=[1],
                                     infer_datetime_format=True,
                                     nrows=10)

# print user_history_dataframe

# lat = user_history_dataframe['latitude']
# lon = user_history_dataframe['longitude']


x, y = map(0, 0)
map.plot(x, y, 'bo', )

###########################################################################

plt.show()
