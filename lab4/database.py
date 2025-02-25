import csv
from country import Country
from city import City
from street import Street


class Database:
    def __init__(self):
        self.countries = []

    def add_country(self, country):
        self.countries.append(country)

    def remove_country(self, country_id):
        self.countries = [c for c in self.countries if c.id != country_id]

    def save_to_csv(self, filename):
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Country ID",
                    "Country Name",
                    "City ID",
                    "City Name",
                    "Street ID",
                    "Street Name",
                ]
            )
            for country in self.countries:
                if not country.cities:  # Если у страны нет городов
                    writer.writerow([country.id, country.name, "", "", "", ""])
                else:
                    for city in country.cities:
                        if not city.streets:  # Если у города нет улиц
                            writer.writerow(
                                [
                                    country.id,
                                    country.name,
                                    city.id,
                                    city.name,
                                    "",
                                    "",
                                ]
                            )
                        else:
                            for street in city.streets:
                                writer.writerow(
                                    [
                                        country.id,
                                        country.name,
                                        city.id,
                                        city.name,
                                        street.id,
                                        street.name,
                                    ]
                                )

    def load_from_csv(self, filename):
        self.countries = []
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                country_id, country_name, city_id, city_name, street_id, street_name = (
                    row
                )
                country = next((c for c in self.countries if c.id == country_id), None)
                if not country:
                    country = Country(country_id, country_name)
                    self.add_country(country)
                city = City(city_id, city_name)
                country.add_city(city)
                street = Street(street_id, street_name, city_id)
                city.add_street(street)

    def display_info(self):
        for country in self.countries:
            print(f"Страна: {country.name}")
            for city in country.cities:
                print(f"  Город: {city.name}, Улиц: {city.count_streets()}")
