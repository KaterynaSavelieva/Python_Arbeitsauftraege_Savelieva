from Rezept.models.storage import  load_json

# Funktion zum Laden der Rezepte aus einer JSON-Datei
def f_load_recipes(all_recipes: dict) -> dict:
# Lädt rezepte.json (falls vorhanden) und gibt aktualisiertes Dictionary zurück.
    data = load_json()  # Datei lesen
    if data:
        all_recipes.update(data)  # Geladene Rezepte hinzufügen/überschreiben
        print("Rezepte wurden erfolgreich geladen (Datei: rezepte.json).")
    return all_recipes
