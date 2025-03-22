from City import City
from ResourceLoader import ResourceLoader
from AmericanSystem import AmericanSystem

if __name__ == '__main__':
    r_loader = ResourceLoader()
    usa_system = AmericanSystem(r_loader)
    path, total_length = usa_system.find_path('Seattle; Washington', 'Dallas; Texas')
    usa_system.show_route(path, total_length*1.60934)

    usa_system.open_pop_up()

