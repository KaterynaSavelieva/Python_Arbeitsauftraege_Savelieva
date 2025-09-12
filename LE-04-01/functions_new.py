def f_print_all_recipes(recipes):             # Parameter: recipes (zeigt z. B. auf all_recipes)
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():     # Variable name = Schlüssel, details = Value
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")   # Variable details
        print(f"   Zubereitung: {details['zubereitung']}\n")    # Variable details

def f_show_menu()-> str:
    print("\n-- Menü --")
    print("A - Alle Rezepte anzeigen")
    print("B - Rezepte nach Zutaten finden")
    print("C - Neues Rezept hinzufügen")
    print("D - Rezept löschen")
    print("E - Rezepte speichern")
    print("G - Rezepte bearbeiten")
    print("F - Rezepte laden")
    print("Q - Beenden")
    return input ("Wählen Sie: ").strip().upper()

def f_input_ingredients() -> list [str]:
    while True:
        ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Kommata)\n")
        ingredients_list= f_parse_ingredients(ingredients_input)#Eingabe in Liste umwandeln, bereinigen
        ok, msg = f_validate_ingredients_list(ingredients_list)# Validierung der Zutatenliste
        if ok:
            return ingredients_list
        print(f"Fehler: {msg}")

#Die Funktion wandelt einen vom Benutzer eingegebenen String mit Zutaten in eine bereinigte Liste um:
def f_parse_ingredients(input: str) -> list[str]:
    return [z.strip().title() for z in input.split(",") if z.strip()]

def f_match_ingredients(recipe_ingredients: dict[str, dict], ingredients_list: list[str]) -> dict[str, dict]:
    # Leeres Dictionary für die Treffer
    match_ingredients: dict[str, dict] = {}
    # Durch alle Rezepte gehen
    for name, details in recipe_ingredients.items():
        # Zutaten des Rezepts in Kleinbuchstaben umwandeln
        details_lower_case = []
        for ingredient in details["zutaten"]:
            details_lower_case.append(ingredient.lower())

        # Prüfen, ob alle gesuchten Zutaten im Rezept vorkommen
        alle_gefunden = True
        for ingredient in ingredients_list:
            if ingredient not in details_lower_case:
                alle_gefunden = False
                break
        # Wenn alle Zutaten gefunden wurden, Rezept speichern
        if alle_gefunden:
            match_ingredients[name] = details
    return match_ingredients

def f_find_ingredients(all_recipes: dict) -> dict[str, dict]:
    ingredients_list=f_input_ingredients()
    matches=f_match_ingredients(all_recipes, ingredients_list)
    return matches

def f_recipe_change()-> str:
    print("1 - Hinzufügen von Zutaten")
    print("2 - Löschen von Zutaten")
    print("3 - Bearbeiten der Anleitung")
    print("4 - Beenden")
    return input ("Wählen Sie: ").strip()

def f_find_recipe(all_recipes: dict) -> dict[str, dict]:
    while True:
        recipe_change = input("Bitte geben der Name des Rezepts ein, das Sie bearbeiten möchten\n").strip().title()
        if recipe_change not in all_recipes:
            print("Rezept nicht gefunden")
            return{}
        else:
            recipe_change= {recipe_change: all_recipes[recipe_change]}
            f_print_all_recipes(recipe_change)
            f_recipe_change()
            return recipe_change

def f_change_instructions(all_recipes, recipe_change) -> None:
    if not recipe_change:
        new_instruction = input("Bitte geben Sie die neue Anleitung zum Rezept `{recipe_change}`\n`")
        all_recipes[recipe_change]["zubereitung"]=new_instruction
        print(f"Die Anleitung für das Rezept `{recipe_change}` wurde geändert!`")



def f_print_matches(matches: dict[str, dict]) -> None:
    if matches:
        print("\nGefundene Rezepte:\n")
        f_print_all_recipes(matches)
    else:
        print("Kein Rezept passt zu deiner Eingabe.")

def f_input_recipe_name() -> str:
    while True:
        name = input("Bitte geben Sie den Name des Rezeptes ein: \n").strip().title()  # ohne Leerzeichen
        # Validierung aufrufen
        ok, msg = f_validate_recipe_name(name)
        if ok:
            return name
        print(f"Fehler: {msg}")

def f_input_recipe_instruction() -> str:
    instruction = input("Bitte geben Sie die Anleitung des Rezeptes ein: \n").strip()
    return instruction

def f_add_recipe(all_recipes: dict) -> None:
    name = f_input_recipe_name()
    ingredients_list = f_input_ingredients()
    instruction = f_input_recipe_instruction()

    all_recipes[name]={"zutaten": ingredients_list, "zubereitung": instruction}
    print(f"Rezept '{name}' wurde hinzugefügt.")
    f_save_recipes(all_recipes)

def f_delete_recipe(all_recipes: dict[str, dict]) -> None:
    name=input("Bitte geben Sie den Name des Rezeptes ein, das Sie löschen möchten: \n").strip().title()
    if name in all_recipes:
        del all_recipes[name]
        print(f"Das Rezept '{name}' wurde gelöscht.\n")
    else:
        print(f"Kein Rezept mit dem Namen '{name}' gefunden.")

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
    ok, msg = f_check_length(name, 1, 200)
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
        ok, msg = f_check_length(z, 1, 100)
        if not ok:
            return False, "Zutat: " + msg

        # Zutaten: Buchstaben + Ziffern + Leerzeichen erlaubt
        ok, msg = f_check_letters_and_digits(z)
        if not ok:
            return False, "Zutat: " + msg

    return True, ""

import json
# Funktion zum Speichern der Rezepte in einer JSON-Datei
def f_save_recipes(all_recipes: dict) -> None:
    #Speichert alle Rezepte in der Datei rezepte.json.
    try:
        # Datei im Schreibmodus ("w") öffnen, UTF-8 Kodierung für Umlaute
        with open("rezepte.json", "w", encoding="utf-8") as f:
            # Dictionary all_recipes in JSON-Datei schreiben
            json.dump(all_recipes, f, ensure_ascii=False, indent=2)
        print("Rezepte wurden erfolgreich gespeichert (Datei: rezepte.json).")
    except Exception as e:
        # Allgemeiner Fehler beim Speichern
        print(f"Fehler beim Speichern: {e}")

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
            print("Rezepte wurden erfolgreich geladen (Datei: rezepte.json).")
    except FileNotFoundError:
        # Wenn Datei nicht existiert
        print("Fehler: Die Datei rezepte.json wurde nicht gefunden.")
    except json.JSONDecodeError:
        # Wenn Datei leer oder beschädigt ist
        print("Fehler: Die Datei rezepte.json ist beschädigt oder leer.")
    return all_recipes