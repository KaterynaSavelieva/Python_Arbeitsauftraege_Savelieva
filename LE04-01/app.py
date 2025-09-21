import tkinter as tk
from tkinter import ttk
from data import all_recipes

def run_gui():
    root = tk.Tk()
    root.title("Rezepte")          # Заголовок вікна
    root.geometry("800x600")       # Розмір вікна 800x600

    # ---- Основний контейнер ----
    main_frame = ttk.Frame(root, padding=20)   # padding=20 → внутрішній відступ
    main_frame.pack(fill="both", expand=True)  # Frame розтягується на все вікно

    # Налаштування сітки для main_frame (2 колонки, 1 рядок)
    main_frame.columnconfigure(0, weight=1)    # перша колонка (зліва) займає 1 частку простору
    main_frame.columnconfigure(1, weight=2)    # друга колонка (справа) займає 2 частки простору
    main_frame.rowconfigure(0, weight=1)       # робимо рядок "розтяжним" по висоті

    # --- ліва колонка: заголовок + список + кнопки ---
    left = ttk.Frame(main_frame)               # створюємо контейнер (ліва колонка) всередині main_frame
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    # row=0, column=0 → ставимо у перший рядок і першу колонку
    # sticky="nsew" → розтягується у всі сторони (North, South, East, West)
    # padx=(0, 12) → зовнішній відступ справа на 12 px (щоб не злипався з правою колонкою)

    # Заголовок
    ttk.Label(left, text="Rezepte", font=("Arial", 22, "bold italic")).pack(pady=(0, 20))
    # pady=(0,20) → відступ зверху 0, знизу 20 px

    # ---- Список рецептів ----
    listbox = tk.Listbox(left, height=10, width=50, font=("Arial", 12, "italic"))
    listbox.pack(pady=10)

    # Тестові дані (тимчасово). Тепер це dict, щоб справа було що показати.
    # all_recipes = {
    #     "Pizza": {
    #         "zutaten": ["Mehl", "Eier", "Tomatensauce", "Käse"],
    #         "zubereitung": "Teig anrühren, belegen und im Ofen backen."
    #     },
    #     "Salat": {
    #         "zutaten": ["Tomaten", "Gurken", "Olivenöl"],
    #         "zubereitung": "Alles klein schneiden und mit Öl mischen."
    #     },
    #     "Pfannkuchen": {
    #         "zutaten": ["Mehl", "Milch", "Eier"],
    #         "zubereitung": "Teig rühren und in der Pfanne ausbacken."
    #     },
    # }

    # Заповнюємо список іменами рецептів (ключами dict)
    for name in all_recipes.keys():
        listbox.insert(tk.END, name)   # tk.END → додаємо новий елемент у кінець списку

    # --- права колонка: деталі рецепта ---
    right = ttk.Frame(main_frame)
    right.grid(row=0, column=1, sticky="nsew")

    ttk.Label(right, text="Details", font=("Arial", 16, "bold")).pack(pady=(0, 8))

    details = tk.Text(right, wrap="word", height=20, font=("Arial", 12))
    details.insert("1.0", "Wähle ein Rezept links, um Details anzuzeigen…")
    details.configure(state="disabled")  # робимо поле тільки для читання
    details.pack(fill="both", expand=True)

    # ---- Маленькі утиліти -------------------------------------------------

    def show_details(name: str):
        """Показуємо деталі рецепта справа."""
        data = all_recipes.get(name)
        details.configure(state="normal")
        details.delete("1.0", tk.END)

        if not data:
            details.insert("1.0", f"🍽️ {name}\n\n(noch keine Details)")
        else:
            zutaten = ", ".join(data.get("zutaten", []))
            zub = data.get("zubereitung", "")
            details.insert("1.0", f"🍽️ {name}\n\nZutaten: {zutaten}\n\nZubereitung:\n{zub}")

        details.configure(state="disabled")

    # ---- КНОПКИ (створюємо зараз, щоб мати на них посилання нижче) --------

    buttons = ttk.Frame(left)          # контейнер для кнопок (2x2)
    buttons.pack(padx=10, pady=15)
    buttons.columnconfigure(0, weight=1)
    buttons.columnconfigure(1, weight=1)

    grid_opts = {"padx": 10, "pady": 10}

    # Заглушки (тимчасово, справжні команди призначимо нижче, коли будуть функції)
    btn_add    = ttk.Button(buttons, text="Add Rezept")
    btn_edit   = ttk.Button(buttons, text="Rezept bearbeiten")
    btn_delete = ttk.Button(buttons, text="Rezept löschen")
    btn_exit   = ttk.Button(buttons, text="Beenden", command=root.destroy)

    btn_add.grid(row=0, column=0, **grid_opts)
    btn_edit.grid(row=0, column=1, **grid_opts)
    btn_delete.grid(row=1, column=0, **grid_opts)
    btn_exit.grid(row=1, column=1, **grid_opts)

    # --- Керування станом кнопок (enable/disable) --------------------------

    def update_buttons_state():                               # ← NEW
        """Вмикає/вимикає кнопки Edit/Delete залежно від виділення."""
        has_sel = bool(listbox.curselection())
        state = "normal" if has_sel else "disabled"
        btn_edit.configure(state=state)
        btn_delete.configure(state=state)

    # ---- Обробники UI -----------------------------------------------------

    def on_select(_evt=None):                                 # ← CHANGED
        """Коли користувач обрав елемент у списку."""
        sel = listbox.curselection()
        if not sel:
            update_buttons_state()
            return
        name = listbox.get(sel[0])
        show_details(name)
        update_buttons_state()

    listbox.bind("<<ListboxSelect>>", on_select)              # реагуємо на зміну вибору
    listbox.bind("<Double-1>", lambda e: f_edit_rezept())     # ← NEW: двоклік = редагувати
    root.bind("<Delete>", lambda e: f_delete_rezept())        # ← NEW: клавіша Delete = видалити

    # ---- Дії: додати / видалити / редагувати ------------------------------

    def f_add_rezept():
        """Додати новий рецепт (діалогове вікно)."""
        top = tk.Toplevel(root)
        top.title("Neues Rezept")
        top.geometry("300x250")

        ttk.Label(top, text="Rezeptname eingeben:").pack(pady=10)

        entry = ttk.Entry(top, width=30)
        entry.pack(pady=10)
        entry.focus_set()                                     # ← NEW: фокус одразу в поле
        top.bind("<Return>", lambda e: f_save_rezept())       # ← NEW: Enter = зберегти

        def f_save_rezept():
            name = entry.get().strip()
            if name:
                listbox.insert(tk.END, name)
                # створюємо пусті деталі, щоб можна було відразу редагувати
                all_recipes.setdefault(name, {"zutaten": [], "zubereitung": ""})

                # виділяємо щойно доданий елемент, прокручуємо до нього, показуємо деталі
                last = listbox.size() - 1                     # ← NEW
                listbox.selection_clear(0, tk.END)            # ← NEW
                listbox.selection_set(last)                   # ← NEW
                listbox.see(last)                             # ← NEW
                listbox.event_generate("<<ListboxSelect>>")   # ← NEW
                update_buttons_state()                        # ← NEW

            top.destroy()

        ttk.Button(top, text="Speichern", command=f_save_rezept).pack(pady=10)

    def f_delete_rezept():
        """Видалити обраний рецепт."""
        sel = listbox.curselection()
        if not sel:
            return

        name = listbox.get(sel[0])
        all_recipes.pop(name, None)                               # 1) прибираємо з dict

        idx = sel[0]
        listbox.delete(idx)                                   # 2) прибираємо зі списку

        # 3) підбираємо новий вибір або чистимо панель
        new_size = listbox.size()
        if new_size > 0:
            new_idx = min(idx, new_size - 1)                  # сусідній/останній
            listbox.selection_set(new_idx)
            listbox.see(new_idx)
            listbox.event_generate("<<ListboxSelect>>")
        else:
            details.configure(state="normal")
            details.delete("1.0", tk.END)
            details.insert("1.0", "Wähle ein Rezept links, um Details anzuzeigen…")
            details.configure(state="disabled")
            update_buttons_state()

    def f_edit_rezept():
        """Редагувати обраний рецепт (інгредієнти + інструкція)."""
        sel = listbox.curselection()
        if not sel:
            return

        name = listbox.get(sel[0])
        data = all_recipes.get(name, {"zutaten": [], "zubereitung": ""})

        top = tk.Toplevel(root)
        top.title(f"Rezept bearbeiten — {name}")
        top.geometry("420x360")

        ttk.Label(top, text="Zutaten (durch Kommata):").pack(pady=(12, 6))
        entry_zutaten = ttk.Entry(top, width=50)
        entry_zutaten.pack(pady=(0, 10))
        entry_zutaten.insert(0, ", ".join(data.get("zutaten", [])))

        ttk.Label(top, text="Zubereitung:").pack(pady=(10, 6))
        txt_zub = tk.Text(top, wrap="word", height=10)
        txt_zub.pack(fill="both", expand=True, padx=6, pady=(0, 10))
        txt_zub.insert("1.0", data.get("zubereitung", ""))

        def save_changes():
            raw = entry_zutaten.get().strip()
            zutaten_list = [z.strip() for z in raw.split(",") if z.strip()]
            zub_text = txt_zub.get("1.0", tk.END).strip()

            all_recipes[name] = {"zutaten": zutaten_list, "zubereitung": zub_text}

            # якщо цей рецепт обраний — перерисувати деталі
            cur = listbox.curselection()
            if cur and listbox.get(cur[0]) == name:
                show_details(name)

            update_buttons_state()                            # ← NEW
            top.destroy()

        ttk.Button(top, text="Speichern", command=save_changes).pack(pady=(0, 10))

    # призначаємо команди на кнопки (тепер функції вже визначені)
    btn_add.configure(command=f_add_rezept)
    btn_edit.configure(command=f_edit_rezept, state="disabled")   # ← NEW: стартово вимкнено
    btn_delete.configure(command=f_delete_rezept, state="disabled")# ← NEW: стартово вимкнено

    # --- Початковий вибір / початковий стан кнопок -------------------------
    if listbox.size() > 0:                                        # ← NEW
        listbox.selection_set(0)
        listbox.event_generate("<<ListboxSelect>>")
    else:
        update_buttons_state()

    root.mainloop()   # запуск головного циклу


if __name__ == "__main__":
    run_gui()