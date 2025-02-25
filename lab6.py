import tkinter as tk
from tkinter import colorchooser
import numpy as np
import matplotlib.pyplot as plt


class GraphApp:
    def __init__(self, master):
        self.master = master
        master.title("График функции")

        self.label_a = tk.Label(master, text="Коэффициент a:")
        self.label_a.pack()
        self.entry_a = tk.Entry(master)
        self.entry_a.pack()

        self.label_b = tk.Label(master, text="Коэффициент b:")
        self.label_b.pack()
        self.entry_b = tk.Entry(master)
        self.entry_b.pack()

        self.label_c = tk.Label(master, text="Коэффициент c:")
        self.label_c.pack()
        self.entry_c = tk.Entry(master)
        self.entry_c.pack()

        self.label_d = tk.Label(master, text="Коэффициент d:")
        self.label_d.pack()
        self.entry_d = tk.Entry(master)
        self.entry_d.pack()

        self.label_f = tk.Label(master, text="Коэффициент f:")
        self.label_f.pack()
        self.entry_f = tk.Entry(master)
        self.entry_f.pack()

        self.label_g = tk.Label(master, text="Коэффициент g:")
        self.label_g.pack()
        self.entry_g = tk.Entry(master)
        self.entry_g.pack()

        self.label_x_min = tk.Label(master, text="Минимальное значение x:")
        self.label_x_min.pack()
        self.entry_x_min = tk.Entry(master)
        self.entry_x_min.pack()

        self.label_x_max = tk.Label(master, text="Максимальное значение x:")
        self.label_x_max.pack()
        self.entry_x_max = tk.Entry(master)
        self.entry_x_max.pack()

        self.button_bg_color = tk.Button(
            master, text="Выбрать цвет фона", command=self.choose_bg_color
        )
        self.button_bg_color.pack()

        self.button_line_color = tk.Button(
            master, text="Выбрать цвет графика", command=self.choose_line_color
        )
        self.button_line_color.pack()

        self.button_plot = tk.Button(
            master, text="Построить график", command=self.plot_graph
        )
        self.button_plot.pack()

        self.bg_color = "white"
        self.line_color = "blue"

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color

    def choose_line_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.line_color = color

    def plot_graph(self):
        a = float(self.entry_a.get()) if self.entry_a.get() else 1
        b = float(self.entry_b.get()) if self.entry_b.get() else 1
        c = float(self.entry_c.get()) if self.entry_c.get() else 1
        d = float(self.entry_d.get()) if self.entry_d.get() else 1
        f = float(self.entry_f.get()) if self.entry_f.get() else 1
        g = float(self.entry_g.get()) if self.entry_g.get() else 1
        x_min = float(self.entry_x_min.get()) if self.entry_x_min.get() else 0
        x_max = float(self.entry_x_max.get()) if self.entry_x_max.get() else 100

        x = np.linspace(x_min, x_max, 400)
        y = np.exp(np.sin(a * x**2 + b * x + c)) + d * np.cos(f * x + g)

        plt.figure(facecolor=self.bg_color)
        plt.plot(x, y, color=self.line_color)
        plt.axhline(0, color="black", lw=0.5)
        plt.axvline(0, color="black", lw=0.5)
        plt.title("График функции")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()
        plt.xlim(x_min, x_max)
        plt.ylim(min(y) - 1, max(y) + 1)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x450")
    app = GraphApp(root)
    root.mainloop()
