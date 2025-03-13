import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import smtplib
from email.mime.text import MIMEText
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

# ----------------------- CONFIGURARE EMAIL -----------------------
SMTP_SERVER = "mail.carscenter.ro"
SMTP_PORT = 587
SMTP_USER = "report@carscenter.ro"
SMTP_PASSWORD = "#I4X#@qYqoNG"

def send_email(comanda, consilier, email, email_sp):
    """ Trimite un email și înregistrează în log """
    try:
        msg = MIMEText(f"Comandă completa: {comanda} pentru consilierul {consilier}.")
        msg["Subject"] = "Comandă completă în sistem"
        msg["From"] = SMTP_USER
        msg["To"] = f"{email}, {email_sp}"

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [email, email_sp], msg.as_string())
        server.quit()

        # messagebox.showinfo("Succes", "Emailul a fost trimis cu succes!")

    except Exception as e:
        messagebox.showerror("Eroare Email", f"Eroare la trimiterea emailului: {e}")

# ----------------------- CONFIGURARE CONSILIERI -----------------------
CONSILIERI = {
    # "Calin Bucur": "calin79fc@yahoo.com",
    "Romeo Vanc": "romeo.vanc@oradea.toyota.ro",
    "David Lukacs": "david.lukacs@oradea.toyota.ro",
    "Arpad Halasz": "arpad.halasz@oradea.toyota.ro",
    "Sandor Matyas": "sandor.mayas@oradea.toyota.ro"
}

# ----------------------- FUNCȚIE SALVARE COMANDĂ -----------------------
def save_order():
    """ Salvează comanda în baza de date și trimite email """
    comanda = entry_comanda.get().strip()
    consilier = combo_consilier.get().strip()

    if not comanda or not consilier:
        messagebox.showwarning("Eroare", "Toate câmpurile sunt obligatorii!")
        return

    email = CONSILIERI.get(consilier)
    email_sp = "romeo.vanc@oradea.toyota.ro"

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = """INSERT INTO _comenzi (comanda, data_inc, data_citit, ok, culoare, consilier, email, email_sp) 
                       VALUES (?, ?, NULL, 0, 'red', ?, ?, ?)"""
            cursor.execute(query, (comanda, now, consilier, email, email_sp))
            conn.commit()
            conn.close()

            send_email(comanda, consilier, email, email_sp)
            messagebox.showinfo("Succes", "Comanda a fost salvată și emailul trimis!")
            entry_comanda.delete(0, tk.END)
            combo_consilier.set("")

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvarea comenzii: {e}")

# ----------------------- CREARE INTERFAȚĂ GRAFICĂ -----------------------
root = tk.Tk()
root.title("Depozit - Introducere Comandă")
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
btn_save = tk.Button(button_frame, text="SAVE", command=save_order, bg="green", fg="white", width=10)
btn_save.grid(row=0, column=0, padx=5)

# Buton EXIT
btn_exit = tk.Button(button_frame, text="EXIT", command=root.destroy, bg="red", fg="white", width=10)
btn_exit.grid(row=0, column=1, padx=5)

# Pornirea interfeței grafice
root.mainloop()
