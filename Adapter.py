from AmericanSystem import AmericanSystem
from SpanishSystem import SpanishSystem
class Adapter(SpanishSystem):
    def __init__(self, usa_system):
        self.usa_system = usa_system # usa_system is the adaptee
        self.miles_to_km = 1.60934

    #
    def print_route_in_console(self, begin, goal):
        path, total_length = self.usa_system.find_path(begin, goal)
        total_length = total_length * self.miles_to_km
        previous = path[0]
        for city in path[1:]:
            print(f'Desde {previous} a {city}')
            previous = city
        print(f'Longitud total: {round(total_length,1)} km')

    def show_route_map(self, begin, goal):
        path, total_length = self.usa_system.find_path(begin, goal)
        total_length = total_length * self.miles_to_km
        self.usa_system.show_route(path, total_length)
        self.usa_system.change_title(f'Desde {begin} a {goal}   ({round(total_length, 1)} km)')
        self.usa_system.open_pop_up()

