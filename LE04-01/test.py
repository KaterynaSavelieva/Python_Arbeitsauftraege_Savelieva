import tkinter as tk
from tkinter import messagebox

# Hauptfenster
root = tk.Tk()
root.title("Meine Applikation")
root.geometry("500x500")

#  1. Label
tk.Label(root, text="Name:").pack()

#  2. Entry
entry_name = tk.Entry(root)
entry_name.pack()

#  3. Button mit Funktion
def save():
    messagebox.showinfo("Titel", "Daten gespeichert.")

def print_name():
    name = entry_name.get()
    output.insert(tk.END, f"Name: {name}\n")

tk.Button(root, text="Speichern", command=save).pack()
tk.Button(root, text="Name printen", command=print_name).pack()

#  4. Textfeld (mehrzeilig)
output = tk.Text(root, height=10, width=40)
output.pack()
output.insert(tk.END, "Vorgefertigter Text\n")

def delete_text():
    output.delete("1.0", tk.END)

tk.Button(root, text="Text löschen", command=delete_text).pack()

#  5. Messagebox
def wrong_input():
    messagebox.showerror("Fehler", "Ungültige Eingabe.")

tk.Button(root, text="Fehlermeldung zeigen", command=wrong_input).pack()

#  6. Listbox
listbox = tk.Listbox(root, height=5, width=30, selectmode="single")
listbox.pack(pady=10)
personen = ["Julia Grabner", "Niklas Grabner", "Bettina Cossee"]
for p in personen:
    listbox.insert(tk.END, p)

#  7. Layout: grid()
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Adresse:").grid(row=0, column=0, padx=5, pady=5)
entry_adresse = tk.Entry(frame)
entry_adresse.grid(row=0, column=1, padx=5, pady=5)

#  8. Layout: place()
tk.Label(root, text="Email:").place(x=50, y=400)
entry_email = tk.Entry(root)
entry_email.place(x=120, y=400)

root.mainloop()