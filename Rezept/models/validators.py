def f_check_length(value: str, min_len: int, max_len: int) -> tuple[bool, str]:
# Prüft, ob die Länge zwischen min_len und max_len liegt.
    if not (min_len <= len(value) <= max_len):
        return False, f"'{value}' muss zwischen {min_len} und {max_len} Zeichen lang sein."
    return True, ""

def f_check_only_letters(value: str) -> tuple[bool, str]:
# Erlaubt nur Buchstaben und Leerzeichen.
    if not value.replace(" ", "").isalpha():
        return False, f"'{value}' darf nur Buchstaben und Leerzeichen enthalten."
    return True, ""

def f_check_letters_and_digits(value: str) -> tuple[bool, str]:
# Erlaubt: Buchstaben, Ziffern und Leerzeichen.
    if not value.replace(" ", "").isalnum():
        return False, f"'{value}' darf nur Buchstaben, Ziffern und Leerzeichen enthalten."
    return True, ""

def f_validate_recipe_name(name: str) -> tuple[bool, str]:
# Kombinierte Prüfung für Rezeptnamen (Länge + erlaubte Zeichen).
    ok, msg = f_check_length(name, 1, 200)
    if not ok:
        return False, "Rezeptname: " + msg
    ok, msg = f_check_only_letters(name)
    if not ok:
        return False, "Rezeptname: " + msg
    return True, ""

def f_validate_ingredients_list(ingredients_list: list[str]) -> tuple[bool, str]:
# Prüft die Zutatenliste: nicht leer, jede Zutat hat OK Länge und Zeichen.
    if not ingredients_list:
        return False, "Die Zutatenliste darf nicht leer sein."
    for z in ingredients_list:
        ok, msg = f_check_length(z, 1, 100)
        if not ok:
            return False, "Zutat: " + msg
        ok, msg = f_check_letters_and_digits(z)
        if not ok:
            return False, "Zutat: " + msg
    return True, ""