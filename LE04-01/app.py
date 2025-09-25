import tkinter as tk
from tkinter import ttk, messagebox

import functions_new as f
from data import all_recipes


# --------- прості "тихі" обгортки ------------------------------------------
def f_load_all_recipes():
    return f.f_load_recipes_silent(all_recipes)

def f_save_all_recipe():
    return f.f_save_recipes_silent(all_recipes)


# ============================== GUI =========================================
def run_gui():
    root = tk.Tk()
    root.title("Rezepte-Manager")
    root.geometry("900x520")

    # ---------------- каркас -------------------------------------------------
    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)
    main.columnconfigure(0, weight=2, uniform="col")
    main.columnconfigure(1, weight=3, uniform="col")
    main.rowconfigure(0, weight=1)

    # ---------------- ЛІВО ---------------------------------------------------
    left = ttk.Frame(main)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    left.columnconfigure(0, weight=1)
    left.rowconfigure(3, weight=1)  # рядок зі списком — тягнеться

    ttk.Label(left, text="Rezepte", font=("Arial", 16, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )

    # панель фільтра
    filter_bar = ttk.Frame(left)
    filter_bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    filter_bar.columnconfigure(1, weight=1)

    mode_var = tk.StringVar(value="name")
    ttk.Radiobutton(filter_bar, text="Name", value="name", variable=mode_var)\
        .grid(row=0, column=0, sticky="w")
    ttk.Radiobutton(filter_bar, text="Zutaten", value="zutaten", variable=mode_var)\
        .grid(row=0, column=1, sticky="w", padx=(10, 0))

    query_var = tk.StringVar()
    entry = ttk.Entry(filter_bar, textvariable=query_var)
    entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    btn_filter = ttk.Button(filter_bar, text="Filtern")
    btn_all    = ttk.Button(filter_bar, text="Alle")
    btn_filter.grid(row=1, column=2, padx=(8, 0))
    btn_all.grid(row=1, column=3, padx=(6, 0))

    # список рецептів + скролбар
    list_wrap = ttk.Frame(left)
    list_wrap.grid(row=3, column=0, sticky="nsew")
    list_wrap.columnconfigure(0, weight=1)
    list_wrap.rowconfigure(0, weight=1)

    listbox = tk.Listbox(list_wrap, font=("Arial", 10, "italic"))
    listbox.grid(row=0, column=0, sticky="nsew")

    sb = ttk.Scrollbar(list_wrap, orient="vertical", command=listbox.yview)
    sb.grid(row=0, column=1, sticky="ns")
    listbox.configure(yscrollcommand=sb.set)

    # статус під списком
    status_var = tk.StringVar(value="")
    ttk.Label(left, textvariable=status_var)\
        .grid(row=4, column=0, sticky="ew", pady=(6, 0))

    # блок кнопок
    buttons = ttk.Frame(left)
    buttons.grid(row=5, column=0, pady=(10, 0), sticky="ew")
    for c in (0, 1):
        buttons.columnconfigure(c, weight=1)

    btn_opts = {"width": 20}
    grid_opts = {"padx": 6, "pady": 6, "sticky": "ew"}

    btn_add    = ttk.Button(buttons, text="Add Rezept", **btn_opts)
    btn_edit   = ttk.Button(buttons, text="Rezept bearbeiten", **btn_opts)
    btn_delete = ttk.Button(buttons, text="Rezept löschen", **btn_opts)
    btn_reload = ttk.Button(buttons, text="Reload", **btn_opts)
    btn_exit   = ttk.Button(buttons, text="Beenden", **btn_opts)

    btn_add.grid(   row=0, column=0, **grid_opts)
    btn_edit.grid(  row=0, column=1, **grid_opts)
    btn_delete.grid(row=1, column=0, **grid_opts)
    btn_reload.grid(row=1, column=1, **grid_opts)
    btn_exit.grid(  row=2, column=0, columnspan=2, **grid_opts)

    # ---------------- ПРАВО --------------------------------------------------
    right = ttk.Frame(main)
    right.grid(row=0, column=1, sticky="nsew")

    ttk.Label(right, text="Details", font=("Arial", 16, "bold")).pack(anchor="w")

    text_wrap = ttk.Frame(right)
    text_wrap.pack(fill="both", expand=True, pady=(6, 0))
    details = tk.Text(text_wrap, wrap="word", font=("Arial", 10), state="disabled")
    details.pack(side="left", fill="both", expand=True)
    sb2 = ttk.Scrollbar(text_wrap, orient="vertical", command=details.yview)
    sb2.pack(side="right", fill="y")
    details.configure(yscrollcommand=sb2.set)

    # ---------------- Дані ---------------------------------------------------
    f_load_all_recipes()

    # === УТИЛІТИ (дуже прості) =============================================

    def all_names_sorted():
        # casefold — щоб сортування з умлаутами виглядало правильно
        return sorted(all_recipes.keys(), key=str.casefold)

    def get_selected_name():
        sel = listbox.curselection()
        return listbox.get(sel[0]) if sel else None

    def show_details(name: str | None):
        details.configure(state="normal")
        details.delete("1.0", tk.END)
        if not name:
            details.insert("1.0", "(kein Rezept ausgewählt)")
        else:
            data = all_recipes.get(name)
            if not data:
                details.insert("1.0", f"🍽 {name}\n\n(noch keine Details)")
            else:
                ingredients = ", ".join(data.get("zutaten", []))
                instruction = data.get("zubereitung", "")
                details.insert("1.0", f"{name}\n\nZutaten: {ingredients}\n\nZubereitung:\n{instruction}")
        details.configure(state="disabled")

    def redraw_list(names: list[str], select_first: bool = True):
        listbox.delete(0, tk.END)
        for n in names:
            listbox.insert(tk.END, n)
        status_var.set(f"Angezeigt: {len(names)} von {len(all_recipes)}")
        if select_first and names:
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(0)
            listbox.see(0)
            show_details(names[0])
        elif not names:
            show_details(None)

    # стартовий список
    redraw_list(all_names_sorted(), select_first=True)

    # === ОБРОБНИКИ ДІЙ ======================================================

    def on_list_select(_e=None):
        show_details(get_selected_name())

    listbox.bind("<<ListboxSelect>>", on_list_select)

    def f_do_filter(_e=None):
        # 1) якщо порожній запит — показати всі
        query = query_var.get().strip()
        names = all_names_sorted()
        if not query:
            redraw_list(names)
            return

        # 2) фільтр за режимом
        if mode_var.get() == "name":
            q = query.casefold()
            filtered = [n for n in names if q in n.casefold()]
            redraw_list(filtered)
            return

        # 3) фільтр за інгредієнтами: усі введені повинні бути в рецепті
        wanted = [z.strip().casefold() for z in query.split(",") if z.strip()]
        if not wanted:
            redraw_list(names)
            return

        filtered = []
        for n in names:
            zlist = [z.casefold() for z in all_recipes.get(n, {}).get("zutaten", [])]
            if all(w in zlist for w in wanted):
                filtered.append(n)

        redraw_list(filtered)

    def f_show_all():
        query_var.set("")
        redraw_list(all_names_sorted())

    def f_add_rezept():
        top = tk.Toplevel(root)
        top.title("Neues Rezept")
        top.geometry("320x200")

        ttk.Label(top, text="Rezeptname eingeben:").pack(pady=10)
        entry_name = ttk.Entry(top, width=30)
        entry_name.pack()
        entry_name.focus_set()

        def _save():
            name = entry_name.get().strip().title()
            if not name:
                top.destroy()
                return
            ok, msg = f.f_validate_recipe_name(name)
            if not ok:
                messagebox.showwarning("Ungültiger Name", msg, parent=top)
                return
            if name in all_recipes:
                messagebox.showinfo("Hinweis", f"„{name}“ existiert bereits.", parent=top)
                return

            all_recipes[name] = {"zutaten": [], "zubereitung": ""}
            if not f_save_all_recipe():
                messagebox.showerror("Fehler", "Speichern fehlgeschlagen.", parent=top)
                return

            # оновити список і виділити новий елемент
            names = all_names_sorted()
            redraw_list(names, select_first=False)
            for i in range(listbox.size()):
                if listbox.get(i) == name:
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(i)
                    listbox.see(i)
                    show_details(name)
                    break
            top.destroy()

        ttk.Button(top, text="Speichern", command=_save).pack(pady=12)

    def f_delete_rezept():
        name = get_selected_name()
        if not name:
            return
        if not messagebox.askyesno("Löschen", f"„{name}“ wirklich löschen?"):
            return
        all_recipes.pop(name, None)
        if not f_save_all_recipe():
            messagebox.showerror("Fehler", "Speichern fehlgeschlagen.")
        # залишаємо активний фільтр
        f_do_filter()

    def f_edit_rezept():
        name = get_selected_name()
        if not name:
            return
        data = all_recipes.get(name, {"zutaten": [], "zubereitung": ""})

        top = tk.Toplevel(root)
        top.title(f"Rezept bearbeiten — {name}")
        top.geometry("900x520")
        top.columnconfigure(0, weight=1, uniform="col")
        top.columnconfigure(1, weight=2, uniform="col")
        top.rowconfigure(1, weight=1)

        ttk.Label(top, text="Zutaten:").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        ttk.Label(top, text="Zubereitung:").grid(row=0, column=1, sticky="w", padx=8, pady=(8, 4))

        # Інгредієнти
        ing_wrap = ttk.Frame(top)
        ing_wrap.grid(row=1, column=0, sticky="nsew", padx=8)
        ing_wrap.columnconfigure(0, weight=1)
        ing_wrap.rowconfigure(0, weight=1)

        lb_ing = tk.Listbox(ing_wrap, font=("Arial", 11), selectmode="extended")
        lb_ing.grid(row=0, column=0, sticky="nsew")

        for z in data.get("zutaten", []):
            lb_ing.insert(tk.END, z)

        row2 = ttk.Frame(ing_wrap)
        row2.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        row2.columnconfigure(0, weight=1)

        new_var = tk.StringVar()
        ent_new = ttk.Entry(row2, textvariable=new_var)
        ent_new.grid(row=0, column=0, sticky="ew")

        def _add_ing(_e=None):
            txt = new_var.get().strip().title()
            if not txt:
                return
            ok, msg = f.f_validate_ingredients_list([txt])
            if not ok:
                messagebox.showwarning("Ungültige Zutat", msg, parent=top)
                return
            current = [lb_ing.get(i) for i in range(lb_ing.size())]
            if txt in current:
                return
            lb_ing.insert(tk.END, txt)
            new_var.set("")
            lb_ing.see(tk.END)

        def _del_ing():
            for i in reversed(lb_ing.curselection()):
                lb_ing.delete(i)

        ttk.Button(row2, text="Hinzufügen", command=_add_ing).grid(row=0, column=1, padx=(8, 0))
        ttk.Button(row2, text="Ausgewählte löschen", command=_del_ing)\
            .grid(row=1, column=0, sticky="w", pady=(6, 0))
        ent_new.bind("<Return>", _add_ing)

        # Інструкція
        txt_zub = tk.Text(top, wrap="word", font=("Arial", 11))
        txt_zub.grid(row=1, column=1, sticky="nsew", padx=(0, 8))
        txt_zub.insert("1.0", data.get("zubereitung", ""))

        # Кнопки низу
        bar = ttk.Frame(top)
        bar.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(bar, text="Abbrechen", command=top.destroy).pack(side="right", padx=6)

        def _save_changes():
            ingredients = [lb_ing.get(i) for i in range(lb_ing.size())]
            instruction = txt_zub.get("1.0", tk.END).strip()

            ok, msg = f.f_validate_ingredients_list(ingredients)
            if not ok:
                messagebox.showwarning("Ungültige Zutaten", msg, parent=top)
                return

            all_recipes[name] = {"zutaten": ingredients, "zubereitung": instruction}
            if not f_save_all_recipe():
                messagebox.showerror("Fehler", "Speichern fehlgeschlagen.", parent=top)
                return

            # якщо саме цей рецепт обраний — оновити праву панель
            cur = get_selected_name()
            if cur == name:
                show_details(name)
            top.destroy()

        ttk.Button(bar, text="Speichern", command=_save_changes).pack(side="right")

    def f_reload():
        # перечитати файл і перерахувати список зі збереженим фільтром
        all_recipes.clear()
        f_load_all_recipes()
        f_do_filter()

    def f_exit():
        root.destroy()

    # прив’язки
    btn_filter.configure(command=f_do_filter)
    btn_all.configure(command=f_show_all)
    btn_add.configure(command=f_add_rezept)
    btn_edit.configure(command=f_edit_rezept)
    btn_delete.configure(command=f_delete_rezept)
    btn_reload.configure(command=f_reload)
    btn_exit.configure(command=f_exit)
    entry.bind("<Return>", f_do_filter)

    # корисні гарячі клавіші (простий UX)
    root.bind("<Escape>", lambda e: f_exit())
    root.bind("<Control-f>", lambda e: entry.focus_set())
    root.bind("<Delete>", lambda e: f_delete_rezept())

    root.mainloop()


if __name__ == "__main__":
    run_gui()
