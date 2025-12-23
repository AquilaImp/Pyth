import tkinter as tk
from tkinter import ttk, messagebox
from itertools import combinations

FILES = "abcdefgh" 
RANKS = "12345678"  
WHITE_PIECES = ["Ферзь", "Ладья", "Слон", "Конь"]
PIECE_SYMBOLS = {"Ферзь": "Q", "Ладья": "R", "Слон": "B", "Конь": "N"}
UNICODE = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "k": "♚"}


def in_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def sq_to_xy(s):
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in FILES or s[1] not in RANKS:
        raise ValueError("Клетка должна быть вида e4")
    return FILES.index(s[0]), RANKS.index(s[1])

def xy_to_sq(x, y):
    return f"{FILES[x]}{RANKS[y]}"

def king_moves(x, y):
    """Возвращает все возможные ходы короля из клетки (x, y)"""
    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nx, ny = x + dx, y + dy
        if in_board(nx, ny):
            yield nx, ny

def knight_moves(x, y):
    """Возвращает все возможные ходы коня из клетки (x, y)"""
    for dx, dy in [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]:
        nx, ny = x + dx, y + dy
        if in_board(nx, ny):
            yield nx, ny

def slide_moves(x, y, dirs, occupied):
    """ход ладьи, слона, ферзя"""
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        while in_board(nx, ny):
            yield nx, ny
            if (nx, ny) in occupied:
                break
            nx += dx
            ny += dy

def rook_moves(x, y, occ):
    """Ходы ладьи"""
    return slide_moves(x, y, [(1,0),(-1,0),(0,1),(0,-1)], occ)

def bishop_moves(x, y, occ):
    """Ходы слона"""
    return slide_moves(x, y, [(1,1),(1,-1),(-1,1),(-1,-1)], occ)

def queen_moves(x, y, occ):
    """Ходы ферзя (ладья + слон)"""
    return list(rook_moves(x, y, occ)) + list(bishop_moves(x, y, occ))

def get_attacks(piece_type, x, y, occupied):
    """атакует фигура"""
    if piece_type == 'K':
        return set(king_moves(x, y))
    elif piece_type == 'Q':
        return set(queen_moves(x, y, occupied))
    elif piece_type == 'R':
        return set(rook_moves(x, y, occupied))
    elif piece_type == 'B':
        return set(bishop_moves(x, y, occupied))
    elif piece_type == 'N':
        return set(knight_moves(x, y))
    return set()

def is_attacked(sq, wk, w1, w2, bk, s1, s2):
    occupied = {wk, w1, w2, bk}
    attacks = set()
    attacks.update(get_attacks('K', wk[0], wk[1], occupied)) 
    attacks.update(get_attacks(s1, w1[0], w1[1], occupied))  
    attacks.update(get_attacks(s2, w2[0], w2[1], occupied))   
    return sq in attacks

def get_king_moves(bk, wk, w1, w2, s1, s2):
    """Возвращает все возможные ходы чёрного короля"""
    moves = []
    for nx, ny in king_moves(bk[0], bk[1]):
        if max(abs(nx - wk[0]), abs(ny - wk[1])) <= 1:
            continue
            
        if not is_attacked((nx, ny), wk, w1, w2, (nx, ny), s1, s2):
            moves.append((nx, ny))
    return moves

def analyze_position(wk, w1, w2, bk, s1, s2):
    """Анализирует позицию на наличие мата или пата"""
    if len({wk, w1, w2, bk}) != 4:  
        return None
        
    if max(abs(wk[0] - bk[0]), abs(wk[1] - bk[1])) <= 1: 
        return None
        
    in_check = is_attacked(bk, wk, w1, w2, bk, s1, s2) 
    has_moves = bool(get_king_moves(bk, wk, w1, w2, s1, s2))  
    
    if in_check and not has_moves:
        return "mate"  
    elif not in_check and not has_moves:
        return "stalemate"  
    return None

def find_positions(bk, s1, s2):
    """Находит все матовые и патовые позиции для заданных фигур"""
    results = []
    all_cells = [(x, y) for x in range(8) for y in range(8) if (x, y) != bk]
    for wk in all_cells:
        if max(abs(wk[0] - bk[0]), abs(wk[1] - bk[1])) <= 1:
            continue
        remaining = [cell for cell in all_cells if cell != wk]
        for w1, w2 in combinations(remaining, 2):
            result = analyze_position(wk, w1, w2, bk, s1, s2)
            if result:  
                results.append((result, wk, w1, w2))
    
    return results


