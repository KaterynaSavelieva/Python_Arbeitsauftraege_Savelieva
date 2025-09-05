all_recipes = {
    "Pasta": {
        "Zutaten": ["Nudeln", "Tomatensauce", "Käse"],
        "Anleitung": "Nudeln kochen, Sauce erhitzen, alles mischen und mit Käse bestreuen."
    },
    "Pfannkuchen": {
        "Zutaten": ["Mehl", "Milch", "Eier"],
        "Anleitung": "Alles verrühren, in der Pfanne ausbacken."
    },
    "Salat": {
        "Zutaten": ["Gurke", "Tomaten", "Olivenöl"],
        "Anleitung": "Alles klein schneiden und mit Öl mischen."
    }
}

print("Rezepte-Manager")
print("A = Alle Rezepte anzeigen")

wahl = input("Bitte wählen: ")

if wahl == "A":
    print("\nAlle Rezepte:")
    for name, details in all_recipes.items():
        print(f"\n{name}")
        print("Zutaten:", ", ".join(details["Zutaten"]))
        print("Anleitung:", details["Anleitung"])
else:
    print("Ungültige Eingabe")