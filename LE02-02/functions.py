def f_print_all_recipes(recipes):
    """Gibt alle Rezepte schön formatiert in der Konsole aus"""
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")
        print(f"   Zubereitung: {details['zubereitung']}\n")

def f_show_menu()-> str:
    print("\n-- Menü --")
    print("A - Alle Rezepte anzeigen")
    print("B - Rezepte nach Zutaten finden")
    print("Q - Beenden")
    return input ("Wählen Sie: ").strip().upper()

def f_input_ingredients():
    ingredients_input = input("Bitte geben Sie die Zutaten ein:\n(getrennt durch Kommata)\n")
    ingredients_list = []
    for z in ingredients_input.split(","):
        ingredients_list.append(z.strip().lower())
    return ingredients_list

def f_find_recipes(all_recipes, ingredients_list):
    matching_recipes = {}
    for recipe_name, details in all_recipes.items():
        recipe_ingredients= [z.lower() for z in details["zutaten"]]
        if all(ingredient in recipe_ingredients for ingredient in ingredients_list):
            matching_recipes[recipe_name]=details
    if matching_recipes:
        print("\n Passende Rezepte gefunden:")
        f_print_all_recipes(matching_recipes)
    else:
        print("\nKein Rezept enthält alle angegebenen Zutaten.")
