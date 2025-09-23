from functions import*
f_print_title("Herzlich Willkommen im Buchbestand der Stadtbücherei `LeseLust`")

all_books = {}

def main() -> None:
    f_load_books(all_books)

    while True:
        user_choice = f_show_menu()
        match user_choice.strip().upper():
            case "A":
                f_print_all_books(all_books)
            case "B":
                f_add_book(all_books)
            case "C":
                f_status(all_books)
            case "D":
                f_find_book(all_books)
            case "Q":
                f_save_books(all_books)
                print("Auf Wiedersehen!")
                break
            case _:
                print("Ungültige Eingabe. Bitte A, B, C, D, oder Q wählen.")
                f_wait_for_enter()

if __name__ == "__main__":
    main()
