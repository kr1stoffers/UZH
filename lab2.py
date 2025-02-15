# "Класс"
# Четыре целый числа: a, b, c, d.
# Вычислить среднее арифметическое чисел.
# Определить максимальное из чисел.


class Chisla:
    def __init__(self, a: int, b: int, c: int, d: int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def arith_mean(self):
        return (self.a + self.b + self.c + self.d) / 4

    def max_value(self):
        return max(self.a, self.b, self.c, self.d)


chis = Chisla(4, 3, 5, 1)

print(chis.arith_mean())
print(chis.max_value())
