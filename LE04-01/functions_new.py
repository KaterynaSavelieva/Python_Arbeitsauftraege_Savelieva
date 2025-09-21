RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

NAME_MIN, NAME_MAX = 2, 20
INGREDIENT_MAX = 30

from tabulate import tabulate

def f_print_all_recipes(recipes):             # Parameter: recipes (zeigt z. B. auf all_recipes)
    f_print_title("📖👩‍🍳 Alle Rezepte:")
    table=[]
    for name, details in sorted(recipes.items()):     # Variable name = Schlüssel, details = Value
        #print(f"🍴 {name}")  # Rezeptname
        #print(f"   Zutaten: {', '.join(details['zutaten'])}")   # Variable details
        #print(f"   Zubereitung: {details['zubereitung']}\n")    # Variable details
        ingredients = ", ".join(details["zutaten"])
        instruction = details['zubereitung']
        table.append([name, ingredients, instruction])
    print(tabulate(table, headers=[BOLD +"Rezept", "Zutaten", "Zubereitung"+ RESET], tablefmt="fancy_grid"))
    f_wait_for_enter()

def f_show_menu()-> str:
    f_print_title("-- 🥗🥘🥞Menü 🥓🫘--")
    print("A - Alle Rezepte anzeigen 📖📖📖📖📖")
    print("B - Rezepte nach Zutaten finden🔎")
    print("C - Neues Rezept hinzufügen➕")
    print("D - Rezept löschen🫳🫳🫳")
    print("E - Rezepte speichern📘📘")
    print("F - Rezepte laden🙌")
    print("G - Rezepte bearbeiten✍️✍️")
    print("Q - Beenden🫡")
    return input ("Wählen Sie: ").strip().upper()

def f_input_ingredients() -> list[str]:
    while True:
        ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Kommata)\n")
        ingredients_list= [z.strip().title() for z in ingredients_input.split(",") if z.strip()]# direkt parsen: splitten, trimmen, Titelcase, leere Einträge filtern
        ok, msg = f_validate_ingredients_list(ingredients_list)# Validierung der Zutatenliste
        if ok:
            return ingredients_list
        print(f"Fehler: {msg}")

def f_match_ingredients(recipe: dict[str, dict], ingredients_list: list[str]) -> dict[str, dict]:
    match_ingredients: dict[str, dict] = {}
    for name, details in recipe.items():
        details_lower_case = [z.lower() for z in details['zutaten']]

        # Prüfen, ob alle gesuchten Zutaten im Rezept vorkommen
        if all (ingredient.lower() in details_lower_case for ingredient in ingredients_list):
            match_ingredients[name] = details
    return match_ingredients

def f_find_ingredients(all_recipes: dict) -> dict[str, dict]:
    f_print_title("Filtern nach vorhandenen Zutaten")
    ingredients_list=f_input_ingredients()
    matches=f_match_ingredients(all_recipes, ingredients_list)
    return matches

def f_recipe_change()-> str:
    print("1 - Hinzufügen von Zutaten")
    print("2 - Löschen von Zutaten")
    print("3 - Bearbeiten der Anleitung")
    print("4 - Änderung speichern")
    print("5 - Beenden")
    return input ("Wählen Sie: ").strip()

def f_add_ingredients(all_recipes, recipe_change) -> None:
    new_ingredients = f_input_ingredients()
    all_recipes[recipe_change]["zutaten"].extend(new_ingredients)
    print(f"Neue Zutaten wurden zu {recipe_change} hinzugefügt")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})

def f_find_recipe(all_recipes: dict) -> str|None:
    while True:
        recipe_change = input("Bitte geben der Name des Rezepts ein, das Sie bearbeiten möchten\n").strip().title()
        if recipe_change not in all_recipes:
            print("Rezept nicht gefunden")
            continue
        else:
            f_print_all_recipes({recipe_change: all_recipes[recipe_change]})
            return recipe_change

def f_change_instructions(all_recipes, recipe_change) -> None:
    new_instruction = input(f"Bitte geben Sie die neue Anleitung zum Rezept `{recipe_change}`\n`")
    all_recipes[recipe_change]["zubereitung"]=new_instruction
    print(f"Die Anleitung für das Rezept {recipe_change} wurde geändert!`")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})

