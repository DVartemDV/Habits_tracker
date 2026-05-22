import sqlite3
import customtkinter as ctk

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
        self.root = ctk.CTk()
        self.root.geometry('700x500')
        self.root.resizable(height=False, width=False)
        self.root.title('Трекер привычек')
        
        self.append_habit_btn = ctk.CTkButton(
            self.root,
            text='Добавить привычку',
            command=self.open_win_ap,
            font=('', 30)
        )
        self.append_habit_btn.place(x=200, y=100)
    
        self.del_habit_btn = ctk.CTkButton(
            self.root,
            text='Удалить привычку',
            command=self.open_win_del_habit,
            font=('', 30)
        )
        self.del_habit_btn.place(x=200, y=200)
    
        self.list_btn = ctk.CTkButton(
            self.root,
            text='Список привычек',
            command=self.open_win_list,
            font=('', 30)
        )
        self.list_btn.place(x=200, y=300)
    
        self.win_ap = None
        self.win_del = None
        self.win_list = None
    
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
        
    def del_habit(self, habit_id):
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
        cursor.execute('SELECT id, name, quantity FROM habits')
        habits = cursor.fetchall()
        return habits

    def open_win_ap(self):
        if self.win_ap is not None and self.win_ap.winfo_exists():
            return    
        
        win_ap = ctk.CTkToplevel(self.root)
        self.win_ap = win_ap
        win_ap.geometry('600x500')
        win_ap.title('Окно для добавления привычки')
        win_ap.resizable(width=False, height=False)
        
        
        
        er_pole = ctk.CTkLabel(win_ap, text='', font=('', 20))
        er_pole.place(x=1, y=380)
        
        label_glav_txt = ctk.CTkLabel(win_ap, text='Добавление привычки', font=('', 20))
        label_glav_txt.place(x=180, y=1)
        
        label_name_text = ctk.CTkLabel(win_ap, text='Название', font=('', 20))
        label_name_text.place(x=100, y=50)
        
        label_quantity_text = ctk.CTkLabel(win_ap, text='Количество повторений', font=('', 20))
        label_quantity_text.place(x=25, y=200)
        
        entry_name = ctk.CTkEntry(win_ap, font=('', 17), width= 300)
        entry_name.place(x=250, y=50)
        
        entry_quantity = ctk.CTkEntry(win_ap, font=('', 17))
        entry_quantity.place(x=250, y=200)
        
        insert_btn = ctk.CTkButton(win_ap, text='Добавить привычку', font=('', 22), command=lambda: self.tap_on_insert(win_ap, entry_name, entry_quantity, er_pole))
        insert_btn.place(x=360, y=420)
        win_ap.after(100, win_ap.focus)
    def tap_on_insert(self, win_ap, entry_name, entry_quantity, er_pole):
        name = entry_name.get()
        quantity = entry_quantity.get()
        if name and quantity:
            setting, message = self.append_habit(name, quantity)
            if setting:
                er_pole.configure(text=message, text_color='green')
                win_ap.after(2000, win_ap.destroy)
            else:
                er_pole.configure(text=message, text_color='red')
        else:
            er_pole.configure(text='Поля не должны быть пустыми', text_color='red')

    def open_win_del_habit(self):
        if self.win_del is not None and self.win_del.winfo_exists():
            return        
        
        win_del = ctk.CTkToplevel(self.root)
        self.win_del = win_del
        win_del.title('Окно для удаления привычки')
        win_del.resizable(width=False, height=False)
        win_del.geometry('600x500')
        
        
        
        
        label_habit_id_text = ctk.CTkLabel(win_del, text='Введите id привычки', font=('', 20))
        label_habit_id_text.place(x=1, y=100)
        
        entry_habit_id = ctk.CTkEntry(win_del, font=('', 17), width= 300)
        entry_habit_id.place(x=250, y=100)
        
        er_pole = ctk.CTkLabel(win_del, text='', font=('', 20))
        er_pole.place(x=1, y=380)
        
        insert_btn = ctk.CTkButton(win_del, text='Удалить привычку', command=lambda: self.tap_on_del(win_del, entry_habit_id, er_pole), font=('', 20))
        insert_btn.place(x=400, y=420)
        win_del.after(100, win_del.focus)
    def tap_on_del(self, win_del, entry_habit_id, er_pole):
        ent_habit_id = entry_habit_id.get()
        if not ent_habit_id:
            er_pole.configure(text='Поле не должно быть пустым', text_color='red')
            return
        setting, message = self.del_habit(ent_habit_id)
        if setting:
            er_pole.configure(text=message, text_color='green')
            win_del.after(2000, win_del.destroy)
        else:
            er_pole.configure(text=message, text_color='red')

    def open_win_list(self):
        if self.win_list is not None and self.win_list.winfo_exists():
            return
            
        win_list = ctk.CTkToplevel(self.root)
        self.win_list = win_list
        win_list.geometry('600x600')
        win_list.title('Список всех привычек')
        win_list.resizable(width=False, height=False)
        
        
        
        er_pole = ctk.CTkLabel(win_list, text='', font=('', 20))
        er_pole.place(x=1, y=450)
        
        list_frame = ctk.CTkScrollableFrame(win_list, width=400, height=400)
        list_frame.place(x=80, y=20)
        
        habits = self.list_habits()
        if not habits:
            er_pole.configure(text='Привычек еще нет')
            return
        
        for id, name, quantity in habits:
            btn = ctk.CTkButton(list_frame, text=f'id:{id}. {name} . {quantity} раз', fg_color="transparent", anchor="w")
            btn.pack(fill="x", padx=5, pady=2)
        win_list.after(100, win_list.focus)
    def run(self):
        self.root.mainloop()

main_win = Habit_tracker()
main_win.run()