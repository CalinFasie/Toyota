from db import get_connection
from logger import log_info, log_error
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from tkinter import messagebox

# Configurare globală SMTP (aceasta trebuie să fie definită înainte de funcții!)
SMTP_SERVER = "mail.carscenter.ro"
SMTP_PORT = 587
SMTP_USER = "report@carscenter.ro"
SMTP_PASSWORD = "#I4X#@qYqoNG"

def save_order(comanda, consilier, email, email_sp):
    """ Salvează comanda și înregistrează evenimentul în log """
    conn = get_connection()
    if not conn:
        log_error("Eroare la conectare la baza de date în save_order()")
        messagebox.showerror("Eroare", "Nu se poate conecta la baza de date!")
        return

    try:
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Inserare comandă
        query = """INSERT INTO _comenzi (comanda, data_inc, data_citit, ok, culoare, consilier, email, email_sp) 
                   VALUES (?, ?, NULL, 0, 'red', ?, ?, ?)"""
        cursor.execute(query, (comanda, now, consilier, email, email_sp))
        conn.commit()
        conn.close()

        log_info(f"Comandă salvată: {comanda} pentru consilierul {consilier}")

        send_email(comanda, consilier, email, email_sp)
        messagebox.showinfo("Succes", "Comanda a fost salvată și emailul a fost trimis!")

    except Exception as e:
        log_error(f"Eroare la salvare comenzii {comanda}: {e}")
        messagebox.showerror("Eroare", f"Eroare la salvare: {e}")

def mark_as_read(order_id):
    """ Marchează o comandă ca citită și schimbă culoarea în verde """
    conn = get_connection()
    if not conn:
        log_error("Eroare la conectare la baza de date în mark_as_read()")
        messagebox.showerror("Eroare", "Nu se poate conecta la baza de date!")
        return

    try:
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """UPDATE _comenzi SET data_citit = ?, culoare = 'green' WHERE id = ?"""
        cursor.execute(query, (now, order_id))
        conn.commit()
        conn.close()

        log_info(f"Comanda ID {order_id} marcată ca citită")

    except Exception as e:
        log_error(f"Eroare la marcarea ca citită a comenzii {order_id}: {e}")
        messagebox.showerror("Eroare", f"Eroare la actualizarea comenzii: {e}")

def send_email(comanda, consilier, email, email_sp):
    """ Trimite un email și înregistrează în log """
    try:
        msg = MIMEText(f"Comandă completa: {comanda} pentru consilierul {consilier}.")
        msg["Subject"] = "Comandă completa în sistem"
        msg["From"] = SMTP_USER
        msg["To"] = f"{email}, {email_sp}"

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [email, email_sp], msg.as_string())
        server.quit()

        log_info(f"Email trimis pentru comanda {comanda} către {email}, {email_sp}")

    except Exception as e:
        log_error(f"Eroare la trimiterea emailului pentru comanda {comanda}: {e}")
        messagebox.showerror("Eroare email", f"Eroare la trimiterea emailului: {e}")
