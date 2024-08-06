import os
import shutil

def clean_programs_error_report():
    # Specifica il percorso della directory da svuotare
    directory = os.path.expandvars(r'%LOCALAPPDATA%\ElevatedDiagnostics')

    # Verifica se la directory esiste
    if os.path.exists(directory):
        # Elimina tutti i file e le sottocartelle nella directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Elimina il file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Elimina la directory e tutto il suo contenuto
            except PermissionError as e:
                print(f'Accesso negato durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia della directory Programs Error Report completata.')
    else:
        print(f'La directory {directory} non esiste')

def pulisci_directory(percorso_directory):
    """
    Pulisce tutti i file e le sottodirectory all'interno della directory specificata.
    
    Args:
    percorso_directory (str): Il percorso della directory da pulire.
    """
    # Espandi il percorso utente e rendilo assoluto
    percorso_directory = os.path.expanduser(percorso_directory)
    
    # Verifica che la directory esista
    if os.path.exists(percorso_directory):
        # Scorri attraverso tutti i file nella directory
        for filename in os.listdir(percorso_directory):
            file_path = os.path.join(percorso_directory, filename)
            try:
                # Verifica se il percorso è un file o un link simbolico e lo elimina
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"File {file_path} eliminato con successo.")
                # Verifica se il percorso è una directory e la elimina
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Directory {file_path} eliminata con successo.")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {file_path}: {e}")
    else:
        print(f"La directory {percorso_directory} non esiste.")

def pulisci_file_recenti():
    """
    Cancella tutti i file nella cartella dei file recenti in Esplora File su Windows.
    """
    # Ottiene il percorso della directory dei file recenti
    percorso_recenti = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Recent')

    # Verifica se la directory esiste
    if os.path.exists(percorso_recenti):
        # Elimina tutti i file nella cartella Recent
        for file_name in os.listdir(percorso_recenti):
            file_path = os.path.join(percorso_recenti, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                    print(f'File eliminato: {file_path}')
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f'Directory eliminata: {file_path}')
            except Exception as e:
                print(f'Errore durante l\'eliminazione di {file_path}: {e}')
    else:
        print(f'La directory {percorso_recenti} non esiste o non è accessibile.')

def clean_windows_temp():
    # Specifica il percorso della directory da svuotare
    directory = r'C:\Windows\Temp'

    # Verifica se la directory esiste
    if os.path.exists(directory):
        # Elimina tutti i file e le sottocartelle nella directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Elimina il file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Elimina la directory e tutto il suo contenuto
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia di C:\\Windows\\Temp completata.')
    else:
        print(f'La directory {directory} non esiste')

def clear_cryptnet_url_cache():
    # Percorso della cache CryptnetUrlCache
    directory = os.path.expandvars(r'%LocalAppData%\..\LocalLow\Microsoft\CryptnetUrlCache')

    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f'Errore durante l\'eliminazione della directory {dir_path}. Eccezione: {e}')
        print(f'Pulizia della CryptnetUrlCache completata.')
    else:
        print(f'La directory {directory} non esiste')

clear_cryptnet_url_cache()
clean_windows_temp()
pulisci_file_recenti()
# Esempio di utilizzo
pulisci_directory("~/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine")
# Chiamata alla funzione
clean_programs_error_report()
