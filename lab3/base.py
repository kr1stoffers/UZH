class Base:
    def __init__(self, angle):
        self.angle = angle

    def get_value(self):
        raise NotImplementedError(
            "Метод get_value должен быть переопределен в производных классах."
        )

    def create_instance(self):
        raise NotImplementedError(
            "Метод create_instance должен быть переопределен в производных классах."
        )

    def __str__(self):
        return f"Угол: {self.angle} радиан"
