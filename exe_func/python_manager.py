import subprocess
import sys
import os
import time
import threading

# Lista delle librerie da installare
libraries_to_install = [
    "wmi",
    "mss",
    "numpy",
    "pywin32",
    "pyyaml",
    "requests",
    "ipython",
    "psutil",
    "gitpython",
    "opencv-python",
    "scipy",
    "thop",
    "tqdm",
    "tensorboard",
    "keyboard",
    "pandas",
    "translate",
    "pytube",
    "openai",
    "rich",
    "pygame",
    "pyserial",
    "colorama",
    "onnxruntime-directml",
    "pefile",
    "matplotlib",
    "seaborn",
    "gradio",
    "ultralytics"
]

# Lista delle librerie specifiche da disinstallare
libraries_to_uninstall = ["onnx_graphsurgeon", "graphsurgeon", "uff", "tensorrt"]

def upgrade_pip():
    print("Aggiornamento di pip alla versione più recente...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("Aggiornamento di pip completato.")

def install_libraries(libraries):
    for library in libraries:
        try:
            print(f"Installazione di {library} iniziata...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"Installazione di {library} completata.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione di {library}: {e}")

def uninstall_library(library):
    try:
        print(f"Disinstallazione di {library} iniziata...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", library, "-y"])
        print(f"Disinstallazione di {library} completata.")
    except subprocess.CalledProcessError as e:
        print(f"Errore nella disinstallazione di {library}: {e}")

def backup_installed_libraries(backup_file):
    print(f"Salvataggio della lista delle librerie Python installate in {backup_file}...")
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    with open(backup_file, 'w') as file:
        for line in result.stdout.splitlines():
            library_name = line.split('==')[0]
            file.write(library_name + '\n')
    print(f"Lista delle librerie Python installate salvata in {backup_file}.")

def uninstall_libraries_from_backup(backup_file):
    print(f"Disinstallazione delle librerie Python da {backup_file} iniziata...")
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-r", backup_file, "-y"])
    print("Disinstallazione completata.")

def clean_pip_cache():
    cache_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'pip', 'Cache')
    if os.path.exists(cache_dir):
        print("Pulizia della cartella cache di pip iniziata...")
        subprocess.check_call(['rmdir', '/s', '/q', cache_dir], shell=True)
        print("Pulizia della cartella cache completata.")
    else:
        print("La cartella cache di pip non esiste o è già stata pulita.")

def update_all_libraries():
    print("Aggiornamento di tutte le librerie Python installate all'ultima versione...")
    installed_packages = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True)
    for line in installed_packages.stdout.splitlines():
        package = line.split('==')[0]
        old_version = line.split('==')[1]
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            new_version = subprocess.run([sys.executable, "-m", "pip", "show", package], capture_output=True, text=True)
            for line in new_version.stdout.splitlines():
                if line.startswith("Version:"):
                    new_version = line.split()[1]
                    break
            print(f"Aggiornamento di {package}: {old_version} -> {new_version} completato.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'aggiornamento di {package} ({old_version}): {e}")

###################extra######################################################
def install_Nvidia_Cuda():
    print("Installazione di CUDA con winget iniziata...")
    try:
        subprocess.check_call(["winget", "install", "--id=Nvidia.CUDA", "-e", "--accept-source-agreements"])
        print("Installazione di CUDA con winget completata.")
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'installazione di CUDA con winget: {e}")
        
def install_torch_cuda_124():
    print("Installazione di Torch con supporto CUDA iniziata...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu124"])
        print("Installazione di Torch con supporto CUDA completata.")
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'installazione di Torch con supporto CUDA: {e}")

def remove_existing_path(path_to_remove):
    # Read the current PATH environment variable
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_READ) as key:
        value, _ = winreg.QueryValueEx(key, "PATH")
    
    # Split the PATH variable into individual paths
    paths = value.split(';')

    # Remove the existing path if it's in the PATH variable
    if path_to_remove in paths:
        paths.remove(path_to_remove)
    
    # Reconstruct the PATH variable
    new_value = ';'.join(paths)
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_value)

def install_cudnn():
    # Install nvidia-cudnn-cu12 via pip
    subprocess.run(["pip", "install", "nvidia-cudnn-cu12"], check=True)

def find_cudnn_dll():
    # Search for cudnn64_8.dll on the C: drive
    for root, dirs, files in os.walk('C:\\'):
        if 'cudnn64_8.dll' in files:
            return os.path.join(root, 'cudnn64_8.dll')
    return None

def add_to_path(new_path):
    # Read the current PATH environment variable
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_READ) as key:
        value, _ = winreg.QueryValueEx(key, "PATH")
    
    # Add the new path if it's not already in PATH
    if new_path not in value:
        new_value = value + ";" + new_path
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_value)

def auto_install_cudnn():
    # Step 1: Find existing cudnn64_8.dll and remove its path from PATH
    cudnn_dll_path = find_cudnn_dll()
    if cudnn_dll_path:
        cudnn_bin_path = os.path.dirname(cudnn_dll_path)
        remove_existing_path(cudnn_bin_path)
        print(f"Removed existing path: {cudnn_bin_path}")
    else:
        print("No existing cudnn64_8.dll found")

    # Step 2: Install cuDNN
    install_cudnn()

    # Step 3: Find cudnn64_8.dll again after installation
    cudnn_dll_path = find_cudnn_dll()
    if cudnn_dll_path:
        cudnn_bin_path = os.path.dirname(cudnn_dll_path)
        print(f"Found cudnn64_8.dll at: {cudnn_bin_path}")
        
        # Step 4: Add to PATH
        add_to_path(cudnn_bin_path)
        print(f"Added {cudnn_bin_path} to PATH")
    else:
        print("cudnn64_8.dll not found after installation")


def uninstall_a():
    upgrade_pip()

    for library in libraries_to_uninstall:
        uninstall_library(library)

    backup_file = "backup.txt"
    backup_installed_libraries(backup_file)
    uninstall_libraries_from_backup(backup_file)
    clean_pip_cache()

def install_a():
    upgrade_pip()
    install_libraries(libraries_to_install)

def auto_c():
    install_Nvidia_Cuda()
    auto_install_cudnn()
    install_torch_cuda_124()

def uninstall_all():
    def target():
        uninstall_a()
        print('Finito')
    threading.Thread(target=target).start()

def install_all():
    def target():
        install_a()
        print('Finito')
    threading.Thread(target=target).start()

def auto_cuda():
    def target():
        auto_c()
        print('Finito')
    threading.Thread(target=target).start()