def f_delete_ingredients(all_recipes:dict, recipe_change:str) -> None:
    new_ingredients = f_input_ingredients()
    delete = []
    not_found = []
    for ingredient in new_ingredients:
        if ingredient in all_recipes[recipe_change]["zutaten"]:
            all_recipes[recipe_change]["zutaten"].remove(ingredient)
            delete.append(ingredient)
        else:
            not_found.append(ingredient)
    if delete:
        print(f"Gelöscht: {','.join(delete)}")
    if not_found:
        print(f"Nicht gefunden: {','.join(not_found)}")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})
    #f_wait_for_enter()

def f_print_matches(matches: dict[str, dict]) -> None:
    if matches:
        print("\nGefundene Rezepte:\n")
        f_print_all_recipes(matches)
    else:
        print("Kein Rezept passt zu deiner Eingabe.")

def f_input_recipe_name(all_recipes: dict):
    while True:
        name = input("Bitte geben Sie den Name des Rezeptes ein: \n").strip().title()  # ohne Leerzeichen
        ok, msg = f_validate_recipe_name(name)
        if not ok:
            print(f"Fehler: {msg}")
            continue
        if name in all_recipes:
            print(f"Fehler: das Rezept {name} existiert bereits. Bitte wählen Sie einen anderen Namen.")
            continue
        return name

def f_input_recipe_instruction() -> str:
    instruction = input("Bitte geben Sie die Anleitung des Rezeptes ein: \n").strip()
    return instruction

def f_add_recipe(all_recipes: dict) -> None:
    name = f_input_recipe_name(all_recipes)
    ingredients_list = f_input_ingredients()
    instruction = f_input_recipe_instruction()

    all_recipes[name]={"zutaten": ingredients_list, "zubereitung": instruction}
    print(f"Rezept '{name}' wurde hinzugefügt und gespeichert.")
    f_save_recipes(all_recipes)
    f_wait_for_enter()

def f_delete_recipe(all_recipes: dict[str, dict]) -> None:
    name=input("Bitte geben Sie den Name des Rezeptes ein, das Sie löschen möchten: \n").strip().title()
    if name in all_recipes:
        del all_recipes[name]  # aus RAM löschen
        print(f"Das Rezept '{name}' wurde gelöscht.\n")
        f_save_changes(all_recipes)

#         save=input("Möchten Sie Änderung speichern? Y/N\n").strip().title()
#         if save == "Y":
#             if f_save_recipes(all_recipes):#, delete= [name]
# #f_save_recipes(...) gibt True zurück, wenn das Speichern ohne Fehler geklappt hat.
# # (z. B. Datei gesperrt, kein Speicherplatz, kaputte JSON-Datei) -False=
#                 print(f"Rezept {name} wurde gelöscht und gespeichert")
#             else:
#                 print("Änderung wurde noch nicht gespeichert")
    else:
        print(f"Kein Rezept mit dem Namen '{name}' gefunden.")

def f_save_changes(all_recipes: dict[str, dict]) -> None:
    save = input("Möchten Sie Änderung speichern? Y/N\n").strip().title()
    if save == "Y":
        if f_save_recipes(all_recipes):  # , delete= [name]
            # f_save_recipes(...) gibt True zurück, wenn das Speichern ohne Fehler geklappt hat.
            # (z. B. Datei gesperrt, kein Speicherplatz, kaputte JSON-Datei) -False=
            print(f"Änderung wurde gespeichert")
    else:
        print("Änderung wurde noch nicht gespeichert")


def f_check_length(value: str, min_len: int, max_len: int) -> tuple[bool, str]:
    if not (min_len <= len(value) <= max_len):
        return False, f"„{value}“ muss zwischen {min_len} und {max_len} Zeichen lang sein."
    return True, ""

def f_check_only_letters(value: str) -> tuple[bool, str]:
    if not value.replace(" ", "").isalpha():
        return False, f"„{value}“ darf nur Buchstaben und Leerzeichen enthalten."
    return True, ""

def f_check_letters_and_digits(value: str) -> tuple[bool, str]:
    if not value.replace(" ", "").isalnum():
        return False, f"„{value}“ darf nur Buchstaben, Ziffern und Leerzeichen enthalten."
    return True, ""

def f_validate_recipe_name(name: str) -> tuple[bool, str]:
    ok, msg = f_check_length(name, NAME_MIN, NAME_MAX)
    if not ok:
        return False, "Rezeptname: " + msg
    # Rezeptname: nur Buchstaben + Leerzeichen
    ok, msg = f_check_only_letters(name)
    if not ok:
        return False, "Rezeptname: " + msg

    return True, ""

