import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class GraphParams:
    def __init__(self):
        self.defaults = {
            "sin_cos": {
                "start": 0.0,
                "end": 1.0,
                "step": 0.01,
                "freq_sin": 2,
                "freq_cos": 1,
            },
            "spiral": {"theta_start": -4, "theta_end": 4, "z_start": -2, "z_end": 2},
            "scatter": {"n1": 20, "n2": 120, "n3": 70},
            "sphere": {"radius": 10, "resolution": 100},
            "surface": {"grid_size": 5, "grid_step": 0.05, "light_angle": 65},
        }


def create_sin_cos_plot(params):
    plt.figure(figsize=(10, 6))
    x = np.arange(params["start"], params["end"], params["step"])
    y_sin = np.sin(params["freq_sin"] * 2 * np.pi * x)
    y_cos = np.cos(params["freq_cos"] * np.pi * x)
    plt.plot(x, y_sin, label="sin")
    plt.plot(x, y_cos, label="cos")
    plt.title("График синуса и косинуса")
    plt.legend()
    plt.grid(True)


def create_spiral_plot(params):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    theta = np.linspace(params["theta_start"] * np.pi, params["theta_end"] * np.pi, 100)
    z = np.linspace(params["z_start"], params["z_end"], 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, z)
    plt.title("3D спираль")


def create_scatter_plot(params):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    colors = ["red", "blue", "green"]
    for i, n in enumerate([params["n1"], params["n2"], params["n3"]]):
        x = np.random.sample(n)
        y = np.random.sample(n)
        ax.scatter(x, y, zs=0, zdir="y", color=colors[i], label=f"Group {i+1}")
    plt.title("3D scatter plot")
    plt.legend()


def create_sphere_plot(params):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, params["resolution"])
    v = np.linspace(0, np.pi, params["resolution"])
    x = params["radius"] * np.outer(np.cos(u), np.sin(v))
    y = params["radius"] * np.outer(np.sin(u), np.sin(v))
    z = params["radius"] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z)
    plt.title("Поверхность сферы")


def create_surface_plot(params):
    fig = plt.figure(figsize=(10, 6))
    X, Y = np.mgrid[
        -params["grid_size"] : params["grid_size"] : params["grid_step"],
        -params["grid_size"] : params["grid_size"] : params["grid_step"],
    ]
    Z = np.sqrt(X**2 + Y**2) + np.sin(X**2 + Y**2)
    ls = LightSource(azdeg=0, altdeg=params["light_angle"])
    rgb = ls.shade(Z, plt.cm.copper)
    plt.imshow(rgb)
    plt.title("Визуализация с использованием imshow")
    plt.colorbar()


