import os
import sys
import time
import random
import subprocess
import shutil
import argparse
from importlib import resources
from pathlib import Path
from datetime import datetime
from termcolor import colored

default_scripts = os.path.expanduser("~/hashCrack")
default_windows_scripts = f"/c/Users/{os.getenv('USER')}/source/repos/ente0v1/hashCrack/scripts/windows"

def define_default_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Linux",
        "default_restorepath": os.path.expanduser("~/.local/share/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": "wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def define_windows_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Windows",
        "default_restorepath": os.path.expanduser("~/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": f"/c/Users/{os.getenv('USER')}/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu1(default_os):
    ascii_art = """
888                        888       .d8888b.                           888     
888                        888      d88P  Y88b                          888     
888                        888      888    888                          888     
88888b.   8888b.  .d8888b  88888b.  888        888d888 8888b.   .d8888b 888  888
888 "88b     "88b 88K      888 "88b 888        888P"      "88b d88P"    888 .88P
888  888 .d888888 "Y8888b. 888  888 888    888 888    .d888888 888      888888K 
888  888 888  888      X88 888  888 Y88b  d88P 888    888  888 Y88b.    888 "88b
888  888 "Y888888  88888P' 888  888  "Y8888P"  888    "Y888888  "Y8888P 888  888
       
       For more information, visit: https://github.com/ente0v1/hashCrack
    """
    print(colored(ascii_art, 'cyan'))
    print(colored("="*80, 'cyan'))
    print(colored(f"   Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    print(colored("="*80, 'cyan'))
    options = [
        f"{colored('[1]', 'blue', attrs=['bold'])} Crack with Wordlist          {colored('[EASY]', 'blue', attrs=['bold'])}",
        f"{colored('[2]', 'green', attrs=['bold'])} Crack with Association       {colored('[MEDIUM]', 'green', attrs=['bold'])}",
        f"{colored('[3]', 'yellow', attrs=['bold'])} Crack with Brute-Force       {colored('[HARD]', 'yellow', attrs=['bold'])}",
        f"{colored('[4]', 'red', attrs=['bold'])} Crack with Combinator        {colored('[ADVANCED]', 'red', attrs=['bold'])}",
    ]
    print("\n   " + "\n   ".join(options))

    print(colored("-"*80, 'cyan')) 

    print(f"{colored('   [0]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile        {colored('[UTILITY]', 'magenta', attrs=['bold'])}")

    print(colored("\n" + "="*80, 'magenta'))
    print(f"   {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored("="*80, 'magenta'))

    user_option = input(colored("\nEnter option (0-4, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()

    if user_option == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
        time.sleep(1)

    elif user_option == 'q':
        print("Exiting program...")
        sys.exit(0) 

    elif user_option == '0':
        if default_os == 'Linux':
            os.system("sudo rm ~/.local/share/hashcat/hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Linux.", 'green'))
        elif default_os == 'Windows':
            os.system("del %userprofile%\\hashcat\\hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Windows.", 'green'))
        time.sleep(1)

    return user_option, default_os

def show_menu2(default_os):
    ascii_art = r"""
dP                         dP       MM"'""'"YMM                            dP      
88                         88       M' .mmm. `M                            88      
88d888b. .d8888b. .d8888b. 88d888b. M  MMMMMooM 88d888b. .d8888b. .d8888b. 88  .dP 
88'  `88 88'  `88 Y8ooooo. 88'  `88 M  MMMMMMMM 88'  `88 88'  `88 88'  `"" 88888"  
88    88 88.  .88       88 88    88 M. `MMM' .M 88       88.  .88 88.  ... 88  `8b.
dP    dP `88888P8 `88888P' dP    dP MM.     .dM dP       `88888P8 `88888P' dP   `YP
                                    MMMMMMMMMMM  
         
         For more information, visit: https://github.com/ente0v1/hashCrack
    """
    print(colored(ascii_art, 'cyan'))
    print(colored("="*83, 'cyan'))
    print(colored(f"   Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    print(colored("="*83, 'cyan'))
    options = [
        f"{colored('[1]', 'blue', attrs=['bold'])} Crack with Wordlist          {colored('[EASY]', 'blue', attrs=['bold'])}",
        f"{colored('[2]', 'green', attrs=['bold'])} Crack with Association       {colored('[MEDIUM]', 'green', attrs=['bold'])}",
        f"{colored('[3]', 'yellow', attrs=['bold'])} Crack with Brute-Force       {colored('[HARD]', 'yellow', attrs=['bold'])}",
        f"{colored('[4]', 'red', attrs=['bold'])} Crack with Combinator        {colored('[ADVANCED]', 'red', attrs=['bold'])}",
    ]
    print("\n   " + "\n   ".join(options))

    print(colored("-"*83, 'cyan')) 

    print(f"{colored('   [0]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile        {colored('[UTILITY]', 'magenta', attrs=['bold'])}")

    print(colored("\n" + "="*83, 'magenta'))
    print(f"   {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored("="*83, 'magenta'))

    user_option = input(colored("\nEnter option (0-4, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()

    if user_option == 'x':
        default_os = "Linux" if default_os == "Windows" else "Windows"
        print(f"System switched to {default_os}")
        time.sleep(1)

    elif user_option == 'q':
        print("Exiting program...")
        sys.exit(0) 

    elif user_option == '0':
        if default_os == 'Linux':
            os.system("sudo rm ~/.local/share/hashcat/hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Linux.", 'green'))
        elif default_os == 'Windows':
            os.system("del %userprofile%\\hashcat\\hashcat.potfile")
            print(colored("[+] Hashcat potfile cleared for Windows.", 'green'))
        time.sleep(1)

    return user_option, default_os


def animate_text(text, delay):
    for i in range(len(text) + 1):
        clear_screen()
        print(text[:i], end="", flush=True)
        time.sleep(delay)

def get_package_script_path(script_name: str, os_type: str) -> Path:
    """Get the correct path for scripts inside the installed package"""
    try:
        with resources.files(f'hashCrack.{os_type.lower()}') as p:
            script_path = p / script_name
            if not script_path.exists():
                raise FileNotFoundError(f"Script {script_name} not found in package")
            return script_path
    except (ImportError, AttributeError):
        import pkg_resources
        package_path = pkg_resources.resource_filename('hashCrack', f'{os_type.lower()}/{script_name}')
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Script {script_name} not found in package")
        return Path(package_path)

def handle_option(option, default_os, hash_file):
    script_map = {
        "1": "crack_wordlist.py",
        "2": "crack_rule.py",
        "3": "crack_bruteforce.py",
        "4": "crack_combo.py"
    }

    print("...", flush=True)

    if option.lower() == "q":
        print("Exiting...")
        print(colored("Done! Exiting...", 'yellow'))
        sys.exit(0)

    script_name = script_map.get(option)
    if not script_name:
        print(colored("Invalid option. Please try again.", 'red'))
        return

    try:
        script_type = "windows" if default_os == "Windows" else "linux"
        script_path = get_package_script_path(script_name, script_type)
        
        print(colored(f'Executing {script_path}', 'green'))
        
        python_cmd = "python3" if default_os == "Linux" else "python"
        os.system(f'{python_cmd} "{script_path}" "{hash_file}"')
    
    except FileNotFoundError as e:
        print(colored(f"Error: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))
    
    input("Press Enter to return to the menu...")

def execute_windows_scripts():
    windows_scripts_dir = "scripts/windows"
    if os.path.isdir(windows_scripts_dir):
        for script in os.listdir(windows_scripts_dir):
            script_path = os.path.join(windows_scripts_dir, script)
            if os.path.isfile(script_path):
                print(f"[+] Executing Windows script: {script}","green")
                os.system(f"python {script_path}")
    else:
        print(colored(f"[!] Error: Windows scripts directory not found: '{windows_scripts_dir}'", "red"))

from pathlib import Path
import os
import shutil
from termcolor import colored

def save_logs(session, hash_file, wordlist_path=None, wordlist=None, mask_path=None, mask=None, rule_path=None, rule=None):
    log_base = Path.home() / ".hashCrack" / "logs" / session
    log_base.mkdir(parents=True, exist_ok=True)
    status_file = log_base / "status.txt"
    plaintext_source = Path("plaintext.txt")
    plaintext_dest = log_base / "plaintext.txt"

    log_content = [
        f"Session: {session}",
        f"Wordlist: {os.path.join(wordlist_path, wordlist) if wordlist_path and wordlist else 'N/A'}",
        f"Mask: {mask if mask else 'N/A'}",
        f"Rule: {os.path.join(rule_path, rule) if rule_path and rule else rule if rule else 'N/A'}"
    ]

    hash_content = "N/A"
    if isinstance(hash_file, (str, Path)):
        hash_path = Path(hash_file)
        if hash_path.is_file():
            try:
                with open(hash_path, 'r') as f:
                    hash_content = f.read().strip()
            except Exception as e:
                print(colored(f"[!] Error reading hash file: {e}", 'red'))
        else:
            print(colored(f"[!] Warning: {hash_file} is not a file or doesn't exist", 'yellow'))
    log_content.append(f"Hash: {hash_content}")

    plaintext_content = "N/A"
    if plaintext_source.exists() and plaintext_source.is_file():
        try:
            shutil.copy2(plaintext_source, plaintext_dest)
            print(colored(f"[+] Copied plaintext.txt to {plaintext_dest}", 'green'))
            with open(plaintext_dest, 'r') as f:
                plaintext_content = f.read().strip()
            plaintext_source.unlink()
        except Exception as e:
            print(colored(f"[!] Error handling plaintext file: {e}", 'red'))
    else:
        print(colored("[!] Warning: plaintext.txt not found in the root directory", 'yellow'))
    
    log_content.append(f"Plaintext: {plaintext_content}")

    try:
        with open(status_file, 'w') as f:
            f.write('\n'.join(log_content))
        print(colored(f"[+] Status saved to {status_file}", 'green'))
    except Exception as e:
        print(colored(f"[!] Error saving status file: {e}", 'red'))

    print(colored("\n[*] Status File Content:", 'blue'))
    print('\n'.join(log_content))
    
    if plaintext_content != "N/A":
        print(colored("\n[*] Plaintext Output:", 'blue'))
        print(plaintext_content)

def list_sessions(default_restorepath):
    try:
        restore_files = [f for f in os.listdir(default_restorepath) if f.endswith('.restore')]
        if restore_files:
            print(colored("[+] Available sessions:", "green"))
            for restore_file in restore_files:
                print(colored("[-]", "yellow") + f" {restore_file}")
        else:
            print(colored("[!] No restore files found...", "red"))
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {default_restorepath} does not exist.", "red"))

def restore_session(restore_file_input, default_restorepath):
    if not restore_file_input:
        list_sessions(default_restorepath)
        restore_file_input = input(colored(f"[+] Restore? (Enter restore file name or leave empty): ", "green"))
    
    restore_file = os.path.join(default_restorepath, f"{restore_file_input}")
     
    if not os.path.isfile(restore_file):
        print(colored(f"[!] Error: Restore file '{restore_file}' not found.", 'red'))
        return

    session = os.path.basename(restore_file).replace(".restore", "")
    print(colored(f"[+] Restoring session >> {restore_file}", 'blue'))

    cmd = f"hashcat --session={session} --restore"
    print(colored(f"[+] Executing: {cmd}", "blue"))
    os.system(cmd)

def define_hashfile():
    parser = argparse.ArgumentParser(description="A tool for cracking hashes using Hashcat.")
    parser.add_argument("hash_file", help="Path to the file containing the hash to crack")
    args = parser.parse_args()
    
    return args.hash_file



