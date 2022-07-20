import numbers
import functions as f
from tkinter import *
from tkinter import messagebox

def read_from_input(file):
    f = open(file, "r")
    dimension_of_matrix = int(f.readline())
    economic_list = [[] for x in range(0, dimension_of_matrix)]
    print(" Dim", dimension_of_matrix)
    line = f.readline()
    while line:
        line = f.readline()
        if not line:
            break
        strings = line.strip().split(",")
        value = float(strings[0])
        row = int(strings[1])
        column = int(strings[2])
        if column > row:
            continue
        occurance = [(x, y) for x, y in economic_list[row] if y == column]
        if not occurance:
            economic_list[row].append((value, column))
        else:
            new_pair = (occurance[0][0] + value, column)
            economic_list[row].remove(occurance[0])
            economic_list[row].append(new_pair)
    return economic_list


def adunare_matrice(matrice1, matrice2):
    matrice_rezultat = [[] for x in range(0, len(matrice1))]
    for iterator in range(0, len(matrice1)):
        for iterator_element in matrice1[iterator]:
            occurance = [(x, y) for x, y in matrice2[iterator] if y == iterator_element[1]]
            if occurance:
                matrice_rezultat[iterator].append((occurance[0][0] + iterator_element[0], iterator_element[1]))
            else:
                matrice_rezultat[iterator].append(iterator_element)
        for iterator_element in matrice2[iterator]:
            occurance = [(x, y) for x, y in matrice1[iterator] if y == iterator_element[1]]
            if not occurance:
                matrice_rezultat[iterator].append(iterator_element)

    return matrice_rezultat


def comparare_matrice(matrice1, matrice2):
    epsilon = 10 ** -6
    for iterator in range(0, len(matrice1)):
        if len(matrice1[iterator]) != len(matrice2[iterator]):
            return False
        for iterator_element in matrice1[iterator]:
            occurance = [(x, y) for x, y in matrice2[iterator] if y == iterator_element[1]]
            if occurance:
                if abs(occurance[0][0] - iterator_element[0]) > epsilon:
                    return False
            else:
                return False
    return True


def transform_line_into_column(matrice, coloana):
    res = []
    if coloana == len(matrice) - 1:
        return matrice[coloana]
    for iterator_element in matrice[coloana]:
        res.append(iterator_element)
    for iterator in range(coloana + 1, len(matrice)):
        occurance = [(x, y) for x, y in matrice[iterator] if y == coloana]
        if occurance:
            res.append((occurance[0][0], iterator))
    return res


def inmultire_matrice(matrice1, matrice2):
    matrice_rezultat = [[] for x in range(0, len(matrice1))]
    coloane_matrice1 = []
    coloane_matrice2 = []
    for iterator in range(0, len(matrice2)):
        coloane_matrice1.append(transform_line_into_column(matrice1, iterator))
        coloane_matrice2.append(transform_line_into_column(matrice2, iterator))

    for iterator_matrice1 in range(0, len(matrice1)):
        for iterator_matrice2 in range(0, len(matrice2)):
            if iterator_matrice1 >= iterator_matrice2:
                suma = 0
                curr_coloana = coloane_matrice2[iterator_matrice2]
                for iterator_element in coloane_matrice1[iterator_matrice1]:
                    occurance = [(x, y) for x, y in curr_coloana if y == iterator_element[1]]
                    if occurance:
                        suma += iterator_element[0] * occurance[0][0]
                if suma != 0:
                    matrice_rezultat[iterator_matrice1].append((suma, iterator_matrice2))
        if iterator_matrice1 % 2 == 0:
            print("Suntem la linia " + str(iterator_matrice1))

    return matrice_rezultat


