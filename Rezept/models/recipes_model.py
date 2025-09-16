
#Ця функція працює з даними (видаляє інгредієнти зі словника),
# тому її місце у Rezept/models/. Назву залишаємо таку ж.
def f_delete_ingredients(all_recipes: dict, recipe_change: str) -> None:
# Entfernt ausgewählte Zutaten aus einem Rezept.
    from Rezept.views.printers import f_print_all_recipes
    from Rezept.views.menus import  f_input_ingredients
    new_ingredients = f_input_ingredients()  # Hier: welche Zutaten sollen weg?
    delete: list[str] = []      # tatsächlich gelöscht
    not_found: list[str] = []   # nicht im Rezept vorhanden
    for ingredient in new_ingredients:
        if ingredient in all_recipes[recipe_change]['zutaten']:
            all_recipes[recipe_change]['zutaten'].remove(ingredient)
            delete.append(ingredient)
        else:
            not_found.append(ingredient)
    if delete:
        print(f"Gelöscht: {', '.join(delete)}")
    if not_found:
        print(f"Nicht gefunden: {', '.join(not_found)}")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})

def f_add_ingredients(all_recipes, recipe_change) -> None:
    # Fügt neue Zutaten zu einem bestehenden Rezept hinzu.
    from Rezept.views.printers import f_print_all_recipes
    from Rezept.views.menus import f_input_ingredients
    new_ingredients = f_input_ingredients()
    all_recipes[recipe_change]['zutaten'].extend(new_ingredients)
    print(f"Neue Zutaten wurden zu {recipe_change} hinzugefügt")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})

def f_change_instructions(all_recipes, recipe_change) -> None:
# Ersetzt die Zubereitungsanleitung eines Rezepts durch eine neue.
    from Rezept.views.printers import f_print_all_recipes
    new_instruction = input(f"Bitte geben Sie die neue Anleitung zum Rezept '{recipe_change}'\n")
    all_recipes[recipe_change]['zubereitung'] = new_instruction
    print(f"Die Anleitung für das Rezept '{recipe_change}' wurde geändert!")
    f_print_all_recipes({recipe_change: all_recipes[recipe_change]})

def f_match_ingredients(recipe_ingredients: dict[str, dict], ingredients_list: list[str]) -> dict[str, dict]:
    # Sucht alle Rezepte, die ALLE gesuchten Zutaten enthalten.
    match_ingredients: dict[str, dict] = {}
    for name, details in recipe_ingredients.items():
        # Zutaten des Rezepts in Kleinbuchstaben zum Vergleichen
        details_lower = [z.lower() for z in details['zutaten']]
        # Prüfen: sind alle gesuchten Zutaten enthalten?
        if all(ing.lower() in details_lower for ing in ingredients_list):
            match_ingredients[name] = details  # Treffer merken
    return match_ingredients

def f_find_ingredients(all_recipes: dict) -> dict[str, dict]:
    # Liest Zutaten vom/von der Nutzer:in und liefert passende Rezepte zurück.
    from Rezept.views.menus import f_input_ingredients
    ingredients_list = f_input_ingredients()
    matches = f_match_ingredients(all_recipes, ingredients_list)
    return matches