class DynamicGraph:
    def __init__(self, graph_type, params):
        self.window = tk.Toplevel()
        self.window.title(f"Динамический график - {graph_type}")
        self.window.geometry("1000x800")

        self.graph_type = graph_type
        self.params = params.copy()

        # Создаем фрейм для графика
        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Добавляем панель инструментов matplotlib
        toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        toolbar.update()

        # Создаем фрейм для слайдеров
        self.control_frame = ttk.Frame(self.window)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Создаем слайдеры в зависимости от типа графика
        self.create_controls()

        # Первоначальное построение графика
        self.update_plot()

    def create_slider(self, name, from_, to_, default, resolution=0.01):
        frame = ttk.Frame(self.control_frame)
        frame.pack(side=tk.TOP, fill=tk.X, pady=2)

        ttk.Label(frame, text=name).pack(side=tk.LEFT)
        slider = ttk.Scale(
            frame,
            from_=from_,
            to=to_,
            orient=tk.HORIZONTAL,
            command=lambda _: self.update_plot(),
        )
        slider.set(default)
        slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return slider

    def create_controls(self):
        self.controls = {}
        if self.graph_type == "sin_cos":
            self.controls["freq_sin"] = self.create_slider(
                "Частота sin", 0, 10, self.params["freq_sin"]
            )
            self.controls["freq_cos"] = self.create_slider(
                "Частота cos", 0, 10, self.params["freq_cos"]
            )
            self.controls["start"] = self.create_slider(
                "Начало", -5, 0, self.params["start"]
            )
            self.controls["end"] = self.create_slider("Конец", 0, 5, self.params["end"])

        elif self.graph_type == "spiral":
            self.controls["theta_start"] = self.create_slider(
                "Начало theta", -10, 0, self.params["theta_start"]
            )
            self.controls["theta_end"] = self.create_slider(
                "Конец theta", 0, 10, self.params["theta_end"]
            )
            self.controls["z_start"] = self.create_slider(
                "Начало z", -5, 0, self.params["z_start"]
            )
            self.controls["z_end"] = self.create_slider(
                "Конец z", 0, 5, self.params["z_end"]
            )

        elif self.graph_type == "scatter":
            self.controls["n1"] = self.create_slider(
                "Группа 1", 5, 100, self.params["n1"], 1
            )
            self.controls["n2"] = self.create_slider(
                "Группа 2", 5, 200, self.params["n2"], 1
            )
            self.controls["n3"] = self.create_slider(
                "Группа 3", 5, 150, self.params["n3"], 1
            )

        elif self.graph_type == "sphere":
            self.controls["radius"] = self.create_slider(
                "Радиус", 1, 20, self.params["radius"]
            )
            self.controls["resolution"] = self.create_slider(
                "Разрешение", 10, 200, self.params["resolution"], 1
            )

        elif self.graph_type == "surface":
            self.controls["grid_size"] = self.create_slider(
                "Размер сетки", 1, 10, self.params["grid_size"]
            )
            self.controls["grid_step"] = self.create_slider(
                "Шаг сетки", 0.01, 0.2, self.params["grid_step"]
            )
            self.controls["light_angle"] = self.create_slider(
                "Угол освещения", 0, 90, self.params["light_angle"]
            )

    def update_params(self):
        for key, control in self.controls.items():
            self.params[key] = control.get()

    def update_plot(self):
        self.update_params()
        self.fig.clear()

        if self.graph_type == "sin_cos":
            ax = self.fig.add_subplot(111)
            x = np.arange(self.params["start"], self.params["end"], self.params["step"])
            y_sin = np.sin(self.params["freq_sin"] * 2 * np.pi * x)
            y_cos = np.cos(self.params["freq_cos"] * np.pi * x)
            ax.plot(x, y_sin, label="sin")
            ax.plot(x, y_cos, label="cos")
            ax.set_title("График синуса и косинуса")
            ax.legend()
            ax.grid(True)

        elif self.graph_type == "spiral":
            ax = self.fig.add_subplot(111, projection="3d")
            theta = np.linspace(
                self.params["theta_start"] * np.pi,
                self.params["theta_end"] * np.pi,
                100,
            )
            z = np.linspace(self.params["z_start"], self.params["z_end"], 100)
            r = z**2 + 1
            x = r * np.sin(theta)
            y = r * np.cos(theta)
            ax.plot(x, y, z)
            ax.set_title("3D спираль")

        elif self.graph_type == "scatter":
            ax = self.fig.add_subplot(111, projection="3d")
            colors = ["red", "blue", "green"]
            for i, n in enumerate(
                [self.params["n1"], self.params["n2"], self.params["n3"]]
            ):
                x = np.random.sample(int(n))
                y = np.random.sample(int(n))
                ax.scatter(x, y, zs=0, zdir="y", color=colors[i], label=f"Group {i+1}")
            ax.set_title("3D scatter plot")
            ax.legend()

        elif self.graph_type == "sphere":
            ax = self.fig.add_subplot(111, projection="3d")
            u = np.linspace(0, 2 * np.pi, int(self.params["resolution"]))
            v = np.linspace(0, np.pi, int(self.params["resolution"]))
            x = self.params["radius"] * np.outer(np.cos(u), np.sin(v))
            y = self.params["radius"] * np.outer(np.sin(u), np.sin(v))
            z = self.params["radius"] * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x, y, z)
            ax.set_title("Поверхность сферы")

        elif self.graph_type == "surface":
            ax = self.fig.add_subplot(111)
            X, Y = np.mgrid[
                -self.params["grid_size"] : self.params["grid_size"] : self.params[
                    "grid_step"
                ],
                -self.params["grid_size"] : self.params["grid_size"] : self.params[
                    "grid_step"
                ],
            ]
            Z = np.sqrt(X**2 + Y**2) + np.sin(X**2 + Y**2)
            ls = LightSource(azdeg=0, altdeg=self.params["light_angle"])
            rgb = ls.shade(Z, plt.cm.copper)
            ax.imshow(rgb)
            ax.set_title("Визуализация с использованием imshow")
            self.fig.colorbar(ax.imshow(rgb))

        self.canvas.draw()


class SimpleGraphApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Графики")
        self.root.geometry("300x200")
        self.params = GraphParams().defaults
        self.setup_ui()

    def setup_ui(self):
        for i, (name, title) in enumerate(
            [
                ("sin_cos", "Синус и Косинус"),
                ("spiral", "3D Спираль"),
                ("scatter", "Scatter Plot"),
                ("sphere", "Сфера"),
                ("surface", "Поверхность"),
            ]
        ):
            btn = ttk.Button(
                self.root,
                text=title,
                command=lambda n=name: self.create_dynamic_graph(n),
            )
            btn.pack(pady=5, padx=10, fill=tk.X)

    def create_dynamic_graph(self, graph_type):
        DynamicGraph(graph_type, self.params[graph_type])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleGraphApp()
    app.run()
