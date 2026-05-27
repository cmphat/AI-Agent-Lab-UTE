import tkinter as tk
import random
import heapq

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

# =========================
# HEURISTIC
# =========================

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
# COST
# =========================

def move_cost(action):

    if action in ["UP", "DOWN"]:
        return 1

    elif action in ["LEFT", "RIGHT"]:
        return 2

    return 1

# =========================
# NODE
# =========================

class Node:

    def __init__(
        self,
        state,
        parent=None,
        action=None,
        depth=0,
        cost=0
    ):

        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

# =========================
# TREE FUNCTIONS
# =========================

def is_cycle(node):

    curr = node.parent

    while curr is not None:

        if curr.state == node.state:
            return True

        curr = curr.parent

    return False

def get_children(node):

    children = []

    for action in model["actions"]:

        if can_move(node.state, action):

            new_state = apply_action(node.state, action)

            child = Node(
                new_state,
                node,
                action,
                node.depth + 1,
                node.cost + move_cost(action)
            )

            children.append(child)

    children.reverse()

    return children

# =========================
# IDS
# =========================

def depth_limited_search(initial_state, limit):

    frontier = [Node(initial_state)]

    result = "failure"

    while frontier:

        node = frontier.pop()

        if is_goal(node.state):
            return node

        if node.depth > limit:

            result = "cutoff"

        elif not is_cycle(node):

            for child in get_children(node):
                frontier.append(child)

    return result

def iterative_deepening_search(
    initial_state,
    gui_root,
    info_label,
    max_depth=25
):

    for depth in range(max_depth + 1):

        info_label.config(
            text=f"IDS đang tìm... Depth: {depth}",
            fg="#eab308"
        )

        gui_root.update()

        result = depth_limited_search(
            initial_state,
            depth
        )

        if result != "cutoff" and result != "failure":
            return result

    return "failure"

# =========================
# UCS
# =========================

def uniform_cost_search(
    initial_state,
    gui_root,
    info_label
):

    frontier = []

    start_node = Node(initial_state, cost=0)

    heapq.heappush(frontier, (0, start_node))

    explored = set()

    while frontier:

        current_cost, node = heapq.heappop(frontier)

        state_str = state_to_string(node.state)

        if state_str in explored:
            continue

        explored.add(state_str)

        info_label.config(
            text=f"UCS đang tìm... Cost: {node.cost} | Explored: {len(explored)}",
            fg="#eab308"
        )

        gui_root.update()

        if is_goal(node.state):
            return node

        for child in get_children(node):

            child_str = state_to_string(child.state)

            if child_str not in explored:

                heapq.heappush(
                    frontier,
                    (child.cost, child)
                )

    return "failure"

# =========================
# GREEDY
# =========================

def greedy_search(
    initial_state,
    gui_root,
    info_label
):

    frontier = []

    start_node = Node(initial_state)

    heapq.heappush(
        frontier,
        (heuristic(initial_state), start_node)
    )

    explored = set()

    while frontier:

        h, node = heapq.heappop(frontier)

        state_str = state_to_string(node.state)

        if state_str in explored:
            continue

        explored.add(state_str)

        info_label.config(
            text=f"Greedy đang tìm... h(n): {h} | Explored: {len(explored)}",
            fg="#eab308"
        )

        gui_root.update()

        if is_goal(node.state):
            return node

        for child in get_children(node):

            child_str = state_to_string(child.state)

            if child_str not in explored:

                heapq.heappush(
                    frontier,
                    (
                        heuristic(child.state),
                        child
                    )
                )

    return "failure"

# =========================
# A*
# =========================

def a_star_search(
    initial_state,
    gui_root,
    info_label
):

    frontier = []

    start_node = Node(initial_state, cost=0)

    start_f = heuristic(initial_state)

    heapq.heappush(
        frontier,
        (start_f, start_node)
    )

    explored = set()

    while frontier:

        f_cost, node = heapq.heappop(frontier)

        state_str = state_to_string(node.state)

        if state_str in explored:
            continue

        explored.add(state_str)

        info_label.config(
            text=f"A* đang tìm... f(n): {f_cost} | Explored: {len(explored)}",
            fg="#eab308"
        )

        gui_root.update()

        if is_goal(node.state):
            return node

        for child in get_children(node):

            child_str = state_to_string(child.state)

            if child_str not in explored:

                g = child.cost
                h = heuristic(child.state)

                f = g + h

                heapq.heappush(
                    frontier,
                    (f, child)
                )

    return "failure"

