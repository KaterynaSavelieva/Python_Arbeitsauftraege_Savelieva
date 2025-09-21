from functions_new import*
f_print_title("Herzlich Willkommen beim Rezepte-Manager der Welt!")
from data  import *


all_recipes = f_load_recipes(all_recipes)
# --- Hauptprogramm ---
while True:
    user_choice = f_show_menu()
    match user_choice.strip().upper():
        case "A":
            f_print_all_recipes(all_recipes)
        case "B":
            matches=f_find_ingredients(all_recipes)
            f_print_matches(matches)
        case "C":
            f_add_recipe(all_recipes)
        case "D":
            f_delete_recipe(all_recipes)
        case "E":
            if f_save_recipes(all_recipes):
                print("Rezepte wurden erfolgreich gespeichert (Datei: rezepte.json).")
            f_wait_for_enter()
        case "F":
            all_recipes = f_load_recipes(all_recipes)
        case "G":
            f_edit_recipe(all_recipes)
        case "Q":
            f_save_changes(all_recipes)
            print("Auf Wiedersehen!")
            break
        case _:
            print("Ungültige Eingabe. Bitte A, B, C, D, E, F, G oder Q wählen.")
            f_wait_for_enter()