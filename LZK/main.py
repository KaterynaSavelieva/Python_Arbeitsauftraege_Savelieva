from functions import *

all_books = {}


def main() -> None:
    f_load_books(all_books)
    while True:
        user_choice = f_show_menu()
        match user_choice:
            case 'A':
                f_print_all_books(all_books)
            case 'B':
                f_add_book(all_books)
            case 'C':
                f_status(all_books)
            case 'D':
                f_find_book(all_books)
            case 'Q':
                f_save_books(all_books)
                print("Auf Wiedersehen!")
                break
            case _:
                print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()