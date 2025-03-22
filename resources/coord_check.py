'''
THIS FILE IS A TEST FILE USED TO CHECK THE COORDINATES OF THE CITIES

'''
if __name__=='__main__':
    import json
    cache_file = 'cities_info.json'
    wrong_cities = []
    with open(cache_file, 'r') as file:
        json_file = json.load(file)
        cities_distances = json_file['distances']
        coords = json_file['coords']

        print('Distances and coordinates loaded from {}'.format(cache_file))

        for city in cities_distances.keys():
            lat,lon = coords[city]
            if lat < 20 or lat > 50 or lon < -160 or lon > -65:
                print(coords[city], city)
                wrong_cities.append(city)
            #(coords[city])


    from geopy.distance import geodesic as GD
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent=__name__)
    box = ((50,-160),(25,-65))

    locator = geolocator.geocode('Honolulu, Hawaii', viewbox=box)
    lat_lon = locator.latitude, locator.longitude
    print(lat_lon, 'Honolulu, Hawaii')

    for c in wrong_cities:
        locator = geolocator.geocode(c, viewbox=box)
        lat_lon = locator.latitude, locator.longitude
        print(lat_lon)