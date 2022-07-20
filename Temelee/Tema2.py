from tkinter import *
from tkinter import messagebox
import numpy as np
import functions as f

def search_pivot(matrix, l, N):
    max = matrix[l][l]
    row = l
    for i in range(l, N):
        if abs(matrix[i][l]) > max:
            max = matrix[i][l]
            row = i
    return row

def interchange_lines(matrix, row, l, b):
    matrix[(l, row), :] = matrix[(row, l), :]

    aux_vector = b[l]
    b[l] = b[row]
    b[row] = aux_vector

def var_2_interchange_lines(matrix, row, l):
    matrix[(l, row), :] = matrix[(row, l), :]

def resolve_superior_triangular_system(matrix, N, b):
    index = N - 1
    solution = [0] * N
    solution[index] = b[index] / matrix[N-1, N-1]
    while index > 0:
        index -= 1
        solution[index] = b[index]
        for j in reversed(range(index + 1 , N)):
            solution[index] -= solution[j] * matrix[index, j]
        solution[index] /= matrix[index, index]
    return solution

def check_solution(results, matrix, N, b, prec):
    #print("With the resulted x-es, we obtain the following y-es for the ecuations:")
    euclidian_norm = 0
    for i in range(0,N):
        ec = 0.0
        for j in range(0, N):
            ec += matrix[i, j] * results[j]
        euclidian_norm += abs(ec - b[i])
        #print(f"y{i} = ", ec) - print pentru a vedea rezultatele obtinute dupa aflarea x-ilor
    if euclidian_norm > 10 ** prec:
        print(f"\nExercise 2: \nWrong solution - euclidian norm {euclidian_norm} exceeds the precision 10 ** {prec}")
    else:
        print(f"\nExercise 2: \nCorrect solution - the euclidian norm {euclidian_norm} is lower than 10 ** {prec}")

def Gauss_elimination(initial_matrix, matrix, b, N, prec, initial_b):
    #initializam pasul
    l = 0
    #caut pivotul
    pivot_row = search_pivot(matrix, l, N)
    interchange_lines(matrix, pivot_row, l, b)
    # print(matrix)
    # print(b)

    #formulele (5), (6), (7) si formarea matricii superior triunghiulare
    while l < N-1 and abs(matrix[l, l]) > 10 ** prec:
        for i in range(l + 1, N ):
            factor = matrix[i, l] / matrix[l, l]
            for j in range(l + 1, N ):
                matrix[i][j] = matrix[i, j] - factor * matrix[l, j]
            b[i] = b[i] - factor * b[l]
            matrix[i, l] = 0
        l += 1
        row = search_pivot(matrix, l, N)
        interchange_lines(matrix, row, l, b)

    if abs(matrix[l, l]) <= 10 ** prec:
        print("\nExercise 1: \nSingular matrix")
    else:
        results = resolve_superior_triangular_system(matrix, N, b)
        print("\nExercise 1: \nThe vector with values of x-es: ", results)
        check_solution(results, initial_matrix, N, initial_b, prec)
        return results
    return 0

def var2_Gauss_elimination(big_matrix, N, prec):
    #initializam pasul
    l = 0
    #caut pivotul
    pivot_row = search_pivot(big_matrix, l, N)
    var_2_interchange_lines(big_matrix, pivot_row, l)
    # print(matrix)
    # print(b)

    #formulele (5), (6), (7) si formarea matricii superior triunghiulare
    while l < N-1 and abs(big_matrix[l, l]) > 10 ** prec:
        for i in range(l + 1, N ):
            factor = big_matrix[i, l] / big_matrix[l, l]
            for j in range(l + 1, N ):
                big_matrix[i][j] = big_matrix[i, j] - factor * big_matrix[l, j]
                big_matrix[i][j+N] = big_matrix[i, j + N] - factor * big_matrix[l, j + N]
            big_matrix[i, l] = 0
        l += 1
        row = search_pivot(big_matrix, l, N)
        var_2_interchange_lines(big_matrix, row, l)

    if abs(big_matrix[l, l]) <= 10 ** prec:
        print("\nExercise 1: \nSingular matrix")
    else:
        results = np.empty((N,N))
        for i in range(0,N):
            results[:, i] = resolve_superior_triangular_system(big_matrix, N, b = big_matrix[:, i + N])
            #print("\nExercise 4: \nOur Inverse is\n: ", results)
        return results

#https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm - Thomas Algorithm
def tridiagonal_matrix_algorithm(matrix_3diag, prec, N):
    pass


