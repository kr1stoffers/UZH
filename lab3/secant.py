import math
from base import Base


class Secant(Base):
    def get_value(self):
        return 1 / math.cos(self.angle)

    def create_instance(self):
        return Secant(self.angle)

    def __str__(self):
        return f"Секанс({self.angle}): {self.get_value()}"
