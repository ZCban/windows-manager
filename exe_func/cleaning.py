import os
import subprocess
import threading

def clean_windows(terminal_insert):
    threading.Thread(target=_clean_windows, args=(terminal_insert,)).start()

def _clean_windows(terminal_insert):
    # Define the path to the cleaner directory on the C drive
    cleaner_directory = os.path.join('C:', 'cleaner')
    
    if not os.path.isdir(cleaner_directory):
        terminal_insert(f"La cartella {cleaner_directory} non esiste.\n")
        return
    
    files = os.listdir(cleaner_directory)
    python_files = [file for file in files if file.endswith('.py')]
    
    if not python_files:
        terminal_insert('Nessun file Python trovato nella cartella cleaner.\n')
        return
    
    for python_file in python_files:
        file_path = os.path.join(cleaner_directory, python_file)
        terminal_insert(f"Eseguendo {python_file}...\n")
        # Capture both stdout and stderr
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        terminal_insert(result.stdout)
        terminal_insert(result.stderr)
    
    terminal_insert('########################################################\n')
    terminal_insert('Pulizia Completata\n')
