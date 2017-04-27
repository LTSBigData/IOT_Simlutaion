import numpy
import shapefile
from pyproj import *

# projection 1: UTM zone 15, grs80 ellipse, NAD83 datum
# (defined by epsg code 26915)

p1 = Proj(init='epsg:3857')
p2 = Proj(init='epsg:4326')


def createShapeFile(lat, lon, filename, project_dir):
    filepath = project_dir + '\\resources\\shapefiles\\' + filename + '\\' + filename
    w = shapefile.Writer(shapefile.POINT)
    w.field('latitude')
    w.field('longitude')

    for i in numpy.arange(start=0, stop=len(lat)):
        x1, y1 = p1(lon[i], lat[i])
        x2, y2 = transform(p1, p2, x1, y1)
        w.point(x2, y2)
        w.record(str(i), 'point')

    w.save(filepath)
    return filepath


    # w = shapefile.Writer(shapefile.POINT)
    # w.point(1,1)
    # w.point(3,1)
    # w.point(4,3)
    # w.point(2,2)
    # w.field('FIRST_FLD')
    # w.field('SECOND_FLD','C','40')
    # w.record('First','Point')
    # w.record('Second','Point')
    # w.record('Third','Point')
    # w.record('Fourth','Point')
    # w.save('shapefiles/test/point')




    # map = Basemap(llcrnrlon=-90, llcrnrlat=-90, urcrnrlon=90, urcrnrlat=90, epsg=4326,
    #               resolution='c')
    #
    # map.readshapefile("C:\\Users\\rajsarka\\PycharmProjects\\IOT_Simlutaion\\com\\visualise\\shapefiles\\test\\point",
    #                   'point')
    # plt.plot()
