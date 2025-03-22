class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.lat = None
        self.lon = None

    def set_coordinates(self, lat_lon):
        self.lat, self.lon = lat_lon

    def get_coordinates(self):
        return self.lat, self.lon

    def __str__(self):
        if self.lat and self.lon:
            return f'Name:\t{self.name}\nPopulation:\t{self.population}\nCoordinates:\t' + str((self.lat, self.lon))
        else:
            return f'Name:\t{self.name}\nPopulation:\t{self.population}'
