import tkinter as tk
from tkinter import ttk, messagebox
from order_utils import save_order, send_email

# Dicționar cu lista consilierilor și email-urile lor
CONSILIERI = {
    "Calin Bucur": "calin@carscenter.ro",
    "Romeo Vanc": "romeo.vanc@oradea.toyota.ro",
    "David Lukacs": "david.lukacs@oradea.toyota.ro",
    "Arpad Halasz": "arpad.halasz@oradea.toyota.ro",
    "Sandor Mayas": "sandor.mayas@oradea.toyota.ro"
}

# Funcție apelată la apăsarea butonului SAVE
def on_save():
    comanda = entry_comanda.get().strip()
    consilier = combo_consilier.get().strip()

    if not comanda or not consilier:
        messagebox.showwarning("Eroare", "Toate câmpurile sunt obligatorii!")
        return

    # Obținem adresa de email a consilierului selectat
    email = CONSILIERI.get(consilier, None)

    if not email:
        messagebox.showerror("Eroare", "Consilierul selectat nu are un email asociat!")
        return

    # Emailul supervizorului
    email_sp = "calin@carscenter.ro"  # --"romeo.vanc@oradea.toyota.ro"

    # Salvăm comanda în baza de date
    save_order(comanda, consilier, email, email_sp)

    # Trimitem email-ul
    send_email(comanda, consilier, email, email_sp)

    # Resetăm câmpurile după salvare
    entry_comanda.delete(0, tk.END)
    combo_consilier.set("")

# Funcție pentru butonul de ieșire
def on_exit():
    root.destroy()  # Închide fereastra aplicației

# Crearea ferestrei principale
root = tk.Tk()
root.title("Introducere Comandă")
root.geometry("400x250")

# Label + Entry pentru Comandă
tk.Label(root, text="Comandă:").pack(pady=5)
entry_comanda = tk.Entry(root, width=30)
entry_comanda.pack()

# Label + Combobox pentru Consilier
tk.Label(root, text="Consilier:").pack(pady=5)
combo_consilier = ttk.Combobox(root, values=list(CONSILIERI.keys()), width=27)
combo_consilier.pack()

# Frame pentru butoane (SAVE & EXIT)
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Buton SAVE
btn_save = tk.Button(button_frame, text="SAVE", command=on_save, bg="green", fg="white", width=10)
btn_save.grid(row=0, column=0, padx=5)

# Buton EXIT
btn_exit = tk.Button(button_frame, text="EXIT", command=on_exit, bg="red", fg="white", width=10)
btn_exit.grid(row=0, column=1, padx=5)

# Pornirea interfeței grafice
root.mainloop()