def calculate_ex_2():
    try:
        N = int(ENTRY1.get())
        lowest = int(ENTRY2.get())
        highest = int(ENTRY3.get())
    except ValueError:
        messagebox.showinfo("Result", "Please enter valid data!")
    else:

        prec = -6  # int(input("EPSILON: precision: "))
        b = np.random.uniform(lowest, highest, N)
        matrix = np.random.uniform(lowest, highest, size=(N, N))

    print("---------------------START--------------------")
    print("\nDimension = ", N)
    print("The matrix is the following: \n", matrix)
    print("B = ", b)
    print(f"We opt for a precision of 10 ** {prec}")

    # copie a matricii initiale
    initial_matrix = matrix.copy()
    initial_b = b.copy()
    results = f.Gauss_elimination(initial_matrix, matrix, b, N, prec, initial_b)

    # Exercise3

    x = np.linalg.solve(initial_matrix, initial_b)
    inverse_of_matrix = np.linalg.inv(initial_matrix)
    vertical_b = np.array(initial_b).reshape(N, 1)
    matrices_result = np.dot(inverse_of_matrix, vertical_b)

    print("\nExercise 3\nX-es from numpy are: ", x)
    print("Inverse of the matrix from numpy is: \n", inverse_of_matrix)
    euclidian_norm_for_x_es = 0.0
    eucl_norm_inverse_matrix = 0.0
    for i in range(0, N):
        euclidian_norm_for_x_es += abs(results[i] - x[i])
        eucl_norm_inverse_matrix += abs(results[i] - matrices_result[i])

    print("Euclidian norm for x_gauss - x_bibl is: ", euclidian_norm_for_x_es)
    print("Euclidian norm for x_gauss - inverse of matrix * b_init is: ", eucl_norm_inverse_matrix[0])

    # Exercise 4

    zeros = [0] * N * N
    identity = np.array(zeros).reshape(N, N)
    for i in range(0, N):
        identity[i][i] = 1

    big_matrix = np.empty((N, N + N))
    for i in range(0, N):
        for j in range(0, N):
            big_matrix[i][j] = initial_matrix[i, j]
            big_matrix[i][j + N] = identity[i, j]

    inverse_Gauss = f.var2_Gauss_elimination(big_matrix, N, prec)
    final_matrix = np.empty((N, N))
    for i in range(0, N):
        for j in range(0, N):
            final_matrix[i, j] = inverse_Gauss[i, j] - inverse_of_matrix[i, j]

    mat_norm = np.linalg.norm(final_matrix)

    print("\nExercise 4:\nThe norm of difference between our approximation of inverse and the numpy's one is: ",
          mat_norm)














       # messagebox.showinfo("Result ex2 : ", str(abs(a * (b * c) - (a * b) * c)))

if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", calculate_ex_2)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab2 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator2 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)
    ENTRY1 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY1.place(x=380, y=221)
    ENTRY2 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY2.place(x=380, y=251)
    ENTRY3 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY3.place(x=380, y=281)


    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu Matrice", padx=33, pady=10, command=calculate_ex_2,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=251)



    TOP.mainloop()



#Tema 2 CN


option = int(input("Choose 1 or 2: 1 for .txt input - 2 for random input with your dimension "))
if option == 1:
    file1 = open('input.txt', 'r')
    Lines = file1.readlines()
    count = 0
    for line in Lines:
        if count == 0:
            N = int(line)
        if count == 1:
            coef = list(map(float, line.split()))
            matrix = np.array(coef).reshape(N, N)
        if count == 2:
            b = list(map(float, line.strip().split()))
        if count == 3:
            prec = float(line)
        count += 1
else:
    N = int(input("N: number of rows/columns: "))
    prec = -6   #int(input("EPSILON: precision: "))
    lowest = float(input("Lowest value for coef: "))
    highest = float(input("Highest value for coef: "))
    b = np.random.uniform(lowest,highest, N)
    matrix = np.random.uniform(lowest,highest,size = (N,N))

print("---------------------START--------------------")
print("\nDimension = ", N)
print("The matrix is the following: \n", matrix)
print("B = ", b)
print(f"We opt for a precision of 10 ** {prec}")


#copie a matricii initiale
initial_matrix = matrix.copy()
initial_b = b.copy()
results = f.Gauss_elimination(initial_matrix, matrix, b, N, prec, initial_b)

#Exercise3

x = np.linalg.solve(initial_matrix, initial_b)
inverse_of_matrix = np.linalg.inv(initial_matrix)
vertical_b = np.array(initial_b).reshape(N, 1)
matrices_result = np.dot(inverse_of_matrix, vertical_b)

print("\nExercise 3\nX-es from numpy are: ", x)
print("Inverse of the matrix from numpy is: \n", inverse_of_matrix)
euclidian_norm_for_x_es = 0.0
eucl_norm_inverse_matrix = 0.0
for i in range(0, N):
    euclidian_norm_for_x_es += abs(results[i] - x[i])
    eucl_norm_inverse_matrix += abs(results[i] - matrices_result[i])

print("Euclidian norm for x_gauss - x_bibl is: ", euclidian_norm_for_x_es)
print("Euclidian norm for x_gauss - inverse of matrix * b_init is: ", eucl_norm_inverse_matrix[0])

#Exercise 4

zeros = [0] * N * N
identity = np.array(zeros).reshape(N, N)
for i in range (0, N):
    identity[i][i] = 1

big_matrix = np.empty((N, N+N))
for i in range(0, N):
    for j in range (0, N):
        big_matrix[i][j] = initial_matrix[i,j]
        big_matrix[i][j + N] = identity[i,j]

inverse_Gauss = f.var2_Gauss_elimination(big_matrix, N, prec)
final_matrix = np.empty((N,N))
for i in range(0, N):
    for j in range(0, N):
        final_matrix[i, j] = inverse_Gauss[i,j] - inverse_of_matrix[i,j]

mat_norm = np.linalg.norm(final_matrix)

print("\nExercise 4:\nThe norm of difference between our approximation of inverse and the numpy's one is: ", mat_norm)

#BONUS

# for i in range (0,N):
#     if i == 1:
#         c[i] = c[i] / b[i]
#         d[i] = d[i] / b[i]
#     else:
#         if i != N-1:
#             c[i] = c[i] / (b[i] - a[i] * c[i-1])
#         d[i] = (d[i] - a[i]*d[i-1]) / ( b[i] - a[i] * c[i-1])


