import os
import sys
import subprocess
import tempfile
import time
import argparse

from datetime import datetime
from termcolor import colored

from hashCrack.functions import (
    list_sessions, save_logs, restore_session, define_windows_parameters, define_hashfile
)

parameters = define_windows_parameters()

def run_hashcat(session, hashmode, mask, workload, status_timer, min_length, max_length, hash_file, hashcat_path, device):
    temp_output = tempfile.mktemp()

    hashcat_command = [
        f"{hashcat_path}/hashcat.exe",
        f"--session={session}",
        "-m", hashmode,
        hash_file,
        "-a", "3",
        "-w", workload,
        "--outfile-format=2",
        "-o", "plaintext.txt",
        f"\"{mask}\"",
        "-d", device,
        "--potfile-disable"
    ]

    hashcat_command.append(f"--increment")
    hashcat_command.append(f"--increment-min={min_length}")
    hashcat_command.append(f"--increment-max={max_length}")

    if status_timer.lower() == "y":
        hashcat_command.extend(["--status", "--status-timer=2"])

    with open(temp_output, 'w') as output_file:
        try:
            subprocess.run(hashcat_command, check=True, stdout=output_file, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(colored("[!] Error while executing hashcat.", "red"))
            return

    with open(temp_output, 'r') as file:
        hashcat_output = file.read()

    print(hashcat_output)

    if "Cracked" in hashcat_output:
        print(colored("[+] Hashcat found the plaintext! Saving logs...", "green"))
        time.sleep(2)
        save_logs(session, mask)
    else:
        print(colored("[!] Hashcat did not find the plaintext.", "red"))
        time.sleep(2)

    os.remove(temp_output)

def main():
    hash_file = define_hashfile()

    list_sessions(parameters["default_restorepath"])
    
    restore_file_input = input(colored("[+] ","green") + f"Restore? (Enter restore file name or leave empty): ")
    restore_file = restore_file_input or parameters["default_restorepath"]
    
    restore_session(restore_file, parameters["default_restorepath"])

    session_input = input(colored("[+] ","green") + f"Enter session name (default '{parameters['default_session']}'): ")
    session = session_input or parameters["default_session"]

    mask_input = input(colored("[+] ","green") + f"Enter Mask (default '{parameters['default_mask']}'): ")
    mask = mask_input or parameters["default_mask"]

    status_timer_input = input(colored("[+] ","green") + f"Use status timer? (default '{parameters['default_status_timer']}') [y/n]: ")
    status_timer = status_timer_input or parameters["default_status_timer"]

    min_length_input = input(colored("[+] ","green") + f"Enter Minimum Length (default '{parameters['default_min_length']}'): ")
    min_length = min_length_input or parameters["default_min_length"]

    max_length_input = input(colored("[+] ","green") + f"Enter Maximum Length (default '{parameters['default_max_length']}'): ")
    max_length = max_length_input or parameters["default_max_length"]

    hashcat_path_input = input(colored("[+] ","green") + f"Enter Hashcat Path (default '{parameters['default_hashcat']}'): ")
    hashcat_path = hashcat_path_input or parameters["default_hashcat"]

    hash_file_input = input(colored("[+] ","green") + f"Enter the path of the hash file: ")
    hash_file = hash_file_input

    if not os.path.isfile(hash_file):
        print(colored(f"[!] Error: The file {hash_file} does not exist.", "red"))
        return

    hashmode_input = input(colored("[+] ","green") + f"Enter hash attack mode (default '{parameters['default_hashmode']}'): ")
    hashmode = hashmode_input or parameters["default_hashmode"]

    workload_input = input(colored("[+] ","green") + f"Enter workload (default '{parameters['default_workload']}') [1-4]: ")
    workload = workload_input or parameters["default_workload"]

    device_input = input(colored("[+] ", "green") + f"Enter device (default '{parameters['default_device']}'): ")
    device = device_input or parameters["default_device"]

    print(colored("[+] Running Hashcat command...", "blue"))
    print(colored(f"[*] Restore >>", "magenta") + f" {hashcat_path}/{session}")
    print(colored(f"[*] Command >>", "magenta") + f" {hashcat_path}/hashcat.exe --session={session} --increment --increment-min={min_length} --increment-max={max_length} -m {hashmode} {hash_file} -a 3 -w {workload} --outfile-format=2 -o plaintext.txt \"{mask}\" -d {device}")

    run_hashcat(session, hashmode, mask, workload, status_timer, min_length, max_length, hash_file, hashcat_path, device)

if __name__ == "__main__":
    main()
