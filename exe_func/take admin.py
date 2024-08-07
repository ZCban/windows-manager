import os
import sys
import ctypes
import subprocess

def is_admin():
    """Verifica se l'utente attuale ha privilegi di amministratore."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def get_current_username():
    """Ottieni il nome utente corrente."""
    try:
        return os.getlogin()
    except Exception as e:
        print(f"Errore durante il recupero del nome utente corrente: {e}")
        sys.exit(1)

def user_exists(username):
    """Verifica se l'utente esiste nel sistema."""
    try:
        result = subprocess.run(["net", "user", username], capture_output=True, text=True)
        return "Nome utente" in result.stdout or "User name" in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la verifica dell'esistenza dell'utente: {e}")
        return False

def add_user_to_admin_group(username):
    """Aggiungi l'utente al gruppo degli amministratori."""
    try:
        subprocess.run(["net", "localgroup", "Administrators", username, "/add"], check=True)
        print(f"L'utente {username} è stato aggiunto al gruppo degli amministratori.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'aggiunta dell'utente al gruppo degli amministratori: {e}")

if __name__ == "__main__":
    if not is_admin():
        print("Questo script deve essere eseguito come amministratore.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)
    
    username = get_current_username()
    print(f"Utente corrente: {username}")

    if user_exists(username):
        add_user_to_admin_group(username)
    else:
        print(f"L'utente {username} non esiste nel sistema.")


