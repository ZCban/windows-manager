import subprocess
import threading

# Creazione di un lock per sincronizzare l'accesso all'output
print_lock = threading.Lock()

def set_service_automatic(service_name):
    try:
        # Comando PowerShell per impostare il servizio in modalità automatica
        command = f'Set-Service -Name "{service_name}" -StartupType "Automatic"'
        subprocess.run(['powershell', '-Command', command], check=True)
        with print_lock:
            print(f"Servizio {service_name} impostato su avvio automatico.")
    except subprocess.CalledProcessError as e:
        with print_lock:
            print(f"Errore nell'impostare il servizio {service_name}: {e}")

# Lista dei servizi da impostare su avvio automatico
services_to_set_automatic = ["vgk", "vgc", "RiotClientServices"]  # Riot Vanguard e altri servizi

# Numero massimo di thread in esecuzione contemporaneamente
max_threads = 3

# Lista per tracciare i thread attivi
active_threads = []

for service in services_to_set_automatic:
    while len(active_threads) >= max_threads:
        # Aspetta che almeno un thread termini
        for thread in active_threads:
            if not thread.is_alive():
                active_threads.remove(thread)
                break

    # Crea e avvia un nuovo thread
    thread = threading.Thread(target=set_service_automatic, args=(service,))
    active_threads.append(thread)
    thread.start()

# Aspetta che tutti i thread terminino
for thread in active_threads:
    thread.join()

print("Tutti i servizi sono stati impostati su avvio automatico.")
