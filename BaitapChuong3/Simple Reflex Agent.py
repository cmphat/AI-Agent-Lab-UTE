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
    return -1, -1


def move_up(arr):
    zero_row, zero_col = find_zero(arr)

    if zero_row > 0:
        arr[zero_row][zero_col], arr[zero_row - 1][zero_col] = arr[zero_row - 1][zero_col], arr[zero_row][zero_col]
        print("\nSau khi di len:")
        print_state(arr)
    else:
        print("\nKhong the di len!")


def move_down(arr):
    zero_row, zero_col = find_zero(arr)

    if zero_row < 2:
        arr[zero_row][zero_col], arr[zero_row + 1][zero_col] = arr[zero_row + 1][zero_col], arr[zero_row][zero_col]
        print("\nSau khi di xuong:")
        print_state(arr)
    else:
        print("\nKhong the di xuong!")


def move_left(arr):
    zero_row, zero_col = find_zero(arr)

    if zero_col > 0:
        arr[zero_row][zero_col], arr[zero_row][zero_col - 1] = arr[zero_row][zero_col - 1], arr[zero_row][zero_col]
        print("\nSau khi di sang trai:")
        print_state(arr)
    else:
        print("\nKhong the di chuyen sang trai!")


def move_right(arr):
    zero_row, zero_col = find_zero(arr)

    if zero_col < 2:
        arr[zero_row][zero_col], arr[zero_row][zero_col + 1] = arr[zero_row][zero_col + 1], arr[zero_row][zero_col]
        print("\nSau khi di sang phai:")
        print_state(arr)
    else:
        print("\nKhong the di chuyen sang phai!")


def is_goal(arr):
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    return arr == goal


import random

numbers = [0,1,2,3,4,5,6,7,8]
random.shuffle(numbers)

arr = []

k = 0
for i in range(3):
    row = []
    for j in range(3):
        row.append(numbers[k])
        k += 1
    arr.append(row)
print("\nPercept hien tai:")
print_state(arr)

while not is_goal(arr):
    print("\nChon hanh dong:")
    print("U - Di len")
    print("D - Di xuong")
    print("L - Di trai")
    print("R - Di phai")

    choice = input("Nhap lua chon: ")

    if choice == "U" or choice == "u":
        move_up(arr)
    elif choice == "D" or choice == "d":
        move_down(arr)
    elif choice == "L" or choice == "l":
        move_left(arr)
    elif choice == "R" or choice == "r":
        move_right(arr)
    else:
        print("\nLua chon khong hop le. Vui long thu lai.")

print("\nChuc mung")