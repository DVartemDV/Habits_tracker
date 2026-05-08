from tkinter import *
from random import *
from tkinter import messagebox
import sqlite3



root = Tk()
root['bg'] = 'white'
root.title('habits_tracker')
root.geometry('700x500')
root.resizable(width=False, height=False)

conn = sqlite3.connect('habits_tracker.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    create_date TEXT,
    quantity INT
    )
''')
conn.commit() 

cursor.execute('''
    CREATE TABLE IF NOT EXISTS completions (
    habit_id INTEGER
    date TEXT
    )
''')
conn.commit()

def open_del_hab():
    win_del=Toplevel(root)
    win_del.title('Окно для удаления приывычки')
    win_del.geometry('600x500')
    
    def tap_on_insert():
        get_ent = entry_del_hab.get()
        del_habit(get_ent, er_pole, win_del)
        
    
    er_pole = Label(win_del, text='', font=('', 15))
    er_pole.place(x=1,y=380)
    label_del_hab = Label(win_del, text='Название привычки', font=('', 15))
    inert_btn = Button(win_del, command=tap_on_insert, font=('', 20), text='Insert')
    er_pole = Label(win_del, text='', font=('',15))
    inert_btn.place(x=450,y=420)
    label_del_hab.place(x=1,y=100)
    entry_del_hab = Entry(win_del, font=('', 17))
    entry_del_hab.place(x=220,y=100)
    er_pole.place(x=1,y=380)


def open_win_ap():
    win_ap = Toplevel(root)
    win_ap.title('Окно для добавления привычки')
    er_pole = Label(win_ap,text='', font=('', 15))
    win_ap.geometry('600x500')
    def tap_on_insert():
        quantity = entry_quantity.get()
        name = entry_name.get()
        if name and quantity:
            append_habit(name, er_pole, quantity, win_ap)
        else:
            er_pole.configure(text='Поля не должны быть пустыми!')
    
    label_glav_txt = Label(win_ap, text='Добавление привчки', font=('', 15), bg='white',)
    label_name_text = Label(win_ap, text='Название', font=('', 15), bg='white')
    label_quantity_text = Label(win_ap,text='Количество повторений', font=('', 15), bg='white')
    insert_btn = Button(win_ap, text='Insert', font=('', 20), command=tap_on_insert)
    entry_quantity = Entry(win_ap,font=('', 17))
    entry_name = Entry(win_ap, font=('', 17))
    label_quantity_text.place(x=25,y=200)
    label_name_text.place(x=100,y=50)
    label_glav_txt.place(x=180,y=1)
    entry_quantity.place(x=250, y= 200)
    er_pole.place(x=1,y=380)
    entry_name.place(x=250,y=50)
    insert_btn.place(x=450,y=420)

def append_habit(name, er_pole, quantity, win_ap):                      # func добавления привычки
    cursor.execute('''SELECT name FROM habits WHERE name = ?''', (name,))
    if cursor.fetchone():
        er_pole.configure(text=('Такая привычка уже существует'))
        return
    cursor.execute('''
    INSERT INTO habits (name, quantity)
    VALUES (?, ?)
    ''', (name, quantity))
    conn.commit()
    er_pole.configure(text=(f'Привчка {name} {quantity} раз успешно добавлена.'), font=('',13))
    win_ap.after(1500, win_ap.destroy)    

def del_habit(name,er_pole, win_del):                        # func удаление привычки
    cursor.execute('''SELECT name FROM habits WHERE name = ?''', (name,))
    if cursor.fetchone():
        cursor.execute('''
        DELETE FROM habits WHERE name = ?
        ''', (name,))
        er_pole.configure(text=f'Привычка {name} успешно удалена.')
        win_del.after(1500, win_del.destroy)
        conn.commit()
    else:
        er_pole.configure(text='Такая привычка не найдена')
        return


def list_habits():                      # Список всех привычек
    cursor.execute('''
    SELECT id, name, create_date FROM habits ''')
    habits = cursor.fetchall()
    if not habits:
        print('Привычек нету, добавь первую')
        return
    else:
        for habit_id, name, date in habits:
            print(f'ID: {habit_id}'),
            print(f'Имя: {name}'),
            print(f'Дата: {date}')

# интерфейс в главном окне
append_habit_btn = Button(
    text='Добавить привычку',
    command=open_win_ap,
    font=('', 20)
)
append_habit_btn.place(x=0,y=1)

del_habit_btn= Button(
    text='Удалить привычку',
    command=open_del_hab,
    font=('',20)
)
del_habit_btn.place(x=1, y=444)

root.mainloop() # Работа программы