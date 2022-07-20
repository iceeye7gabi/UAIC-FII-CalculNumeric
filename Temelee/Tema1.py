import numpy as np
import math
import random

# Exercise1
print("Exercitiul1:")
u = 1.0
for i in range(100, 0, -1):
    u = pow(10, -i)
    if 1.0 + u != 1.0:
        print("Cel mai mic numar u este: ", u)
        break
print("\n")
# Exercise2 - Partea cu +
print("Exercitiul2: (asociativitate)")
a = 1.0
b = u / 10
c = u / 10

print("Calcul1: (a+b)+c = ", (a + b) + c)
print("Calcul1: a+(b+c) = ", a + (b + c))

print("\n")
# Exercise2 - Partea cu x
print("Exercitiul2: (multiplicitate)")
while True:
    a = random.uniform(0, 1)
    b = random.uniform(0, 1)
    c = random.uniform(0, 1)
    if a * (b * c) != (a * b) * c:
        print("a =", a)
        print("b =", b)
        print("c =", c)
        print("a*(b*c) = ", a * (b * c))
        print("(a*b)*c = ", (a * b) * c)
        print("abs(a*(b*c) -  (a*b)*c) = " + str(abs(a * (b * c) - (a * b) * c)))
        break

print("\n")
# Exercise3
coefSinusP = [
    1805490264.690988571178600370234394843221,
    -164384678.227499837726129612587952660511,
    3664210.647581261810227924465160827365,
    -28904.140246461781357223741935980097,
    76.568981088717405810132543523682
]

coefSinusQ = [
    2298821602.638922662086487520330827251172,
    27037050.118894436776624866648235591988,
    155791.388546947693206469423979505671,
    540.567501261284024767779280700089,
    1.0
]

coefCosinusP = [
    1090157078.174871420428849017262549038606,
    - 321324810.993150712401352959397648541681,
    12787876.849523878944051885325593878177,
    - 150026.206045948110568310887166405972,
    538.333564203182661664319151379451
]

coefCosinusQ = [
    1090157078.174871420428867295670039506886,
    14907035.776643879767410969509628406502,
    101855.811943661368302608146695082218,
    429.772865107391823245671264489311,
    1.0
]

coefLogP = [
    75.151856149910794642732375452928,
    -134.730399688659339844586721162914,
    74.201101420634257326499008275515,
    -12.777143401490740103758406454323,
    0.332579601824389206151063529971
]

coefLogQ = [
    37.575928074955397321366156007781,
    -79.890509202648135695909995521310,
    56.215534829542094277143417404711,
    -14.516971195056682948719125661717,
    1.0
]


def ex3_function(x, coeficienti):
    result = coeficienti[0] + x * (coeficienti[1] + x * (coeficienti[2] + x * (coeficienti[3] + x * coeficienti[4])))
    return result


print("Exercitiul3: (sinus)")

x = 1 / 2
print("Pentru valoarea x = " + str(x) + " vom avea urmatoarele rezultate: ")
sin_normal = math.sin(x * 0.25 * math.pi)
numitor = ex3_function(x * x, coefSinusQ)
if numitor < pow(10, -12):
    numitor = pow(10, -12)
sin_ex3_function = x * (ex3_function(x * x, coefSinusP) / numitor)
print("Valoarea sinus returnata de math.sin: " + str(sin_normal))
print("Valoarea sinus returnata de functia noastra: " + str(sin_ex3_function))
print("Modulul diferentei dintre cele 2 rezultate este: " + str(abs(sin_normal - sin_ex3_function)))
res1 = abs(sin_normal - sin_ex3_function)

print("\n")

print("Exercitiul3: (cosinus)")
print("Pentru valoarea x = " + str(x) + " vom avea urmatoarele rezultate: ")
cos_normal = math.cos(x * 0.25 * math.pi)
numitor = ex3_function(x * x, coefCosinusQ)
if numitor < pow(10, -12):
    numitor = pow(10, -12)
cos_ex3_function = (ex3_function(x * x, coefCosinusP) / numitor)
print("Valoarea cosinus returnata de math.cos: " + str(cos_normal))
print("Valoarea cosinus returnata de functia noastra: " + str(cos_ex3_function))
print("Modulul diferentei dintre cele 2 rezultate este: " + str(abs(cos_normal - cos_ex3_function)))
res2 = abs(cos_normal - cos_ex3_function)

print("\n")

x = 1.3
z = (x - 1) / (x + 1)
print("Exercitiul3: (ln)")
print("Pentru valoarea x = " + str(x) + " vom avea urmatoarele rezultate: ")
ln_normal = math.log(x, math.e)
numitor = ex3_function(z * z, coefLogQ)
if numitor < pow(10, -12):
    numitor = pow(10, -12)
ln_ex3_function = z * (ex3_function(z * z, coefLogP) / numitor)
print("Valoarea ln returnata de math.log(x, math.e): " + str(ln_normal))
print("Valoarea ln returnata de functia noastra: " + str(ln_ex3_function))
print("Modulul diferentei dintre cele 2 rezultate este: " + str(abs(ln_normal - ln_ex3_function)))
res3 = abs(ln_normal - ln_ex3_function)

print("\n")


from tkinter import *
from tkinter import messagebox


def ex1():
    messagebox.showinfo("Cel mai mic numar u este: ", u)


def calculate_ex_2():
    try:
        a = float(ENTRY1.get())
        b = float(ENTRY2.get())
        c = float(ENTRY3.get())
    except ValueError:
        messagebox.showinfo("Result", "Please enter valid data!")
    else:
        messagebox.showinfo("Result ex2 : ", str(abs(a * (b * c) - (a * b) * c)))

def show_ex_3():
    messagebox.showinfo("Dif sinus: ", str(res1))
    messagebox.showinfo("Dif cosinus: ", str(res2))
    messagebox.showinfo("Dif ln: ", str(res3))

if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", ex1)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab1 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator1 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)
    ENTRY1 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY1.place(x=340, y=221)
    ENTRY2 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY2.place(x=340, y=251)
    ENTRY3 = Entry(TOP, bd=8, width=10, font="Roboto 11")
    ENTRY3.place(x=340, y=281)

    BUTTON = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiul1", padx=33, pady=10, command=ex1,
                    font=("Helvetica", 20, "bold"))
    BUTTON.grid(row=5, column=0, sticky=W)
    BUTTON.place(x=55, y=60)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiul2", padx=33, pady=10, command=calculate_ex_2,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=251)

    BUTTON3 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiul3", padx=33, pady=10, command=show_ex_3,
                     font=("Helvetica", 20, "bold"))
    BUTTON3.grid(row=5, column=0, sticky=W)
    BUTTON3.place(x=55, y=391)

    TOP.mainloop()
