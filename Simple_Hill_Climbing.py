import tkinter as tk
from tkinter import ttk

# --- PHẦN 1: LOGIC THUẬT TOÁN ---

def heuristic(state, goal):
    """Tính khoảng cách Manhattan chi tiết"""
    distance = 0
    flat_state = sum(state, [])
    flat_goal = sum(goal, [])
    for i, val in enumerate(flat_state):
        if val != 0:
            gi = flat_goal.index(val)
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(gi, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    """Sinh các trạng thái láng giềng và xác định hướng di chuyển"""
    neighbors = []
    x, y = 0, 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
    
    # Định nghĩa các hướng: (dx, dy, Tên hướng)
    moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]
    
    for dx, dy, move_name in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((new_state, move_name))
    return neighbors

def hill_climbing_logic(start, goal, max_steps=100):
    """Thuật toán Hill Climbing với việc lưu trữ lịch sử chi tiết"""
    current = start
    current_h = heuristic(current, goal)
    # Lưu trữ: (trạng thái, giá trị h, hành động dẫn đến trạng thái này)
    history = [(current, current_h, "START")]
    
    for _ in range(max_steps):
        neighbors = get_neighbors(current)
        # Tìm láng giềng có h nhỏ nhất
        best_state, best_move = min(neighbors, key=lambda x: heuristic(x[0], goal))
        best_h = heuristic(best_state, goal)
        
        if best_h < current_h:
            current, current_h = best_state, best_h
            history.append((current, current_h, best_move))
        else:
            break # Kẹt tại cực tiểu cục bộ
            
        if current_h == 0:
            return history, True
    return history, False

# --- PHẦN 2: GIAO DIỆN NGƯỜI DÙNG (UI) ---

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A.I Expert: 8-Puzzle Analysis Dashboard")
        self.root.geometry("1000x650")
        self.root.configure(bg="#362B6A") # Nền tối chuyên sâu
        
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.start_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
        
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = tk.Frame(self.root, bg="#121212")
        header_frame.pack(fill="x", pady=15)
        
        tk.Label(header_frame, text="8-PUZZLE SIMPLE HILL CLIMBING", font=("Consolas", 20, "bold"), 
                 fg="#00e5ff", bg="#121212").pack()

        # Main Layout
        main_container = tk.Frame(self.root, bg="#121212")
        main_container.pack(expand=True, fill="both", padx=30)

        # Left Column: Visual Board
        left_col = tk.Frame(main_container, bg="#121212")
        left_col.pack(side="left", padx=10)

        self.board_frame = tk.Frame(left_col, bg="#212121", bd=10, relief="ridge")
        self.board_frame.pack()
        
        self.cells = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                cell = tk.Label(self.board_frame, text="", width=4, height=1, 
                                font=("Impact", 40), fg="#ffffff", bg="#2c3e50")
                cell.grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j] = cell

        # Right Column: Analytics & Control
        right_col = tk.Frame(main_container, bg="#121212")
        right_col.pack(side="right", fill="both", expand=True, padx=20)

        # Status & Info
        info_frame = tk.Frame(right_col, bg="#1e1e1e", padx=15, pady=10)
        info_frame.pack(fill="x")
        
        self.status_lbl = tk.Label(info_frame, text="STATUS: IDLE", font=("Verdana", 10, "bold"), 
                                   fg="#757575", bg="#1e1e1e")
        self.status_lbl.pack(anchor="w")
        
        self.h_lbl = tk.Label(info_frame, text="HEURISTIC: -", font=("Verdana", 10), 
                              fg="#ffca28", bg="#1e1e1e")
        self.h_lbl.pack(anchor="w")

        # Console/Log Area
        tk.Label(right_col, text="SYSTEM LOGS:", font=("Consolas", 9), fg="#9e9e9e", bg="#121212").pack(anchor="w", pady=(10,0))
        
        log_frame = tk.Frame(right_col, bg="#000000")
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, bg="#0a0a0a", fg="#00ff41", font=("Consolas", 10),
                                bd=0, padx=10, pady=10, insertbackground="white")
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Tags for colored logging
        self.log_text.tag_config("step_header", foreground="#ffffff", font=("Consolas", 10, "bold"))
        self.log_text.tag_config("success", foreground="#00e676")
        self.log_text.tag_config("fail", foreground="#ff5252")
        self.log_text.tag_config("action", foreground="#00b0ff")

        # Control Buttons
        btn_frame = tk.Frame(right_col, bg="#121212")
        btn_frame.pack(fill="x", pady=15)

        self.solve_btn = tk.Button(btn_frame, text="EXECUTE ALGORITHM", command=self.run_process,
                                   font=("Arial", 11, "bold"), bg="#00e5ff", fg="#000000", 
                                   activebackground="#00b2cc", cursor="hand2", bd=0, pady=8)
        self.solve_btn.pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="RESET DATA", command=self.reset_system,
                  font=("Arial", 11), bg="#424242", fg="#ffffff", 
                  activebackground="#616161", cursor="hand2", bd=0, pady=5).pack(fill="x")

        self.update_board_ui(self.start_state)

    def update_board_ui(self, state):
        h_val = heuristic(state, self.goal_state)
        self.h_lbl.config(text=f"HEURISTIC (Manhattan): {h_val}")
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val == 0:
                    self.cells[i][j].config(text="", bg="#121212")
                else:
                    color = "#00838f" if val % 2 == 0 else "#2e7d32"
                    self.cells[i][j].config(text=str(val), bg=color)

    def write_log(self, step_idx, state, h_val, action):
        """Ghi đầy đủ thông số vào Console"""
        self.log_text.insert(tk.END, f"--- STEP {step_idx} ---\n", "step_header")
        self.log_text.insert(tk.END, f"ACTION: ", "")
        self.log_text.insert(tk.END, f"{action}\n", "action")
        self.log_text.insert(tk.END, f"HEURISTIC: {h_val}\n")
        self.log_text.insert(tk.END, "STATE:\n")
        for row in state:
            row_str = " ".join(str(x) if x != 0 else "_" for x in row)
            self.log_text.insert(tk.END, f"  [ {row_str} ]\n")
        self.log_text.insert(tk.END, "\n")
        self.log_text.see(tk.END)

    def run_process(self):
        self.solve_btn.config(state="disabled", bg="#263238")
        self.log_text.delete("1.0", tk.END)
        self.status_lbl.config(text="STATUS: COMPUTING...", fg="#ffca28")
        
        history, solved = hill_climbing_logic(self.start_state, self.goal_state)
        
        def animate(idx=0):
            if idx < len(history):
                state, h_val, action = history[idx]
                self.update_board_ui(state)
                self.write_log(idx, state, h_val, action)
                self.root.after(500, lambda: animate(idx + 1))
            else:
                if solved:
                    self.status_lbl.config(text="STATUS: SOLVED", fg="#00e676")
                    self.log_text.insert(tk.END, ">>> TARGET STATE REACHED SUCCESSFULLY.\n", "success")
                else:
                    self.status_lbl.config(text="STATUS: LOCAL OPTIMUM", fg="#ff5252")
                    self.log_text.insert(tk.END, ">>> TERMINATED: NO BETTER NEIGHBORS FOUND.\n", "fail")
                self.solve_btn.config(state="normal", bg="#00e5ff")

        animate()

    def reset_system(self):
        self.update_board_ui(self.start_state)
        self.log_text.delete("1.0", tk.END)
        self.status_lbl.config(text="STATUS: IDLE", fg="#757575")
        self.solve_btn.config(state="normal", bg="#00e5ff")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()