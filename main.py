from City import City
from ResourceLoader import ResourceLoader
from AmericanSystem import AmericanSystem
from Adapter import Adapter

if __name__ == '__main__':
    r_loader = ResourceLoader()
    usa_system = AmericanSystem(r_loader)


    begin, goal = 'Seattle; Washington', 'Dallas; Texas'

    adapted_system = Adapter(usa_system)
    adapted_system.print_route_in_console(begin,goal)
    adapted_system.show_route_map(begin, goal)



