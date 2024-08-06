import subprocess
import os
import sys
import time
import platform
import wmi
import shutil


#########################################################################
##DDU 
########################################################################
class DisplayDriverUninstaller:
    ddu_path = None

    @classmethod
    def is_ddu_installed(cls):
        try:
            result = subprocess.run(['winget', 'list', '--source=winget', 'Display Driver Uninstaller'], capture_output=True, text=True)
            return 'Display Driver Uninstaller' in result.stdout
        except Exception as e:
            print(f"Error checking for DDU: {e}")
            return False

    @classmethod
    def install_ddu(cls):
        try:
            subprocess.run(['winget', 'install', '--id=TeamDDU.DisplayDriverUninstaller'], check=True)
        except Exception as e:
            print(f"Error installing DDU: {e}")

    @classmethod
    def find_ddu_path(cls):
        default_paths = [
            r'C:\Program Files\Display Driver Uninstaller',
            r'C:\Program Files (x86)\Display Driver Uninstaller'
        ]
        for path in default_paths:
            if os.path.exists(path):
                cls.ddu_path = path
                return path
        return None

    @classmethod
    def get_gpu_manufacturer(cls):
        try:
            result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'name'], capture_output=True, text=True)
            output = result.stdout.lower()
            if 'amd' in output:
                return 'AMD'
            elif 'nvidia' in output:
                return 'NVIDIA'
            elif 'intel' in output:
                return 'Intel'
            else:
                return None
        except Exception as e:
            print(f"Error detecting GPU manufacturer: {e}")
            return None

    @classmethod
    def execute_ddu_command(cls, gpu_manufacturer):
        commands = {
            'AMD': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent  -cleanamd -NoRestorePoint  -RemoveAMDCP -RemoveAMDKMPFD -RemoveAudioBus  -removeamddirs -removecrimsoncache -removemonitors -cleanallgpus',
            'NVIDIA': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent  -cleannvidia -NoRestorePoint -RemovePhysx -RemoveGFE -RemoveNVBROADCAST -RemoveNVCP    -RemoveVulkan -removemonitors -removenvidiadirs -remove3dtvplay -cleanallgpus',
            'Intel': f'"{cls.ddu_path}\\Display Driver Uninstaller.exe" -silent  -cleanintel -NoRestorePoint  -RemoveINTELCP  -RemoveVulkan -removemonitors  -cleanallgpus'
        }
        command = commands.get(gpu_manufacturer)
        if command:
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(f"Error executing DDU command: {e}")
        else:
            print("Unsupported GPU manufacturer or no GPU detected.")

    @classmethod
    def restart_system(cls):
        try:
            subprocess.run(["shutdown", "/r", "/t", "3"], check=True)
            print("System will restart in 3 seconds.")
        except subprocess.CalledProcessError as e:
            print(f"Error initiating system restart: {e}")

    @classmethod
    def auto_uninstall(cls):
        if not cls.is_ddu_installed():
            print("DDU is not installed. Installing...")
            cls.install_ddu()
        
        cls.ddu_path = cls.find_ddu_path()
        if not cls.ddu_path:
            print("DDU installation path not found.")
            sys.exit(1)

        gpu_manufacturer = cls.get_gpu_manufacturer()
        if gpu_manufacturer:
            print(f"Detected GPU Manufacturer: {gpu_manufacturer}")
            cls.execute_ddu_command(gpu_manufacturer)
            cls. restart_system()
        else:
            print("No supported GPU manufacturer detected or an error occurred. Try to reinstall Driver")

        

#########################################################################
##driver manager
########################################################################

