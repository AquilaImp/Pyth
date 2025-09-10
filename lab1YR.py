import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import pandas as pd
import os
from tkinter import Tk, filedialog

class SimplePlotter:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self.fig.suptitle('Графики функций', fontsize=14)
        
        for ax in [self.ax1, self.ax2]:
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(0, color='black', lw=1)
            ax.axvline(0, color='black', lw=1)
        
        self.ax1.set_title('Аналитическая функция')
        self.ax2.set_title('Данные из файла') 
        plt.subplots_adjust(bottom=0.2)
        self.func_box = TextBox(plt.axes([0.2, 0.1, 0.3, 0.05]), 'Функция f(x)=', initial='sin(x)/x')
        self.plot_btn = Button(plt.axes([0.55, 0.1, 0.15, 0.06]), 'Построить график')
        self.load_btn = Button(plt.axes([0.75, 0.1, 0.15, 0.06]), 'Загрузить файл')
        self.plot_btn.on_clicked(lambda event: self.plot_function())
        self.load_btn.on_clicked(lambda event: self.load_from_file())
        self.ax1.plot([], [])[0]
        self.ax2.plot([], [])[0]
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.xlim1 = self.ylim1 = self.xlim2 = self.ylim2 = (0, 1)

    def on_scroll(self, event):
        if event.inaxes not in [self.ax1, self.ax2]: return
            
        ax = event.inaxes
        x, y = event.xdata, event.ydata
        scale = 0.8 if event.button == 'up' else 1.25
        
        xlim = np.array(ax.get_xlim())
        ylim = np.array(ax.get_ylim())
        
        new_xlim = x - (x - xlim) * scale
        new_ylim = y - (y - ylim) * scale
        
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        
        if ax == self.ax1: 
            self.xlim1, self.ylim1 = new_xlim, new_ylim
        else: 
            self.xlim2, self.ylim2 = new_xlim, new_ylim
        
        self.fig.canvas.draw_idle()
    
    def plot_function(self, event=None):
        try:
            x = np.linspace(-10, 10, 2000)
            y = np.array([self.safe_eval(self.func_box.text, xi) for xi in x])
            
            self.ax1.clear()
            self.ax1.grid(True, linestyle='--', alpha=0.7)
            self.ax1.axhline(0, color='black', lw=1)
            self.ax1.axvline(0, color='black', lw=1)
            
            valid = np.isfinite(y)
            valid_indices = np.where(valid)[0]
            
            if len(valid_indices) > 1:
                breaks = np.where(np.diff(valid_indices) > 1)[0]
                segments = np.split(valid_indices, breaks + 1)
                
                for seg in segments:
                    if len(seg) > 1:
                        seg_x = x[seg]
                        seg_y = y[seg]
                        self.ax1.plot(seg_x, seg_y, 'b-', lw=2)
            
            invalid_indices = np.where(~valid)[0]
            if len(invalid_indices) > 0:
                breaks = np.split(invalid_indices, np.where(np.diff(invalid_indices) > 1)[0] + 1)
                for brk in breaks:
                    if len(brk) > 0:
                        x_brk = x[brk[0] - 1] if brk[0] > 0 else x[0]
                        self.ax1.axvline(x=x_brk, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
            
            self.ax1.relim()
            self.ax1.autoscale_view()
            self.fig.canvas.draw_idle()
            
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_from_file(self, event=None):
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл с данными",
                filetypes=[("Excel files", "*.xlsx *.xls"), ("Text files", "*.txt *.csv"), ("All files", "*.*")]
            )
            
            if not file_path: return
                
            try:
                df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else \
                     pd.read_csv(file_path, sep='\s+|,', header=None, engine='python')
                
                x = df.iloc[:, 0].values.astype(float)
                y = df.iloc[:, 1].values.astype(float) if len(df.columns) >= 2 else df[0].values.astype(float)
                
                sort_idx = np.argsort(x)
                x, y = x[sort_idx], y[sort_idx]
                
                self.ax2.clear()
                self.ax2.grid(True, linestyle='--', alpha=0.7)
                self.ax2.axhline(0, color='black', lw=1)
                self.ax2.axvline(0, color='black', lw=1)
                
                valid = np.isfinite(y) & np.isfinite(x)
                valid_indices = np.where(valid)[0]
                
                if len(valid_indices) > 1:
                    diff_indices = np.diff(valid_indices)
                    break_points = np.where(diff_indices > 1)[0]
                    segments = np.split(valid_indices, break_points + 1)
                    
                    for seg in segments:
                        if len(seg) > 1:
                            seg_x = x[seg]
                            seg_y = y[seg]
                            self.ax2.plot(seg_x, seg_y, 'b-', lw=2, marker='o', markersize=3)
                    
                    for bp in break_points:
                        if bp < len(valid_indices) - 1:
                            x_brk = x[valid_indices[bp]]
                            self.ax2.axvline(x=x_brk, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
                elif len(valid_indices) == 1:
                    self.ax2.plot(x[valid], y[valid], 'bo', markersize=3)
                
                self.ax2.relim()
                self.ax2.autoscale_view()
                self.fig.canvas.draw_idle()
                
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                
        except Exception as e:
            print(f"Ошибка: {e}")

    def safe_eval(self, expr, x):
        try:
            return eval(expr, {'x': x, 'np': np, 'sin': np.sin, 'cos': np.cos, 
                             'tan': np.tan, 'exp': np.exp, 'log': np.log, 
                             'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
        except:
            return np.nan

if __name__ == "__main__":
    app = SimplePlotter()
    plt.show()
