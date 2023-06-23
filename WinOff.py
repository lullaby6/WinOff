import os, time, subprocess, sys, winreg, ctypes

if not sys.platform == 'win32':
    input('WinOff is only for Windows. If you have Windows make sure you have the correct version of Windows installed.')
    sys.exit()

def run_as_admin():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    except Exception as e:
        input(f"An error occurred while elevating administrator privileges: {str(e)}")
        sys.exit()

run_as_admin()

os.system('title WinOff')

def disable_sysmain():
    os.system('sc stop SysMain')
    os.system('sc config SysMain start=disabled')
    
def disable_wpnservice():
    os.system('sc stop WpnService')
    os.system('sc config WpnService start=disabled')
       
def disable_windows_defender():
    try:
        subprocess.run(['sc', 'stop', 'WinDefend'], check=True)
        subprocess.run(['sc', 'config', 'WinDefend', 'start=', 'disabled'], check=True)
        
        print("[Service] Windows Defender disabled.")
    except subprocess.CalledProcessError as e:
        print(f"[Service] An error occurred while disabling Windows Defender: {str(e)}")
    
    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        value_name = "DisableAntiSpyware"
        value_data = 1

        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

        winreg.CloseKey(key)
        
        print("[Regedit] Windows Defender disabled.")
    except Exception as e:
        print(f"[Rgedit] An error occurred while disabling Windows Defender: {str(e)}")

    
def disable_telemetry():
    os.system('sc stop DiagTrack')
    os.system('sc config DiagTrack start=disabled')
    
    key_path = r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    value_name = "AllowTelemetry"
    value_data = 0

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

        winreg.CloseKey(key)
        print("Telemetry has been deactivated correctly.")
    except FileNotFoundError:
        print("The registry key does not exist. Make sure you have the correct version of Windows installed.")


def disable_transparency():
    os.system('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v EnableTransparency /t REG_DWORD /d 0 /f')

menu = {
    'Disable SysMain/SuperFetch': disable_sysmain,
    'Disable WPN Service': disable_wpnservice,
    'Disable Telemetry': disable_telemetry,
    'Disable Transparency': disable_transparency,
    'Disable Windows Defender': disable_windows_defender,
    'Exit': lambda: sys.exit()
}

while True:
    os.system('cls')
    print('WinOff - github.com/lullaby6/WinOff\n')
    
    menu_keys = list(menu.keys())
    for index, option in enumerate(menu_keys):
        print(f'{index+1} - {option}')
        
    selected_option = input('\nSelect option: ')
    
    if selected_option.isdigit() and int(selected_option) > 0 and int(selected_option) <= len(menu_keys):
        key_selected = menu_keys[int(selected_option)-1]
        menu[key_selected]()
        input()