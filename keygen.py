import os
import time
import datetime
from eth_account import Account
from multiprocessing import Pool, cpu_count
from colorama import init, Fore, Style
init(autoreset=True)

def banner():
    print(Fore.GREEN + r"""
██████╗  ██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗ ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔═══██╗████╗  ██║
██║  ██║██║   ██║██████╔╝█████╗  ███████║██╔████╔██║██║   ██║██╔██╗ ██║
██║  ██║██║   ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║██║   ██║██║╚██╗██║
██████╔╝╚██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝                                                                      
              MADE BY :- Đôrêmon                               
    """ + Style.RESET_ALL)

def timestamp():
    return "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
def log_info(message):
    print(f"{timestamp()} {Fore.BLUE}[*] {message}{Style.RESET_ALL}")
def log_success(message):
    print(f"{timestamp()} {Fore.GREEN}[+] {message}{Style.RESET_ALL}")
def log_error(message):
    print(f"{timestamp()} {Fore.RED}[-] {message}{Style.RESET_ALL}")
def generate_chunk(start, end):
    private_keys = []
    addresses = []
    for _ in range(start, end):
        acct = Account.create()
        private_key = acct._private_key.hex()
        address = acct.address
        private_keys.append(private_key)
        addresses.append(address)
    return private_keys, addresses

def main():
    banner()
    num_keys = 1000
    n_processes = cpu_count()
    chunk_size = num_keys // n_processes
    log_info(f"Starting generation of {num_keys} key pairs across {n_processes} processes...")
    tasks = []
    for i in range(n_processes):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < n_processes - 1 else num_keys
        tasks.append((start_idx, end_idx))
    with Pool(n_processes) as pool:
        results = pool.starmap(generate_chunk, tasks)
    log_info("Generation complete. Writing to files...")
    try:
        with open("key.txt", "w") as priv_file, open("address.txt", "w") as pub_file:
            for priv_keys_chunk, addrs_chunk in results:
                for pk, addr in zip(priv_keys_chunk, addrs_chunk):
                    priv_file.write(f"{pk}\n")
                    pub_file.write(f"{addr}\n")
        log_success("Key generation completed. Private and public keys have been saved.")
    except Exception as e:
        log_error(f"Error writing to files: {e}")
if __name__ == '__main__':
    main()
