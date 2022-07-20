import math
from tkinter import *
from tkinter import messagebox
import random
import math

h = 10 ** (-6)
epsilon = 10 ** (-8)

def steffensen(f):
    global epsilon
    x = random.uniform(-100, 100)
    delta_x = 0
    for _ in range(iterations):
        g_x = get_df(f, x)
        g_x_plus_gx = get_df(f, x + g_x)
        if abs(g_x_plus_gx - g_x) <= epsilon:
            if g1(f, x, h) > g2(f, x, h):
                print("G1 MAI MARE")
            elif g1(f, x, h) <= g2(f, x, h):
                print("G2 MAI MARE")
            return x
        delta_x = (g_x ** 2) / (g_x_plus_gx - g_x)
        x = x - delta_x
        if delta_x <= epsilon or delta_x >= (10 ** 8):
            break
    if abs(delta_x) <= epsilon:
        if g1(f, x, h) > g2(f, x, h):
            print("G1 MAI MARE")
        elif g1(f, x, h) <= g2(f, x, h):
            print("G2 MAI MARE")
        return x
    return None


def get_df(f,x):
    return g2(f, x, h)


def difference(f, x):
    if g1(f, x, h) > g2(f, x, h):
        messagebox.showinfo("G1?G2?", str("G1"))
    else:
        messagebox.showinfo("G1?G2?", str("G2"))


def g1(f, x, h):
    return (3 * f(x) - 4 * f(x - h) + f(x - 2 * h)) / (2 * h)


def g2(f, x, h):
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)





def run():
    f = read_f()
    while True:
        x = steffensen(f)
        if x is None:
            continue
        print(x)


if __name__ == "__main__":
    TOP = Tk()
    TOP.bind("<Return>", run)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab8 CN")
    TOP.resizable(width=False, height=False)
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator8 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu", padx=33, pady=10,
                     command=run,
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=151)

    TOP.mainloop()

    run()