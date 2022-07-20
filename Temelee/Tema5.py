import numpy as np
import copy
from numpy import linalg as LA
from tkinter import *
from tkinter import messagebox


def calculate_ex():
    def read_from_file(file_txt):
        info = open(file_txt, "r")
        lines = info.readlines()
        count = 0
        for line in lines:
            if count == 0:
                p = int(line)
                if p < 1:
                    print("ERR :: Error at reading number of lines\n")
                    info.close()
                    return -1
            if count == 1:
                n = int(line)
                if p < 1:
                    print("ERR :: Error at reading number of columns\n")
                    info.close()
                    return -1
            if count == 2:
                epsilon = float(line)
            if count == 3:
                string_vector_for_matrix = line.split(' ')
                vector_for_matrix = [float(x) for x in string_vector_for_matrix]
            count += 1
        return [p, n, epsilon, vector_for_matrix]

    info = read_from_file("example1.txt")

    matrix = info[3]
    intial_vector_matrix = copy.deepcopy(matrix)
    epsilon = info[2]
    a = 10 ** -epsilon
    nb_lines = info[0]
    nb_columns = info[1]

    def find_p_and_q(matrix_in_rare_form, lines):
        max = -1000000
        index_in_vector = -1

        regularisation_index = 0
        real_index = -1

        for i in range(len(matrix_in_rare_form)):
            real_index += 1
            if real_index % lines == 0 and real_index != 0:
                regularisation_index += 1
                real_index = real_index + regularisation_index

            line = regularisation_index
            column = real_index % lines

            if line != column:
                if abs(matrix_in_rare_form[i]) >= max:
                    max = abs(matrix_in_rare_form[i])
                    p = line
                    q = column
                    index_in_vector = i
        return [p, q, index_in_vector]

    def transform_from_p_and_q_into_single_index_and_return_element(p, q, lines, matrix_in_rare_form):
        index = -1
        line = 0
        array = list(range(lines))
        array.reverse()

        if q < p:
            aux = q
            q = p
            p = aux

        for i in array:
            for j in range(0, i + 1):
                index += 1
                if line == p and j + line == q:
                    return [matrix_in_rare_form[index], index]
            line += 1

    def find_with_index_the_p_q_element(matrix_in_rare_form, lines, p, q):
        regularisation_index = 0
        real_index = -1

        for i in range(len(matrix_in_rare_form)):
            real_index += 1
            if real_index % lines == 0 and real_index != 0:
                regularisation_index += 1
                real_index = real_index + regularisation_index

            line = regularisation_index
            column = real_index % lines

            if line == p and column == q:
                if matrix_in_rare_form[i] == None:
                    print("You go out of the matrix\n")
                return matrix_in_rare_form[i]

    def check_if_diagonal(matrix_in_rare_form, lines):
        ok = 1
        for i in range(lines):
            for j in range(lines):
                if i == j:
                    continue
                if find_with_index_the_p_q_element(matrix_in_rare_form, lines, i, j) != 0:
                    ok = 0
        # -1 inseamna ca nu e diagonala
        if ok == 0:
            return -1
        return 1

    def create_matrix_from_vector(matrix_in_rare_form, lines):
        new_matrix = np.zeros((lines, lines))
        regularisation_index = 0
        real_index = -1

        for i in range(len(matrix_in_rare_form)):
            real_index += 1
            if real_index % lines == 0 and real_index != 0:
                regularisation_index += 1
                real_index = real_index + regularisation_index

            line = regularisation_index
            column = real_index % lines

            new_matrix[line][column] = new_matrix[column][line] = matrix_in_rare_form[i]

        return new_matrix

    def Jacobi_aprox(matrix_in_rare_form, lines, columns, epsilon):
        if lines != columns:
            print("ERR : not the same value for lines and columns")
            return -1
        k = 0
        U_mat = np.identity(lines)

        # calcul indici p si q
        p_and_q = find_p_and_q(matrix_in_rare_form, lines)
        p = p_and_q[0]
        q = p_and_q[1]

        # calcul unghiul theta, c, s, t
        element_p_p = transform_from_p_and_q_into_single_index_and_return_element(p, p, lines, matrix_in_rare_form)[0]
        element_q_q = transform_from_p_and_q_into_single_index_and_return_element(q, q, lines, matrix_in_rare_form)[0]
        element_p_q = transform_from_p_and_q_into_single_index_and_return_element(p, q, lines, matrix_in_rare_form)[0]

        alpha = (element_p_p - element_q_q) / (2 * element_p_q)

        # t
        if alpha >= 0:
            t = -alpha + pow(pow(alpha, 2) + 1, 1 / 2)
        else:
            t = -alpha - pow(pow(alpha, 2) + 1, 1 / 2)

        # c
        c = 1 / pow(1 + pow(t, 2), 1 / 2)

        # s
        s = t / pow(1 + pow(t, 2), 1 / 2)

        k_max = 10000
        k = 0
        while check_if_diagonal(matrix_in_rare_form, lines) == -1 and k < k_max:
            # print(f"At iter {k}, the vector is: {matrix_in_rare_form}")
            # pasul 5
            for j in range(lines):
                if j != p and j != q:
                    matrix_in_rare_form[
                        transform_from_p_and_q_into_single_index_and_return_element(p, j, lines, matrix_in_rare_form)[
                            1]] = c * matrix_in_rare_form[
                        transform_from_p_and_q_into_single_index_and_return_element(p, j, lines, matrix_in_rare_form)[
                            1]] + s * matrix_in_rare_form[
                                      transform_from_p_and_q_into_single_index_and_return_element(q, j, lines,
                                                                                                  matrix_in_rare_form)[
                                          1]]

                    matrix_in_rare_form[
                        transform_from_p_and_q_into_single_index_and_return_element(q, j, lines, matrix_in_rare_form)[
                            1]] = -s * matrix_in_rare_form[
                        transform_from_p_and_q_into_single_index_and_return_element(j, p, lines, matrix_in_rare_form)[
                            1]] + c * matrix_in_rare_form[
                                      transform_from_p_and_q_into_single_index_and_return_element(q, j, lines,
                                                                                                  matrix_in_rare_form)[
                                          1]]

                    matrix_in_rare_form[
                        transform_from_p_and_q_into_single_index_and_return_element(j, p, lines, matrix_in_rare_form)[
                            1]] = \
                        matrix_in_rare_form[
                            transform_from_p_and_q_into_single_index_and_return_element(p, j, lines,
                                                                                        matrix_in_rare_form)[1]]

            matrix_in_rare_form[
                transform_from_p_and_q_into_single_index_and_return_element(p, p, lines, matrix_in_rare_form)[1]] += t * \
                                                                                                                     matrix_in_rare_form[
                                                                                                                         transform_from_p_and_q_into_single_index_and_return_element(
                                                                                                                             p,
                                                                                                                             q,
                                                                                                                             lines,
                                                                                                                             matrix_in_rare_form)[
                                                                                                                             1]]

            matrix_in_rare_form[
                transform_from_p_and_q_into_single_index_and_return_element(q, q, lines, matrix_in_rare_form)[1]] -= t * \
                                                                                                                     matrix_in_rare_form[
                                                                                                                         transform_from_p_and_q_into_single_index_and_return_element(
                                                                                                                             p,
                                                                                                                             q,
                                                                                                                             lines,
                                                                                                                             matrix_in_rare_form)[
                                                                                                                             1]]

            matrix_in_rare_form[
                transform_from_p_and_q_into_single_index_and_return_element(p, q, lines, matrix_in_rare_form)[1]] = 0

            # pasul 7
            for i in range(lines):
                aux = U_mat[i, p]
                U_mat[i, p] = c * U_mat[i, p] + s * U_mat[i, q]
                U_mat[i, q] = -s * aux + c * U_mat[i, q]

            # pasul 1
            p_and_q = find_p_and_q(matrix_in_rare_form, lines)
            p = p_and_q[0]
            q = p_and_q[1]

            # pasii 3, 4

            # calcul unghiul theta, c, s, t
            element_p_p = transform_from_p_and_q_into_single_index_and_return_element(p, p, lines, matrix_in_rare_form)[
                0]
            element_q_q = transform_from_p_and_q_into_single_index_and_return_element(q, q, lines, matrix_in_rare_form)[
                0]
            element_p_q = transform_from_p_and_q_into_single_index_and_return_element(p, q, lines, matrix_in_rare_form)[
                0]

            if abs(element_p_q) < 10 ** -epsilon:
                return [matrix_in_rare_form, U_mat]

            alpha = (element_p_p - element_q_q) / (2 * element_p_q)
            # t
            if alpha >= 0:
                t = -alpha + pow(pow(alpha, 2) + 1, 1 / 2)
            else:
                t = -alpha - pow(pow(alpha, 2) + 1, 1 / 2)

            # c
            c = 1 / pow(1 + pow(t, 2), 1 / 2)
            s = t / pow(1 + pow(t, 2), 1 / 2)

            k += 1

        return [matrix_in_rare_form, U_mat]

    def take_lambdas(matrix_in_rare_form, lines):
        lambdas = np.zeros(lines)
        for i in range(lines):
            for j in range(lines):
                if i == j:
                    lambdas[i] = find_with_index_the_p_q_element(matrix_in_rare_form, lines, i, j)
        return lambdas

    def sum_min_lambda(numpy_lambda, my_lambda_vector):
        summ = 0
        for i in range(nb_lines):
            min = abs(numpy_lambda[0] - my_lambda_vector[i])
            for j in range(nb_lines):
                if abs(numpy_lambda[j] - my_lambda_vector[i]) < min:
                    min = abs(numpy_lambda[j] - my_lambda_vector[i])
            summ += min * a
        return summ

    def difference_of_matrices(A, B):
        resulted_matrix = np.zeros((len(A), len(A)))
        for i in range(nb_lines):
            for j in range(nb_columns):
                resulted_matrix[i, j] = (A[i, j] - B[i, j]) * a
        return resulted_matrix

    ###Ex1 -- calcularea normei

    results = Jacobi_aprox(matrix, nb_lines, nb_columns, epsilon)
    final_vector_matrix = results[0]
    U_matrix = results[1]
    ###imi scriu ca o matrice normala vectorul, dupa ce am ajuns la forma finala

    initial_matrix = create_matrix_from_vector(intial_vector_matrix, nb_lines)
    final_matrix = create_matrix_from_vector(matrix, nb_lines)

    A_init_U = np.dot(initial_matrix, U_matrix)
    U_lambda = np.dot(U_matrix, final_matrix)

    resulted_matrix = difference_of_matrices(A_init_U, U_lambda)
    print(f"Ex 1: Norma este = {LA.norm(resulted_matrix)}")
    messagebox.showinfo("Solutie?", str("Am gasit solutie!"))
    messagebox.showinfo("Norma este: ", str(LA.norm(resulted_matrix)))

    # Ex2

    my_lambda_vec = take_lambdas(final_vector_matrix, nb_lines)
    numpy_vec = LA.eig(initial_matrix)[0]

    print(f"Ex 2: Suma de diferente lambda este: {sum_min_lambda(numpy_vec, my_lambda_vec)}")
    messagebox.showinfo("SumaDifLambda este: ", str(sum_min_lambda(numpy_vec, my_lambda_vec)))

    # Ex3
    svd_matrix = [[1, 10, 3, 4, 5], [1, 2, 3, 6, 5], [1, 2, 3, 12, 5], [1, 20, 3, 4, 5], [1, 2, 3, 4, 5],
                  [1, 2, 3, 4, 5]]

    u, s, v = np.linalg.svd(svd_matrix)
    s_without_zeroes = [elem for elem in s if elem != 0]
    matrix_s = [[0 if j != i or i >= len(s_without_zeroes) else s_without_zeroes[i] for j in range(len(u))] for i in
                range(len(v))]
    rang = len(s_without_zeroes)
    nr_conditionare = max(s_without_zeroes) / min(s_without_zeroes)
    pseudoinversa_0 = np.dot(v, matrix_s)
    pseudoinversa = np.dot(pseudoinversa_0, np.transpose(u))
    pseudoinversa_mici_patrate = np.dot(np.linalg.inv(np.dot(np.transpose(svd_matrix), svd_matrix)),
                                        np.transpose(svd_matrix))

    norma_Manhattan = np.linalg.norm(np.subtract(pseudoinversa, pseudoinversa_mici_patrate).tolist(), ord=1)
    print("Ex 3: SVD")
    print(f"Valorile singulare ale matricei sunt: {s}")
    print(f"Rangul matricei este: {rang}")
    print(f"Numarul de conditionare al matricei este: {nr_conditionare}")
    print(f"Pseudoinversa Moore-Penrose a matricei este:\n {pseudoinversa}")
    print(f"Matricea pseudo-inversa in sensul celor mai mici patrate este:\n {pseudoinversa_mici_patrate}")
    print(f"Norma Manhattan A_i - A_j este: {norma_Manhattan}")

    messagebox.showinfo("Valorile singulare ale matricei sunt: ", str(s))
    messagebox.showinfo("Rangul matricei este: ", str(rang))
    messagebox.showinfo("Numarul de conditionare al matricei este: ", str(nr_conditionare))
    messagebox.showinfo("Pseudoinversa Moore-Penrose a matricei este: ", str(pseudoinversa))
    messagebox.showinfo("Matricea pseudo-inversa cmmp: ", str(pseudoinversa_mici_patrate))
    messagebox.showinfo("Norma Manhattan A_i - A_J este: ", str(norma_Manhattan))
    messagebox.showinfo("Cezar face licenta in: ", str("Dart"))


if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", calculate_ex)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab5 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator5 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu", padx=33, pady=10,
                     command=calculate_ex,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=151)

    TOP.mainloop()