class ChessAnalyzer:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ шахматных позиций")
        self.bk_pos = (4, 4) 
        self.piece1 = "Ферзь"
        self.piece2 = "Ладья"
        self.results = []
        self.current_idx = 0
        self.create_widgets()
        
    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        ttk.Label(control_frame, text="Позиция чёрного короля:").grid(row=0, column=0, sticky=tk.W)
        self.bk_entry = ttk.Entry(control_frame, width=5)
        self.bk_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.bk_entry.insert(0, "e5")
        ttk.Label(control_frame, text="Белые фигуры:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.piece1_var = tk.StringVar(value=self.piece1)
        self.piece2_var = tk.StringVar(value=self.piece2)
        
        ttk.Label(control_frame, text="Фигура 1:").grid(row=2, column=0, sticky=tk.W)
        self.piece1_menu = ttk.Combobox(control_frame, textvariable=self.piece1_var, 
                                      values=WHITE_PIECES, state="readonly", width=8)
        self.piece1_menu.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(control_frame, text="Фигура 2:").grid(row=3, column=0, sticky=tk.W)
        self.piece2_menu = ttk.Combobox(control_frame, textvariable=self.piece2_var, 
                                      values=WHITE_PIECES, state="readonly", width=8)
        self.piece2_menu.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        self.analyze_btn = ttk.Button(control_frame, text="Анализировать", command=self.analyze)
        self.analyze_btn.grid(row=4, column=0, columnspan=2, pady=10)
        nav_frame = ttk.Frame(control_frame)
        nav_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.prev_btn = ttk.Button(nav_frame, text="← Назад", command=self.prev_result, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(nav_frame, text="Вперёд →", command=self.next_result, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Укажите позицию чёрного короля и нажмите 'Анализировать'")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, wraplength=300)
        status_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.board_frame = ttk.Frame(self.root, padding="10")
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        self.create_board()
        
    def create_board(self):
        """Создаёт шахматную доску"""
        self.squares = []
        for row in range(8):
            row_squares = []
            for col in range(8):
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                square = tk.Canvas(self.board_frame, width=60, height=60, bg=color, 
                                 highlightthickness=0, borderwidth=0)
                square.grid(row=7-row, column=col) 
                square.bind("<Button-1>", lambda e, x=col, y=7-row: self.on_square_click(x, y))
                row_squares.append(square)
            self.squares.append(row_squares)
    
    def on_square_click(self, x, y):
        self.bk_pos = (x, y)
        self.bk_entry.delete(0, tk.END)
        self.bk_entry.insert(0, xy_to_sq(x, y))
        self.draw_board()
    
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.squares[7-row][col].config(bg=color)
                self.squares[7-row][col].delete("all")
        x, y = self.bk_pos
        self.squares[7-y][x].create_text(30, 30, text="♚", font=("Arial", 36), tags="piece")
        

        if hasattr(self, 'current_result'):
            result_type, wk, w1, w2 = self.current_result
            x, y = wk
            self.squares[7-y][x].create_text(30, 30, text="♔", font=("Arial", 36), tags="piece")
            s1 = PIECE_SYMBOLS[self.piece1_var.get()]
            s2 = PIECE_SYMBOLS[self.piece2_var.get()]
            
            x, y = w1
            self.squares[7-y][x].create_text(30, 30, text=UNICODE[s1], font=("Arial", 36), tags="piece")
            
            x, y = w2
            self.squares[7-y][x].create_text(30, 30, text=UNICODE[s2], font=("Arial", 36), tags="piece")
            x, y = self.bk_pos
            if result_type == "mate":
                self.squares[7-y][x].config(bg="#ff9999")
            else:
                self.squares[7-y][x].config(bg="#99ccff") 
    
    def analyze(self):
        """Запускает анализ позиции"""
        try:
            bk_sq = self.bk_entry.get().strip()
            self.bk_pos = sq_to_xy(bk_sq)
            
            p1 = self.piece1_var.get()
            p2 = self.piece2_var.get()
            if p1 == p2:
                messagebox.showerror("Ошибка", "Выберите разные фигуры")
                return
                
            s1 = PIECE_SYMBOLS[p1]
            s2 = PIECE_SYMBOLS[p2]

            self.status_var.set("Вычисление...")
            self.root.update() 
        
            self.results = find_positions(self.bk_pos, s1, s2)
            self.current_idx = 0
        
            if not self.results:
                self.status_var.set("Не найдено ни одной позиции мата или пата")
                self.prev_btn.config(state=tk.DISABLED)
                self.next_btn.config(state=tk.DISABLED)
                self.draw_board()
                return
                
            self.show_result(0)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def show_result(self, idx):
        """Отображает результат с указанным индексом"""
        if not self.results or idx < 0 or idx >= len(self.results):
            return
            
        self.current_idx = idx
        self.current_result = self.results[idx]
        
        result_type, wk, w1, w2 = self.current_result
        total = len(self.results)
        
        if result_type == "mate":
            status = f"Матовая позиция ({idx+1}/{total})"
        else:
            status = f"Патовая позиция ({idx+1}/{total})"
            
        self.status_var.set(status)
        
        self.prev_btn.config(state=tk.NORMAL if idx > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if idx < len(self.results) - 1 else tk.DISABLED)
        self.draw_board()
    
    def next_result(self):
        if self.current_idx < len(self.results) - 1:
            self.show_result(self.current_idx + 1)
    
    def prev_result(self):
        if self.current_idx > 0:
            self.show_result(self.current_idx - 1)

def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = ChessAnalyzer(root)
    root.geometry("800x800")  
    root.mainloop()

if __name__ == "__main__":
    main()
