import tkinter as tk
from tkinter import ttk
import random
from typing import List, Tuple

State = List[List[int]]

# =========================
# PHẦN 1: LOGIC THUẬT TOÁN
# =========================

def is_solvable(state: State) -> bool:
    """Kiểm tra 8-puzzle có lời giải (dựa trên số nghịch thế)."""
    flat = [v for row in state for v in row if v != 0]
    inv = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv += 1
    # 8-puzzle bảng 3x3: chẵn => solvable
    return inv % 2 == 0

def goal_positions_map(goal: State):
    """Tạo map giá trị -> (row, col) trong goal để tính heuristic nhanh."""
    pos = {}
    for i in range(3):
        for j in range(3):
            v = goal[i][j]
            pos[v] = (i, j)
    return pos

def heuristic(state: State, goal_map: dict[int, Tuple[int, int]]) -> int:
    """Heuristic Manhattan tổng (bỏ ô 0)."""
    distance = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0:
                gi, gj = goal_map[v]
                distance += abs(i - gi) + abs(j - gj)
    return distance

def get_neighbors(state: State) -> List[Tuple[State, str]]:
    """Sinh trạng thái kề bằng cách di chuyển ô trống."""
    neighbors = []
    x, y = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
    moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]
    for dx, dy, move_name in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((new_state, move_name))
    return neighbors

def simple_hill_climbing_logic(start: State, goal: State, max_steps: int = 100):
    """Hill climbing đơn giản với tie-break ổn định theo tên move."""
    gmap = goal_positions_map(goal)
    current = start
    current_h = heuristic(current, gmap)
    history = [(current, current_h, "START")]
    for _ in range(max_steps):
        neighbors = get_neighbors(current)
        # Sắp theo (h, move) để ổn định
        best_state, best_move = min(neighbors, key=lambda x: (heuristic(x[0], gmap), x[1]))
        best_h = heuristic(best_state, gmap)
        if best_h < current_h:
            current, current_h = best_state, best_h
            history.append((current, current_h, best_move))
        else:
            break
        if current_h == 0:
            return history, True
    return history, False

def stochastic_hill_climbing_logic(start: State, goal: State, max_steps: int = 100):
    """Hill climbing ngẫu nhiên: chọn ngẫu nhiên 1 neighbor tốt hơn."""
    gmap = goal_positions_map(goal)
    current = start
    current_h = heuristic(current, gmap)
    history = [(current, current_h, "START")]
    for _ in range(max_steps):
        neighbors = get_neighbors(current)
        better = [(s, m) for s, m in neighbors if heuristic(s, gmap) < current_h]
        if not better:
            break
        current, best_move = random.choice(better)
        current_h = heuristic(current, gmap)
        history.append((current, current_h, best_move))
        if current_h == 0:
            return history, True
    return history, False

def random_valid_state() -> State:
    """Sinh ngẫu nhiên trạng thái hợp lệ."""
    while True:
        flat = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        random.shuffle(flat)
        st = [flat[0:3], flat[3:6], flat[6:9]]
        if is_solvable(st):
            return st

def random_restart_logic(start: State, goal: State, restarts: int = 5):
    """Random-restart hill climbing, đảm bảo state restart là solvable."""
    total_history = []
    current_start = start
    for i in range(restarts):
        history, solved = simple_hill_climbing_logic(current_start, goal)
        total_history.extend([(s, h, f"R{i+1}-{m}") for s, h, m in history])
        if solved:
            return total_history, True
        current_start = random_valid_state()
    return total_history, False

def local_beam_search_logic(start: State, goal: State, k: int = 3, max_steps: int = 50):
    """Local Beam Search với lọc trùng trạng thái."""
    gmap = goal_positions_map(goal)
    beam = [(start, heuristic(start, gmap), "START")]
    history = []
    visited = {tuple(v for row in start for v in row)}
    for _ in range(max_steps):
        history.extend(beam)
        if any(h == 0 for _, h, _ in beam):
            return history, True
        all_cands = []
        for state, _, _ in beam:
            for n_s, m in get_neighbors(state):
                key = tuple(v for row in n_s for v in row)
                if key in visited:
                    continue
                visited.add(key)
                all_cands.append((n_s, heuristic(n_s, gmap), m))
        if not all_cands:
            break
        all_cands.sort(key=lambda x: (x[1], x[2]))
        beam = all_cands[:k]
    return history, False


