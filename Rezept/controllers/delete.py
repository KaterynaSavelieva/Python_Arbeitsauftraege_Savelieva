from Rezept.controllers.save import *


def f_delete_recipe(all_recipes: dict) -> None:
# Löscht ein bestehendes Rezept (mit optionalem Speichern).
    name = input("Bitte geben Sie den Name des Rezepts ein, das Sie löschen möchten: \n").strip().title()
    if name in all_recipes:
        del all_recipes[name]     # Aus dem RAM löschen
        print(f"Das Rezept '{name}' wurde gelöscht.\n")
        save = input("Möchten Sie die Änderung speichern? (Y/N)\n").strip().title()
        if save == "Y":
            if f_save_recipes(all_recipes, delete=[name]):  # gezielt nur dieses löschen
                print(f"Rezept '{name}' wurde gelöscht und gespeichert.")
            else:
                print("Änderung wurde noch nicht gespeichert.")
    else:
        print("Kein Rezept mit dem Namen '{name}' gefunden.")