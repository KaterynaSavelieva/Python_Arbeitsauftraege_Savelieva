import json
import tkinter as tk
from tkinter import ttk, messagebox

import functions_new as f          # валідатори + робота з JSON
from data import all_recipes       # початкові рецепти в RAM


# --------- тихі обгортки для файлу -----------------------------------------
def _load_recipes_into(target: dict) -> bool:
    """Тихо підвантажити rezepte.json у target (без принтів/пауz)."""
    if hasattr(f, "f_load_recipes_silent"):
        return bool(f.f_load_recipes_silent(target))
    try:
        with open("rezepte.json", "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            target.update(data)
            return True
        return False
    except Exception:
        return False


def _save_recipes_from(source: dict) -> bool:
    """Тихо зберегти source у rezepte.json (True/False)."""
    if hasattr(f, "f_save_recipes_silent"):
        return bool(f.f_save_recipes_silent(source))
    return bool(f.f_save_recipes(source))


# ============================== GUI ========================================
def run_gui():
    root = tk.Tk()
    root.title("Rezepte")
    root.geometry("1000x600")

    # каркас 2 колонки у пропорції 2:3
    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)
    main.columnconfigure(0, weight=2, uniform="col")
    main.columnconfigure(1, weight=3, uniform="col")
    main.rowconfigure(0, weight=1)

    # ---------------- ЛІВО --------------------------------------------------
    left = ttk.Frame(main)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    left.rowconfigure(2, weight=1)       # рядок зі списком — тягнеться
    left.columnconfigure(0, weight=1)

    ttk.Label(left, text="Rezepte", font=("Arial", 16, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )

    # панель фільтра
    filter_bar = ttk.Frame(left)
    filter_bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    filter_bar.columnconfigure(1, weight=1)

    mode_var = tk.StringVar(value="name")
    rb_name = ttk.Radiobutton(filter_bar, text="Name", value="name", variable=mode_var)
    rb_zut  = ttk.Radiobutton(filter_bar, text="Zutaten", value="zutaten", variable=mode_var)
    rb_name.grid(row=0, column=0, sticky="w")
    rb_zut.grid(row=0, column=1, sticky="w", padx=(10, 0))

    query_var = tk.StringVar()
    entry = ttk.Entry(filter_bar, textvariable=query_var)     # поле пошуку
    entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    btn_filter = ttk.Button(filter_bar, text="Filtern")       # кнопка фільтру
    btn_all    = ttk.Button(filter_bar, text="Alle")          # показати все
    btn_filter.grid(row=1, column=2, padx=(8, 0))
    btn_all.grid(row=1, column=3, padx=(6, 0))

    # список рецептів
    listbox = tk.Listbox(left, font=("Arial", 12, "italic"))
    listbox.grid(row=2, column=0, sticky="nsew")

    # статус під списком
    status_var = tk.StringVar(value="")
    ttk.Label(left, textvariable=status_var).grid(row=3, column=0, sticky="ew", pady=(6, 0))

    # блок кнопок
    buttons = ttk.Frame(left)
    buttons.grid(row=4, column=0, pady=(10, 0), sticky="ew")
    for c in (0, 1):
        buttons.columnconfigure(c, weight=1)

    btn_opts = {"width": 20}                        # однакова ширина кнопок
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

    # ---------------- ПРАВО -------------------------------------------------
    right = ttk.Frame(main)
    right.grid(row=0, column=1, sticky="nsew")
    ttk.Label(right, text="Details", font=("Arial", 16, "bold")).pack(anchor="w")
    details = tk.Text(right, wrap="word", font=("Arial", 12), state="disabled")
    details.pack(fill="both", expand=True, pady=(6, 0))

    # ---------------- Дані у список ----------------------------------------
    _load_recipes_into(all_recipes)

    def f_all_names_sorted():
        """
        Допоміжна функція.
        Повертає всі назви рецептів (ключі словника all_recipes),
        відсортовані у алфавітному порядку (без врахування регістру).
        Використовується, щоб список рецептів у вікні завжди був охайно відсортований.
        """
        # str.casefold()— кращий за lower() для алфавітів із умлаутами тощо
        return sorted(all_recipes.keys(), key=str.casefold)

    def f_refresh_list(names):
        """Оновлює список рецептів у Listbox зліва + рядок статусу."""
        listbox.delete(0, tk.END)
        for n in names:
            listbox.insert(tk.END, n)
        status_var.set(f"Angezeigt: {len(names)} von {len(all_recipes)}")

    # Виклик на старті: показати всі рецепти (відсортовані по алфавіту)
    f_refresh_list(f_all_names_sorted())

    # ---------------- Утиліти ----------------------------------------------
    def f_update_buttons_state():
        # Ця функція робить кнопки активними лише тоді, коли в списку рецептів щось вибрано.
        there_is_selection = bool(listbox.curselection())
        new_state = "normal" if there_is_selection else "disabled"
        btn_edit.configure(state=new_state)
        btn_delete.configure(state=new_state)

    def f_show_details(name):
        """Заповнює праву панель деталями обраного рецепта."""
        data = all_recipes.get(name)
        details.configure(state="normal")
        details.delete("1.0", tk.END)

        if not data:
            details.insert("1.0", f"🍽 {name}\n\n(noch keine Details)")
        else:
            ingredients = ", ".join(data.get("zutaten", []))
            instruction = data.get("zubereitung", "")
            details.insert("1.0", f"{name}\n\nZutaten: {ingredients}\n\nZubereitung:\n{instruction}")

        details.configure(state="disabled")

    # ---------------- Обробник єдиної потрібної події ----------------------
    def f_on_select(_event=None):
        """Користувач вибрав елемент у Listbox."""
        selected_indices = listbox.curselection()
        if not selected_indices:
            f_update_buttons_state()
            return
        selected_index = selected_indices[0]          # одинарний вибір
        selected_recipe_name = listbox.get(selected_index)
        f_show_details(selected_recipe_name)
        f_update_buttons_state()

    # лише вибір у списку (без Double-Click і без Delete-клавіші)
    listbox.bind("<<ListboxSelect>>", f_on_select)

    # ---------------- Команди кнопок ---------------------------------------
    def f_do_filter(_event=None):
        """Застосувати фільтр за назвою або списком інгредієнтів."""
        query = query_var.get().strip()
        mode = mode_var.get()
        names = f_all_names_sorted()

        if not query:
            f_refresh_list(names)
            if listbox.size():
                listbox.selection_set(0)
                f_on_select()
            return

        if mode == "name":
            ql = query.lower()
            filtered = [n for n in names if ql in n.lower()]
        else:
            # по інгредієнтах: усі введені мають бути в рецепті
            wanted = [z.strip().lower() for z in query.split(",") if z.strip()]
            if not wanted:
                f_refresh_list(names)
                if listbox.size():
                    listbox.selection_set(0)
                    f_on_select()
                return

            def f_has_all(nm):
                det = all_recipes.get(nm, {})
                zlist = [z.lower() for z in det.get("zutaten", [])]
                return all(w in zlist for w in wanted)

            filtered = [n for n in names if f_has_all(n)]

        f_refresh_list(filtered)
        if listbox.size():
            listbox.selection_set(0)
            f_on_select()

    def f_show_all():
        """Скинути фільтр і показати всі рецепти."""
        query_var.set("")
        f_refresh_list(f_all_names_sorted())
        if listbox.size():
            listbox.selection_set(0)
            f_on_select()

    def f_add_rezept():
        """Додати новий порожній рецепт (тільки назву)."""
        top = tk.Toplevel(root)
        top.title("Neues Rezept")
        top.geometry("320x220")

        ttk.Label(top, text="Rezeptname eingeben:").pack(pady=10)
        entry_name = ttk.Entry(top, width=30)
        entry_name.pack(pady=10)
        entry_name.focus_set()

        def f_save_new():
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
            if not _save_recipes_from(all_recipes):
                messagebox.showerror("Fehler", "Speichern fehlgeschlagen.")
            f_show_all()

            # виділити новий елемент
            for i in range(listbox.size()):
                if listbox.get(i) == name:
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(i)
                    listbox.see(i)
                    f_on_select()
                    break
            top.destroy()

        ttk.Button(top, text="Speichern", command=f_save_new).pack(pady=10)

    def f_delete_rezept():
        """Видалити вибраний рецепт."""
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        # if not messagebox.askyesno("Löschen", f"„{name}“ wirklich löschen?"): return
        all_recipes.pop(name, None)
        if not _save_recipes_from(all_recipes):
            messagebox.showerror("Fehler", "Speichern fehlgeschlagen.")
        f_do_filter()   # оновити список відповідно до активного фільтру

    def f_edit_rezept():
        """Діалог редагування інгредієнтів і інструкції (без скролів і стрілок)."""
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        data = all_recipes.get(name, {"zutaten": [], "zubereitung": ""})

        top = tk.Toplevel(root)
        top.title(f"Rezept bearbeiten — {name}")
        top.geometry("900x520")

        # простий двоколонковий макет
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=2)
        top.rowconfigure(1, weight=1)

        ttk.Label(top, text="Zutaten:").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        ttk.Label(top, text="Zubereitung:").grid(row=0, column=1, sticky="w", padx=8, pady=(8, 4))

        # інгредієнти —
        ing_wrap = ttk.Frame(top)
        ing_wrap.grid(row=1, column=0, sticky="nsew", padx=8)
        ing_wrap.rowconfigure(0, weight=1)
        ing_wrap.columnconfigure(0, weight=1)

        lb_ing = tk.Listbox(ing_wrap, font=("Arial", 11))
        lb_ing.grid(row=0, column=0, sticky="nsew")

        for z in data.get("zutaten", []):
            lb_ing.insert(tk.END, z)

        # додавання / видалення
        row2 = ttk.Frame(ing_wrap)
        row2.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        row2.columnconfigure(0, weight=1)

        new_var = tk.StringVar()
        ent_new = ttk.Entry(row2, textvariable=new_var, width=20)
        ent_new.grid(row=0, column=0, sticky="ew")

        btn_add_ing  = ttk.Button(row2, text="Hinzufügen")
        btn_del_sel  = ttk.Button(row2, text="Ausgewählte löschen")
        btn_add_ing.grid(row=0, column=1, padx=(8, 0))
        btn_del_sel.grid(row=1, column=0, sticky="w", pady=(6, 0))

        def f_do_add_ing():
            """Додати один інгредієнт із поля нижче списку."""
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

        def f_do_del_selected():
            """Видалити всі виділені інгредієнти зі списку."""
            for i in reversed(lb_ing.curselection()):
                lb_ing.delete(i)

        btn_add_ing.configure(command=f_do_add_ing)
        btn_del_sel.configure(command=f_do_del_selected)
        ent_new.bind("<Return>", lambda _e=None: f_do_add_ing())  # Enter додає (ця bind не обов'язкова)

        # інструкція
        txt_zub = tk.Text(top, wrap="word", font=("Arial", 11))
        txt_zub.grid(row=1, column=1, sticky="nsew", padx=(0, 8))
        txt_zub.insert("1.0", data.get("zubereitung", ""))

        # низ діалогу
        bar = ttk.Frame(top)
        bar.grid(row=2, column=0, columnspan=2, pady=10)
        btn_cancel = ttk.Button(bar, text="Abbrechen", command=top.destroy)
        btn_save   = ttk.Button(bar, text="Speichern")
        btn_cancel.pack(side="right", padx=6)
        btn_save.pack(side="right")

        def f_save_changes():
            """Зібрати дані з віджетів, провалідувати та зберегти."""
            zutaten_list = [lb_ing.get(i) for i in range(lb_ing.size())]
            zub_text = txt_zub.get("1.0", tk.END).strip()

            ok, msg = f.f_validate_ingredients_list(zutaten_list)
            if not ok:
                messagebox.showwarning("Ungültige Zutaten", msg, parent=top)
                return

            all_recipes[name] = {"zutaten": zutaten_list, "zubereitung": zub_text}
            if not _save_recipes_from(all_recipes):
                messagebox.showerror("Fehler", "Speichern fehlgeschlagen.", parent=top)
                return

            # якщо цей рецепт обраний — оновити панель деталей
            cur = listbox.curselection()
            if cur and listbox.get(cur[0]) == name:
                f_show_details(name)
            top.destroy()

        btn_save.configure(command=f_save_changes)

    def f_reload():
        """Перечитати rezepte.json і перебудувати список згідно фільтру."""
        all_recipes.clear()
        _load_recipes_into(all_recipes)
        f_do_filter()

    def f_exit():
        """Закрити програму."""
        root.destroy()

    # прив’язки кнопок
    btn_filter.configure(command=f_do_filter)
    btn_all.configure(command=f_show_all)
    btn_add.configure(command=f_add_rezept)
    btn_edit.configure(command=f_edit_rezept, state="disabled")
    btn_delete.configure(command=f_delete_rezept, state="disabled")
    btn_reload.configure(command=f_reload)
    btn_exit.configure(command=f_exit)
    entry.bind("<Return>", f_do_filter)   # Enter у полі пошуку

    # старт: виділити перший елемент або просто оновити стан кнопок
    if listbox.size():
        listbox.selection_set(0)
        f_on_select()
    else:
        f_update_buttons_state()

    root.mainloop()


if __name__ == "__main__":
    run_gui()
