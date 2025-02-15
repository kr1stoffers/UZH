# Вариант 10
# 1. Определить, есть ли в списке повторяющиеся элементы, если да,
#   то вывести на экран это значение, иначе сообщение об их отсутствии
# 2. Дан одномерный массив из 15 элементов. Элементам массива меньше 10 присвоить "0", а элементам больше 20 присвоить "1".
#   Вывести на экран монитора первоначальный и преобразованный массивы в строчку.

import random

arr = [random.randint(0, 20) for i in range(10)]
set_arr = set()

for i in arr:
    if arr.count(i) > 1:
        set_arr.add(i)
print("Исходный массив:")
print("\t", arr)

print("Повторений:")
print("\t", set_arr) if len(set_arr) > 0 else print("\t", "Повторений нет 😔")

print("=========")

arr2 = [random.randint(0, 50) for i in range(15)]

print("Исходный массив")
print("\t", arr2)

for i in arr2:
    if i > 20:
        arr2[arr2.index(i)] = 1
    if i < 10:
        arr2[arr2.index(i)] = 0

print("Измененный массив:")
print("\t", arr2)
