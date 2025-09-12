print("Herzlich Willkommen beim Rezepte-Manager der Welt!")
from functions_new import*

# Dictionary mit allen Rezepten  →  Variable (global)
all_recipes = {
    "Pizza": {
        "zutaten": ["Mehl", "eier", "Teig", "Tomatensauce", "Käse"],
        "zubereitung": "Die Zutaten auf den Teig legen und im Ofen backen."
    },
    "Salat": {
        "zutaten": ["Tomaten", "Gurken", "Olivenöl"],
        "zubereitung": "Alles klein schneiden und mit Olivenöl mischen."
    },
    "Pfannkuchen": {
        "zutaten": ["Mehl", "Milch", "Eier"],
        "zubereitung": "Teig anrühren und in einer Pfanne ausbacken."
    }
}

all_recipes = f_load_recipes(all_recipes)
# --- Hauptprogramm ---
while True:
    user_choice = f_show_menu()
    match user_choice.upper():
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
            f_save_recipes(all_recipes)
        case "F":
            all_recipes = f_load_recipes(all_recipes)
        case "G":
            print("Rezept bearbeiten!")
            recipe_change=f_find_recipe(all_recipes)
            if recipe_change:
                while True:
                    user_change_choice = f_recipe_change()
                    match user_change_choice:
                        case "1":
                            print("1 - Hinzufügen von Zutaten")
                        case "2":
                            print("2 - Löschen von Zutaten")
                        case "3":
                            print("3 - Bearbeiten der Anleitung")
                        case "4":
                            print("4 - Beenden")
                            break
        case "Q":
            print("Auf Wiedersehen!!")
            break
        case _:
            print("Ungültige Eingabe. Bitte A, B oder Q wählen.")