# =========================
# REFLEX AGENT
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

        self.root.title("8 Puzzle AI")

        self.root.geometry("1350x700")

        self.root.configure(bg="#0f172a")

        self.current_state = create_random_state()

        visited.clear()

        visited.add(
            state_to_string(self.current_state)
        )

        self.steps = 0
        self.total_cost = 0

        self.ai_running = False
        self.is_animating = False

        self.solution_path = []

        # TITLE

        title = tk.Label(
            root,
            text="8 Puzzle AI",
            font=("Arial", 24, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        )

        title.pack(pady=10)

        # MAIN AREA

        main_area = tk.Frame(
            root,
            bg="#0f172a"
        )

        main_area.pack()

        # BOARD

        board = tk.Frame(
            main_area,
            bg="#0f172a"
        )

        board.grid(row=0, column=0, padx=25)

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
                    fg="white"
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

        # VISITED BOX

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
            width=35,
            height=18,
            font=("Consolas", 8),
            bg="#0b1220",
            fg="#22c55e"
        )

        self.memory_box.pack(
            padx=8,
            pady=8
        )

        # INFO

        self.info_label = tk.Label(
            root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )

        self.info_label.pack(pady=5)

        # MOVE BUTTONS

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

        # EXTRA BUTTONS

        extra = tk.Frame(
            root,
            bg="#0f172a"
        )

        extra.pack(pady=10)

        self.make_button(extra, "Random", self.random_board, 0, 0)
        self.make_button(extra, "Reflex Step", self.ai_next_step, 0, 1)
        self.make_button(extra, "Reflex Solve", self.toggle_ai, 0, 2)
        self.make_button(extra, "Reset Memory", self.reset_memory, 0, 3)
        self.make_button(extra, "IDS Solve", self.run_ids_solve, 0, 4)
        self.make_button(extra, "UCS Solve", self.run_ucs_solve, 0, 5)
        self.make_button(extra, "Greedy Solve", self.run_greedy_solve, 0, 6)
        self.make_button(extra, "A* Solve", self.run_astar_solve, 0, 7)

        # KEYBOARD

        root.bind("<Up>", lambda e: self.move("UP"))
        root.bind("<Down>", lambda e: self.move("DOWN"))
        root.bind("<Left>", lambda e: self.move("LEFT"))
        root.bind("<Right>", lambda e: self.move("RIGHT"))

        self.update_gui()

    # =========================
    # BUTTON
    # =========================

    def make_button(
        self,
        parent,
        text,
        command,
        r,
        c
    ):

        btn = tk.Button(
            parent,
            text=text,
            width=13,
            command=command,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )

        btn.grid(
            row=r,
            column=c,
            padx=5,
            pady=5,
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
                        bg=colors[value]
                    )

        if not self.is_animating:

            self.info_label.config(
                text=f"Steps: {self.steps} | Cost: {self.total_cost} | Visited: {len(visited)}",
                fg="white"
            )

        self.memory_box.delete(1.0, tk.END)

        for s in visited:
            self.memory_box.insert(
                tk.END,
                s + "\n\n"
            )

        if is_goal(self.current_state):

            self.info_label.config(
                text=f"GOAL REACHED! Steps: {self.steps} | Cost: {self.total_cost}",
                fg="#22c55e"
            )

            self.is_animating = False

    # =========================
    # SOLVERS
    # =========================

    def solve_with_algorithm(
        self,
        algorithm,
        name
    ):

        if is_goal(self.current_state) or self.is_animating:
            return

        self.ai_running = False
        self.is_animating = True

        goal_node = algorithm(
            self.current_state,
            self.root,
            self.info_label
        )

        if goal_node != "failure":

            path = []

            curr = goal_node

            while curr.parent is not None:

                path.append(curr.action)
                curr = curr.parent

            path.reverse()

            self.solution_path = path

            self.info_label.config(
                text=f"{name} tìm thấy lời giải ({len(path)} bước) | Cost: {goal_node.cost}",
                fg="#22c55e"
            )

            self.root.after(
                1000,
                self.animate_solution
            )

        else:

            self.info_label.config(
                text=f"{name} không tìm thấy lời giải",
                fg="#ef4444"
            )

            self.is_animating = False

    def run_ids_solve(self):

        if is_goal(self.current_state) or self.is_animating:
            return

        self.ai_running = False
        self.is_animating = True

        goal_node = iterative_deepening_search(
            self.current_state,
            self.root,
            self.info_label
        )

        if goal_node != "failure":

            path = []

            curr = goal_node

            while curr.parent is not None:

                path.append(curr.action)
                curr = curr.parent

            path.reverse()

            self.solution_path = path

            self.root.after(
                1000,
                self.animate_solution
            )

    def run_ucs_solve(self):
        self.solve_with_algorithm(
            uniform_cost_search,
            "UCS"
        )

    def run_greedy_solve(self):
        self.solve_with_algorithm(
            greedy_search,
            "Greedy"
        )

    def run_astar_solve(self):
        self.solve_with_algorithm(
            a_star_search,
            "A*"
        )

    # =========================
    # ANIMATION
    # =========================

    def animate_solution(self):

        if not self.solution_path:

            self.is_animating = False
            self.update_gui()

            return

        action = self.solution_path.pop(0)

        self.move(action)

        self.root.after(
            400,
            self.animate_solution
        )

    # =========================
    # MOVE
    # =========================

    def move(self, action):

        if can_move(self.current_state, action):

            self.current_state = apply_action(
                self.current_state,
                action
            )

            visited.add(
                state_to_string(
                    self.current_state
                )
            )

            self.steps += 1

            self.total_cost += move_cost(action)

            self.update_gui()

    # =========================
    # RANDOM
    # =========================

    def random_board(self):

        self.ai_running = False
        self.is_animating = False

        self.solution_path = []

        self.current_state = create_random_state()

        visited.clear()

        visited.add(
            state_to_string(
                self.current_state
            )
        )

        self.steps = 0
        self.total_cost = 0

        self.update_gui()

    # =========================
    # RESET MEMORY
    # =========================

    def reset_memory(self):

        visited.clear()

        visited.add(
            state_to_string(
                self.current_state
            )
        )

        self.update_gui()

    # =========================
    # REFLEX STEP
    # =========================

    def ai_next_step(self):

        if is_goal(self.current_state):
            return

        action = model_based_reflex_agent(
            self.current_state
        )

        if action == "STOP":
            return

        self.move(action)

    # =========================
    # REFLEX SOLVE
    # =========================

    def toggle_ai(self):

        if self.is_animating:
            return

        self.ai_running = not self.ai_running

        if self.ai_running:
            self.ai_solve()

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

        self.move(action)

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