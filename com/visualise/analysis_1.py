# Not working. Just trying out.

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

llcrnrlon = -122.1257
llcrnrlat = 37.2273
urcrnrlon = -121.7536
urcrnrlat = 37.4315

map = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, epsg=5520)
# http://server.arcgisonline.com/arcgis/rest/services

map.arcgisimage(service='ESRI_StreetMap_World_2D ', xpixels=1500, verbose=True)
plt.show()
