import tkinter as tk
import random
import threading
import time
from abc import ABC, abstractmethod


class ArrayVisualizer(ABC):
    def __init__(self, size):
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.canvas = None

    def display_array(self):
        if self.canvas:
            self.canvas.delete("all")
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            bar_width = width // len(self.array)
            for i, value in enumerate(self.array):
                x0 = i * bar_width
                y0 = height - (value * height // 100)
                x1 = (i + 1) * bar_width
                y1 = height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

    def fill_array(self):
        self.array = [random.randint(1, 100) for _ in range(len(self.array))]

    @abstractmethod
    def sort(self):
        pass


class SelectionSort(ArrayVisualizer):
    def sort(self):
        for i in range(len(self.array)):
            min_idx = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.display_array()
            time.sleep(0.1)


class QuickSort(ArrayVisualizer):
    def sort(self):
        self._quick_sort(0, len(self.array) - 1)

    def _quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self._quick_sort(low, pi - 1)
            self._quick_sort(pi + 1, high)
            self.display_array()
            time.sleep(0.1)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1


class MergeSort(ArrayVisualizer):
    def sort(self):
        self._merge_sort(0, len(self.array) - 1)

    def _merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(left, mid)
            self._merge_sort(mid + 1, right)
            self.merge(left, mid, right)
            self.display_array()
            time.sleep(0.1)

    def merge(self, left, mid, right):
        left_half = self.array[left : mid + 1]
        right_half = self.array[mid + 1 : right + 1]
        i = j = 0
        k = left
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                self.array[k] = left_half[i]
                i += 1
            else:
                self.array[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            self.array[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            self.array[k] = right_half[j]
            j += 1
            k += 1


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортировка массивов")

        self.selection_canvas = tk.Canvas(root, width=800, height=200, bg="white")
        self.selection_canvas.pack()
        self.quick_canvas = tk.Canvas(root, width=800, height=200, bg="white")
        self.quick_canvas.pack()
        self.merge_canvas = tk.Canvas(root, width=800, height=200, bg="white")
        self.merge_canvas.pack()

        self.size = 100
        self.selection_sort = SelectionSort(self.size)
        self.quick_sort = QuickSort(self.size)
        self.merge_sort = MergeSort(self.size)

        self.selection_sort.canvas = self.selection_canvas
        self.quick_sort.canvas = self.quick_canvas
        self.merge_sort.canvas = self.merge_canvas

        self.selection_thread = None
        self.quick_thread = None
        self.merge_thread = None

        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(
            self.root, text="Запустить сортировки", command=self.start_sorting
        )
        self.start_button.pack()

        self.reset_button = tk.Button(
            self.root, text="Сбросить массив", command=self.reset_array
        )
        self.reset_button.pack()

        self.priority_label = tk.Label(self.root, text="Приоритеты потоков (1-10):")
        self.priority_label.pack()

        self.selection_priority = tk.Scale(
            self.root, from_=1, to=10, orient=tk.HORIZONTAL, label="Сортировка выбором"
        )
        self.selection_priority.set(5)
        self.selection_priority.pack()

        self.quick_priority = tk.Scale(
            self.root, from_=1, to=10, orient=tk.HORIZONTAL, label="Быстрая сортировка"
        )
        self.quick_priority.set(5)
        self.quick_priority.pack()

        self.merge_priority = tk.Scale(
            self.root, from_=1, to=10, orient=tk.HORIZONTAL, label="Сортировка слиянием"
        )
        self.merge_priority.set(5)
        self.merge_priority.pack()

    def reset_array(self):
        self.selection_sort.fill_array()
        self.quick_sort.fill_array()
        self.merge_sort.fill_array()
        self.selection_sort.display_array()
        self.quick_sort.display_array()
        self.merge_sort.display_array()

    def start_sorting(self):
        self.reset_array()
        self.start_threads()

    def start_threads(self):
        if self.selection_thread is not None:
            self.selection_thread.join()
        if self.quick_thread is not None:
            self.quick_thread.join()
        if self.merge_thread is not None:
            self.merge_thread.join()

        self.selection_thread = threading.Thread(target=self.run_selection_sort)
        self.quick_thread = threading.Thread(target=self.run_quick_sort)
        self.merge_thread = threading.Thread(target=self.run_merge_sort)

        self.selection_thread.start()
        self.quick_thread.start()
        self.merge_thread.start()

    def run_selection_sort(self):
        self.set_thread_priority(self.selection_thread, self.selection_priority.get())
        self.selection_sort.sort()

    def run_quick_sort(self):
        self.set_thread_priority(self.quick_thread, self.quick_priority.get())
        self.quick_sort.sort()

    def run_merge_sort(self):
        self.set_thread_priority(self.merge_thread, self.merge_priority.get())
        self.merge_sort.sort()

    def set_thread_priority(self, thread, priority):
        time.sleep(1 / priority)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
