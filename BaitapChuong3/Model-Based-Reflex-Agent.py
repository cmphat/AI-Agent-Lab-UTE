import random
import time

def print_state(arr):
    for i in range(3):
        for j in range(3):
            if arr[i][j] == 0:
                print("_", end=" ")
            else:
                print(arr[i][j], end=" ")
        print()


def find_zero(arr):
    for i in range(3):
        for j in range(3):
            if arr[i][j] == 0:
                return i, j


def state_to_string(arr):
    return str(arr)


def save_state(arr, visited):
    visited.add(state_to_string(arr))


def is_visited(arr, visited):
    return state_to_string(arr) in visited


def is_goal(arr):
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    return arr == goal


def create_random_state():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(numbers)

    arr = []
    k = 0

    for i in range(3):
        row = []
        for j in range(3):
            row.append(numbers[k])
            k += 1
        arr.append(row)

    return arr


def copy_state(arr):
    return [row[:] for row in arr]


def move_up(arr, visited):
    zero_row, zero_col = find_zero(arr)

    if zero_row > 0:
        new_arr = copy_state(arr)

        new_arr[zero_row][zero_col], new_arr[zero_row - 1][zero_col] = \
            new_arr[zero_row - 1][zero_col], new_arr[zero_row][zero_col]

        if is_visited(new_arr, visited):
            print("\nTrang thai nay da di qua, khong di lai.")
            return False

        arr[zero_row][zero_col], arr[zero_row - 1][zero_col] = \
            arr[zero_row - 1][zero_col], arr[zero_row][zero_col]

        save_state(arr, visited)
        print("\nSau khi di len:")
        print_state(arr)
        return True
    else:
        print("\nKhong the di len!")
        return False


def move_down(arr, visited):
    zero_row, zero_col = find_zero(arr)

    if zero_row < 2:
        new_arr = copy_state(arr)

        new_arr[zero_row][zero_col], new_arr[zero_row + 1][zero_col] = \
            new_arr[zero_row + 1][zero_col], new_arr[zero_row][zero_col]

        if is_visited(new_arr, visited):
            print("\nTrang thai nay da di qua, khong di lai.")
            return False

        arr[zero_row][zero_col], arr[zero_row + 1][zero_col] = \
            arr[zero_row + 1][zero_col], arr[zero_row][zero_col]

        save_state(arr, visited)
        print("\nSau khi di xuong:")
        print_state(arr)
        return True
    else:
        print("\nKhong the di xuong!")
        return False


def move_left(arr, visited):
    zero_row, zero_col = find_zero(arr)

    if zero_col > 0:
        new_arr = copy_state(arr)

        new_arr[zero_row][zero_col], new_arr[zero_row][zero_col - 1] = \
            new_arr[zero_row][zero_col - 1], new_arr[zero_row][zero_col]

        if is_visited(new_arr, visited):
            print("\nTrang thai nay da di qua, khong di lai.")
            return False

        arr[zero_row][zero_col], arr[zero_row][zero_col - 1] = \
            arr[zero_row][zero_col - 1], arr[zero_row][zero_col]

        save_state(arr, visited)
        print("\nSau khi di sang trai:")
        print_state(arr)
        return True
    else:
        print("\nKhong the di sang trai!")
        return False


def move_right(arr, visited):
    zero_row, zero_col = find_zero(arr)

    if zero_col < 2:
        new_arr = copy_state(arr)

        new_arr[zero_row][zero_col], new_arr[zero_row][zero_col + 1] = \
            new_arr[zero_row][zero_col + 1], new_arr[zero_row][zero_col]

        if is_visited(new_arr, visited):
            print("\nTrang thai nay da di qua, khong di lai.")
            return False

        arr[zero_row][zero_col], arr[zero_row][zero_col + 1] = \
            arr[zero_row][zero_col + 1], arr[zero_row][zero_col]

        save_state(arr, visited)
        print("\nSau khi di sang phai:")
        print_state(arr)
        return True
    else:
        print("\nKhong the di sang phai!")
        return False


#main

arr = create_random_state()
visited = set()
steps = 0

save_state(arr, visited)

start_time = time.time()

print("Trang thai random ban dau:")
print_state(arr)

while not is_goal(arr):
    print("\nChon hanh dong:")
    print("U - Di len")
    print("D - Di xuong")
    print("L - Di trai")
    print("R - Di phai")
    print("Q - Thoat")

    choice = input("Nhap lua chon: ")

    moved = False

    if choice == "U" or choice == "u":
        moved = move_up(arr, visited)
    elif choice == "D" or choice == "d":
        moved = move_down(arr, visited)
    elif choice == "L" or choice == "l":
        moved = move_left(arr, visited)
    elif choice == "R" or choice == "r":
        moved = move_right(arr, visited)
    elif choice == "Q" or choice == "q":
        print("\nDa thoat chuong trinh.")
        break
    else:
        print("\nLua chon khong hop le.")

    if moved:
        steps += 1
        print("So buoc da di:", steps)

end_time = time.time()
total_time = end_time - start_time

if is_goal(arr):
    print("\nChuc mung! Puzzle da duoc giai.")

print("\nThong ke:")
print("So buoc hop le:", steps)
print("So trang thai da luu:", len(visited))
print("Thoi gian chay:", round(total_time, 4), "giay")