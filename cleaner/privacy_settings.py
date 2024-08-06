import winreg
import subprocess

class PrivacySettingsDisabler:
    def disable_privacy_settings(self):
        self.disable_ad_tracking()
        self.disable_activity_history()
        self.disable_location_tracking()
        self.disable_diagnostics_feedback()
        self.disable_cortana()
        self.disable_typing_data_collection()
        self.disable_voice_data_collection()
        self.disable_feedback_notifications()
        self.disable_edge_privacy_settings()

    def disable_ad_tracking(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Pubblicità personalizzata disattivata.")
        except Exception as e:
            print(f"Errore durante la disattivazione della pubblicità personalizzata: {e}")

    def disable_activity_history(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\System', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'PublishUserActivities', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Cronologia delle attività disattivata.")
        except Exception as e:
            print(f"Errore durante la disattivazione della cronologia delle attività: {e}")

    def disable_location_tracking(self):
        try:
            subprocess.run(['powershell', '-Command', 'Set-Service -Name lfsvc -StartupType Disabled'], check=True)
            subprocess.run(['powershell', '-Command', 'Stop-Service -Name lfsvc'], check=True)
            print("Tracciamento della posizione disattivato.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la disattivazione del tracciamento della posizione: {e}")

    def disable_diagnostics_feedback(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\DataCollection', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowTelemetry', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Diagnostica e dati di feedback disattivati.")
        except Exception as e:
            print(f"Errore durante la disattivazione della diagnostica e dei dati di feedback: {e}")

    def disable_cortana(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\Windows Search', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Cortana disattivata.")
        except Exception as e:
            print(f"Errore durante la disattivazione di Cortana: {e}")

    def disable_typing_data_collection(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\InputPersonalization', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'RestrictImplicitTextCollection', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'RestrictImplicitInkCollection', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Raccolta dati sulla digitazione disattivata.")
        except Exception as e:
            print(f"Errore durante la disattivazione della raccolta dati sulla digitazione: {e}")

    def disable_voice_data_collection(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\Speech', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowInputPersonalization', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Raccolta dati sulla voce disattivata.")
        except FileNotFoundError:
            print("La chiave di registro per la raccolta dati sulla voce non è stata trovata.")

    def disable_feedback_notifications(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Siuf\Rules', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'NumberOfSIUFInPeriod', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Siuf\Rules', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'PeriodInNanoSeconds', 0, winreg.REG_QWORD, 0)
            winreg.CloseKey(key)
            print("Notifiche di feedback disattivate.")
        except Exception as e:
            print(f"Errore durante la disattivazione delle notifiche di feedback: {e}")

    def disable_edge_privacy_settings(self):
        try:
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\MicrosoftEdge\\Main" -Name "DoNotTrack" -Value 1'], check=True)
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Edge\\Privacy" -Name "SendDoNotTrackHeader" -Value 1'], check=True)
            print("Impostazioni di privacy di Microsoft Edge configurate.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la configurazione delle impostazioni di privacy di Microsoft Edge: {e}")

class PrivacySettingsEnabler:
    def enable_privacy_settings(self):
        self.enable_ad_tracking()
        self.enable_activity_history()
        self.enable_location_tracking()
        self.enable_diagnostics_feedback()
        self.enable_cortana()
        self.enable_typing_data_collection()
        self.enable_voice_data_collection()
        self.enable_feedback_notifications()
        self.enable_edge_privacy_settings()

    def enable_ad_tracking(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Enabled', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Pubblicità personalizzata attivata.")
        except Exception as e:
            print(f"Errore durante l'attivazione della pubblicità personalizzata: {e}")

    def enable_activity_history(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\System', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'PublishUserActivities', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Cronologia delle attività attivata.")
        except Exception as e:
            print(f"Errore durante l'attivazione della cronologia delle attività: {e}")

    def enable_location_tracking(self):
        try:
            subprocess.run(['powershell', '-Command', 'Set-Service -Name lfsvc -StartupType Automatic'], check=True)
            subprocess.run(['powershell', '-Command', 'Start-Service -Name lfsvc'], check=True)
            print("Tracciamento della posizione attivato.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'attivazione del tracciamento della posizione: {e}")

    def enable_diagnostics_feedback(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\DataCollection', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowTelemetry', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Diagnostica e dati di feedback attivati.")
        except Exception as e:
            print(f"Errore durante l'attivazione della diagnostica e dei dati di feedback: {e}")

    def enable_cortana(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\Windows Search', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Cortana attivata.")
        except Exception as e:
            print(f"Errore durante l'attivazione di Cortana: {e}")

    def enable_typing_data_collection(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\InputPersonalization', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'RestrictImplicitTextCollection', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'RestrictImplicitInkCollection', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Raccolta dati sulla digitazione attivata.")
        except Exception as e:
            print(f"Errore durante l'attivazione della raccolta dati sulla digitazione: {e}")

    def enable_voice_data_collection(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Windows\Speech', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'AllowInputPersonalization', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("Raccolta dati sulla voce attivata.")
        except FileNotFoundError:
            print("La chiave di registro per la raccolta dati sulla voce non è stata trovata.")

    def enable_feedback_notifications(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Siuf\Rules', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'NumberOfSIUFInPeriod', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Siuf\Rules', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'PeriodInNanoSeconds', 0, winreg.REG_QWORD, 1)
            winreg.CloseKey(key)
            print("Notifiche di feedback attivate.")
        except Exception as e:
            print(f"Errore durante l'attivazione delle notifiche di feedback: {e}")

    def enable_edge_privacy_settings(self):
        try:
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\MicrosoftEdge\\Main" -Name "DoNotTrack" -Value 0'], check=True)
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Edge\\Privacy" -Name "SendDoNotTrackHeader" -Value 0'], check=True)
            print("Impostazioni di privacy di Microsoft Edge configurate.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la configurazione delle impostazioni di privacy di Microsoft Edge: {e}")


# Esempio di utilizzo:
disabler = PrivacySettingsDisabler()
disabler.disable_privacy_settings()

enabler = PrivacySettingsEnabler()
#enabler.enable_privacy_settings()
