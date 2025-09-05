# Rezepte-Manager – Aufgabe LE02-01
# Dieses Programm speichert einige Rezepte und zeigt sie auf Wunsch an.

# Dictionary mit allen Rezepten
all_recipes = {
    "Pizza": {
        "zutaten": ["Teig", "Tomatensauce", "Käse"],
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


def print_all_recipes(recipes):
    """Gibt alle Rezepte schön formatiert in der Konsole aus"""
    print("\n📖👩‍🍳 Alle Rezepte:\n")
    for name, details in recipes.items():
        print(f"🍴 {name}")  # Rezeptname
        print(f"   Zutaten: {', '.join(details['zutaten'])}")
        print(f"   Zubereitung: {details['zubereitung']}\n")


# --- Hauptprogramm ---
user_choice = input("Menü: \nA) Alle Rezepte anzeigen\nWählen Sie: ")

if user_choice.upper() == "A":
    print_all_recipes(all_recipes)
else:
    print("Ungültige Eingabe. Bitte 'A' wählen.")