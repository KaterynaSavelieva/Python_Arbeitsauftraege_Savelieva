# Funktion zum Ausgeben aller Rezepte
def f_print_all_recipes(recipes):             # Parameter: recipes (zeigt z. B. auf all_recipes)
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():     # Variable name = Schlüssel, details = Value
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")   # Variable details
        print(f"   Zubereitung: {details['zubereitung']}\n")    # Variable details

# Funktion zum Anzeigen des Menüs
def f_show_menu()-> str:
    print("\n-- Menü --")
    print("A - Alle Rezepte anzeigen")
    print("B - Rezepte nach Zutaten finden")
    print("Q - Beenden")
    return input ("Wählen Sie: ").strip().upper()    # Rückgabe: Variable user_choice im Hauptprogramm

# Funktion zum Eingeben der Zutaten
def f_input_ingredients():
    ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Kommata)\n")   # Variable: ingredients_input (String)
    ingredients_list = []                               # Variable: Liste, wird gefüllt
    for z in ingredients_input.split(","):              # Variable: z (Laufvariable in der Schleife)
        ingredients_list.append(z.strip().lower())      # Variable ingredients_list wird erweitert
    return ingredients_list                             # Rückgabe an Variable im Hauptprogramm

# Funktion zum Finden passender Rezepte
def f_find_recipes(all_recipes, ingredients_list):      # Parameter: all_recipes (Dictionary), ingredients_list (Liste von Zutaten)
    matching_recipes = {}                               # Variable: Dictionary für Treffer
    for recipe_name, details in all_recipes.items():                    # recipe_name = Schlüssel, details = Value
        recipe_ingredients= [z.lower() for z in details["zutaten"]]     # Variable recipe_ingredients = Liste der Zutaten aus einem Rezept
        if all(ingredient in recipe_ingredients for ingredient in ingredients_list):    # Variable ingredient = einzelne Benutzereingabe
            matching_recipes[recipe_name]=details           # Variable matching_recipes wird erweitert
    if matching_recipes:                    # Variable matching_recipes
        print("\n Passende Rezepte gefunden:")
        f_print_all_recipes(matching_recipes)   # Übergabe an Parameter recipes
    else:
        print("\nKein Rezept enthält alle angegebenen Zutaten.")
