from shapely import LineString
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geodatasets
import matplotlib.pyplot as plt

from ResourceLoader import ResourceLoader

class AmericanSystem:
    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            r = ResourceLoader()
        else:
            r = ResourceLoader(filename)

        self.distances, self.cities = r.quick_load(10)  # discard info on city population, ecc

    def print_route(self, begin, goal):

        path, total_length = self.find_path(begin, goal)
        previous = path[0]
        for city in path[1:]:
            print('From ' + str(previous) + ' to ' + str(city))
            previous = city
        print('Total length: ' + str(total_length))

    def show_route(self, begin, goal):
        path, total_length = self.find_path(begin, goal)
        print('Path calculated')
        geometry = []
        lat_list = []
        lon_list = []

        coords_list = []

        for city_name in path:
            lat, lon = self.cities[city_name].get_coordinates()
            geometry.append(Point(lon, lat))
            lat_list.append(lat)
            lon_list.append(lon)
            coords_list.append([lon, lat])

        d = {'Longitude': lon_list, 'Latitude': lat_list}

        gdf = GeoDataFrame(d, geometry=geometry)

        states = gpd.read_file("./resources/cb_2018_us_state_500k/")

        from shapely import Polygon
        polygon = Polygon([(-160, 15), (-160, 50), (-50, 50), (-50, 15)])

        gdf.plot(ax=states.clip(polygon).plot(figsize=(10, 6)), marker='o', color='red', markersize=15)

        for i in range(1, len(path)):
            plt.plot([coords_list[i-1][0], coords_list[i][0]], [coords_list[i-1][1],coords_list[i][1]], color='blue')
            print(coords_list[i-1], coords_list[i])

        plt.show()


    def find_path(self, begin, goal):
        if begin == goal:
            return [begin], 0

        # Dijkstra
        inf = 2**100
        city_from = {}  # inverse path I'll need to follow
        city_value = {}  # cost of the best path so far

        for name in self.distances:
            city_from[name] = None
            city_value[name] = inf

        city_value[begin] = 0
        border = [begin]  # border nodes are reachable nodes that we haven't visited yet

        found = False
        while len(border) > 0:
            # this would be more efficient with a min-heap (but would require implementing a min-heap or importing a
            # library). cost: O(log n) to extract the minimum, O(log n) to add an element to the heap
            # another solution (worse) would be keeping border sorted and every time I add/change elements to it I put
            # it in the correct position to keep it sorted O(1) to extract min, O(n) add an element
            # but since I don't have that many cities (100) I don't need that much efficiency
            min_pos = 0
            for i in range(1, len(border)):
                if city_value[border[i]] < city_value[border[min_pos]]:
                    min_pos = i
            el = border[min_pos]
            del border[min_pos]

            for (next_city, dis) in self.distances[el]:
                new_value = dis + city_value[el]
                if new_value < city_value[next_city]:
                    city_value[next_city] = new_value
                    city_from[next_city] = el
                    border.append(next_city)

                    if next_city == goal:
                        found = True
                        break

        if not found:
            raise Exception('No route found')
        else:
            route = [goal]
            previous_city = None
            while previous_city != begin:
                # build path
                # add to route the city I needed to go to get to the last element of route
                previous_city = city_from[route[-1]]
                route.append(previous_city)
                # list insert(0) in python costs theta of n
                # so it's cheaper to append and then reverse
            route.reverse()
            return route, city_value[goal]



if __name__ == '__main__':
    am = AmericanSystem()
    am.show_route('Honolulu; Hawaii', 'Boston; Massachusetts')

    '''
    # this can be used to check reachability
    import random
    err_count = 0
    for i in range(1000):
        city1 = random.choice(list(am.distances.keys()))
        city2 = random.choice(list(am.distances.keys()))
        try:
            am.find_path(city1, city2)
        except Exception as e:
            print(f'attempt{i}')
            print(city1, '--->', city2)
            err_count += 1
            #raise e
    '''
