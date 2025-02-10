import requests
import time
import json
import datetime
import sys

def banner():
    print("\033[92m")  # Bright Green
    print(r"""
██████╗  ██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗ ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔═══██╗████╗  ██║
██║  ██║██║   ██║██████╔╝█████╗  ███████║██╔████╔██║██║   ██║██╔██╗ ██║
██║  ██║██║   ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║██║   ██║██║╚██╗██║
██████╔╝╚██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝                                                                      
              MADE BY :- Đôrêmon
    """)
    print("\033[0m")  # Reset color

def timestamp():
    return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
def log_info(msg):
    print(f"{timestamp()} \033[94m[*] {msg}\033[0m")
def log_success(msg):
    print(f"{timestamp()} \033[92m[+] {msg}\033[0m")
def log_error(msg):
    print(f"{timestamp()} \033[91m[-] {msg}\033[0m")

def main():
    banner()
    try:
        with open('proxy.txt', 'r', encoding='utf-8') as f:
            proxies_list = [p.strip() for p in f if p.strip()]
        log_success(f"Loaded {len(proxies_list)} proxies from proxy.txt")
    except Exception as e:
        log_error(f"Could not read 'proxy.txt': {e}")
        sys.exit(1)
    try:
        with open('address.txt', 'r', encoding='utf-8') as f:
            addresses = [a.strip() for a in f if a.strip()]
        log_success(f"Loaded {len(addresses)} addresses from address.txt")
    except Exception as e:
        log_error(f"Could not read 'address.txt': {e}")
        sys.exit(1)
    for i, address in enumerate(addresses):
        proxy = proxies_list[i % len(proxies_list)]
        send_request(proxy, address)
        time.sleep(4)

def send_request(proxy, address):
    log_info(f"Using Proxy: {proxy} | Address: {address}")

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://faucet.haust.app/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    proxies = {
        "http": proxy,
        "https": proxy
    }

    data = {"address": address}
    try:
        response = requests.post(
            "https://faucet.haust.app/api/claim",
            headers=headers,
            json=data,
            proxies=proxies,
            timeout=30
        )
        response_text = response.text
        log_success(f"Response: {response_text}")
        try:
            json_data = json.loads(response_text)
            log_info(f"Parsed JSON: {json_data}")
        except json.JSONDecodeError:
            log_error("Response is not valid JSON.")
    except Exception as e:
        log_error(f"Error with proxy {proxy} for address {address}: {e}")

if __name__ == "__main__":
    main()
