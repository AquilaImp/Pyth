import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog

def plot_function(func_str):
    try:
        x = np.linspace(-10, 10, 400)
        y = eval(func_str)
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, label=f'y = {func_str}', color='blue')
        plt.title('График аналитической функции')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.grid()
        plt.legend()
        plt.ylim(-10, 10)
        plt.xlim(-10, 10)
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def plot_from_file(filename):
    try:
        data = pd.read_csv(filename)
        plt.figure(figsize=(10, 5))
        plt.plot(data['x'], data['y'], label='Данные из файла', color='red')
        plt.title('График из файла')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.grid()
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def on_plot_button_click():
    func_str = func_entry.get()
    plot_function(func_str)

def on_load_file_button_click():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        plot_from_file(filename)

root = Tk()
root.title("График аналитической функции")

Label(root, text="Введите функцию (например, np.sqrt(x) или x**2):").pack()
func_entry = Entry(root, width=50)
func_entry.pack()

plot_button = Button(root, text="Построить график", command=on_plot_button_click)
plot_button.pack()

load_file_button = Button(root, text="Загрузить данные из файла", command=on_load_file_button_click)
load_file_button.pack()

root.mainloop()
