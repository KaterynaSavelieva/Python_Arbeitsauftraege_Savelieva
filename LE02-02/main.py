print("Herzlich Willkommen beim Rezepte-Manager der Welt!")

from functions import*
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
# --- Hauptprogramm ---
while True:
    user_choice = f_show_menu()     # Variable: user_choice = Eingabe des Benutzers
    match user_choice.upper():      # Variable user_choice wird geprüft
        case "A":
            f_print_all_recipes(all_recipes)            # Übergabe von globaler Variable all_recipes
        case "B":
            ingredients_list = f_input_ingredients()    # Variable ingredients_list
            f_find_recipes(all_recipes, ingredients_list)
        case "Q":
            print("Auf Wiedersehen!!")
            break
        case _:
            print("Ungültige Eingabe. Bitte A, B oder Q wählen.")


