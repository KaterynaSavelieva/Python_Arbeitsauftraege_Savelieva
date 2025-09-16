from Rezept.controllers.save import *

def f_add_recipe(all_recipes: dict) -> None:
# Legt ein neues Rezept an (Name, Zutaten, Anleitung) und speichert es im Speicher.
    from Rezept.views.menus import (
        f_input_ingredients,
        f_input_recipe_instruction,
        f_input_recipe_name
    )

    name = f_input_recipe_name()
    if name in all_recipes:
        print("Hinweis: Dieses Rezept gibt es bereits.")
        return
    ingredients_list = f_input_ingredients()
    instruction = f_input_recipe_instruction()
    all_recipes[name] = {"zutaten": ingredients_list, "zubereitung": instruction}
    print(f"Rezept '{name}' wurde hinzugefügt und gespeichert.")
    f_save_recipes(all_recipes)