def f_validate_ingredients_list(ingredients_list: list[str]) -> tuple[bool, str]:
    # Leere Eingabe (auch nur Kommas) wird hier erkannt
    if not ingredients_list:
        return False, "Die Zutatenliste darf nicht leer sein."

    for z in ingredients_list:
        ok, msg = f_check_length(z, NAME_MIN, INGREDIENT_MAX)
        if not ok:
            return False, "Zutat: " + msg
        # Zutaten: Buchstaben + Ziffern + Leerzeichen erlaubt
        ok, msg = f_check_letters_and_digits(z)
        if not ok:
            return False, "Zutat: " + msg
    return True, ""

import json
# Funktion zum Speichern von Rezepten in eine JSON-Datei
# all_recipes:  komplettes Dictionary mit allen Rezepten im RAM
# subset:       optionales Dictionary mit nur einem/mehreren Rezepten, die gespeichert werden sollen
# Rückgabe: True = erfolgreich gespeichert, False = Fehler
def f_save_recipes(all_recipes: dict, subset: dict  | None=None, delete: list[str]| None=None ) -> bool:
    #Speichert alle Rezepte in der Datei rezepte.json.
    try:
        to_save =dict(all_recipes)
        # Falls nur bestimmte Rezepte gespeichert werden sollen
        if subset: # Nur die übergebenen Rezepte speichern. Zuerst die bestehende Datei öffnen und laden
            to_save.update(subset)             # überschreibt gleiche Keys oder fügt neue hinzu
        # Falls Rezepte gelöscht werden sollen
        if delete:
            for name in delete:
                to_save.pop(name, None)
        # Speichern
        with open("rezepte.json", "w", encoding="utf-8") as f:
            # Dictionary all_recipes in JSON-Datei schreiben
            json.dump(to_save, f, ensure_ascii=False, indent=2)# hübsch formatiert, Umlaute lesbar
        return True
    except Exception as e:
        # Allgemeiner Fehler beim Speichern
        print(f"Fehler beim Speichern: {e}")
        return False

# Funktion zum Laden der Rezepte aus einer JSON-Datei
def f_load_recipes(all_recipes: dict) -> dict:
   #Lädt Rezepte aus rezepte.json und gibt das aktualisierte Dictionary zurück.
    try:
        # Datei im Lesemodus ("r") öffnen
        with open("rezepte.json", "r", encoding="utf-8") as f:
            # Inhalt der Datei als Dictionary laden
            data = json.load(f)
            # Neue Rezepte zu bestehendem Dictionary hinzufügen
            all_recipes.update(data)
            print("\nRezepte wurden erfolgreich geladen (Datei: rezepte.json).")
    except FileNotFoundError:
        # Wenn Datei nicht existiert
        print("Fehler: Die Datei rezepte.json wurde nicht gefunden.")
    except json.JSONDecodeError:
        # Wenn Datei leer oder beschädigt ist
        print("Fehler: Die Datei rezepte.json ist beschädigt oder leer.")
    f_wait_for_enter()
    return all_recipes

def f_edit_recipe(all_recipes:dict)->None:
    print("Rezepte bearbeiten!")
    recipe_change = f_find_recipe(all_recipes)
    if recipe_change:
        while True:
            user_change_choice = f_recipe_change()
            match user_change_choice:
                case "1":
                    f_add_ingredients(all_recipes, recipe_change)
                case "2":
                    f_delete_ingredients(all_recipes, recipe_change)
                case "3":
                    f_change_instructions(all_recipes, recipe_change)
                case "4":
                    if f_save_recipes(all_recipes, {recipe_change: all_recipes[recipe_change]}):
                        print(f"Rezept {recipe_change} wurde gespeichert.")
                case "5":
                    print("Auf Wiedersehen!")
                    break
    f_wait_for_enter()

def f_wait_for_enter() -> None:
    input("\nDrücken Sie ENTER, um fortzufahren...\n")

def f_print_title(text: str) -> None:
    breit =70
    print(f"{YELLOW}\n{'='*breit}{RESET}")
    print(BOLD+BLUE+text.center(breit)+RESET)
    print(f"{YELLOW}{'='*breit}{RESET}")



# --- GUI-friendly wrappers (нічого не друкують, не чекають ENTER) ---

def f_load_recipes_silent(all_recipes: dict) -> bool:
    """Як f_load_recipes, але без print і без очікування ENTER."""
    import json
    try:
        with open("rezepte.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            all_recipes.update(data)
        return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

def f_save_recipes_silent(all_recipes: dict) -> bool:
    """Як f_save_recipes, але точно без друку."""
    try:
        with open("rezepte.json", "w", encoding="utf-8") as f:
            import json
            json.dump(all_recipes, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False