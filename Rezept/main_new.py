print("Herzlich Willkommen beim Rezepte-Manager der Welt!")

from Rezept.views.menus import f_show_menu
from Rezept.views.printers import f_print_matches
from Rezept.views.printers import f_print_all_recipes

from Rezept.models.recipes_model import f_find_ingredients

from Rezept.controllers.add import f_add_recipe
from Rezept.controllers.editor import f_edit_recipe
from Rezept.controllers.delete import f_delete_recipe
from Rezept.controllers.load import *
from Rezept.controllers.save import *

# Dictionary mit allen Rezepten = Variable (global)
all_recipes = {
    "Pizza": {
        "zutaten": ["Mehl", "Eier", "Teig", "Tomatensauce", "Käse"],
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

all_recipes = f_load_recipes(all_recipes) # Rezepte aus Datei laden

# --- Hauptprogramm ---
while True:
    user_choice = f_show_menu()    # Menü anzeigen und Auswahl einlesen
    match user_choice: # Auswahl prüfen mit match-case

        case "A":    # Alle Rezepte anzeigen
            print("\n📖 Alle Rezepte:\n")
            f_print_all_recipes(all_recipes)

        case "B":    # Rezepte nach Zutaten suchen
            matches = f_find_ingredients(all_recipes)
            f_print_matches(matches)

        case "C":   # Neues Rezept hinzufügen
            f_add_recipe(all_recipes)

        case "D":    # Rezept löschen
            f_delete_recipe(all_recipes)

        case "E":   # Rezepte speichern in JSON-Datei
            if f_save_recipes(all_recipes):
                print("Rezepte wurden erfolgreich gespeichert (Datei: rezepte.json).")

        case "F":  # Rezepte aus Datei neu laden
            all_recipes = f_load_recipes(all_recipes)

        case "G":  # Rezept bearbeiten
            f_edit_recipe(all_recipes)

        case "Q":  # Programm beenden
            print("Auf Wiedersehen!!")
            break

        case _:  # Fehlermeldung bei falscher Eingabe
            print("Ungültige Eingabe. Bitte A, B, C, D, E, F, G oder Q wählen.")