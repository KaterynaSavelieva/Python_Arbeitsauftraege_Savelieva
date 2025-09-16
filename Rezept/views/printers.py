def f_print_all_recipes(recipes):             # Parameter: recipes (zeigt z. B. auf all_recipes)
    for name, details in recipes.items():     # Variable name = Schlüssel, details = Value
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")   # Variable details
        print(f"   Zubereitung: {details['zubereitung']}\n")    # Variable details


def f_print_matches(matches: dict[str, dict]) -> None:
# Zeigt die gefundenen Rezepte (oder Meldung, wenn keine).
    if matches:
        print("\nGefundene Rezepte:\n")
        f_print_all_recipes(matches)
    else:
        print("Kein Rezept passt zu deiner Eingabe.")