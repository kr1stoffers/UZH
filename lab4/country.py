from city import City


class Country:
    def __init__(self, country_id, name):
        self.id = country_id
        self.name = name
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def remove_city(self, city_id):
        self.cities = [c for c in self.cities if c.id != city_id]
