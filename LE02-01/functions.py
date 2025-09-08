def print_all_recipes(recipes):
    """Gibt alle Rezepte schön formatiert in der Konsole aus"""
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")
        print(f"   Zubereitung: {details['zubereitung']}\n")




