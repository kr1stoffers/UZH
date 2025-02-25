import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import Database
from country import Country
from city import City
from street import Street


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("База данных стран, городов и улиц")
        self.root.geometry("600x400")

        self.db = Database()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        buttons = [
            ("Добавить страну", self.add_country),
            ("Добавить город", self.add_city),
            ("Добавить улицу", self.add_street),
            ("Удалить страну", self.remove_country),
            ("Удалить город", self.remove_city),
            ("Удалить улицу", self.remove_street),
            ("Сохранить в CSV", self.save_to_csv),
            ("Загрузить из CSV", self.load_from_csv),
            ("Показать информацию", self.show_info),
            ("Обновить таблицу", self.update_table),
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 5
            col = i % 5
            tk.Button(
                button_frame,
                text=text,
                command=command,
            ).grid(row=row, column=col, padx=5, pady=5)

        self.tree = ttk.Treeview(
            root, columns=("Country", "City", "Street"), show="headings"
        )
        self.tree.heading("Country", text="Страна")
        self.tree.heading("City", text="Город")
        self.tree.heading("Street", text="Улица")
        self.tree.column("Country", anchor="center")
        self.tree.column("City", anchor="center")
        self.tree.column("Street", anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_table()

    def add_country(self):
        name = simpledialog.askstring("Добавить страну", "Введите название страны:")
        if name:
            country_id = len(self.db.countries) + 1
            country = Country(country_id, name)
            self.db.add_country(country)
            messagebox.showinfo("Успех", f"Страна '{name}' добавлена.")
            self.update_table()

    def add_city(self):
        country_name = simpledialog.askstring(
            "Добавить город", "Введите название страны:"
        )
        country = next((c for c in self.db.countries if c.name == country_name), None)
        if country:
            city_name = simpledialog.askstring(
                "Добавить город", "Введите название города:"
            )
            city_id = len(country.cities) + 1
            city = City(city_id, city_name)
            country.add_city(city)
            messagebox.showinfo(
                "Успех", f"Город '{city_name}' добавлен в страну '{country_name}'."
            )
            self.update_table()
        else:
            messagebox.showerror("Ошибка", f"Страна '{country_name}' не найдена.")

    def add_street(self):
        country_name = simpledialog.askstring(
            "Добавить улицу", "Введите название страны:"
        )
        country = next((c for c in self.db.countries if c.name == country_name), None)
        if country:
            city_name = simpledialog.askstring(
                "Добавить улицу", "Введите название города:"
            )
            city = next((c for c in country.cities if c.name == city_name), None)
            if city:
                street_name = simpledialog.askstring(
                    "Добавить улицу", "Введите название улицы:"
                )
                street_id = len(city.streets) + 1
                street = Street(street_id, street_name, city.id)
                city.add_street(street)
                messagebox.showinfo(
                    "Успех", f"Улица '{street_name}' добавлена в город '{city_name}'."
                )
                self.update_table()
            else:
                messagebox.showerror(
                    "Ошибка",
                    f"Город '{city_name}' не найден в стране '{country_name}'.",
                )
        else:
            messagebox.showerror("Ошибка", f"Страна '{country_name}' не найдена.")

    def remove_country(self):
        country_name = simpledialog.askstring(
            "Удалить страну", "Введите название страны для удаления:"
        )
        country = next((c for c in self.db.countries if c.name == country_name), None)
        if country:
            self.db.remove_country(country.id)
            messagebox.showinfo("Успех", f"Страна '{country_name}' удалена.")
            self.update_table()
        else:
            messagebox.showerror("Ошибка", f"Страна '{country_name}' не найдена.")

    def remove_city(self):
        country_name = simpledialog.askstring(
            "Удалить город", "Введите название страны:"
        )
        country = next((c for c in self.db.countries if c.name == country_name), None)
        if country:
            city_name = simpledialog.askstring(
                "Удалить город", "Введите название города для удаления:"
            )
            city = next((c for c in country.cities if c.name == city_name), None)
            if city:
                country.remove_city(city.id)
                messagebox.showinfo(
                    "Успех", f"Город '{city_name}' удален из страны '{country_name}'."
                )
                self.update_table()
            else:
                messagebox.showerror(
                    "Ошибка",
                    f"Город '{city_name}' не найден в стране '{country_name}'.",
                )
        else:
            messagebox.showerror("Ошибка", f"Страна '{country_name}' не найдена.")

    def remove_street(self):
        country_name = simpledialog.askstring(
            "Удалить улицу", "Введите название страны:"
        )
        country = next((c for c in self.db.countries if c.name == country_name), None)
        if country:
            city_name = simpledialog.askstring(
                "Удалить улицу", "Введите название города:"
            )
            city = next((c for c in country.cities if c.name == city_name), None)
            if city:
                street_name = simpledialog.askstring(
                    "Удалить улицу", "Введите название улицы для удаления:"
                )
                street = next((s for s in city.streets if s.name == street_name), None)
                if street:
                    city.remove_street(street.id)
                    messagebox.showinfo(
                        "Успех",
                        f"Улица '{street_name}' удалена из города '{city_name}'.",
                    )
                    self.update_table()
                else:
                    messagebox.showerror(
                        "Ошибка",
                        f"Улица '{street_name}' не найдена в городе '{city_name}'.",
                    )
            else:
                messagebox.showerror(
                    "Ошибка",
                    f"Город '{city_name}' не найден в стране '{country_name}'.",
                )
        else:
            messagebox.showerror("Ошибка", f"Страна '{country_name}' не найдена.")

    def save_to_csv(self):
        filename = simpledialog.askstring(
            "Сохранить в CSV", "Введите имя файла для сохранения (с .csv):"
        )
        if filename:
            self.db.save_to_csv(filename)
            messagebox.showinfo("Успех", f"Данные сохранены в '{filename}'.")

    def load_from_csv(self):
        filename = simpledialog.askstring(
            "Загрузить из CSV", "Введите имя файла для загрузки (с .csv):"
        )
        if filename:
            self.db.load_from_csv(filename)
            messagebox.showinfo("Успех", f"Данные загружены из '{filename}'.")
            self.update_table()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for country in self.db.countries:
            has_cities = False
            for city in country.cities:
                has_cities = True
                for street in city.streets:
                    self.tree.insert(
                        "", "end", values=(country.name, city.name, street.name)
                    )
                if not city.streets:
                    self.tree.insert(
                        "", "end", values=(country.name, city.name, "Нет улиц")
                    )

            if not has_cities:
                self.tree.insert(
                    "", "end", values=(country.name, "Нет городов", "Нет улиц")
                )

    def show_info(self):
        info = ""
        for country in self.db.countries:
            info += f"Страна: {country.name}\n"
            for city in country.cities:
                info += f"  Город: {city.name}, Улиц: {city.count_streets()}\n"
            if info:
                messagebox.showinfo("Информация", info)
            else:
                messagebox.showinfo("Информация", "Нет данных для отображения.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
