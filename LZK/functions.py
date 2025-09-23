RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

NAME_MIN, NAME_MAX = 2, 20
AVAILABILITY_FALSE, AVAILABILITY_TRUE = "False", "True"
YEAR_MIN, YEAR_MAX = 0, 2025

from pathlib import Path
DATEI = Path("library.json")

def f_wait_for_enter() -> None:
    input("\nDrücken Sie ENTER, um fortzufahren...\n")

def f_print_title(text: str) -> None:
    breit =70
    print(f"{YELLOW}\n{'='*breit}{RESET}")
    print(BOLD+BLUE+text.center(breit)+RESET)
    print(f"{YELLOW}{'='*breit}{RESET}")

from tabulate import tabulate
def f_print_all_books(books):
    f_print_title("📖 Alle Bücher:")
    table=[]
    for name, details in sorted(books.items()):
        author = details['author']
        year = details['year']
        available = details['available']
        table.append([name, author, year, available])
    print(tabulate(table, headers=[BOLD +"Titel", "Autor", "Erscheinungsjahr", "Verfügbarkeit"+ RESET], tablefmt="fancy_grid"))
    f_wait_for_enter()

def f_show_menu()-> str:
    f_print_title("📖📖📖📖📖Menü 📖📖📖📖📖")
    print("A - Alle Bücher anzeigen 📖📖📖📖📖")
    print("B - Neues Buch hinzufügen➕")
    print("C - Buch ausleihen / zurückgeben🔃")
    print("D - Bücher suchen🔎")
    print("Q - Beenden🫡")
    return input ("Wählen Sie: ").strip().upper()

def f_load_books(all_books: dict) -> bool:
    import json
    try:
        with open("library.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            all_books.update(data)
        return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

def f_save_books(all_books: dict) -> bool:
    try:
        with open("library.json", "w", encoding="utf-8") as f:
            import json
            json.dump(all_books, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def f_safe_year(year: str) -> int:
    while True:
        raw = input(year).strip()
        try:
            y = int(raw)
            if YEAR_MIN <= y <= YEAR_MAX:
                return y
            else:
                print(f"Jahr muss {YEAR_MIN}–{YEAR_MAX} sein.")
        except ValueError:
            print("Bitte eine ganze Zahl eingeben.")

def f_ok_len(length, min, max):
    return min <= len(length) <= max

def f_valid_name(name_length):
    return f_ok_len(name_length, NAME_MIN, NAME_MAX)

def f_add_book(data: dict) -> None:
    f_print_title("Buch hinzufügen")
    titel = input("Titel: ").strip()
    if not f_valid_name(titel):
        print("Fehler: Titel hat ungültige Länge.")
        f_wait_for_enter()
        return
    if titel in data:
        print("Fehler: Titel existiert bereits.")
        f_wait_for_enter()
        return

    autor = input("Autor: ").strip().title()
    if not f_valid_name(autor):
        print("Fehler: Autor hat ungültige Länge.")
        f_wait_for_enter()
        return

    year = f_safe_year("Erscheinungsjahr: ")

    data[titel] = {
        "author": autor,
        "year": year,
        "available": AVAILABILITY_TRUE
    }
    print(f"{GREEN} „{titel}“ hinzugefügt und gespeichert.{RESET}")

    f_save_books(data)
    f_wait_for_enter()

def f_find_book(all_books):
    while True:
        find_book = input("Bitte geben der Name des Buches ein:\n").strip()
        if find_book not in all_books:
            print("Nicht gefunden")
            continue
        else:
            f_print_all_books({find_book: all_books[find_book]})
            return find_book

def f_status(data):
    titel=f_find_book(data)
    status_change = input("Möchten Sie Status ändern? Y/N\n").strip().title()

    status_old = data[titel].get("available")
    if status_change == "Y":
        status_new = AVAILABILITY_TRUE if status_old == AVAILABILITY_TRUE else AVAILABILITY_FALSE
        data[titel]["available"] = status_new
        f_save_books(data)
        print(f"Änderung wurde gespeichert")
    else:
        print("Änderung wurde noch nicht gespeichert")