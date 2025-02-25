from street import Street


class City:
    def __init__(self, city_id, name):
        self.id = city_id
        self.name = name
        self.streets = []

    def add_street(self, street):
        self.streets.append(street)

    def remove_street(self, street_id):
        self.streets = [s for s in self.streets if s.id != street_id]

    def count_streets(self):
        return len(self.streets)
