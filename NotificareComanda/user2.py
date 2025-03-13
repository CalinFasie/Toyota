import os
import tkinter as tk
from tkinter import ttk, messagebox
from order_utils import mark_as_read
from db import get_connection

# Mapare utilizatori Windows -> Consilieri
USER_TO_CONSILIER = {
    "calin": "Calin Bucur",
    "romeo": "Romeo Vanc",
    "garantii1": "David Lukacs",
    "itp1": "Arpad Halasz",
    "toyota1": "Sandor Mayas"
}

# Obținem utilizatorul logat
current_user = os.getlogin()
consilier = USER_TO_CONSILIER.get(current_user, None)  # Vedem dacă există un consilier asociat

def load_orders():
    if not consilier:
        messagebox.showerror("Eroare", f"Utilizatorul {current_user} nu este asociat niciunui consilier!")
        return

    conn = get_connection()
    if not conn:
        messagebox.showerror("Eroare", "Nu se poate conecta la baza de date!")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, comanda, CONVERT(VARCHAR, data_inc, 120), consilier FROM _comenzi WHERE culoare = 'red' AND consilier = ?", (consilier,))
        orders = cursor.fetchall()
        conn.close()

        # Curățăm tabelul înainte de reîncărcare
        for row in tree.get_children():
            tree.delete(row)

        # Adăugăm comenzile în tabel
        for order in orders:
            clean_order = (str(order[0]).strip("(),' "), str(order[1]).strip("(),' "), str(order[2]), str(order[3]).strip("(),' "))
            tree.insert("", "end", values=clean_order, tags=("new_order",))

    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea comenzilor: {e}")

# Funcție pentru butonul CITIT
def mark_selected_as_read():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectați o comandă pentru a o marca ca citită!")
        return

    item = tree.item(selected_item)

    try:
        order_id = int(str(item["values"][0]).strip("(),' "))  # Curățăm și convertim ID-ul la INT
    except ValueError:
        messagebox.showerror("Eroare", "ID-ul comenzii nu este valid!")
        return

    mark_as_read(order_id)  # Apelăm funcția din order_utils.py
    tree.delete(selected_item)  # Eliminăm rândul din tabel

# Funcție pentru butonul EXIT cu mesaj de confirmare
def on_exit():
    confirm = messagebox.askyesno("Confirmare", "Sigur doriți să închideți aplicația?")
    if confirm:
        root.destroy()  # Închide fereastra aplicației

# Crearea ferestrei principale
root = tk.Tk()
root.title(f"Vizualizare Comenzi - {consilier}")  # Afișează numele consilierului în titlu
root.geometry("550x350")

# Tabel pentru afișarea comenzilor
columns = ("ID", "Comandă", "Data Introducere", "Consilier")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Comandă", text="Comandă")
tree.heading("Data Introducere", text="Data Introducere")
tree.heading("Consilier", text="Consilier")

tree.column("ID", width=50)
tree.column("Comandă", width=100)
tree.column("Data Introducere", width=150)
tree.column("Consilier", width=150)

tree.tag_configure("new_order", background="red")
tree.tag_configure("read_order", background="lightgreen")

tree.pack(fill="both", expand=True, pady=10)

# Frame pentru butoane (CITIT & EXIT)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buton CITIT
btn_mark_read = tk.Button(button_frame, text="CITIT", command=mark_selected_as_read, bg="blue", fg="white", width=10)
btn_mark_read.grid(row=0, column=0, padx=5)

# Buton EXIT
btn_exit = tk.Button(button_frame, text="EXIT", command=on_exit, bg="red", fg="white", width=10)
btn_exit.grid(row=0, column=1, padx=5)

# Încărcăm comenzile la pornire
load_orders()

# Pornirea interfeței grafice
root.mainloop()
