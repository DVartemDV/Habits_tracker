from tkinter import *
from random import *
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('habits_tracker.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INT
    )
''')
conn.commit() 

cursor.execute('''
    CREATE TABLE IF NOT EXISTS completions (
    habit_id INTEGER
    )
''')
conn.commit()

class Habit_tracker:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('700x500')
        self.root.resizable(height=False, width=False)
        self.root.title('Трекер привычек')
        
        append_habit_btn = Button(
            text='Добавить привычку',
            command=self.open_win_ap,
            font=('', 20)
        ).place(x=200,y=100)
    
        del_habit_btn = Button(
            text='Удалить привычку',
            command=self.open_win_del_habit,
            font=('', 20)
        ).place(x=200,y=200)
    
    def append_habit(self, name, quantity):
        cursor.execute('''SELECT name FROM habits WHERE name = ?''', (name,))
        if cursor.fetchone():
            return False, 'Такая привычка уже существует'
        cursor.execute('''
        INSERT INTO habits (name, quantity)
        VALUES (?, ?)
        ''', (name, quantity))
        conn.commit()
        return True, f'Привычка {name} {quantity} раз была добавлена.'
        
    def del_habit(self, habit_id):                        # func удаление привычки   
        cursor.execute('''SELECT name, id FROM habits WHERE id = ?''', (habit_id,))
        habit = cursor.fetchone()
        if habit:        
            name = habit[0]
            cursor.execute('''
            DELETE FROM habits WHERE id = ?
            ''', (habit_id,))
            conn.commit()
            return True, f'Привычка {name} была удалена.'   
        else:
            conn.commit()
            return False, f'Привычки c id: {habit_id} не было найдено.'
    
    def list_habits(self):
        cursor.execute('''
    SELECT id, name, quantity FROM habits ''')
        habits = cursor.fetchall()
        return habits
    
    def open_win_ap(self):      # Окно добавления привычки
        win_ap = Toplevel(self.root)
        win_ap.geometry('600x500')
        win_ap.title('Окно для добавления привычки')
        win_ap.resizable(width=False, height=False)
        er_pole = Label(win_ap,text='', font=('', 15))
        def tap_on_insert():
            name = entry_name.get()
            quantity = entry_quantity.get()
            if name and quantity:
                setting, message = self.append_habit(name, quantity)
                if setting:
                    er_pole.configure(text=message, fg='green')
                    win_ap.after(2000, win_ap.destroy)
                else:
                    er_pole.configure(text=message, fg='red')
            else:
                er_pole.configure(text='Поля не должны быть пустыми', fg='red')
        
        er_pole.place(x=1,y=380)
        label_glav_txt = Label(win_ap, text='Добавление привычки', font=('', 15), bg='white')
        label_glav_txt.place(x=180,y=1)
        label_name_text = Label(win_ap, text='Название', font=('', 15), bg='white')    
        label_name_text.place(x=100,y=50)
        label_quantity_text = Label(win_ap,text='Количество повторений', font=('', 15), bg='white')
        label_quantity_text.place(x=25,y=200)
        insert_btn = Button(win_ap, text='Insert', font=('', 20), command=tap_on_insert)
        insert_btn.place(x=450,y=420)
        entry_quantity = Entry(win_ap,font=('', 17))
        entry_quantity.place(x=250, y= 200)
        entry_name = Entry(win_ap, font=('', 17))
        entry_name.place(x=250,y=50)

    def open_win_del_habit(self):
        win_del = Toplevel(self.root)
        win_del.title('Окно для удаления привычки')
        win_del.resizable(width=False, height=False)
        win_del.geometry('600x500')
        er_pole = Label(win_del, text='', font=('',15))
        
        def tap_on_insert():
            ent_habit_id = entry_habit_id.get()
            if not ent_habit_id:
                er_pole.configure(text='Поле не должно быть пустым', fg='red')
                return
            setting, message = self.del_habit(ent_habit_id)
            if setting:
                er_pole.configure(fg='green', text=message)
                win_del.after(2000, win_del.destroy)
            else:
                er_pole.configure(text=message)
            
                
        insert_btn = Button(win_del, text='Удалить привычку', command=tap_on_insert, font=('', 15))
        insert_btn.place(x=400,y=420)
        er_pole.place(x=1,y=380)
        entry_habit_id = Entry(win_del, font=('', 17))
        entry_habit_id.place(x=250,y=100)
        label_habit_id_text = Label(win_del, text='Введите id привычки', font=('', 17))
        label_habit_id_text.place(x=1,y=100)

    def run(self):
        self.root.mainloop()

main_win = Habit_tracker()
main_win.run()


