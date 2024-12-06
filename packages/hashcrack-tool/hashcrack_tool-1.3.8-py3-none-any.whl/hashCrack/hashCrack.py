import os
import time
import sys
import argparse
import subprocess
from pathlib import Path
from termcolor import colored
from hashCrack.functions import (
    define_default_parameters, define_windows_parameters, clear_screen, 
    show_menu1, show_menu2, handle_option, define_hashfile
)

def clean_hashcat_cache():
    try:
        potfile_paths = [
            Path.home() / '.local/share/hashcat/hashcat.potfile',
            Path.home() / '.hashcat/hashcat.potfile',
            #Path('/root/.hashcat/hashcat.potfile'),
            #Path('/root/.local/share/hashcat/hashcat.potfile'),
            Path.home() / 'venv/lib/python3.12/site-packages/hashcat/hashcat/hashcat.potfile'
        ]
        
        for potfile in potfile_paths:
            if potfile.exists():
                potfile.unlink()
                print(colored(f"[+] Removed existing potfile: {potfile}", 'green'))
        
        subprocess.run(['hashcat', '--flush-cache'], 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        print(colored("[+] Hashcat cache flushed", 'green'))
        return True
    except Exception as e:
        print(colored(f"[!] Error cleaning hashcat cache: {e}", 'red'))
        return False

def verify_hash_crackable(hash_file):
    try:
        clean_hashcat_cache()
        result = subprocess.run(
            ['hashcat', '-m', '22000', hash_file, '--show'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if not result.stdout.strip():
            return True
            
        print(colored("[!] Hash already found in potfile:", 'yellow'))
        print(result.stdout)
        return False
        
    except Exception as e:
        print(colored(f"[!] Error verifying hash: {e}", 'red'))
        return False

def main():
    define_windows_parameters()
    define_default_parameters()
    
    while True:
        try:
            default_os = "Linux"
            clear_screen()
            
            user_option, default_os = show_menu1(default_os)
            
            hash_file = define_hashfile()
            if not os.path.isfile(hash_file):
                print(colored(f"[!] Error: The file '{hash_file}' does not exist.", 'red'))
                time.sleep(2)
                continue
                
            if user_option in ['1', '2', '3', '4']:
                if not verify_hash_crackable(hash_file):
                    print(colored("[!] Hash might already be cracked or there was an error.", 'yellow'))
                    input("Press Enter to continue...")
                    continue
                    
                try:
                    handle_option(user_option, default_os, hash_file)
                except KeyboardInterrupt:
                    print(colored("\n[!] Operation cancelled by user", 'yellow'))
                    time.sleep(1)
                except Exception as e:
                    print(colored(f"[!] Error occurred while processing: {e}", 'red'))
                    time.sleep(2)
            
            elif user_option.lower() == 'q':
                clear_screen()
                print(colored("Goodbye!", 'green'))
                sys.exit(0)
            else:
                print(colored("[!] Invalid option selected", 'red'))
                time.sleep(1)
                
        except KeyboardInterrupt:
            clear_screen()
            print(colored("\nExiting safely...", 'yellow'))
            sys.exit(0)
        except Exception as e:
            print(colored(f"[!] Unexpected error: {e}", 'red'))
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(colored("\nExiting safely...", 'yellow'))
        sys.exit(0)