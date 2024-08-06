import subprocess
import time
import os
import shutil

def run_powershell_command(command, capture_output=True):
    """Esegue un comando PowerShell e ritorna l'output."""
    try:
        completed_process = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=capture_output, text=True, check=True
        )
        if capture_output:
            print(completed_process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando: {e}")
        if capture_output:
            print(e.stdout)
            print(e.stderr)

def disinstalla_versione_precedente_DesktopAppInstaller():
    print("Disinstallazione delle versioni precedenti del pacchetto DesktopAppInstaller")
    run_powershell_command('Get-AppxPackage -Name "Microsoft.DesktopAppInstaller" | Remove-AppxPackage')

def ripristina_windows_store():
    print("Reset di Microsoft Store...")
    run_powershell_command('wsreset.exe', capture_output=False)
    time.sleep(1)  # Attende che lo Store si apra completamente
    print("Chiusura di Microsoft Store...")
    run_powershell_command('Stop-Process -Name "WinStore.App" -Force')
    print("Pulizia della cache del Microsoft Store...")
    cache_path = os.path.expandvars(r"%localappdata%\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalCache")
    
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
            print(f"Cache del Microsoft Store rimossa: {cache_path}")
        except Exception as e:
            print(f"Errore durante la rimozione della cache: {e}")
    else:
        print(f"La cartella di cache non esiste")


def ripristina_AppXManifest_app_predefinite():
    print("Ripristino AppXManifest delle app predefinite...")
    run_powershell_command('Get-AppxPackage | foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}')

def esegui_sfc():
    print("Esecuzione di SFC (System File Checker)...")
    try:
        subprocess.run(
            ["powershell", "-Command", "sfc /scannow"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando SFC: {e}")


def usa_dism():
    print("Utilizzo di DISM per riparare l'immagine del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "DISM /Online /Cleanup-Image /RestoreHealth"],
            check=True
        )
        print('completato')
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando DISM: {e}")


def aggiorna_sistema():
    print("Verifica e installazione degli aggiornamenti del sistema...")
    try:
        subprocess.run(
            ["powershell", "-Command", "Install-WindowsUpdate -AcceptAll -AutoReboot"],
            check=True, text=True
        )
        print("Comando Eseguito.")
    except subprocess.CalledProcessError as e:
        print("Aggiornamento del sistema non riuscito.")
        print(f"Errore: {e}")

def controlla_servizi_critici():
    servizi = [
        #"wuauserv",           # Windows Update
        "BITS",               # Background Intelligent Transfer Service
        "AppXSvc",            # AppX Deployment Service
        "TrustedInstaller",   # Windows Modules Installer
        "CryptSvc",           # Cryptographic Services
        "DcomLaunch",         # DCOM Server Process Launcher
        "EventLog",           # Windows Event Log
        "RpcSs",              # Remote Procedure Call
        "ShellHWDetection",   # Shell Hardware Detection
        "Winmgmt",            # Windows Management Instrumentation
        "LanmanWorkstation",  # Workstation
        "Spooler",            # Print Spooler
        "Netman",             # Network Connections
        "WlanSvc",            # WLAN AutoConfig
        "Dhcp",               # DHCP Client
        "Dnscache"            # DNS Client# Print Spooler
    ]
    for servizio in servizi:
        print(f"Verifica del servizio {servizio}...")
        output = run_powershell_command(f'Get-Service -Name {servizio}')
        if output:
            if "Running" not in output:
                print(f"Il servizio {servizio} non è in esecuzione. Avvio del servizio...")
                run_powershell_command(f'Start-Service -Name {servizio}')
            else:
                print(f"Il servizio {servizio} è già in esecuzione.")
            # Assicurati che il servizio sia impostato per avviarsi automaticamente
            run_powershell_command(f'Set-Service -Name {servizio} -StartupType Automatic')
        else:
            print(f"Impossibile ottenere informazioni sul servizio {servizio}.")


if __name__ == "__main__":
    disinstalla_versione_precedente_DesktopAppInstaller()
    ripristina_windows_store()
    ripristina_AppXManifest_app_predefinite()
    esegui_sfc()
    usa_dism()
    aggiorna_sistema()
    controlla_servizi_critici()

