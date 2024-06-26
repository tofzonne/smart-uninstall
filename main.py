import winreg
import psutil
import os

def get_installed_programs():
    programs = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                sub_key = winreg.EnumKey(reg_key, i)
                sub_key_path = f"{reg_path}\\{sub_key}"
                try:
                    sub_key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key_path, 0, winreg.KEY_READ)
                    display_name, _ = winreg.QueryValueEx(sub_key_handle, "DisplayName")
                    programs.append(display_name)
                except WindowsError:
                    continue
        except WindowsError:
            continue
    return programs

def get_installed_services():
    services = []
    for service in psutil.win_service_iter():
        services.append(service.name())
    return services

def find_orphaned_files(programs, search_paths):
    orphaned_files = []
    for root_path in search_paths:
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if not any(prog in file for prog in programs):
                    orphaned_files.append(os.path.join(root, file))
    return orphaned_files

def calculate_size(files):
    total_size = 0
    for file in files:
        total_size += os.path.getsize(file)
    return total_size

def prompt_for_deletion(files, size):
    print(f"The following orphaned files have been found ({size / (1024*1024):.2f} MB):")
    # for file in files:
    #     print(file)
    user_input = input("Do you want to delete these files? (yes/no): ")
    if user_input.lower() == 'yes':
        for file in files:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    else:
        print("No files were deleted.")

if __name__ == '__main__':
    installed_programs = get_installed_programs()
    for i in installed_programs:
        print(i)
    # installed_services = get_installed_services()
    # search_paths = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users\\alamm\\AppData\\"]
    # orphaned_files = find_orphaned_files(installed_programs, search_paths)
    # orphaned_files_size = calculate_size(orphaned_files)
    # prompt_for_deletion(orphaned_files, orphaned_files_size)
