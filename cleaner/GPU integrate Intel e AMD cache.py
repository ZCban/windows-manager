import os
import shutil

def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Errore durante l\'eliminazione del file {file_path}. Eccezione: {e}')
        print(f'Pulizia della directory {directory} completata.')
    else:
        print(f'La directory {directory} non esiste')

def clean_integrated_intel():
    # Cache degli shader Intel
    intel_cache_dirs = [
        os.path.expandvars(r'%LocalAppData%\..\LocalLow\Intel\ShaderCache'),
        os.path.expandvars(r'%LocalAppData%\..\LocalLow\Intel\DxCache')
    ]
    for directory in intel_cache_dirs:
        print(f'Pulizia della cache degli shader Intel: {directory}')
        clear_directory(directory)

def clean_integrated_amd():
    # Cache degli shader AMD
    amd_cache_dirs = [
        os.path.expandvars(r'%LocalAppData%\AMD\DxCache'),
        os.path.expandvars(r'%LocalAppData%\AMD\GLCache')
    ]
    for directory in amd_cache_dirs:
        print(f'Pulizia della cache degli shader AMD: {directory}')
        clear_directory(directory)

# Esegui la pulizia per Intel
clean_integrated_intel()

# Esegui la pulizia per AMD
clean_integrated_amd()

