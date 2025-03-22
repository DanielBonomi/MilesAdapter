from abc import ABC, abstractmethod


class SpanishSystem(ABC):
    @abstractmethod
    def show_route_map(self, begin, goal):
        pass

    @abstractmethod
    def print_route_in_console(self, begin, goal):
        pass