# =========================
# PHẦN 2: GIAO DIỆN HIỆN ĐẠI
# =========================

class PuzzleApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AI Expert: 8-Puzzle Elite Dashboard")
        self.root.geometry("1150x780")
        self.root.configure(bg="#0B0E14")

        # Fonts & Colors
        self.font_title = ("Inter", 24, "bold")
        self.font_label = ("Inter", 12, "bold")
        self.font_mono  = ("JetBrains Mono", 10)
        self.font_btn   = ("Inter", 10, "bold")
        self.font_tile  = ("Inter", 42, "bold")

        self.colors = {
            "bg": "#0B0E14",
            "panel": "#151921",
            "panel2": "#1A202C",
            "divider": "#2D3748",
            "text": "#F8FAFC",
            "muted": "#94A3B8",
            "accent": "#38BDF8",
            "ok": "#50FA7B",
            "warn": "#FFB86C",
            "err": "#FF5555",
            "btn": "#1E293B",
            "btn_hover": "#334155",
            "log_bg": "#0B0F16",
            "log_fg": "#C1F4D3",
        }

        # Tile colors
        self.tile_colors = {
            1: "#FF5555", 2: "#50FA7B", 3: "#8BE9FD",
            4: "#BD93F9", 5: "#FF79C6", 6: "#F1FA8C",
            7: "#FFB86C", 8: "#6272A4"
        }

        # States
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.start_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
        if not is_solvable(self.start_state):
            self.start_state = random_valid_state()

        self._running = False
        self._buttons = []  # để enable/disable khi animate

        self.setup_ui()
        self.update_board(self.start_state, update_title=True)

    def setup_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=self.colors["panel"], width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="SYSTEM CORE", font=self.font_label,
                 fg=self.colors["accent"], bg=self.colors["panel"]).pack(pady=(32, 16))

        self.add_btn(sidebar, "SIMPLE CLIMBING", lambda: self.run("simple"))
        self.add_btn(sidebar, "STOCHASTIC", lambda: self.run("stochastic"))
        self.add_btn(sidebar, "RANDOM RESTART", lambda: self.run("restart"))
        self.add_btn(sidebar, "LOCAL BEAM (k=3)", lambda: self.run("beam"))

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=20, pady=18)

        # Speed control
        sp = tk.Frame(sidebar, bg=self.colors["panel"])
        sp.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(sp, text="ANIMATION SPEED", font=("Inter", 9, "bold"),
                 fg=self.colors["muted"], bg=self.colors["panel"]).pack(anchor="w", pady=(0, 6))
        self.speed_var = tk.IntVar(value=300)
        self.speed_scale = ttk.Scale(sp, from_=80, to=800, orient="horizontal",
                                     command=lambda v: None, variable=self.speed_var)
        self.speed_scale.pack(fill="x")

        # Reset buttons
        tk.Button(sidebar, text="RESET DATA", command=self.reset_system,
                  bg="#E11D48", fg="white", font=self.font_btn, bd=0, pady=10,
                  activebackground="#BE123C").pack(fill="x", padx=20, pady=(16, 6))

        tk.Button(sidebar, text="RANDOM START (SOLVABLE)", command=self.randomize_start,
                  bg=self.colors["btn"], fg="white", font=self.font_btn, bd=0, pady=10,
                  activebackground=self.colors["btn_hover"]).pack(fill="x", padx=20)

        # Main
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(side="right", expand=True, fill="both", padx=40, pady=30)

        # Header
        header = tk.Frame(main, bg=self.colors["bg"])
        header.pack(fill="x")
        tk.Label(header, text="8-PUZZLE VISUALIZER", font=self.font_title,
                 fg=self.colors["text"], bg=self.colors["bg"]).pack(anchor="w")
        self.status_lbl = tk.Label(header, text="STATUS: SYSTEM READY",
                                   font=self.font_mono, fg=self.colors["muted"], bg=self.colors["bg"])
        self.status_lbl.pack(anchor="w", pady=(4, 18))

        # Container
        container = tk.Frame(main, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        # Board area
        board_outer = tk.Frame(container, bg=self.colors["panel2"])
        board_outer.pack(side="left", anchor="n", padx=(0, 24))
        # Title above board
        self.board_title = tk.Label(board_outer, text="Board 3x3  |  h= -",
                                    font=("Inter", 12, "bold"), fg=self.colors["muted"], bg=self.colors["panel2"])
        self.board_title.pack(anchor="w", padx=12, pady=(12, 4))

        self.board_frame = tk.Frame(board_outer, bg=self.colors["panel2"], padx=12, pady=12)
        self.board_frame.pack()

        self.cells = [[self.create_tile(i, j) for j in range(3)] for i in range(3)]

        # Log Panel
        log_frame = tk.Frame(container, bg=self.colors["panel"])
        log_frame.pack(side="right", fill="both", expand=True)
        log_head = tk.Label(log_frame, text="EXECUTION LOG",
                            font=("Inter", 12, "bold"), fg=self.colors["accent"], bg=self.colors["panel"])
        log_head.pack(anchor="w", padx=16, pady=(12, 6))

        self.log_text = tk.Text(log_frame, bg=self.colors["log_bg"], fg=self.colors["log_fg"],
                                font=("JetBrains Mono", 10), bd=0, padx=16, pady=16, height=20)
        self.log_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def add_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd, bg=self.colors["btn"],
                        fg="white", font=self.font_btn, bd=0, pady=10, activebackground=self.colors["btn_hover"],
                        cursor="hand2")
        btn.pack(fill="x", padx=20, pady=6)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["btn_hover"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["btn"]))
        self._buttons.append(btn)

    def set_buttons_state(self, state: str):
        for b in self._buttons:
            b.config(state=state)

    def create_tile(self, r, c):
        tile = tk.Label(self.board_frame, text="", width=3, height=1,
                        font=self.font_tile, fg="#FFFFFF", bg="#2D3748")
        tile.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
        return tile

    def update_board(self, state: State, update_title: bool = False):
        gmap = goal_positions_map(self.goal_state)
        h_val = heuristic(state, gmap)
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val == 0:
                    self.cells[i][j].config(text="", bg=self.colors["panel2"])
                else:
                    self.cells[i][j].config(text=str(val), bg=self.tile_colors.get(val, "#4A5568"))
        if update_title:
            self.board_title.config(text=f"Board 3x3  |  h={h_val}")

    def run(self, mode: str):
        if self._running:
            return
        self._running = True
        self.set_buttons_state("disabled")
        self.log_text.delete("1.0", tk.END)
        self.status_lbl.config(text=f"STATUS: EXECUTING {mode.upper()}...", fg=self.colors["accent"])

        if mode == "simple":
            history, solved = simple_hill_climbing_logic(self.start_state, self.goal_state)
        elif mode == "stochastic":
            history, solved = stochastic_hill_climbing_logic(self.start_state, self.goal_state)
        elif mode == "restart":
            history, solved = random_restart_logic(self.start_state, self.goal_state)
        else:
            history, solved = local_beam_search_logic(self.start_state, self.goal_state)

        delay = max(60, int(self.speed_var.get()))

        def animate(idx=0):
            if idx < len(history):
                state, h, act = history[idx]
                self.update_board(state, update_title=True)
                self.log_text.insert(tk.END, f"[STEP {idx:02d}] {act:12} | h={h}\n")
                self.log_text.see(tk.END)
                self.root.after(delay, lambda: animate(idx + 1))
            else:
                txt = "SOLVED SUCCESSFULLY" if solved else "FAILED: LOCAL OPTIMUM"
                color = self.colors["ok"] if solved else self.colors["err"]
                self.status_lbl.config(text=f"STATUS: {txt}", fg=color)
                self._running = False
                self.set_buttons_state("normal")

        animate()

    def reset_system(self):
        if self._running:
            return
        self.update_board(self.start_state, update_title=True)
        self.log_text.delete("1.0", tk.END)
        self.status_lbl.config(text="STATUS: SYSTEM READY", fg=self.colors["muted"])

    def randomize_start(self):
        if self._running:
            return
        self.start_state = random_valid_state()
        self.reset_system()


if __name__ == "__main__":
    root = tk.Tk()
    # Cải thiện ttk default theme chút (nếu muốn có thể chọn 'clam')
    try:
        style = ttk.Style()
        style.theme_use("clam")
    except Exception:
        pass
    app = PuzzleApp(root)
    root.mainloop()
