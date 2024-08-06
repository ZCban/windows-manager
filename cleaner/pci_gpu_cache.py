import os
import shutil
import time
import subprocess

def clear_amd_cache():
    # Ottieni il percorso della directory principale dell'utente corrente
    user_home = os.path.expanduser('~')
    base_cache_path = os.path.join(user_home, "AppData", "Local", "AMD")

    # Percorsi della cache
    dx_cache_path = os.path.join(base_cache_path, "DxCache")
    ogl_cache_path = os.path.join(base_cache_path, "OglCache")
    vk_cache_path = os.path.join(base_cache_path, "VkCache")

    # Funzione per cancellare i file all'interno di una cartella
    def clear_cache(cache_path):
        if os.path.exists(cache_path):
            for root, dirs, files in os.walk(cache_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"File rimosso: {file_path}")
                    except Exception as e:
                        print(f"Errore nella rimozione forse serve a sistema {file_path}")
        else:
            print(f"La cartella {cache_path} non esiste")

    # Cancella le cache
    clear_cache(dx_cache_path)
    clear_cache(ogl_cache_path)
    clear_cache(vk_cache_path)

def clear_nvidia_cache():
    # Specifica il percorso della directory da svuotare
    directory = os.path.expandvars(r'%AppData%\..\LocalLow\NVIDIA\PerDriverVersion\DXCache')

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
                if "[WinError 32]" in str(e):
                    print(f'Non elimino, serve al sistema: {file_path}')
                else:
                    print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print('Pulizia dxcache completata.')
    else:
        print(f'La directory {directory} non esiste')

    # Specifica il percorso della directory da svuotare
    directory = os.path.expandvars(r'%AppData%\..\Local\NVIDIA\GLCache')

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
        print('Pulizia glcache completata.')
    else:
        print(f'La directory {directory} non esiste')


if __name__ == "__main__":
    clear_amd_cache()
    print("Pulizia della cache AMD completata.")
    clear_nvidia_cache()
    print("Pulizia della cache NVIDIA completata.")
    
