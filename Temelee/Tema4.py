import functions as f
import numpy as np
import statistics as s
from tkinter import *
from tkinter import messagebox
import math
import copy


def read_rare_matrix_from_file(file, prec):
    f = open(file, "r")
    dimension_of_matrix = int(f.readline())
    economic_list = [[] for x in range(0, dimension_of_matrix)]
    diagonal_vector = np.zeros(dimension_of_matrix)
    while f:
        line = f.readline()
        if not line:
            f.close()
            break
        if line.isspace():
            continue
        strings = line.strip().split(",")
        value = float(strings[0])
        row = int(strings[1])
        column = int(strings[2])
        if column > row:
            continue
        if column == row:
            if abs(value) < 10 ** -prec:
                print("\nSistemul nu poate fi rezolvat.\n")
                return [-1, -1, -1]
            else:
                diagonal_vector[row] += value
        occurance = [(x, y) for x, y in economic_list[row] if y == column]
        if not occurance:
            economic_list[row].append((value, column))
        else:
            new_pair = (occurance[0][0] + value, column)
            economic_list[row].remove(occurance[0])
            economic_list[row].append(new_pair)
    print(diagonal_vector)
    return economic_list, diagonal_vector


def read_b_from_file(file, size_of_file):
    f = open(file, "r")
    b = []
    i = 0
    while f:
        line = f.readline().strip()
        if not line:
            f.close()
            break
        if line.isspace():
            continue
        b.append(float(line))
        i += 1
    return b


def reading_same_index_files(file_a, file_b):
    precision = int(input("Give the power of precision. We'll do it as a negative power for you 💻\n"))
    returned_info = read_rare_matrix_from_file(file_a, precision)
    rare_matrix = returned_info[0]
    diagonal_vector = returned_info[1]
    b = read_b_from_file(file_b, returned_info[0])
    return [rare_matrix, b, precision, diagonal_vector]


def euclidean_norm(current_vector, previous_vector):
    norm_value = 0
    if len(current_vector) != len(previous_vector):
        return "Lungime diferita vectori"
    for i in range(len(current_vector)):
        norm_value += pow(current_vector[i] - previous_vector[i], 2)
    norm_value = pow(norm_value, 1/2)
    return norm_value


def calculate_x(previous_vector_x, vector_b, rare_matrix, diag):
    current_vector_x = [0 for _ in range(0, len(previous_vector_x))]
    for i in range(0, len(current_vector_x)):
        for element in rare_matrix[i]:
            if element[1] != i:
                current_vector_x[element[1]] += element[0] * previous_vector_x[i]
                current_vector_x[i] += element[0] * previous_vector_x[element[1]]
    for i in range(0, len(current_vector_x)):
        current_vector_x[i] = (vector_b[i] - current_vector_x[i]) / diag[i]
    return current_vector_x


def verify_solution_print_norm(rare_matrix, current_vector_x_solution_jacobi, vector_b):
    new_vector_sum = [0 for _ in range(0, len(vector_b))]
    for i in range(0, len(rare_matrix)):
        for element in rare_matrix[i]:
            new_vector_sum[i] += element[0] * current_vector_x_solution_jacobi[element[1]]
            if i != element[1]:
                new_vector_sum[element[1]] += element[0] * current_vector_x_solution_jacobi[i]
    vector_sums = []
    for i in range(len(current_vector_x_solution_jacobi)):
        vector_sums.append(abs(new_vector_sum[i] - vector_b[i]))
    return max(vector_sums)


def jacobi_solution(rare_matrix, vector_b, diag, precision):
    x_current = [0 for _ in range(0, len(diag))]
    x_previous = [0 for _ in range(0, len(diag))]
    max_iter = 1000
    i = 0
    while True:
        i += 1
        x_previous = copy.deepcopy(x_current)
        x_current = calculate_x(x_previous, vector_b, rare_matrix, diag)
        norm = euclidean_norm(x_previous, x_current)
        if norm < precision:
            break
        if i > max_iter:
            break
        if norm > pow(10, 8):
            break
    print(f"Numarul de iteratii este: {i}")
    if norm > pow(10, 8):
        print("Norm error")
    if norm < precision:
        return x_current
    else:
        print("Divergence")



def calculate_ex():
    info = f.reading_same_index_files("a_1.txt", "b_1.txt")

    rare_matrix = info[0]
    vector_b = info[1]
    precision = 10 ** -info[2]
    diagonal_vector = info[3]

    solution = f.jacobi_solution(rare_matrix, vector_b, diagonal_vector, precision)
    if solution:
        norm = f.verify_solution_print_norm(rare_matrix, solution, vector_b)
        print(f"Norma calculata este: {norm}")
        messagebox.showinfo("Solutie?", str("Am gasit solutie!"))
        messagebox.showinfo("Norma este: ", str(norm))


if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", calculate_ex)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab4 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator4 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu Jacobi Matrice", padx=33, pady=10,
                     command=calculate_ex,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=151)

    TOP.mainloop()