def inmultire_matrice_lazy(matrice1, matrice2):
    matrice_rezultat = [[] for x in range(0, len(matrice1))]

    for iterator_matrice1 in range(0, len(matrice1)):
        for iterator_matrice2 in range(0, len(matrice2)):
            if iterator_matrice1 >= iterator_matrice2:
                suma = 0


                curr_coloana_1 = []
                if iterator_matrice2 == len(matrice2) - 1:
                    return matrice2[iterator_matrice2]
                for iterator_element in matrice2[iterator_matrice2]:
                    curr_coloana_1.append(iterator_element)
                for iterator in range(iterator_matrice2 + 1, len(matrice2)):
                    occurance = [(x, y) for x, y in matrice2[iterator] if y == iterator_matrice2]
                    if occurance:
                        curr_coloana_1.append((occurance[0][0], iterator))

                curr_coloana_2 = []
                if iterator_matrice1 == len(matrice1) - 1:
                    return matrice1[iterator_matrice1]
                for iterator_element in matrice1[iterator_matrice1]:
                    curr_coloana_2.append(iterator_element)
                for iterator in range(iterator_matrice1 + 1, len(matrice1)):
                    occurance = [(x, y) for x, y in matrice1[iterator] if y == iterator_matrice1]
                    if occurance:
                        curr_coloana_2.append((occurance[0][0], iterator))


                for iterator_element in curr_coloana_2:
                    occurance = [(x, y) for x, y in curr_coloana_1 if y == iterator_element[1]]
                    if occurance:
                        suma += iterator_element[0] * occurance[0][0]
                if suma != 0:
                    matrice_rezultat[iterator_matrice1].append((suma, iterator_matrice2))
        if iterator_matrice1 % 2 == 0:
            print("Suntem la linia " + str(iterator_matrice1))

    return matrice_rezultat


def calculate_ex_2():
    matrice1 = f.read_from_input("a.txt")
    matrice2 = f.read_from_input("b.txt")
    matrice_rezultat_fisier_adunare = f.read_from_input("a_plus_b.txt")
    matrice_rezultat_fisier_inmultire = f.read_from_input("a_ori_a.txt")
    matrice_rezultat = f.adunare_matrice(matrice1, matrice2)
    rezultat = f.comparare_matrice(matrice_rezultat, matrice_rezultat_fisier_adunare)
    # print(matrice_rezultat_fisier)
    # print(matrice_rezultat)
    # print(matrice1)
    # print(matrice2)
    print(rezultat)

    # rezultat_inmultire = f.inmultire_matrice(matrice1, matrice1)
    # rezultat2 = f.comparare_matrice(rezultat_inmultire, matrice_rezultat_fisier_inmultire)

    # print(rezultat_inmultire)
    # print(rezultat2)
    messagebox.showinfo("Rezultat adunare matrice: ", str(rezultat))


def calculate_ex_3():
    matrice1 = f.read_from_input("a.txt")
    matrice_rezultat_fisier_inmultire = f.read_from_input("a_ori_a.txt")
    rezultat_inmultire = f.inmultire_matrice(matrice1, matrice1)
    print(rezultat_inmultire)
    rezultat2 = f.comparare_matrice(rezultat_inmultire, matrice_rezultat_fisier_inmultire)
    # print(rezultat_inmultire)
    print(rezultat2)
    messagebox.showinfo("Rezultat inmultire matrice: ", str(rezultat2))


def calculate_ex_4():
    matrice1 = f.read_from_input("a.txt")
    matrice_rezultat_fisier_inmultire = f.read_from_input("a_ori_a.txt")
    rezultat_inmultire = f.inmultire_matrice_lazy(matrice1, matrice1)
    rezultat2 = f.comparare_matrice(rezultat_inmultire, matrice_rezultat_fisier_inmultire)
    # print(rezultat_inmultire)
    print(rezultat2)
    messagebox.showinfo("Rezultat inmultire matrice: ", str(rezultat2))

if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", calculate_ex_2)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab3 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator3 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu Matrice Adunare", padx=33, pady=10,
                     command=calculate_ex_2,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=151)

    BUTTON3 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu Matrice Inmultire Fast", padx=33, pady=10,
                     command=calculate_ex_3,
                     font=("Helvetica", 20, "bold"))
    BUTTON3.grid(row=5, column=0, sticky=W)
    BUTTON3.place(x=55, y=301)

    BUTTON3 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu Matrice Inmultire Lazy", padx=33, pady=10,
                     command=calculate_ex_4,
                     font=("Helvetica", 20, "bold"))
    BUTTON3.grid(row=5, column=0, sticky=W)
    BUTTON3.place(x=55, y=451)

    TOP.mainloop()
