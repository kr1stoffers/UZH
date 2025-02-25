import tkinter as tk
from tkinter import messagebox
import random
import time


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def generate_random_data(size):
    return [random.randint(0, 100) for _ in range(size)]


def generate_nearly_sorted_data(size):
    arr = generate_random_data(size)
    arr.sort()
    for _ in range(size // 10):
        i, j = random.sample(range(size), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def sort_and_display():
    try:
        if var_input_type.get() == "manual":
            original_array = list(map(int, entry_manual.get().split(",")))
            size = len(original_array)
        else:
            size = int(entry_size.get())
            if size <= 0:
                raise ValueError("Размер должен быть положительным.")

            data_type = var_data_type.get()
            if data_type == "random":
                original_array = generate_random_data(size)
            else:
                original_array = generate_nearly_sorted_data(size)

        start_time = time.time()
        sorted_array_builtin = sorted(original_array)
        builtin_time = time.time() - start_time

        start_time = time.time()
        sorted_array_selection = selection_sort(original_array.copy())
        selection_time = time.time() - start_time

        if size <= 10:
            result_text = f"Исходный массив: {original_array}\n"
            result_text += (
                f"Отсортированный массив (библиотечный): {sorted_array_builtin}\n"
            )
            result_text += (
                f"Отсортированный массив (выбором): {sorted_array_selection}\n"
            )
        else:
            result_text = (
                f"Исходный массив: {original_array[:5]} ... {original_array[-5:]}\n"
            )
            result_text += f"Отсортированный массив (библиотечный): {sorted_array_builtin[:5]} ... {sorted_array_builtin[-5:]}\n"
            result_text += f"Отсортированный массив (выбором): {sorted_array_selection[:5]} ... {sorted_array_selection[-5:]}\n"

        result_text += (
            f"\nВремя работы библиотечной сортировки: {builtin_time:.6f} секунд\n"
        )
        result_text += f"Время работы сортировки выбором: {selection_time:.6f} секунд\n"
        if builtin_time > 0:
            speedup = builtin_time / selection_time
            result_text += f"Ускорение библиотечной сортировки: {speedup:.2f} раз\n"

        messagebox.showinfo("Результаты сортировки", result_text)

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("Сортировка вектора")

var_input_type = tk.StringVar(value="generate")

tk.Radiobutton(
    root, text="Генерировать данные", variable=var_input_type, value="generate"
).pack()

tk.Radiobutton(
    root,
    text="Вводить вручную (через запятую)",
    variable=var_input_type,
    value="manual",
).pack()

entry_size = tk.Entry(root)
entry_size.pack()
tk.Label(root, text="Введите количество элементов (для генерации):").pack()

entry_manual = tk.Entry(root)
entry_manual.pack()
tk.Label(root, text="Введите массив (через запятую):").pack()

var_data_type = tk.StringVar(value="random")
tk.Radiobutton(
    root, text="Случайные данные", variable=var_data_type, value="random"
).pack()

tk.Radiobutton(
    root,
    text="Почти отсортированные данные",
    variable=var_data_type,
    value="nearly_sorted",
).pack()

tk.Button(root, text="Сортировать", command=sort_and_display).pack()
root.mainloop()
