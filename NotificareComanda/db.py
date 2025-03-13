import pyodbc

# Configurarea conexiunii la SQL Server
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=or-sql\\am;"
    "DATABASE=gmro011p;"
    "UID=sa;"
    "PWD=am@123#;"
)

def get_connection():
    """ Returnează o conexiune la baza de date SQL Server """
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("Eroare la conectare:", e)
        return None