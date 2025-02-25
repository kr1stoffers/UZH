import tkinter as tk
from tkinter import messagebox
from secant import Secant
from cosecant import Cosecant
from cotangent import Cotangent


def calculate():
    try:
        angle = float(entry_angle.get())

        sec = Secant(angle)
        cosec = Cosecant(angle)
        cot = Cotangent(angle)

        sec_value = sec.get_value()
        cosec_value = cosec.get_value()
        cot_value = cot.get_value()

        result_text = (
            f"Секанс({angle}): {sec_value}\n"
            f"Косеканс({angle}): {cosec_value}\n"
            f"Котангенс({angle}): {cot_value}"
        )

        messagebox.showinfo("Результаты", result_text)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число.")


root = tk.Tk()
root.title("Тригонометрические функции")

root.geometry("300x200")

tk.Label(root, text="Введите угол в радианах:").pack()
entry_angle = tk.Entry(root)
entry_angle.pack()

calculate_button = tk.Button(root, text="Вычислить", command=calculate)
calculate_button.pack()

root.mainloop()
