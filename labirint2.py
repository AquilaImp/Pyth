import tkinter as tk
from tkinter import messagebox, filedialog
import random

CELL_SIZE = 40
ROWS = 10
COLS = 10

class LabyrinthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт")
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.mode = 0  
        self.create_ui()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()
        # 0=пусто, 1=стена, 2=вход, 3=выход
        tk.Button(frame, text="Пусто", command=lambda: self.set_mode(0)).pack(side=tk.LEFT)
        tk.Button(frame, text="Стена", command=lambda: self.set_mode(1)).pack(side=tk.LEFT)
        tk.Button(frame, text="Вход", command=lambda: self.set_mode(2)).pack(side=tk.LEFT)
        tk.Button(frame, text="Выход", command=lambda: self.set_mode(3)).pack(side=tk.LEFT)
        tk.Button(frame, text="Рассчитать путь", command=self.find_path).pack(side=tk.LEFT)
        tk.Button(frame, text="Сгенерировать лабиринт", command=self.generate_maze).pack(side=tk.LEFT)
        tk.Button(frame, text="Сохранить", command=self.save_grid).pack(side=tk.LEFT)
        tk.Button(frame, text="Открыть", command=self.load_grid).pack(side=tk.LEFT)
        tk.Button(frame, text="Очистить", command=self.clear_grid).pack(side=tk.LEFT)

    def set_mode(self, mode):
        self.mode = mode
    #нажималка со сбросом
    def on_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < COLS and 0 <= y < ROWS:
            if self.mode == 2:  # вход
                if self.start:
                    self.grid[self.start[1]][self.start[0]] = 0
                self.start = (x, y)
                self.grid[y][x] = 2
            elif self.mode == 3:  # выход
                if self.end:
                    self.grid[self.end[1]][self.end[0]] = 0
                self.end = (x, y)
                self.grid[y][x] = 3
            else:
                # Очищаем старый путь при изменении стен
                if self.grid[y][x] == 4 or (self.mode == 1 and self.grid[y][x] == 0):
                    self.clear_path()
                self.grid[y][x] = self.mode
            self.draw_grid()

    def draw_grid(self):#рис
        self.canvas.delete("all")
        for y in range(ROWS):
            for x in range(COLS):
                color = "white"
                val = self.grid[y][x]
                if val == 1:
                    color = "black"
                elif val == 2:
                    color = "blue"
                elif val == 3:
                    color = "red"
                elif val == 4:
                    color = "green"
                self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE,
                                             (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                                             fill=color, outline="gray")

    def find_path(self):
        if not self.start or not self.end:
            messagebox.showerror("Ошибка", "Установите вход и выход")
            return
            
        # Очищаем старый путь
        self.clear_path()

        # Волновой алгоритм
        from collections import deque
        queue = deque()
        visited = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        sx, sy = self.start
        ex, ey = self.end
        queue.append((sx, sy))
        visited[sy][sx] = 0
        directions = [(-1,0),(1,0),(0,-1),(0,1)]  # Вверх, вниз, влево, вправо

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.end:
                break
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if self.grid[ny][nx] != 1 and visited[ny][nx] == -1:
                        visited[ny][nx] = visited[y][x] + 1
                        queue.append((nx, ny))

        if visited[ey][ex] == -1:
            messagebox.showinfo("Результат", "Путь не найден")
            return

        # Восстановление пути
        path = []
        x, y = ex, ey
        while (x, y) != (sx, sy):
            path.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if visited[ny][nx] == visited[y][x] - 1:
                        x, y = nx, ny
                        break
        path.append((sx, sy))
        path.reverse()
        for x, y in path:
            if self.grid[y][x] not in (2, 3):
                self.grid[y][x] = 4
        self.draw_grid()
    #Сохранялка
    def save_grid(self):
        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file:
            return
        with file:
            for row in self.grid:
                file.write("".join(map(str, row)) + "\n")
    #Подсветка 
    def load_grid(self):
        file = filedialog.askopenfile(filetypes=[("Text files", "*.txt")])
        if not file:
            return
        with file:
            lines = file.readlines()
            for y, line in enumerate(lines[:ROWS]):
                for x, ch in enumerate(line.strip()[:COLS]):
                    val = int(ch)
                    self.grid[y][x] = val
                    if val == 2:
                        self.start = (x, y)
                    elif val == 3:
                        self.end = (x, y)
        self.draw_grid()
        
    def clear_path(self):
        """Очищает только путь (зелёные клетки), оставляя стены, вход и выход"""
        for y in range(ROWS):
            for x in range(COLS):
                if self.grid[y][x] == 4:  # 4 - это путь (зелёный)
                    self.grid[y][x] = 0  # 0 - пустая клетка
        # Не вызываем draw_grid() здесь, чтобы избежать лишних перерисовок

    def clear_grid(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None
        self.draw_grid()
        
    def generate_maze(self):
        """Генерирует случайный лабиринт используя алгоритм поиска в глубину"""
        self.clear_grid()
        for y in range(ROWS):
            for x in range(COLS):
                self.grid[y][x] = 1
        stack = [(0, 0)]
        self.grid[0][0] = 0 
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and self.grid[ny][nx] == 1:
                    self.grid[ny][nx] = 0
                    self.grid[y + dy//2][x + dx//2] = 0
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()
        
        border_cells = []
        for x in range(COLS):
            if self.grid[0][x] == 0: border_cells.append((x, 0))
            if self.grid[ROWS-1][x] == 0: border_cells.append((x, ROWS-1))
        for y in range(1, ROWS-1):
            if self.grid[y][0] == 0: border_cells.append((0, y))
            if self.grid[y][COLS-1] == 0: border_cells.append((COLS-1, y))
        
        if len(border_cells) >= 2:

            random.shuffle(border_cells)
            self.start = border_cells[0]
            self.end = border_cells[-1]
            self.grid[self.start[1]][self.start[0]] = 2
            self.grid[self.end[1]][self.end[0]] = 3
        
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabyrinthApp(root)
    root.mainloop()