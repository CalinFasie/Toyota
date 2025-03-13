import os
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

# ----------------------- CONFIGURARE BAZĂ DE DATE -----------------------
CONN_STR = (
    "DRIVER={SQL Server};"
    "SERVER=or-sql\\am;"
    "DATABASE=gmro011p;"
    "UID=sa;"
    "PWD=am@123#;"
)

def get_connection():
    """ Returnează o conexiune la baza de date SQL Server """
    try:
        conn = pyodbc.connect(CONN_STR)
        return conn
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la conectare: {e}")
        return None

# ----------------------- MAPARE UTILIZATORI WINDOWS -> CONSILIERI -----------------------
USER_TO_CONSILIER = {
    "calin": "Calin Bucur",
    "romeo": "Romeo Vanc",
    "garantii1": "David Lukacs",
    "itp1": "Arpad Halasz",
    "toyota1": "Sandor Mayas"
}

# Obținem utilizatorul logat
current_user = os.getlogin()
consilier = USER_TO_CONSILIER.get(current_user, None)

def load_orders():
    """ Încarcă comenzile adresate consilierului curent """
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

        # Adăugăm comenzile în tabel cu date curate
        for order in orders:
            clean_order = (
                str(order[0]).strip("(),' "),  # Curăță ID-ul
                str(order[1]).strip("(),' "),  # Curăță comanda
                str(order[2]).strip("(),' "),  # Curăță data
                str(order[3]).strip("(),' ")   # Curăță consilierul
            )
            tree.insert("", "end", values=clean_order, tags=("new_order",))

    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea comenzilor: {e}")

def mark_as_read():
    """ Marchează o comandă ca citită """
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectați o comandă pentru a o marca ca citită!")
        return

    item = tree.item(selected_item)
    order_id = item["values"][0]

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE _comenzi SET data_citit = ?, culoare = 'green' WHERE id = ?", (now, order_id))
            conn.commit()
            conn.close()
            tree.delete(selected_item)  # Elimină rândul după marcarea ca citit
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la marcarea comenzii: {e}")

# ----------------------- CREARE INTERFAȚĂ GRAFICĂ -----------------------
root = tk.Tk()
root.title(f"Vizualizare Comenzi - {consilier}")
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
tree.pack(fill="both", expand=True, pady=10)

# Frame pentru butoane (CITIT & EXIT)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buton CITIT
btn_mark_read = tk.Button(button_frame, text="CITIT", command=mark_as_read, bg="blue", fg="white", width=10)
btn_mark_read.grid(row=0, column=0, padx=5)

# Buton EXIT
btn_exit = tk.Button(button_frame, text="EXIT", command=root.destroy, bg="red", fg="white", width=10)
btn_exit.grid(row=0, column=1, padx=5)

# Încărcăm comenzile la pornire
load_orders()

# Pornirea interfeței grafice
root.mainloop()
