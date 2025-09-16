from Rezept.models.validators import *
from Rezept.views.printers import f_print_all_recipes

def f_show_menu()-> str: # Druckt das Hauptmenü und gibt die Auswahl des/der Nutzer:in zurück.
    print("\n-- 🥗🥘🥞Menü 🥓🫘--")
    print("A - Alle Rezepte anzeigen 📖📖📖📖📖")
    print("B - Rezepte nach Zutaten finden🔎")
    print("C - Neues Rezept hinzufügen➕")
    print("D - Rezept löschen🫳🫳🫳")
    print("E - Rezepte speichern📘📘")
    print("G - Rezepte bearbeiten✍️✍️")
    print("F - Rezepte laden🙌")
    print("Q - Beenden🫡")
    return input ("Wählen Sie: ").strip().upper()

def f_recipe_change()-> str:
# Zeigt das Untermenü für „Rezept bearbeiten“ und gibt die Auswahl zurück.
    print("1 - Hinzufügen von Zutaten")
    print("2 - Löschen von Zutaten")
    print("3 - Bearbeiten der Anleitung")
    print("4 - Änderung speichern")
    print("5 - Beenden")
    return input ("Wählen Sie: ").strip()

def f_input_ingredients() -> list[str]:
    # Fragt die Zutaten als Text ab (durch Komma getrennt),
    # wandelt in eine Liste um und validiert sie.
    while True:
        ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Komma)\n")
        # Direkt parsen: splitten, trimmen, TitleCase, leere Einträge filtern
        ingredients_list = [z.strip().title() for z in ingredients_input.split(",") if z.strip()]
        ok, msg = f_validate_ingredients_list(ingredients_list)  # Prüfen
        if ok:
            return ingredients_list
        print(f"Fehler: {msg}")

def f_find_recipe(all_recipes: dict) -> str | None:
    # Fragt einen Rezeptnamen ab, solange bis es existiert.
    while True:
        recipe_change = input("Bitte geben der Name des Rezepts ein, das Sie bearbeiten möchten\n").strip().title()
        if recipe_change not in all_recipes:
            print("Rezept nicht gefunden")
            continue  # Noch einmal versuchen
        # Gefunden → einmal das Rezept zeigen (zur Kontrolle)
        f_print_all_recipes({recipe_change: all_recipes[recipe_change]})
        return recipe_change

def f_input_recipe_instruction() -> str:
# Fragt die Zubereitungsanleitung als Text ab (eine Zeile).
    instruction = input("Bitte geben Sie die Anleitung des Rezepts ein: \n").strip()
    return instruction

def f_input_recipe_name() -> str:
# Fragt den Rezeptnamen ab und validiert ihn (Länge, Zeichen etc).
    while True:
        name = input("Bitte geben Sie den Name des Rezepts ein: \n").strip().title()
        ok, msg = f_validate_recipe_name(name)
        if ok:
            return name
        print(f"Fehler: {msg}")