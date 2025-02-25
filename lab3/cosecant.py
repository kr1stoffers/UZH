import math
from base import Base


class Cosecant(Base):
    def get_value(self):
        return 1 / math.sin(self.angle)

    def create_instance(self):
        return Cosecant(self.angle)

    def __str__(self):
        return f"Косеканс({self.angle}): {self.get_value()}"
