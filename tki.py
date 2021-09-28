import tkinter as tk
from pprint import pprint
from my_parserrr import start_the_parser #, start_the_parser_habr
import os
import sys


root = tk.Tk()
pprint(sys.path)
root.title('Парсер')


btn_1 = tk.Button(
    text="Запустить парсер",
    width=25,
    height=5,
)

btn_2 = tk.Button(
    text="открыть БД",
    width=25,
    height=5,
)
label = tk.Label(text='Введите ключевое слово.')
txt = tk.Entry(root)
label.pack()
txt.pack()

def handle_click_btn_2(event):
    """Выводит символ, связанный с нажатой клавишей"""
    os.startfile('bd.db')
# Связывает событие нажатия клавиши с handle_keypress()
btn_2.bind("<Button-1>", handle_click_btn_2)

def handle_click_btn_1(event):
    key = txt.get()

    return start_the_parser(key) , start_the_parser_habr(key)

btn_1.bind("<Button-1>", handle_click_btn_1)

btn_1.pack()
btn_2.pack()

root.mainloop()
# Добавим всякой новой фигни