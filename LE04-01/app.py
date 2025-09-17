import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Rezepte")
    root.geometry("800x800")

    # ---- Основний контейнер ----
    frame = ttk.Frame(root, padding=20) #padding=20 → внутрішній відступ.
    frame.pack(fill="both", expand=True) #Frame розтягується на все вікно.

    #Заголовок
    label =  ttk.Label(frame, text="Rezepte", font =("Arial", 22, "bold italic"))
    label.pack(pady=20) #відступ зверху/знизу 20 px.

    #Підзаголовок
    sub=ttk.Label(frame, text="(nur Interface noch")
    sub.pack()

    # ---- Список рецептів ----
    listbox=tk.Listbox(frame, height=10, width=50, font=("Arial", 12, "italic"))
    listbox.pack(pady=10)

    # Тестові дані (потім замінимо на дані з rezepte.json)
    rezepte=["Pizza", "Salat", "Pfannkuchen"]
    for r in rezepte:
        listbox.insert(tk.END, r) # tk.END, новий елемент додається після останнього існуючого.

    # ---- Контейнер для кнопок ----
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20) #відступ вниз

    def f_add_recept():
        top=tk.Toplevel(root) # нове вікно
        top.title("Neues Rezept")
        top.geometry("300x250")

        label= ttk.Label(top, text="Rezeptname eingeben:")
        label.pack(pady=10)

        entry = ttk.Entry(top, width=30)  # ← створюємо ДО функції
        entry.pack(pady=10)

        def f_save_recept():
            name = entry.get().strip()
            if name: # якщо не порожній
                listbox.insert(tk.END, name)
            top.destroy()

        btn_save = ttk.Button(top, text="Speichern", command=f_save_recept)
        btn_save.pack(pady=10)



    # Кнопки в ряд
    btn_add=ttk.Button(button_frame, text="Add Rezepte", command=f_add_recept)
    btn_add.grid(row=0, column=0, padx=5)
    """grid - рядок
            row=0 – елемент ставиться у 0-й рядок сітки (перший зверху).
            column=0 – у 0-й стовпчик сітки (перший зліва).
            padx=5 – відступ по горизонталі (зліва/справа по 5 px)."""

    btn_edit = ttk.Button(button_frame, text="Rezept bearbeiten")
    btn_edit.grid(row=2, column=1, padx=5) #рядок

    btn_delete = ttk.Button(button_frame, text="Rezept löschen")
    btn_delete.grid(row=0, column=2, padx=5)

    btn_exit = ttk.Button(button_frame, text="Beenden", command=root.destroy)
    btn_exit.grid(row=0, column=3, padx=5)
    root.mainloop() #Запуск головного циклу

if __name__=="__main__":
    main()