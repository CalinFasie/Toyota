import tkinter as tk
import subprocess

# Funcție pentru deschiderea interfeței corespunzătoare
def open_interface(user_type):
    if user_type == "Depozit":
        subprocess.Popen(["python", "user1.py"])
    elif user_type == "Consilieri":
        subprocess.Popen(["python", "user2.py"])

    root.destroy()  # Închide fereastra principală

# Crearea ferestrei principale
root = tk.Tk()
root.title("Selectează Modul")
root.geometry("300x150")

# Butoane pentru selecția modulului
btn_depozit = tk.Button(root, text="Depozit", command=lambda: open_interface("Depozit"), bg="green", fg="white", width=15)
btn_consilieri = tk.Button(root, text="Consilieri", command=lambda: open_interface("Consilieri"), bg="blue", fg="white", width=15)

btn_depozit.pack(pady=20)
btn_consilieri.pack(pady=10)

# Pornirea interfeței grafice
root.mainloop()