class DriverInstaller:
    wmi_instance = wmi.WMI()

    @classmethod
    def install_chocolatey(cls):
        try:
            install_command = (
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "[System.Net.ServicePointManager]::SecurityProtocol = "
                "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            )
            subprocess.run(["powershell", "-Command", install_command], check=True)
            print("Chocolatey installato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione di Chocolatey: {e}")

    @classmethod
    def uninstall_amd_ryzen_chipset(cls):
        try:
            subprocess.run(["choco", "uninstall", "amd-ryzen-chipset", "-y", "--force"], check=True)
            print("Driver AMD Ryzen Chipset disinstallati con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nella disinstallazione dei driver AMD Ryzen Chipset: {e}")

    @classmethod
    def install_amd_ryzen_chipset(cls):
        try:
            subprocess.run(["choco", "install", "amd-ryzen-chipset", "-y"], check=True)
            print("Driver AMD Ryzen Chipset installati con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione dei driver AMD Ryzen Chipset: {e}")

    @classmethod
    def install_intel_dsa(cls):
        try:
            command = 'choco install intel-dsa -y --ignore-checksums'
            subprocess.run(command, shell=True, check=True)
            print("Intel Driver & Support Assistant installation initiated.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during installation: {e}")

    @classmethod
    def install_intel_network_drivers_win10(cls):
        try:
            command = 'choco install intel-network-drivers-win10 -y'
            subprocess.run(command, shell=True, check=True)
            print("Intel Network Drivers for Windows 10 installation initiated.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during installation: {e}")

    @classmethod
    def install_intel_arc_graphics_driver(cls):
        try:
            command = 'choco install intel-arc-graphics-driver -y'
            subprocess.run(command, shell=True, check=True)
            print("Intel Arc Graphics Driver installation initiated.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during installation: {e}")

    @classmethod
    def install_nvidia_driver(cls):
        directories = [
            "C:\\Program Files\\NVIDIA Corporation",
            "C:\\Program Files (x86)\\NVIDIA Corporation",
            os.path.join(os.environ['APPDATA'], "NVIDIA"),
            os.path.join(os.environ['LOCALAPPDATA'], "NVIDIA"),
            os.path.join(os.environ['LOCALAPPDATA'], "NVIDIA Corporation"),
            os.path.join(os.environ['USERPROFILE'], "AppData\\LocalLow\\NVIDIA")
        ]
        for directory in directories:
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                    print(f"Removed residual files in {directory}.")
                except Exception as e:
                    print(f"Error removing residual files in {directory}: {e}")
            else:
                print(f"No residual files found in {directory}.")
        try:
            subprocess.run(["choco", "install", "nvidia-display-driver", "-y", "--force"], check=True)
            print("NVIDIA drivers installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing NVIDIA drivers: {e}")

    @classmethod
    def install_realtek_hd_audio_driver(cls):
        try:
            command = 'choco install realtek-hd-audio-driver -y'
            subprocess.run(command, shell=True, check=True)
            print("Realtek HD Audio Driver installation initiated.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during installation: {e}")

    @classmethod
    def install_samsung_universal_printer_driver(cls):
        try:
            subprocess.run(["choco", "install", "supd2", "-y"], check=True)
            print("Samsung Universal Printer Driver installato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione del Samsung Universal Printer Driver: {e}")

    @classmethod
    def install_hp_universal_print_driver(cls):
        try:
            subprocess.run(["choco", "install", "hp-universal-print-driver-pcl", "-y"], check=True)
            print("HP Universal Print Driver installato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'installazione dell'HP Universal Print Driver: {e}")


    @classmethod
    def restart_system(cls):
        try:
            subprocess.run(["shutdown", "/r", "/t", "3"], check=True)
            print("System will restart in 3 seconds.")
        except subprocess.CalledProcessError as e:
            print(f"Error initiating system restart: {e}")

    

    @classmethod
    def get_cpu_info(cls):
        cpu_info = {'Processor': platform.processor()}
        try:
            for cpu in cls.wmi_instance.Win32_Processor():
                cpu_info.update({
                    'Name': cpu.Name,
                    'Manufacturer': cpu.Manufacturer,
                    'NumberOfCores': cpu.NumberOfCores,
                    'NumberOfLogicalProcessors': cpu.NumberOfLogicalProcessors,
                    'PNPDeviceID': cpu.PNPDeviceID
                })
        except Exception as e:
            print(f"Error retrieving CPU info: {e}")
        return cpu_info

    @classmethod
    def get_gpu_info(cls):
        gpu_info = []
        try:
            for video in cls.wmi_instance.Win32_VideoController():
                brand = 'Unknown'
                driver_package = None
                for key, value in {'VEN_10DE': {'brand': 'NVIDIA', 'driver_package': 'nvidia-display-driver'},
                                   'VEN_1002': {'brand': 'AMD', 'driver_package': 'amd-ryzen-chipset'},
                                   'VEN_8086': {'brand': 'Intel', 'driver_package': 'intel-arc-graphics-driver'}}.items():
                    if key in video.PNPDeviceID:
                        brand = value['brand']
                        driver_package = value['driver_package']
                        break
                gpu_info.append({
                    'DriverName': video.Name,
                    'Brand': brand,
                    'DriverPackage': driver_package
                })
        except Exception as e:
            print(f"Error retrieving GPU info: {e}")
        return gpu_info

    @classmethod
    def get_audio_info(cls):
        audio_info = []
        try:
            for sound in cls.wmi_instance.Win32_SoundDevice():
                audio_info.append({
                    'Name': sound.Name,
                    'Manufacturer': sound.Manufacturer,
                    'Status': sound.Status
                })
        except Exception as e:
            print(f"Error retrieving audio info: {e}")
        return audio_info

    @classmethod
    def get_printer_info_usb(cls):
        printer_info = []
        try:
            for device in cls.wmi_instance.Win32_PnPEntity():
                # Check for common printer-related keywords
                if device.Description and any(keyword in device.Description.lower() for keyword in ['printer', 'print']):
                    printer_info.append({
                        'Name': device.Name,
                        'Description': device.Description,
                        'PNPDeviceID': device.PNPDeviceID,
                        'Status': device.Status
                    })
        except Exception as e:
            print(f"Error retrieving printer info: {e}")
        return printer_info

    @classmethod
    def auto_install_drivers(cls):
        cls.install_chocolatey()
        cpu_info = cls.get_cpu_info()
        gpu_infos = cls.get_gpu_info()

        cpu_manufacturer = cpu_info.get('Manufacturer', '').lower()
        if 'amd' in cpu_manufacturer:
            cls.install_amd_ryzen_chipset()
        elif 'intel' in cpu_manufacturer:
            print("Support for Intel CPU drivers is not yet implemented.")
        else:
            print(f"CPU manufacturer {cpu_manufacturer} not supported for automatic driver installation.")

        for gpu_info in gpu_infos:
            brand = gpu_info.get('Brand', '').lower()
            if brand:
                if 'nvidia' in brand:
                    cls.install_nvidia_driver()
                elif 'intel' in brand:
                    cls.install_intel_arc_graphics_driver()
                elif 'amd' in brand:
                    print('Support for AMD GPU drivers is not yet implemented.')
            else:
                print(f"GPU {gpu_info.get('Name', 'Unknown')} not supported for automatic driver installation.")

        # Check and install audio drivers if Realtek is found
        print("Retrieving audio information...")
        audio_infos = cls.get_audio_info()
        for audio_info in audio_infos:
            print(f"Checking audio device: {audio_info.get('Name', '')}")
            if 'realtek' in audio_info.get('Name', '').lower():
                print("Realtek audio device found, initiating driver installation.")
                cls.install_realtek_hd_audio_driver()
            else:
                print("audio device not supported.")

        # Check and install Samsung Universal Printer Driver if Samsung printer is found
        print("Retrieving printer information...")
        printer_infos = cls.get_printer_info_usb()
        for printer_info in printer_infos:
            description_lower = printer_info.get('Description', '').lower()
            print(f"Checking printer device: {printer_info.get('Description', '')}")
            if 'samsung' in description_lower:
                print("Samsung printer found, initiating driver installation.")
                cls.install_samsung_universal_printer_driver()
            elif 'hp' in description_lower:
                print("HP printer found, initiating driver installation.")
                cls.install_hp_universal_print_driver()
            else:
                print("printer device not supported.")

        cls. restart_system()

#EXEMPLE
#DisplayDriverUninstaller.auto_uninstall()
#DriverInstaller.auto_install_drivers()


