print("\nHerzlich Willkommen beim Rezepte-Manager der Welt!")
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
    match user_choice.strip().upper():
        case "A":
            print("\n📖👩‍🍳 Alle Rezepte:\n")
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
        case "F":
            all_recipes = f_load_recipes(all_recipes)
        case "G":
            f_edit_recipe(all_recipes)
        case "Q":
            print("Auf Wiedersehen!!")
            break
        case _:
            print("Ungültige Eingabe. Bitte A, B, C, D, E, F, G oder Q wählen.")