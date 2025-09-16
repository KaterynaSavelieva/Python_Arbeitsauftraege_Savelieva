from Rezept.models.storage import save_json

def f_save_recipes(all_recipes: dict,
                   subset: dict | None=None,
                   delete: list[str] | None=None) -> bool:
    to_save = dict(all_recipes)  # Kopie bauen (Original bleibt unberührt)
    if subset:
        to_save.update(subset)  # Nur diese überschreiben/ergänzen
    if delete:
        for name in delete:
            to_save.pop(name, None)  # sicher entfernen (ohne Fehler)
    return save_json(to_save)