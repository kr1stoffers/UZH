import math
from base import Base


class Cotangent(Base):
    def get_value(self):
        return 1 / math.tan(self.angle)

    def create_instance(self):
        return Cotangent(self.angle)

    def __str__(self):
        return f"Котангенс({self.angle}): {self.get_value()}"
