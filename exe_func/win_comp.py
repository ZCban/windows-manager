import os
import subprocess
import shutil
import threading

def terminal_insert(text):
    """
    Log text output, modify this function as per actual GUI handling.
    """
    print(text)  # Modify as per actual GUI handling

def run_powershell_command(command):
    """
    Run a PowerShell command and print the result.
    """
    try:
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            terminal_insert("Comando eseguito con successo:\n" + stdout.decode())
        else:
            terminal_insert("Errore durante l'esecuzione del comando:\n" + stderr.decode())
    except Exception as e:
        terminal_insert(f"Errore durante l'esecuzione del comando PowerShell: {e}")

def run_command(command):
    """
    Run a command and print the result.
    """
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            terminal_insert("Command executed successfully:\n" + stdout.decode())
        else:
            terminal_insert("Error during command execution:\n" + stderr.decode())
    except Exception as e:
        terminal_insert(f"Error during command execution: {e}")

def install_winget():
    """
    Check if WinGet is installed, and if not, download and install it along with its dependencies.
    """
    winget_check_command = 'Get-Command winget -ErrorAction SilentlyContinue'
    winget_check = subprocess.run(["powershell", "-Command", winget_check_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if winget_check.returncode != 0:
        terminal_insert("winget non trovato. Inizio installazione...")
        
        urls = {
            "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle": "https://aka.ms/getwinget",
            "Microsoft.VCLibs.x64.14.00.Desktop.appx": "https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx",
            "Microsoft.UI.Xaml.2.7.x64.appx": "https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.7.3/Microsoft.UI.Xaml.2.7.x64.appx"
        }

        for filename, url in urls.items():
            download_command = f'Start-BitsTransfer -Source "{url}" -Destination "{filename}"'
            subprocess.run(["powershell", "-Command", download_command], check=True)
            terminal_insert(f"Scaricato {filename}")

        install_commands = [
            "Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx",
            "Add-AppxPackage Microsoft.UI.Xaml.2.7.x64.appx",
            "Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
        ]

        for command in install_commands:
            try:
                subprocess.run(["powershell", "-Command", command], check=True)
                terminal_insert(f"Installato {command.split()[-1]}")
            except subprocess.CalledProcessError as e:
                terminal_insert(f"Errore durante l'installazione del pacchetto: {e}")

        for filename in urls.keys():
            remove_command = f'Remove-Item {filename}'
            subprocess.run(["powershell", "-Command", remove_command], check=True)
            terminal_insert(f"Rimosso {filename}")

    else:
        terminal_insert("winget già installato. Procedo con le altre installazioni...")

    update_command = 'winget source update --accept-source-agreements'
    subprocess.run(["powershell", "-Command", update_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    terminal_insert("Aggiornate le sorgenti di winget")

def uninstall_winget():
    """
    Uninstall WinGet and related components.
    """
    commands = [
        'Get-AppxPackage Microsoft.DesktopAppInstaller | Remove-AppxPackage',
        'Get-AppxPackage Microsoft.UI.Xaml.2.7 | Remove-AppxPackage -ErrorAction SilentlyContinue'
    ]
    
    for command in commands:
        run_powershell_command(command)
    
    paths_to_clean = [
        os.path.expandvars(r'%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet'),
        os.path.expandvars(r'%ProgramFiles%\WindowsApps\Microsoft.DesktopAppInstaller*')
    ]
    
    for path in paths_to_clean:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    terminal_insert(f"Rimossa la directory: {path}")
                else:
                    os.remove(path)
                    terminal_insert(f"Rimosso il file: {path}")
            else:
                terminal_insert('Nessun file residuo trovato.')
        except Exception as e:
            terminal_insert(f"Errore durante la pulizia del percorso {path}: {e}")

def install_chocolatey():
    """
    Install Chocolatey package manager.
    """
    choco_check_command = 'Get-Command choco -ErrorAction SilentlyContinue'
    choco_check = subprocess.run(["powershell", "-Command", choco_check_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if choco_check.returncode == 0:
        terminal_insert("Chocolatey è già installato.")
    else:
        try:
            install_command = (
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "[System.Net.ServicePointManager]::SecurityProtocol = "
                "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            )
            subprocess.run(["powershell", "-Command", install_command], check=True)
            terminal_insert("Chocolatey installato con successo.")
        except subprocess.CalledProcessError as e:
            terminal_insert(f"Errore nell'installazione di Chocolatey: {e}")

def uninstall_chocolatey():
    """
    Uninstall Chocolatey and clean up residual files.
    """
    choco_check_command = 'Get-Command choco -ErrorAction SilentlyContinue'
    choco_check = subprocess.run(["powershell", "-Command", choco_check_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if choco_check.returncode != 0:
        terminal_insert("Chocolatey non trovato. Procedo con la pulizia dei file residui...")
    else:
        command = 'choco uninstall chocolatey -y'
        run_powershell_command(command)
    
    paths_to_clean = [
        os.path.expandvars(r'%ProgramData%\chocolatey'),
        os.path.expandvars(r'%ProgramData%\chocolateyinstall'),
        os.path.expandvars(r'%ChocolateyInstall%')
    ]
    
    for path in paths_to_clean:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    terminal_insert(f"Rimossa la directory: {path}")
                else:
                    os.remove(path)
                    terminal_insert(f"Rimosso il file: {path}")
            else:
                terminal_insert('Nessun file residuo trovato.')
        except Exception as e:
            terminal_insert(f"Errore durante la pulizia del percorso {path}: {e}")

def uninstall_and_clean_comp(microsoft_apps, residual_paths):
    """
    Uninstall specified Microsoft components and clean up residual files.
    """
    for package in microsoft_apps:
        command = f'winget uninstall {package} --silent'
        run_powershell_command(command)
    
    for path in residual_paths:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    terminal_insert(f"Rimossa la directory: {path}")
                else:
                    os.remove(path)
                    terminal_insert(f"Rimosso il file: {path}")
            else:
                terminal_insert('Nessun file residuo trovato.')
        except Exception as e:
            terminal_insert(f"Errore durante la pulizia del percorso {path}: {e}")

def uninstall_win_comp():
    """
    Uninstall various Microsoft components and clean up residual files.
    """
    microsoft_apps = [
        'Microsoft.VCRedist.2008.x86',
        'Microsoft.VCRedist.2008.x64',
        'Microsoft.VCRedist.2010.x86',
        'Microsoft.VCRedist.2010.x64',
        'Microsoft.VCRedist.2012.x86',
        'Microsoft.VCRedist.2012.x64',
        'Microsoft.VCRedist.2013.x86',
        'Microsoft.VCRedist.2013.x64',
        'Microsoft.VCRedist.2015+.x86',
        'Microsoft.VCRedist.2015+.x64',
        'Microsoft.DirectX',
        'Microsoft.DotNet.Framework.DeveloperPack_4'
    ]
    
    residual_paths = [
        os.path.expandvars(r'%SystemDrive%\Program Files (x86)\Common Files\Microsoft Shared\VC'),
        os.path.expandvars(r'%SystemDrive%\Program Files\Common Files\Microsoft Shared\VC'),
        os.path.expandvars(r'%SystemDrive%\Program Files (x86)\Microsoft DirectX'),
        os.path.expandvars(r'%SystemDrive%\Program Files\Microsoft DirectX'),
        os.path.expandvars(r'%SystemDrive%\Program Files\dotnet'),
        os.path.expandvars(r'%SystemDrive%\Program Files (x86)\dotnet'),
    ]

    uninstall_and_clean_comp(microsoft_apps, residual_paths)

def install_and_clean_comp(microsoft_apps):
    """
    Install specified Microsoft components using WinGet.
    """
    for package in microsoft_apps:
        check_command = f'winget list {package} -q'
        check_result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        if package in check_result.stdout.decode():
            terminal_insert(f"{package} is already installed.")
        else:
            terminal_insert(f"Installing {package}...")
            install_command = f'winget install {package} --accept-package-agreements --accept-source-agreements'
            run_command(install_command)

def install_win_comp():
    """
    Install various Microsoft components.
    """
    microsoft_apps = [
        'Microsoft.VCRedist.2008.x86',
        'Microsoft.VCRedist.2008.x64',
        'Microsoft.VCRedist.2010.x86',
        'Microsoft.VCRedist.2010.x64',
        'Microsoft.VCRedist.2012.x86',
        'Microsoft.VCRedist.2012.x64',
        'Microsoft.VCRedist.2013.x86',
        'Microsoft.VCRedist.2013.x64',
        'Microsoft.VCRedist.2015+.x86',
        'Microsoft.VCRedist.2015+.x64',
        'Microsoft.DirectX',
        'Microsoft.DotNet.Framework.DeveloperPack_4'
    ]

    install_and_clean_comp(microsoft_apps)

def set_execution_policy():
    """
    Ensure execution policy is set to allow script running
    """
    check_policy_command = 'Get-ExecutionPolicy -Scope CurrentUser'
    current_policy = subprocess.run(["powershell", "-Command", check_policy_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if "Unrestricted" in current_policy.stdout.decode():
        terminal_insert("Execution policy is already set to Unrestricted.")
    else:
        try:
            subprocess.run(["powershell", "Set-ExecutionPolicy", "Unrestricted", "-Scope", "CurrentUser"], check=True)
            terminal_insert("Execution policy set to Unrestricted.")
        except subprocess.CalledProcessError as e:
            terminal_insert(f"Errore nell'impostazione dell'execution policy: {e}")

def uninstall():
    """
    Threaded function to uninstall components.
    """
    def target():
        set_execution_policy()
        uninstall_win_comp()
        uninstall_winget()
        uninstall_chocolatey()
        print('Finito')
    threading.Thread(target=target).start()

def install():
    """
    Threaded function to install components.
    """
    def target():
        set_execution_policy()
        install_winget()
        install_win_comp()
        install_chocolatey()
        print('Finito')
    threading.Thread(target=target).start()

#uninstall()
#install()


