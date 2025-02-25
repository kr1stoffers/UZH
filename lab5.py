import sqlite3
import tkinter as tk
from tkinter import messagebox


def create_database():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Должность (
            id INTEGER PRIMARY KEY,
            Название TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Кафедра (
            id INTEGER PRIMARY KEY,
            Название TEXT,
            Институт TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Преподаватель (
            id INTEGER PRIMARY KEY,
            ФИО TEXT,
            Возраст INTEGER,
            id_Кафедры INTEGER,
            id_Должности INTEGER,
            FOREIGN KEY (id_Кафедры) REFERENCES Кафедра(id),
            FOREIGN KEY (id_Должности) REFERENCES Должность(id)
        )
    """
    )

    cursor.execute(
        "INSERT INTO Должность (Название) VALUES ('Профессор'), ('Доцент'), ('Ассистент')"
    )
    cursor.execute(
        "INSERT INTO Кафедра (Название, Институт) VALUES ('Кафедра математики', 'Физико-математический'), ('Кафедра физики', 'Физико-математический'), ('Кафедра информатики', 'Институт информационных технологий')"
    )

    cursor.execute(
        "INSERT INTO Преподаватель (ФИО, Возраст, id_Кафедры, id_Должности) VALUES ('Иванов И.И.', 45, 1, 1)"
    )
    cursor.execute(
        "INSERT INTO Преподаватель (ФИО, Возраст, id_Кафедры, id_Должности) VALUES ('Петров П.П.', 38, 1, 2)"
    )
    cursor.execute(
        "INSERT INTO Преподаватель (ФИО, Возраст, id_Кафедры, id_Должности) VALUES ('Сидоров С.С.', 29, 2, 3)"
    )
    cursor.execute(
        "INSERT INTO Преподаватель (ФИО, Возраст, id_Кафедры, id_Должности) VALUES ('Кузнецов К.К.', 50, 2, 1)"
    )
    cursor.execute(
        "INSERT INTO Преподаватель (ФИО, Возраст, id_Кафедры, id_Должности) VALUES ('Смирнова А.А.', 35, 3, 2)"
    )

    conn.commit()
    conn.close()


def get_department_with_most_employees():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT Кафедра.Название, COUNT(Преподаватель.id) AS Количество
        FROM Кафедра
        LEFT JOIN Преподаватель ON Кафедра.id = Преподаватель.id_Кафедры
        GROUP BY Кафедра.id
        ORDER BY Количество DESC
        LIMIT 1
    """
    )
    result = cursor.fetchone()
    conn.close()
    return result


def get_departments_by_employee_count():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT Кафедра.Название, COUNT(Преподаватель.id) AS Количество
        FROM Кафедра
        LEFT JOIN Преподаватель ON Кафедра.id = Преподаватель.id_Кафедры
        GROUP BY Кафедра.id
        ORDER BY Количество DESC
    """
    )
    result = cursor.fetchall()
    conn.close()
    return result


def get_youngest_department():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT Кафедра.Название, AVG(Преподаватель.Возраст) AS Средний_возраст
        FROM Кафедра
        LEFT JOIN Преподаватель ON Кафедра.id = Преподаватель.id_Кафедры
        GROUP BY Кафедра.id
        ORDER BY Средний_возраст ASC
        LIMIT 1
    """
    )
    result = cursor.fetchone()
    conn.close()
    return result


def show_results():
    most_employees = get_department_with_most_employees()
    departments_count = get_departments_by_employee_count()
    youngest_department = get_youngest_department()

    most_employees_str = f"Кафедра с наибольшим количеством сотрудников: {most_employees[0]} ({most_employees[1]} сотрудников)"

    departments_count_str = "Список кафедр по убыванию количества сотрудников:\n"
    for dept in departments_count:
        departments_count_str += f"{dept[0]}: {dept[1]} сотрудников\n"

    youngest_department_str = f"Самая молодая кафедра: {youngest_department[0]} (Средний возраст: {youngest_department[1]:.2f} лет)"

    result_window = tk.Toplevel()
    result_window.title("Результаты")

    result_text = (
        f"{most_employees_str}\n\n{departments_count_str}\n{youngest_department_str}"
    )
    result_label = tk.Label(result_window, text=result_text, justify=tk.LEFT)
    result_label.pack(padx=10, pady=10)


def main():
    create_database()

    root = tk.Tk()
    root.title("Управление кафедрами")

    show_results_button = tk.Button(
        root, text="Показать результаты", command=show_results
    )
    show_results_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
