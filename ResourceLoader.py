
from City import City

from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim

import json

class ResourceLoader:
    def __init__(self, filename):
        self.filename = filename
        self.cache_file = 'resources/cities_distances.json'

    def load(self, closest_to_keep=5, read_distances=False,verbose=False):

        geolocator = Nominatim(user_agent="ResourceLoader")

        # files are a csv where first column is city name, second is
        cities_dict = {}
        with open(self.filename) as file:
            for line in file:
                split_line = line.split(',')

                city_name = split_line[0]
                pop_str = ''.join(split_line[1:]) # there are commas in the number as well

                population = int(pop_str[1:-2]) # remove " "
                if city_name not in cities_dict:
                    cities_dict[city_name] = City(city_name,population)

        if verbose:
            print('Loaded csv')

        if read_distances: # read distances from json instead of computing them
            with open(self.cache_file, 'r') as file:
                json_file = json.load(file)
                cities_distances = json_file['distances']
                coords = json_file['coords']
                if verbose:
                    print('Distances and coordinates loaded from {}'.format(self.cache_file))

                for city in cities_dict.values():
                    city.set_coordinates(coords[city.name])
                return cities_distances, cities_dict
        else:
            # load distances from geopy
            for city in cities_dict.keys():
                try:
                    locator = geolocator.geocode(city)
                    lat_lon = locator.latitude, locator.longitude
                    cities_dict[city].set_coordinates(lat_lon)
                except Exception as e:
                    print(type(e))
                    print('Could not geolocate {}'.format(city))
                    raise e

            if verbose:
                print('Loaded positions')
            cities_distances = {}
            for city in cities_dict.keys():
                cities_distances[city] = []

            city_names = list(cities_dict.keys())
            # compute distances
            for i in range(len(cities_dict)):
                for j in range(i+1, len(cities_dict)):
                    coor1 = cities_dict[city_names[i]].get_coordinates()
                    coor2 = cities_dict[city_names[j]].get_coordinates()
                    distance = GD(coor1, coor2).miles

                    cities_distances[city_names[i]].append((city_names[j],distance))
                    cities_distances[city_names[j]].append((city_names[i],distance))
            if verbose:
                print('Loaded distances')

            for city in cities_distances.keys():
                # keep only closest cities
                # actual version cost: O(n) for loading, O(n log n * n) sorting n times
                # here a heapmin would be more efficient (n log n) for loading, O(k * log n) getting best k
                # or keeping only the best k while loading: O(n k)
                # but with 100 cities the cost is manageable
                t = cities_distances[city]
                sorted_cities = sorted(t, key=lambda x: x[1], reverse=False)
                cities_distances[city] = sorted_cities[:closest_to_keep]

            if verbose:
                print('Removed extra distances')

            # get coord list to write down in json file
            coords = {}
            for el in cities_dict.values():
                coords[el.name] = el.get_coordinates()
            with open(self.cache_file, 'w') as outfile:
                d = {'distance': cities_distances, 'coords': coords}
                json.dump(d, outfile)

        return cities_distances, cities_dict
