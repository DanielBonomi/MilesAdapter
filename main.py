from City import City
from ResourceLoader import ResourceLoader
from AmericanSystem import AmericanSystem
from Adapter import Adapter


def get_city(resource, purpose):
    city_list = list(resource.quick_load()[0].keys())

    city = input(f'Insert a city as a {purpose}\n')
    while city not in city_list:
        poss_cities = []
        for c in city_list:
            if city.lower() in c.lower():
                poss_cities.append(c)

        if len(poss_cities) == 0:
            print("I'm sorry I couldn't understand")
        elif len(poss_cities) == 1:
            yeses = ['yes', 'y', 'si']
            response = input(f'Did you mean {poss_cities[0]}? ({"/".join(yeses)} for Yes, anything else no)\n')
            if response.lower() in yeses:
                city = poss_cities[0]
                break
        else:  # case many cities with similar names
            print('Could you be more precise?')
            s = ''
            first = True
            for c in poss_cities:
                if first:
                    first = False
                else:
                    s += ' OR '
                s += c
            city = input(s+'\n')
            if city in city_list:
                break
            else:
                continue
        city = input(f'Insert a city as a {purpose}\n')
    print("Ok, so you've chosen " + city)
    return city


if __name__ == '__main__':
    # PLEASE READ README.md
    r_loader = ResourceLoader()
    usa_system = AmericanSystem(r_loader)
    begin = get_city(r_loader, 'starting city')
    goal = get_city(r_loader, 'goal city')

    #begin, goal = 'Seattle; Washington', 'Dallas; Texas'

    adapted_system = Adapter(usa_system)
    adapted_system.print_route_in_console(begin,goal)
    adapted_system.show_route_map(begin, goal)