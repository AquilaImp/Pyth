import tkinter as tk
from tkinter import ttk
import random

move_x = [2, 1, -1, -2, -2, -1, 1, 2]
move_y = [1, 2, 2, 1, -1, -2, -2, -1]

class KnightTourApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Коняш")

        self.width = 8
        self.height = 8
        self.CELL_SIZE = 60
        self.solutions_count = {}  # (x, y) -> количество решений

        control_frame = ttk.Frame(master)
        control_frame.pack(pady=10)

        self.width_var = tk.StringVar(value="8")
        width_entry = ttk.Entry(control_frame, textvariable=self.width_var, width=5)
        width_entry.pack(side=tk.LEFT, padx=5)

        self.height_var = tk.StringVar(value="8")
        height_entry = ttk.Entry(control_frame, textvariable=self.height_var, width=5)
        height_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Применить", command=self.apply_size).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(master, width=self.width*self.CELL_SIZE, height=self.height*self.CELL_SIZE)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        self.start_x = None
        self.start_y = None
        self.board = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        self.draw_board()

        self.start_button = tk.Button(master, text="Начать тур", command=self.start_tour)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="Сброс", command=self.reset)
        self.reset_button.pack(pady=5)

        self.status = tk.Label(master, text="Выберите начальную клетку (клик)")
        self.status.pack()

    def apply_size(self):
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            if new_width < 3 or new_width > 10 or new_height < 3 or new_height > 10:
                self.status.config(text="Размер доски должен быть от 3 до 10 (из-за сложности)")
                return

            self.width = new_width
            self.height = new_height
            max_dimension = max(self.width, self.height)
            self.CELL_SIZE = max(30, 500 // max_dimension)
            self.canvas.config(width=self.width*self.CELL_SIZE, height=self.height*self.CELL_SIZE)
            self.solutions_count = {}
            self.reset()
            self.status.config(text=f"Доска {self.width}x{self.height} готова.")
        except ValueError:
            self.status.config(text="Введите корректные числа")

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.width):
            for j in range(self.height):
                color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"
                x1 = i * self.CELL_SIZE
                y1 = j * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if self.board[j][i] != -1:
                    total_moves = self.width * self.height
                    fill_color = "red" if self.board[j][i] == total_moves else "blue"
                    font_size = max(10, self.CELL_SIZE // 3)
                    self.canvas.create_text(x1 + self.CELL_SIZE // 2, y1 + self.CELL_SIZE // 2,
                                            text=str(self.board[j][i]), font=("Arial", font_size), fill=fill_color)

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == -1
    #перебор коня
    def count_solutions_from(self, start_x, start_y):
        count = 0
        total_moves = self.width * self.height
        board = [[-1 for _ in range(self.width)] for _ in range(self.height)]

        def backtrack(x, y, move_num):
            nonlocal count
            if move_num == total_moves + 1:
                count += 1
                return
            for i in range(8):
                nx = x + move_x[i]
                ny = y + move_y[i]
                if 0 <= nx < self.width and 0 <= ny < self.height and board[ny][nx] == -1:
                    board[ny][nx] = move_num
                    backtrack(nx, ny, move_num + 1)
                    board[ny][nx] = -1

        board[start_y][start_x] = 1
        backtrack(start_x, start_y, 2)
        return count

    def on_click(self, event):
        i = event.x // self.CELL_SIZE
        j = event.y // self.CELL_SIZE
        if 0 <= i < self.width and 0 <= j < self.height:
            self.start_x = i
            self.start_y = j
            self.board = [[-1 for _ in range(self.width)] for _ in range(self.height)]
            self.board[j][i] = 1
            self.draw_board()

            if (i, j) not in self.solutions_count:
                self.status.config(text=f"Считаю решения для ({i}, {j})...")
                self.master.update()
                count = self.count_solutions_from(i, j)
                self.solutions_count[(i, j)] = count

            count = self.solutions_count[(i, j)]
            self.status.config(text=f"Начальная клетка: ({i}, {j}) — решений: {count}")

    def start_tour(self):
        if self.start_x is None or self.start_y is None:
            self.status.config(text="Сначала выберите стартовую клетку!")
            return
            
        x, y = self.start_x, self.start_y
        total_moves = self.width * self.height
        move_number = 2
        
        # Reset board
        self.board = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        self.board[y][x] = 1
        
        # Find solution
        while move_number <= total_moves:
            min_deg = 9
            next_x, next_y = -1, -1
            
            for i in range(8):
                nx = x + move_x[i]
                ny = y + move_y[i]
                if self.is_valid(nx, ny):
                    c = self.get_degree(nx, ny)
                    if c < min_deg:
                        min_deg = c
                        next_x, next_y = nx, ny
            
            if next_x == -1:
                self.status.config(text="Нет решения с этой точки")
                return
                
            x, y = next_x, next_y
            self.board[y][x] = move_number
            move_number += 1
        
        self.draw_board()
        self.status.config(text=f"Найдено решение! Все {total_moves} клеток посещены.")
    
    #Считает число свободных по Варнсдорфу.
    def get_degree(self, x, y):
        count = 0
        for i in range(8):
            nx = x + move_x[i]
            ny = y + move_y[i]
            if self.is_valid(nx, ny):
                count += 1
        return count

    def reset(self):
        self.start_x = None
        self.start_y = None
        self.board = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        self.solutions_count = {}
        self.draw_board()
        self.status.config(text="Выберите клетку")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourApp(root)
    root.mainloop()