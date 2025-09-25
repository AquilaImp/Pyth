import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button, TextBox
import re

class GraphPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.current_function = "x**2"
        self.x_range = (-10, 10)
        self.y_range = (-10, 10)
        self.points = 1000
        self.data_points = []
        
        self.setup_interface()
        self.plot_function()
        
    def setup_interface(self):
        plt.subplots_adjust(bottom=0.3)
        
        ax_function = plt.axes([0.1, 0.15, 0.3, 0.04])
        self.function_text = TextBox(ax_function, 'Функция: ', initial=self.current_function)
        self.function_text.on_submit(self.on_function_submit)
        
        ax_plot = plt.axes([0.45, 0.15, 0.1, 0.04])
        ax_reset = plt.axes([0.1, 0.05, 0.1, 0.04])
        ax_zoom_in = plt.axes([0.25, 0.05, 0.1, 0.04])
        ax_zoom_out = plt.axes([0.4, 0.05, 0.1, 0.04])
        ax_load_file = plt.axes([0.7, 0.05, 0.1, 0.04])
        ax_export = plt.axes([0.85, 0.05, 0.1, 0.04])
        
        self.btn_plot = Button(ax_plot, 'Построить')
        self.btn_reset = Button(ax_reset, 'Сброс')
        self.btn_zoom_in = Button(ax_zoom_in, 'Увеличить')
        self.btn_zoom_out = Button(ax_zoom_out, 'Уменьшить')
        self.btn_load_file = Button(ax_load_file, 'Файл')
        self.btn_export = Button(ax_export, 'Экспорт')
        
        self.btn_plot.on_clicked(self.on_plot_clicked)
        self.btn_reset.on_clicked(self.on_reset_clicked)
        self.btn_zoom_in.on_clicked(self.on_zoom_in_clicked)
        self.btn_zoom_out.on_clicked(self.on_zoom_out_clicked)
        self.btn_load_file.on_clicked(self.on_load_file_clicked)
        self.btn_export.on_clicked(self.on_export_clicked)
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        
    def safe_eval(self, expression, x):
        try:
            expression = expression.replace('^', '**')
            expression = expression.replace('sin', 'np.sin')
            expression = expression.replace('cos', 'np.cos')
            expression = expression.replace('tan', 'np.tan')
            expression = expression.replace('log', 'np.log')
            expression = expression.replace('ln', 'np.log')
            expression = expression.replace('exp', 'np.exp')
            expression = expression.replace('sqrt', 'np.sqrt')
            expression = expression.replace('abs', 'np.abs')
            
            def cbrt(x):
                if x >= 0:
                    return x**(1/3)
                else:
                    return -((-x)**(1/3))
            
            if '**(1/3)' in expression:
                import re
                expression = re.sub(r'\(([^)]+)\)\*\*\(1/3\)', r'cbrt(\1)', expression)
            if '**(1.0/3)' in expression:
                expression = expression.replace('**(1.0/3)', '**(1/3)')
                expression = re.sub(r'\(([^)]+)\)\*\*\(1/3\)', r'cbrt(\1)', expression)
            
            result = eval(expression, {"x": x, "np": np, "cbrt": cbrt, "__builtins__": {}})
            
            if '**(1/3)' in expression:
                if np.iscomplexobj(result):
                    result = result.real
                return result
            
            if np.iscomplexobj(result):
                return np.nan
            if np.isfinite(result) and (result.imag != 0 if np.iscomplexobj(result) else False):
                return np.nan
                
            return result
        except:
            return np.nan
    
    def plot_function(self):
        self.ax.clear()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        
        self.ax.set_xlim(self.x_range)
        
        if self.data_points:
            x_data = [p[0] for p in self.data_points]
            y_data = [p[1] for p in self.data_points]
            self.ax.plot(x_data, y_data, 'b-', linewidth=2, label='Данные из файла')
        else:
            x = np.linspace(self.x_range[0], self.x_range[1], self.points)
            y = np.array([self.safe_eval(self.current_function, xi) for xi in x])
            
            self.ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {self.current_function}')
        
        self.ax.legend()
        self.ax.set_title(f'График функции: {self.current_function}')
        
        if self.y_range is not None:
            self.ax.set_ylim(self.y_range)
        
        plt.draw()
    
    def plot_implicit_function(self):
        try:
            if 'x=' in self.current_function:
                right_side = self.current_function.split('x=')[1].strip()
                
                x = np.linspace(self.x_range[0], self.x_range[1], 100)
                y = np.linspace(self.y_range[0] if self.y_range else -10, 
                               self.y_range[1] if self.y_range else 10, 100)
                X, Y = np.meshgrid(x, y)
                
                left_side = X
                right_side_eval = self.safe_eval(right_side, Y)
                
                Z = left_side - right_side_eval
                
                self.ax.contour(X, Y, Z, levels=[0], colors='blue', linewidths=2, label=f'{self.current_function}')
                
        except Exception as e:
            print(f"Ошибка при построении неявной функции: {e}")
    
    
    def on_function_submit(self, text):
        if text:
            self.current_function = text
            self.data_points = []
            self.plot_function()
    
    def on_plot_clicked(self, event):
        function = self.function_text.text
        if function:
            self.current_function = function
            self.data_points = []
            self.plot_function()
    
    def on_reset_clicked(self, event):
        self.x_range = (-10, 10)
        self.y_range = None
        self.plot_function()
    
    def on_zoom_in_clicked(self, event):
        center_x = (self.x_range[0] + self.x_range[1]) / 2
        width = (self.x_range[1] - self.x_range[0]) * 0.5
        self.x_range = (center_x - width/2, center_x + width/2)
        self.plot_function()
    
    def on_zoom_out_clicked(self, event):
        center_x = (self.x_range[0] + self.x_range[1]) / 2
        width = (self.x_range[1] - self.x_range[0]) * 2
        self.x_range = (center_x - width/2, center_x + width/2)
        self.plot_function()
    
    def on_load_file_clicked(self, event):
        import os
        possible_files = ['data.txt', 'data.csv', 'test_data.txt', 'sample.csv']
        
        for filename in possible_files:
            if os.path.exists(filename):
                try:
                    self.load_data_from_file(filename)
                    self.current_function = "Данные из файла"
                    self.plot_function()
                    print(f"Загружено {len(self.data_points)} точек из файла {filename}")
                    return
                except Exception as e:
                    print(f"Ошибка при загрузке файла {filename}: {str(e)}")
                    continue
        
        print("Файлы данных не найдены. Создайте файл data.txt с данными в формате:")
        print("1 2")
        print("2 4") 
        print("3 6")
        print("4 8")
        print("5 10")
    
    def load_data_from_file(self, file_path):
        self.data_points = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                parts = re.split(r'[,\s;]+', line)
                if len(parts) >= 2:
                    try:
                        x = float(parts[0])
                        y = float(parts[1])
                        self.data_points.append((x, y))
                    except ValueError:
                        continue

        self.data_points.sort(key=lambda p: p[0])
        
        if self.data_points:
            x_values = [p[0] for p in self.data_points]
            y_values = [p[1] for p in self.data_points]
            
            x_padding = (max(x_values) - min(x_values)) * 0.1
            y_padding = (max(y_values) - min(y_values)) * 0.1
            
            self.x_range = (min(x_values) - x_padding, max(x_values) + x_padding)
            self.y_range = (min(y_values) - y_padding, max(y_values) + y_padding)
    
    def on_export_clicked(self, event):
        if not self.data_points:
            x = np.linspace(self.x_range[0], self.x_range[1], self.points)
            y = np.array([self.safe_eval(self.current_function, xi) for xi in x])
            
            data = list(zip(x, y))
        else:
            data = self.data_points
        
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exported_data_{timestamp}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("x,y\n")
                for x, y in data:
                    if np.isfinite(y):
                        file.write(f"{x},{y}\n")
            print(f"Данные сохранены в {filename}")
            print(f"Полный путь: {os.path.abspath(filename)}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {str(e)}")
    
    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return
        
        x_mouse = event.xdata
        y_mouse = event.ydata
        
        if x_mouse is None or y_mouse is None:
            return
        
        if hasattr(event, 'step'):
            scale_factor = 1.0 - event.step * 0.1
        else:
            scale_factor = 0.9 