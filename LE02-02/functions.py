# Funktion zum Ausgeben aller Rezepte
def f_print_all_recipes(recipes):             # Parameter: recipes (zeigt z. B. auf all_recipes)
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():     # Variable name = Schlüssel, details = Value
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")   # Variable details
        print(f"   Zubereitung: {details['zubereitung']}\n")    # Variable details

# Funktion zum Anzeigen des Menüs
def f_show_menu()-> str: #-> str → sagt: diese Funktion gibt einen Wert vom Typ str (String/Text) zurück.
    print("\n-- Menü --")
    print("A - Alle Rezepte anzeigen")
    print("B - Rezepte nach Zutaten finden")
    print("Q - Beenden")
    return (input ("Wählen Sie: ").strip().upper())    # Rückgabe: Variable user_choice im Hauptprogramm

# Funktion zum Eingeben der Zutaten
def f_input_ing() -> list [str]:
    ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Kommata)\n")
    ingredients_list = []                               # Variable: Liste, wird gefüllt
    for k in ingredients_input.split(","):
        k= k.strip()
        k= k.lower()
        ingredients_list.append(k)      # Variable ingredients_list wird erweitert
    return ingredients_list                             # Rückgabe an Variable im Hauptprogramm


def f_match_ingredients(recipe_ingredient: dict[str, dict], ingredients_list: list[str]) -> dict[str, dict]:
    match_ingredients: dict[str, dict] = {}
    for name, details in recipe_ingredient.items():
        details_lower_case= [ingredient.lower() for ingredient in details["zutaten"]]
        if all(ingredient in details_lower_case for ingredient in ingredients_list):
            match_ingredients[name] = details
    return match_ingredients

def f_find_recipes(all_recipes: dict) -> dict[str, list[str]]:
    ingredients_list=f_input_ing()
    matches=f_match_ingredients(all_recipes, ingredients_list)
    return matches

def f_print_matches(matches: dict[str, list[str]]) -> None:
    if matches:
        print("\nGefundene Rezepte:\n")
        f_print_all_recipes(matches)
    else:
        print("Kein Rezept passt zu deiner Eingabe.")




