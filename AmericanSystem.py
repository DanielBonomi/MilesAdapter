import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geodatasets

from ResourceLoader import ResourceLoader

class AmericanSystem:
    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            r = ResourceLoader()
        else:
            r = ResourceLoader(filename)

        self.distances = r.quick_load(10)[0]  # discard info on city population, ecc

    def show_route(self, begin, goal):

        path, total_length = self.find_path(begin, goal)
        last = path[0]
        for city in path[1:]:
            print('From ' + str(last) + ' to ' + str(city))
            last = city
        print('Total length: ' + str(total_length))

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
            # would be more efficient with a min-heap
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
    am.show_route('Los Angeles; California', 'San Antonio; Texas')

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
