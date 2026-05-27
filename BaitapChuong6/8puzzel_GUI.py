import tkinter as tk
import random

# =========================
# GOAL STATE
# =========================

GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# =========================
# MODEL
# =========================

model = {
    "actions": ["UP", "DOWN", "LEFT", "RIGHT"],
    "goal": GOAL
}

state = None
visited = set()

# =========================
# LOGIC FUNCTIONS
# =========================

def copy_state(arr):
    return [row[:] for row in arr]


def state_to_string(arr):
    return str(arr)


def find_zero(arr):

    for i in range(3):
        for j in range(3):

            if arr[i][j] == 0:
                return i, j


def can_move(arr, action):

    r, c = find_zero(arr)

    if action == "UP":
        return r > 0

    elif action == "DOWN":
        return r < 2

    elif action == "LEFT":
        return c > 0

    elif action == "RIGHT":
        return c < 2

    return False


def apply_action(arr, action):

    new_arr = copy_state(arr)

    r, c = find_zero(new_arr)

    if action == "UP":

        new_arr[r][c], new_arr[r - 1][c] = \
            new_arr[r - 1][c], new_arr[r][c]

    elif action == "DOWN":

        new_arr[r][c], new_arr[r + 1][c] = \
            new_arr[r + 1][c], new_arr[r][c]

    elif action == "LEFT":

        new_arr[r][c], new_arr[r][c - 1] = \
            new_arr[r][c - 1], new_arr[r][c]

    elif action == "RIGHT":

        new_arr[r][c], new_arr[r][c + 1] = \
            new_arr[r][c + 1], new_arr[r][c]

    return new_arr


def heuristic(arr):

    wrong = 0

    for i in range(3):
        for j in range(3):

            if arr[i][j] != 0 and arr[i][j] != GOAL[i][j]:
                wrong += 1

    return wrong


def is_goal(arr):
    return arr == GOAL


def create_random_state():

    nums = list(range(9))
    random.shuffle(nums)

    arr = []

    idx = 0

    for i in range(3):

        row = []

        for j in range(3):

            row.append(nums[idx])
            idx += 1

        arr.append(row)

    return arr


# =========================
# AI
# =========================

def rule_match(state, model, visited):

    possible_actions = []

    for action in model["actions"]:

        if can_move(state, action):

            next_state = apply_action(state, action)

            if state_to_string(next_state) not in visited:

                score = heuristic(next_state)

                possible_actions.append(
                    (score, action, next_state)
                )

    if len(possible_actions) == 0:
        return None

    possible_actions.sort(key=lambda x: x[0])

    return possible_actions[0][1]


def model_based_reflex_agent(percept):

    action = rule_match(
        percept,
        model,
        visited
    )

    if action is None:
        return "STOP"

    return action


# =========================
# GUI
# =========================

class PuzzleGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "8 Puzzle - Cinematic Edition"
        )

        self.root.geometry("980x650")
        self.root.configure(bg="#0f172a")

        self.current_state = create_random_state()

        visited.clear()

        visited.add(
            state_to_string(self.current_state)
        )

        self.steps = 0

        self.ai_running = False

        # =========================
        # TITLE
        # =========================

        title = tk.Label(
            root,
            text="8 Puzzle AI",
            font=("Arial", 24, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        )

        title.pack(pady=8)

        # =========================
        # MAIN AREA
        # =========================

        main_area = tk.Frame(
            root,
            bg="#0f172a"
        )

        main_area.pack(pady=5)

        # =========================
        # BOARD
        # =========================

        board = tk.Frame(
            main_area,
            bg="#0f172a"
        )

        board.grid(
            row=0,
            column=0,
            padx=20
        )

        self.cells = []

        for i in range(3):

            row = []

            for j in range(3):

                label = tk.Label(
                    board,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 28, "bold"),
                    bg="#1e293b",
                    fg="white",
                    relief="flat"
                )

                label.grid(
                    row=i,
                    column=j,
                    padx=6,
                    pady=6,
                    ipadx=18,
                    ipady=18
                )

                row.append(label)

            self.cells.append(row)

        # =========================
        # VISITED STATES
        # =========================

        memory_frame = tk.Frame(
            main_area,
            bg="#111827"
        )

        memory_frame.grid(
            row=0,
            column=1,
            sticky="n"
        )

        memory_title = tk.Label(
            memory_frame,
            text="VISITED STATES",
            font=("Arial", 14, "bold"),
            bg="#111827",
            fg="#22c55e"
        )

        memory_title.pack(pady=8)

        self.memory_box = tk.Text(
            memory_frame,
            width=30,
            height=16,
            font=("Consolas", 8),
            bg="#0b1220",
            fg="#22c55e",
            insertbackground="white",
            relief="flat"
        )

        self.memory_box.pack(
            padx=8,
            pady=8
        )

        # =========================
        # INFO
        # =========================

        self.info_label = tk.Label(
            root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )

        self.info_label.pack(pady=5)

        # =========================
        # MOVE BUTTONS
        # =========================

        control = tk.Frame(
            root,
            bg="#0f172a"
        )

        control.pack(pady=5)

        self.make_button(
            control,
            "UP",
            lambda: self.move("UP"),
            0,
            1
        )

        self.make_button(
            control,
            "LEFT",
            lambda: self.move("LEFT"),
            1,
            0
        )

        self.make_button(
            control,
            "DOWN",
            lambda: self.move("DOWN"),
            1,
            1
        )

        self.make_button(
            control,
            "RIGHT",
            lambda: self.move("RIGHT"),
            1,
            2
        )

        # =========================
        # EXTRA BUTTONS
        # =========================

        extra = tk.Frame(
            root,
            bg="#0f172a"
        )

        extra.pack(pady=8)

        self.make_button(
            extra,
            "Random",
            self.random_board,
            0,
            0
        )

        self.make_button(
            extra,
            "AI Step",
            self.ai_next_step,
            0,
            1
        )

        self.make_button(
            extra,
            "AI Solve",
            self.toggle_ai,
            0,
            2
        )

        self.make_button(
            extra,
            "Reset Memory",
            self.reset_memory,
            0,
            3
        )

        # =========================
        # KEYBOARD CONTROL
        # =========================

        root.bind("<Up>", lambda e: self.move("UP"))
        root.bind("<Down>", lambda e: self.move("DOWN"))
        root.bind("<Left>", lambda e: self.move("LEFT"))
        root.bind("<Right>", lambda e: self.move("RIGHT"))

        self.update_gui()

    # =========================
    # BUTTON STYLE
    # =========================

    def make_button(self, parent, text, command, r, c):

        btn = tk.Button(
            parent,
            text=text,
            width=12,
            height=1,
            command=command,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )

        btn.grid(
            row=r,
            column=c,
            padx=6,
            pady=6,
            ipadx=5,
            ipady=5
        )

    # =========================
    # UPDATE GUI
    # =========================

    def update_gui(self):

        colors = {
            1: "#ef4444",
            2: "#f97316",
            3: "#eab308",
            4: "#22c55e",
            5: "#06b6d4",
            6: "#3b82f6",
            7: "#8b5cf6",
            8: "#ec4899"
        }

        for i in range(3):
            for j in range(3):

                value = self.current_state[i][j]

                if value == 0:

                    self.cells[i][j].config(
                        text="",
                        bg="#334155"
                    )

                else:

                    self.cells[i][j].config(
                        text=str(value),
                        bg=colors[value],
                        fg="white"
                    )

        self.info_label.config(
            text=
            f"Steps: {self.steps}   |   "
            f"Visited States: {len(visited)}"
        )

        self.memory_box.delete(1.0, tk.END)

        for s in visited:

            self.memory_box.insert(
                tk.END,
                s + "\n\n"
            )

        if is_goal(self.current_state):

            self.info_label.config(
                text=
                f"GOAL REACHED!  Steps: {self.steps}",
                fg="#22c55e"
            )

    # =========================
    # PLAYER MOVE
    # =========================

    def move(self, action):

        if can_move(self.current_state, action):

            self.current_state = apply_action(
                self.current_state,
                action
            )

            visited.add(
                state_to_string(self.current_state)
            )

            self.steps += 1

            self.update_gui()

    # =========================
    # RANDOM
    # =========================

    def random_board(self):

        self.ai_running = False

        self.current_state = create_random_state()

        visited.clear()

        visited.add(
            state_to_string(self.current_state)
        )

        self.steps = 0

        self.update_gui()

    # =========================
    # RESET MEMORY
    # =========================

    def reset_memory(self):

        visited.clear()

        visited.add(
            state_to_string(self.current_state)
        )

        self.update_gui()

    # =========================
    # AI STEP
    # =========================

    def ai_next_step(self):

        if is_goal(self.current_state):
            return

        action = model_based_reflex_agent(
            self.current_state
        )

        if action == "STOP":
            return

        self.current_state = apply_action(
            self.current_state,
            action
        )

        visited.add(
            state_to_string(self.current_state)
        )

        self.steps += 1

        self.update_gui()

    # =========================
    # AI TOGGLE
    # =========================

    def toggle_ai(self):

        self.ai_running = not self.ai_running

        if self.ai_running:
            self.ai_solve()

    # =========================
    # AI SOLVE
    # =========================

    def ai_solve(self):

        if not self.ai_running:
            return

        if is_goal(self.current_state):

            self.ai_running = False
            return

        action = model_based_reflex_agent(
            self.current_state
        )

        if action == "STOP":

            self.ai_running = False
            return

        self.current_state = apply_action(
            self.current_state,
            action
        )

        visited.add(
            state_to_string(self.current_state)
        )

        self.steps += 1

        self.update_gui()

        self.root.after(
            300,
            self.ai_solve
        )


# =========================
# MAIN
# =========================

root = tk.Tk()

app = PuzzleGUI(root)

root.mainloop()