from Rezept.views.menus import f_find_recipe
from Rezept.views.menus import f_recipe_change
from Rezept.models.recipes_model import f_delete_ingredients
from Rezept.models.recipes_model import f_add_ingredients
from Rezept.models.recipes_model import f_change_instructions
from Rezept.controllers.save import *



def f_edit_recipe(all_recipes: dict) -> None:
    # Interaktive Bearbeitung eines Rezepts (Zutaten + Anleitung).
    print("Rezepte bearbeiten!")
    recipe_change = f_find_recipe(all_recipes)  # gültigen Namen holen
    if recipe_change:
        while True:
            user_change_choice = f_recipe_change()  # Untermenü anzeigen
            match user_change_choice:
                case "1":
                    f_add_ingredients(all_recipes, recipe_change)
                case "2":
                    f_delete_ingredients(all_recipes, recipe_change)
                case "3":
                    f_change_instructions(all_recipes, recipe_change)
                case "4":
                    # Nur dieses Rezept speichern (optional)
                    if f_save_recipes(all_recipes, subset={recipe_change: all_recipes[recipe_change]}):
                        print(f"Rezept '{recipe_change}' wurde gespeichert.")
                case "5":
                    print("Beenden")
                    break
                case _:
                    print("Ungültige Eingabe. Bitte 1, 2, 3, 4 oder 5 wählen.")
