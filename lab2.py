# "Класс"
# Четыре целый числа: a, b, c, d.
# Вычислить среднее арифметическое чисел.
# Определить максимальное из чисел.


import tkinter as tk
from tkinter import messagebox


class Number:
    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        print(f"Объект создан: {self}")

    def __del__(self):
        print(f"Объект уничтожен: {self}")

    def average(self):
        return (self.a + self.b + self.c + self.d) / 4

    def maximum(self):
        return max(self.a, self.b, self.c, self.d)

    def __str__(self):
        return f"Числа: {self.a}, {self.b}, {self.c}, {self.d}"


def calculate():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        c = int(entry_c.get())
        d = int(entry_d.get())

        num = Number(a, b, c, d)
        avg = num.average()
        max_num = num.maximum()

        result_text = f"Среднее арифметическое: {avg}\nМаксимальное число: {max_num}"
        messagebox.showinfo("Результаты", result_text)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите целые числа.")


root = tk.Tk()
root.title("лаб 2")

root.geometry("300x300")
tk.Label(root, text="Введите a:").pack()
entry_a = tk.Entry(root)
entry_a.pack()

tk.Label(root, text="Введите b:").pack()
entry_b = tk.Entry(root)
entry_b.pack()

tk.Label(root, text="Введите c:").pack()
entry_c = tk.Entry(root)
entry_c.pack()

tk.Label(root, text="Введите d:").pack()
entry_d = tk.Entry(root)
entry_d.pack()

calculate_button = tk.Button(root, text="Вычислить", command=calculate)
calculate_button.pack()

root.mainloop()
