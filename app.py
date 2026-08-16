from flask import Flask, render_template_string, request, jsonify
import os
import sys
import json
import random

# ============================================================
# إغلاق السيرفر القديم فوراً وتعيين المنفذ 7000
# ============================================================
def force_shutdown_old_server(port=7000):
    try:
        if sys.platform.startswith("win"):
            os.system(f"for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :{port}') do taskkill /f /pid %a >nul 2>&1")
        else:
            os.system(f"fuser -k {port}/tcp >/dev/null 2>&1 || fuser -k -9 {port}/tcp >/dev/null 2>&1")
    except Exception:
        pass

force_shutdown_old_server(7000)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ============================================================
# بيانات المواقع السياحية الجزائرية (17 موقعاً)
# ============================================================
ALGERIAN_SITES = [
    {"id": 1, "name": "القصبة", "city": "الجزائر", "desc": "مدينة قديمة مصنفة ضمن التراث العالمي", "lat": 36.7850, "lng": 3.0600},
    {"id": 2, "name": "تيبازة", "city": "تيبازة", "desc": "آثار رومانية ومدرج", "lat": 36.5945, "lng": 2.4430},
    {"id": 3, "name": "تيمقاد", "city": "باتنة", "desc": "مدينة رومانية أثرية", "lat": 35.4850, "lng": 6.4680},
    {"id": 4, "name": "جانت", "city": "إليزي", "desc": "واحة ولوحات صخرية", "lat": 24.5540, "lng": 9.4750},
    {"id": 5, "name": "تاسيلي ناجر", "city": "إليزي", "desc": "موقع فني صخري عالمي", "lat": 25.2167, "lng": 8.6667},
    {"id": 6, "name": "وهران", "city": "وهران", "desc": "مدينة ساحلية وقلعة", "lat": 35.6969, "lng": -0.6331},
    {"id": 7, "name": "شرشال", "city": "تيبازة", "desc": "مدينة تاريخية وميناء", "lat": 36.6080, "lng": 2.1950},
    {"id": 8, "name": "تيبازة (المدرج)", "city": "تيبازة", "desc": "مدرج روماني", "lat": 36.5945, "lng": 2.4430},
    {"id": 9, "name": "بجاية", "city": "بجاية", "desc": "مدينة ساحلية وقلعة", "lat": 36.7500, "lng": 5.0667},
    {"id": 10, "name": "قسنطينة", "city": "قسنطينة", "desc": "جسور معلقة ومدينة قديمة", "lat": 36.3650, "lng": 6.6147},
    {"id": 11, "name": "الجزائر العاصمة", "city": "الجزائر", "desc": "العاصمة ومباني استعمارية", "lat": 36.7538, "lng": 3.0588},
    {"id": 12, "name": "الشلف", "city": "الشلف", "desc": "مدينة زراعية وموقع أثري", "lat": 36.1650, "lng": 1.3310},
    {"id": 13, "name": "عين وسارة", "city": "الجلفة", "desc": "منطقة سياحية وجبلية", "lat": 35.2640, "lng": 2.9300},
    {"id": 14, "name": "غرداية", "city": "غرداية", "desc": "مدينة إباضية وواحة", "lat": 32.4830, "lng": 3.6667},
    {"id": 15, "name": "تمنراست", "city": "تمنراست", "desc": "بوابة الصحراء", "lat": 22.7850, "lng": 5.5228},
    {"id": 16, "name": "جيجل", "city": "جيجل", "desc": "شواطئ وغابات", "lat": 36.8200, "lng": 5.7667},
    {"id": 17, "name": "سكيكدة", "city": "سكيكدة", "desc": "مدينة ساحلية وميناء", "lat": 36.8667, "lng": 6.9000}
]

# ============================================================
# القالب الكامل (HTML + CSS + JavaScript) مدمج داخل ملف Python
# ============================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI GLOBAL TOURISM V6 | Hologram & AI Twin Platform</title>
    <!-- Font Awesome & Google Fonts (CDN) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet" />
    <style>
        /* ===== ROOT ===== */
        :root {
            --bg-gradient: radial-gradient(circle at top center, #070b14 0%, #02040a 70%, #000000 100%);
            --glass-bg: rgba(6, 182, 212, 0.04);
            --glass-border: rgba(6, 182, 212, 0.28);
            --glass-card: rgba(15, 23, 42, 0.8);
            --glass-modal: rgba(2, 6, 23, 0.96);
            --accent-cyan: #06b6d4;
            --accent-cyan-glow: rgba(6, 182, 212, 0.6);
            --accent-emerald: #10b981;
            --accent-gold: #f59e0b;
            --accent-red: #ef4444;
            --neon-purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Cairo', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 80px;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
            background-size: 25px 25px;
            pointer-events: none;
            z-index: -1;
        }

        header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(2, 6, 23, 0.88);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-bottom: 1px solid var(--glass-border);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand i {
            font-size: 1.6rem;
            color: var(--accent-cyan);
            text-shadow: 0 0 12px var(--accent-cyan);
        }
        .brand h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.05rem;
            font-weight: 900;
            background: linear-gradient(90deg, #06b6d4, #8b5cf6, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-actions {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .lang-switch {
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid var(--glass-border);
            color: var(--accent-cyan);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            outline: none;
            cursor: pointer;
        }
        .login-btn {
            background: var(--neon-purple);
            border: none;
            color: #fff;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            font-size: 0.8rem;
        }
        .login-btn i {
            margin-left: 4px;
        }

        .container {
            padding: 0 16px;
            max-width: 600px;
            margin: 0 auto;
        }

        .app-screen {
            display: none;
            animation: fadeIn 0.35s ease;
        }
        .app-screen.active {
            display: block;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.98);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        .holo-card {
            background: rgba(15, 23, 42, 0.82);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 18px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
            margin-top: 14px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(6, 182, 212, 0.12);
        }

        .holo-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.35) 0%, rgba(3, 7, 18, 0.95) 100%);
            border: 2px solid var(--neon-purple);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: var(--accent-cyan);
            box-shadow: 0 0 25px rgba(139, 92, 246, 0.5);
            position: relative;
        }
        .holo-avatar.speaking {
            animation: holo-pulse 0.7s infinite alternate;
            border-color: var(--accent-emerald);
        }
        @keyframes holo-pulse {
            0% {
                box-shadow: 0 0 10px var(--neon-purple);
            }
            100% {
                box-shadow: 0 0 35px var(--accent-emerald);
            }
        }

        .ai-input-group {
            display: flex;
            gap: 8px;
            margin-top: 14px;
        }
        .ai-input-group input {
            flex: 1;
            padding: 12px;
            border-radius: 14px;
            border: 1px solid var(--glass-border);
            background: rgba(2, 6, 23, 0.8);
            color: #fff;
            font-size: 0.85rem;
            outline: none;
        }
        .ai-input-group button {
            background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
            color: #fff;
            border: none;
            padding: 12px 16px;
            border-radius: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.15s;
        }
        .ai-input-group button:active {
            transform: scale(0.94);
        }

        .quick-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-top: 14px;
        }
        .quick-btn {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 10px 4px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: var(--text-main);
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.2s;
        }
        .quick-btn i {
            font-size: 1.1rem;
            color: var(--accent-cyan);
        }
        .quick-btn:hover {
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
        }

        .glass-box {
            background: var(--glass-card);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 16px;
            margin-top: 12px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        #aiResponse {
            margin-top: 12px;
            font-size: 0.85rem;
            display: none;
            color: #4ade80;
            background: rgba(16, 185, 129, 0.1);
            padding: 10px;
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.3);
            transition: all 0.3s;
        }

        .map-wrapper {
            background: var(--glass-card);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 10px;
            margin-top: 14px;
            position: relative;
            overflow: hidden;
        }
        .map-wrapper::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, transparent 60%);
            pointer-events: none;
            box-shadow: inset 0 0 30px rgba(6, 182, 212, 0.15);
            z-index: 2;
        }
        .map-frame-3d {
            width: 100%;
            height: 250px;
            border-radius: 16px;
            border: none;
            filter: contrast(1.1) saturate(1.2);
            transform: perspective(600px) rotateX(4deg);
            transition: transform 0.4s ease;
            position: relative;
            z-index: 1;
        }
        .map-frame-3d:hover {
            transform: perspective(600px) rotateX(0deg);
        }
        .map-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            position: relative;
            z-index: 3;
        }

        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 68px;
            background: rgba(2, 6, 23, 0.94);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-top: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 1000;
            overflow-x: auto;
            padding: 0 4px;
        }
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: var(--text-muted);
            font-size: 0.65rem;
            background: none;
            border: none;
            cursor: pointer;
            padding: 4px 8px;
            white-space: nowrap;
        }
        .nav-item.active {
            color: var(--accent-cyan);
            font-weight: bold;
        }
        .nav-item i {
            font-size: 1.1rem;
        }

        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(2, 6, 23, 0.88);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 2000;
            display: flex;
            align-items: flex-end;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .modal-content {
            background: var(--glass-modal);
            border: 1px solid var(--accent-cyan);
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            border-radius: 28px 28px 0 0;
            padding: 22px 18px 30px 18px;
            transform: translateY(100%);
            transition: transform 0.35s ease;
        }
        .modal-overlay.active .modal-content {
            transform: translateY(0);
        }

        .sites-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
            margin-top: 12px;
        }
        .site-card {
            background: var(--glass-card);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .site-card:hover {
            border-color: var(--accent-cyan);
            transform: scale(1.02);
        }
        .site-card i {
            font-size: 2rem;
            color: var(--accent-gold);
        }
        .site-card h4 {
            font-size: 0.8rem;
            margin: 4px 0;
        }
        .site-card p {
            font-size: 0.65rem;
            color: var(--text-muted);
        }

        .chat-box {
            background: rgba(2, 6, 23, 0.7);
            border-radius: 16px;
            padding: 12px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 8px;
        }
        .chat-msg {
            margin: 6px 0;
            padding: 8px 12px;
            border-radius: 12px;
            max-width: 85%;
        }
        .chat-msg.user {
            background: var(--neon-purple);
            color: #fff;
            align-self: flex-end;
            margin-left: auto;
        }
        .chat-msg.bot {
            background: var(--glass-card);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
        }

        .link-card {
            background: var(--glass-card);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 8px;
            text-decoration: none;
            color: var(--text-main);
            transition: 0.2s;
        }
        .link-card:hover {
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
        }

        .login-form input {
            width: 100%;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid var(--glass-border);
            background: rgba(2, 6, 23, 0.8);
            color: #fff;
            margin-top: 8px;
            outline: none;
        }
        .login-form button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--neon-purple));
            color: #fff;
            font-weight: bold;
            margin-top: 12px;
            cursor: pointer;
        }
        .verification-code {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin: 12px 0;
        }
        .verification-code input {
            width: 45px;
            height: 50px;
            text-align: center;
            font-size: 1.2rem;
            border-radius: 10px;
            border: 1px solid var(--glass-border);
            background: rgba(2, 6, 23, 0.8);
            color: #fff;
            outline: none;
        }

        @media (max-width: 480px) {
            .brand h1 {
                font-size: 0.8rem;
            }
            .quick-grid {
                gap: 6px;
            }
            .quick-btn {
                padding: 8px 2px;
                font-size: 0.6rem;
            }
            .sites-grid {
                grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <i class="fa-solid fa-vr-cardboard"></i>
            <h1>CPAY HOLOGRAM AI V6</h1>
        </div>
        <div class="header-actions">
            <button class="login-btn" onclick="openLoginModal()">
                <i class="fa-solid fa-user"></i> <span id="loginBtnText">تسجيل الدخول</span>
            </button>
            <select class="lang-switch" id="langSelect" onchange="switchLanguage()">
                <option value="ar">🇩🇿 العربية</option>
                <option value="en">🇬🇧 English</option>
                <option value="fr">🇫🇷 Français</option>
            </select>
        </div>
    </header>

    <div class="container">

        <section id="screen-home" class="app-screen active">
            <div class="holo-card">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div class="holo-avatar" id="robotAvatar">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <div>
                        <h3 id="robotName" style="font-size:1rem; font-weight:800;">الروبوت السياحي الهولوغرامي 3D</h3>
                        <p id="robotStatus" style="font-size:0.75rem; color:var(--text-muted);">مساعد الذكاء الاصطناعي و AI Twin Active</p>
                    </div>
                </div>
                <div class="ai-input-group">
                    <input type="text" id="aiQuery" placeholder="اسأل الروبوت الهولوغرامي أو ابحث عن وجهة..." />
                    <button onclick="askAIAndSpeak()"><i class="fa-solid fa-wand-magic-sparkles"></i></button>
                </div>
                <div class="quick-grid">
                    <div class="quick-btn" onclick="openModal('hospitals')">
                        <i class="fa-solid fa-hospital" style="color:var(--accent-red);"></i>
                        <span id="qHospitals">مستشفيات</span>
                    </div>
                    <div class="quick-btn" onclick="openModal('flights')">
                        <i class="fa-solid fa-plane-departure" style="color:var(--accent-cyan);"></i>
                        <span id="qFlights">طيران</span>
                    </div>
                    <div class="quick-btn" onclick="openModal('ferry')">
                        <i class="fa-solid fa-ship" style="color:var(--neon-purple);"></i>
                        <span id="qFerry">باخرة</span>
                    </div>
                    <div class="quick-btn" onclick="openModal('stations')">
                        <i class="fa-solid fa-bus" style="color:var(--accent-gold);"></i>
                        <span id="qStations">محطات</span>
                    </div>
                </div>
                <div id="aiResponse"></div>
            </div>

            <div class="glass-box" style="border-color: var(--neon-purple);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4><i class="fa-solid fa-user-gear" style="color:var(--neon-purple);"></i> <span id="twinTitle">التخطيط التلقائي (AI Twin Travel)</span></h4>
                    <span style="font-size:0.68rem; background:rgba(139,92,246,0.2); color:var(--neon-purple); padding:2px 8px; border-radius:10px;">النسخة الرقمية</span>
                </div>
                <p id="twinDesc" style="font-size:0.78rem; color:var(--text-muted); margin-top:6px;">تحليل الميزانية، الوقت، والاهتمامات لإنشاء مسار سياحي ذكي مخصص.</p>
                <button onclick="runAITwin()" style="width:100%; margin-top:10px; padding:10px; background:linear-gradient(135deg, var(--neon-purple) 0%, #6d28d9 100%); border:none; border-radius:12px; color:#fff; font-weight:bold; cursor:pointer;">
                    <span id="twinBtn">توليد خطة الرحلة التلقائية 🚀</span>
                </button>
            </div>

            <div class="map-wrapper">
                <div class="map-controls">
                    <span style="font-size:0.78rem; color:var(--text-muted);" id="mapLocationLabel">الجزائر 3D View AR</span>
                    <button class="quick-btn" style="padding:4px 8px;" onclick="toggleARMode()">
                        <i class="fa-solid fa-eye"></i> <span id="arBtnText">نمط الواقع المعزز AR</span>
                    </button>
                </div>
                <iframe id="gmapFrame" class="map-frame-3d" src="https://maps.google.com/maps?q=Algiers,Algeria&t=k&z=15&ie=UTF8&iwloc=&output=embed"></iframe>
            </div>

            <div style="display:flex; gap:10px; margin-top:14px; flex-wrap:wrap;">
                <button onclick="switchTab('explore', document.querySelector('[data-screen=\\'explore\\']'))" class="quick-btn" style="flex:1;">
                    <i class="fa-solid fa-compass"></i> <span id="navExplore">المغامرات</span>
                </button>
                <button onclick="switchTab('sites', document.querySelector('[data-screen=\\'sites\\']'))" class="quick-btn" style="flex:1;">
                    <i class="fa-solid fa-map-location-dot"></i> <span>المواقع</span>
                </button>
                <button onclick="switchTab('robot', document.querySelector('[data-screen=\\'robot\\']'))" class="quick-btn" style="flex:1;">
                    <i class="fa-solid fa-robot"></i> <span>الروبوت الذكي</span>
                </button>
            </div>
        </section>

        <section id="screen-explore" class="app-screen">
            <div style="padding: 12px 0;">
                <h2 id="exploreTitle">اكتشاف المغامرات والتصنيفات 🏜️🌊</h2>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div class="glass-box" onclick="selectAdventure('سياحة صحراوية جانت والهقار')">
                    <h4>🏜️ <span id="adv1">سياحة صحراوية (جانْت والهقّار)</span></h4>
                    <p style="font-size:0.75rem; color:var(--text-muted);" id="adv1desc">مغامرات الكثبان والرسومات التاسيلي التاريخية</p>
                </div>
                <div class="glass-box" onclick="selectAdventure('سياحة بحرية وهران وشرشال')">
                    <h4>🌊 <span id="adv2">سياحة بحرية (وهران، تيبازة، وشرشال)</span></h4>
                    <p style="font-size:0.75rem; color:var(--text-muted);" id="adv2desc">شواطئ ساحرة وموانئ سياحية يختية</p>
                </div>
                <div class="glass-box" onclick="selectAdventure('سياحة جبلية جرجرة وتيكجدة')">
                    <h4>⛰️ <span id="adv3">سياحة جبلية (جرجرة وتيكجدة)</span></h4>
                    <p style="font-size:0.75rem; color:var(--text-muted);" id="adv3desc">مسارات الجبال، الثلوج، والتخييم</p>
                </div>
            </div>
        </section>

        <section id="screen-passport" class="app-screen">
            <div style="padding: 12px 0;">
                <h2 id="passportTitle">جواز السفر الرقمي والأمان 🛡️</h2>
            </div>
            <div class="glass-box" style="border-color:var(--accent-red);">
                <h4><i class="fa-solid fa-triangle-exclamation" style="color:var(--accent-red);"></i> <span id="safetyTitle">مساعد الأمان والخدمات المحلية</span></h4>
                <p style="font-size:0.78rem; color:var(--text-muted); margin:6px 0;" id="safetyDesc">تنبيهات الطقس والازدحام المباشرة زر الطوارئ السريع</p>
                <button onclick="triggerEmergency()" style="width:100%; padding:10px; background:var(--accent-red); border:none; border-radius:12px; color:#fff; font-weight:bold; cursor:pointer;">
                    <span id="emergencyBtn">إرسال استغاثة طوارئ سريعة 🆘</span>
                </button>
            </div>
            <div class="glass-box">
                <h4><i class="fa-solid fa-passport" style="color:var(--accent-gold);"></i> <span id="digitalPassport">جواز السفر السياحي الرقمي</span></h4>
                <div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap;">
                    <span style="background:rgba(245,158,11,0.2); color:var(--accent-gold); padding:6px 12px; border-radius:10px; font-size:0.78rem;">🏅 <span id="badge1">وسام الاستكشاف الصحراوي</span></span>
                    <span style="background:rgba(6,182,212,0.2); color:var(--accent-cyan); padding:6px 12px; border-radius:10px; font-size:0.78rem;">⭐ <span id="badge2">450 نقطة مكافآت</span></span>
                </div>
            </div>
        </section>

        <section id="screen-profile" class="app-screen">
            <div style="padding: 12px 0;">
                <h2 id="translatorTitle">المترجم الفوري والنظام 🌐</h2>
            </div>
            <div class="glass-box">
                <h4><i class="fa-solid fa-language" style="color:var(--accent-cyan);"></i> <span id="liveTranslator">المترجم الفوري المباشر</span></h4>
                <div style="display:flex; gap:8px; margin-top:10px;">
                    <input type="text" id="transInput" placeholder="اكتب النص للترجمة المباشرة..." style="flex:1; padding:10px; border-radius:10px; border:1px solid var(--glass-border); background:rgba(2,6,23,0.7); color:#fff; outline:none;" />
                    <button onclick="translateLive()" style="padding:10px 14px; background:var(--accent-cyan); border:none; border-radius:10px; font-weight:bold; color:#0f172a; cursor:pointer;">
                        <span id="translateBtn">ترجمة</span>
                    </button>
                </div>
                <div id="transResult" style="margin-top:10px; font-size:0.85rem; color:var(--accent-emerald);"></div>
            </div>
        </section>

        <section id="screen-sites" class="app-screen">
            <div style="padding:12px 0; display:flex; justify-content:space-between; align-items:center;">
                <h2 id="sitesTitle">🗺️ 17 موقعاً سياحياً جزائرياً</h2>
                <button onclick="switchTab('home', document.querySelector('[data-screen=\\'home\\']'))" class="quick-btn" style="padding:4px 10px;">
                    <i class="fa-solid fa-arrow-right"></i> رجوع
                </button>
            </div>
            <div class="sites-grid" id="sitesContainer">
                <!-- يتم تعبئتها بواسطة JavaScript -->
            </div>
        </section>

        <section id="screen-robot" class="app-screen">
            <div style="padding:12px 0; display:flex; justify-content:space-between; align-items:center;">
                <h2 id="robotTitle">🤖 الروبوت الذكي لتوجيه السياح</h2>
                <button onclick="switchTab('home', document.querySelector('[data-screen=\\'home\\']'))" class="quick-btn" style="padding:4px 10px;">
                    <i class="fa-solid fa-arrow-right"></i> رجوع
                </button>
            </div>
            <div class="glass-box">
                <p style="font-size:0.8rem; color:var(--text-muted);">اسأل الروبوت عن أي موقع سياحي جزائري، وسيقدم لك معلومات وإرشادات.</p>
                <div class="chat-box" id="chatBox">
                    <div class="chat-msg bot">مرحباً! أنا الروبوت الذكي المتخصص في السياحة الجزائرية. اسألني عن أي موقع.</div>
                </div>
                <div class="ai-input-group" style="margin-top:10px;">
                    <input type="text" id="robotQuery" placeholder="اكتب سؤالك عن المواقع الجزائرية..." />
                    <button onclick="sendRobotQuery()"><i class="fa-solid fa-paper-plane"></i></button>
                </div>
            </div>
        </section>

        <!-- ===== شاشة الدعم الفني للحصول على إجابة دقيقة ===== -->
        <section id="screen-support" class="app-screen">
            <div style="padding: 12px 0; display:flex; justify-content:space-between; align-items:center;">
                <h2 id="supportTitle">🎧 الدعم الفني الذكي 24/7</h2>
                <button onclick="switchTab('home', document.querySelector('[data-screen=\\'home\\']'))" class="quick-btn" style="padding:4px 10px;">
                    <i class="fa-solid fa-arrow-right"></i> رجوع
                </button>
            </div>
            <div class="glass-box" style="border-color: var(--accent-cyan);">
                <h4><i class="fa-solid fa-headset" style="color:var(--accent-cyan);"></i> قسم الاستفسارات التقنية والمساعدة</h4>
                <p style="font-size:0.78rem; color:var(--text-muted); margin-top:4px;">احصل على إجابات دقيقة ومباشرة بخصوص الخرائط، الحجوزات، والخدمات الميدانية.</p>
                <div class="chat-box" id="supportChatBox" style="margin-top:12px;">
                    <div class="chat-msg bot">أهلاً بك في الدعم الفني لـ AI GLOBAL TOURISM. كيف يمكننا مساعدتك اليوم؟</div>
                </div>
                <div class="ai-input-group" style="margin-top:10px;">
                    <input type="text" id="supportQuery" placeholder="اكتب مشكلتك أو استفسارك التقني هنا..." />
                    <button onclick="sendSupportQuery()"><i class="fa-solid fa-headset"></i></button>
                </div>
            </div>
        </section>

        <!-- ===== شاشة روابط سيارات الأجرة والمستشفيات والعيادات والحافلات والفنادق ===== -->
        <section id="screen-links" class="app-screen">
            <div style="padding: 12px 0; display:flex; justify-content:space-between; align-items:center;">
                <h2 id="linksTitle">🔗 دليل الخدمات والنقل السريع</h2>
                <button onclick="switchTab('home', document.querySelector('[data-screen=\\'home\\']'))" class="quick-btn" style="padding:4px 10px;">
                    <i class="fa-solid fa-arrow-right"></i> رجوع
                </button>
            </div>
            <div style="display:flex; flex-direction:column; gap:8px;">
                <a href="https://www.google.com/maps/search/Taxi+Algeria" target="_blank" class="link-card">
                    <div>
                        <h5 style="color:var(--accent-gold);"><i class="fa-solid fa-taxi"></i> سيارات الأجرة (Taxi Services)</h5>
                        <p style="font-size:0.72rem; color:var(--text-muted);">حجز وتتبع سيارات الأجرة والقرب من موقعك</p>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <a href="https://www.google.com/maps/search/Hospitals+and+Clinics+Algeria" target="_blank" class="link-card">
                    <div>
                        <h5 style="color:var(--accent-red);"><i class="fa-solid fa-hospital"></i> المستشفيات والعيادات الطبية</h5>
                        <p style="font-size:0.72rem; color:var(--text-muted);">أقرب مراكز طوارئ وعيادات طبية مباشرة</p>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <a href="https://www.google.com/maps/search/Bus+Station+Algeria" target="_blank" class="link-card">
                    <div>
                        <h5 style="color:var(--accent-cyan);"><i class="fa-solid fa-bus"></i> محطات الحافلات للنقل البري</h5>
                        <p style="font-size:0.72rem; color:var(--text-muted);">خطوط ومواعيد انطلاق الحافلات بين الولايات</p>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <a href="https://www.google.com/maps/search/Hotels+Algeria" target="_blank" class="link-card">
                    <div>
                        <h5 style="color:var(--neon-purple);"><i class="fa-solid fa-hotel"></i> الفنادق والإقامات السياحية</h5>
                        <p style="font-size:0.72rem; color:var(--text-muted);">عروض وحجوزات الفنادق والنزل القريبة</p>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
                <a href="https://www.google.com/maps/search/Airports+Algeria" target="_blank" class="link-card">
                    <div>
                        <h5 style="color:var(--accent-emerald);"><i class="fa-solid fa-plane-up"></i> مطارات ورحلات الطيران</h5>
                        <p style="font-size:0.72rem; color:var(--text-muted);">مواعيد الإقلاع والهبوط بالمطارات الجزائرية</p>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            </div>
        </section>

    </div>

    <!-- ===== LOGIN MODAL ===== -->
    <div class="modal-overlay" id="loginModal" onclick="closeLoginModalOnOuter(event)">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <h3 id="loginTitle"><i class="fa-solid fa-user-lock"></i> تسجيل الدخول</h3>
                <div style="cursor:pointer;" onclick="closeLoginModal()"><i class="fa-solid fa-xmark"></i></div>
            </div>
            <div class="login-form">
                <input type="text" id="loginPhone" placeholder="أدخل رقم الهاتف أو البريد الإلكتروني" />
                <div style="margin-top:10px;">
                    <button onclick="sendVerificationCode()" id="sendCodeBtn">إرسال رمز التحقق</button>
                </div>
                <div class="verification-code" id="verificationArea" style="display:none;">
                    <input type="text" maxlength="1" class="code-input" />
                    <input type="text" maxlength="1" class="code-input" />
                    <input type="text" maxlength="1" class="code-input" />
                    <input type="text" maxlength="1" class="code-input" />
                </div>
                <button onclick="verifyLogin()" id="verifyBtn" style="display:none;">تأكيد وتسجيل الدخول</button>
                <p id="loginStatus" style="margin-top:8px; font-size:0.8rem; color:var(--accent-gold);"></p>
            </div>
        </div>
    </div>

    <!-- ===== SERVICE MODAL ===== -->
    <div class="modal-overlay" id="serviceModal" onclick="closeModalOnOuter(event)">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <h3 id="modalTitle"><i class="fa-solid fa-circle-info"></i> تفاصيل الخدمة</h3>
                <div style="cursor:pointer;" onclick="closeModal()"><i class="fa-solid fa-xmark"></i></div>
            </div>
            <div id="modalBody" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>
    </div>

    <!-- ===== BOTTOM NAV ===== -->
    <nav class="bottom-nav">
        <button class="nav-item active" data-screen="home" onclick="switchTab('home', this)">
            <i class="fa-solid fa-vr-cardboard"></i>
            <span id="navHome">الرئيسية</span>
        </button>
        <button class="nav-item" data-screen="sites" onclick="switchTab('sites', this)">
            <i class="fa-solid fa-map-location-dot"></i>
            <span id="navSites">المواقع</span>
        </button>
        <button class="nav-item" data-screen="robot" onclick="switchTab('robot', this)">
            <i class="fa-solid fa-robot"></i>
            <span id="navRobot">الروبوت</span>
        </button>
        <button class="nav-item" data-screen="support" onclick="switchTab('support', this)">
            <i class="fa-solid fa-headset"></i>
            <span id="navSupport">الدعم</span>
        </button>
        <button class="nav-item" data-screen="links" onclick="switchTab('links', this)">
            <i class="fa-solid fa-link"></i>
            <span id="navLinks">الخدمات</span>
        </button>
        <button class="nav-item" data-screen="passport" onclick="switchTab('passport', this)">
            <i class="fa-solid fa-passport"></i>
            <span id="navPassport">الجواز</span>
        </button>
        <button class="nav-item" data-screen="profile" onclick="switchTab('profile', this)">
            <i class="fa-solid fa-globe"></i>
            <span id="navProfile">المترجم</span>
        </button>
    </nav>

    <script>
        // ==================== TRANSLATIONS ====================
        const translations = {
            ar: {
                robotName: 'الروبوت السياحي الهولوغرامي 3D',
                robotStatus: 'مساعد الذكاء الاصطناعي و AI Twin Active',
                aiPlaceholder: 'اسأل الروبوت الهولوغرامي أو ابحث عن وجهة...',
                qHospitals: 'مستشفيات',
                qFlights: 'طيران',
                qFerry: 'باخرة',
                qStations: 'محطات',
                twinTitle: 'التخطيط التلقائي (AI Twin Travel)',
                twinDesc: 'تحليل الميزانية، الوقت، والاهتمامات لإنشاء مسار سياحي ذكي مخصص.',
                twinBtn: 'توليد خطة الرحلة التلقائية 🚀',
                mapLabel: 'الجزائر 3D View AR',
                arBtnText: 'نمط الواقع المعزز AR',
                exploreTitle: 'اكتشاف المغامرات والتصنيفات 🏜️🌊',
                adv1: 'سياحة صحراوية (جانْت والهقّار)',
                adv1desc: 'مغامرات الكثبان والرسومات التاسيلي التاريخية',
                adv2: 'سياحة بحرية (وهران، تيبازة، وشرشال)',
                adv2desc: 'شواطئ ساحرة وموانئ سياحية يختية',
                adv3: 'سياحة جبلية (جرجرة وتيكجدة)',
                adv3desc: 'مسارات الجبال، الثلوج، والتخييم',
                passportTitle: 'جواز السفر الرقمي والأمان 🛡️',
                safetyTitle: 'مساعد الأمان والخدمات المحلية',
                safetyDesc: 'تنبيهات الطقس والازدحام المباشرة زر الطوارئ السريع',
                emergencyBtn: 'إرسال استغاثة طوارئ سريعة 🆘',
                digitalPassport: 'جواز السفر السياحي الرقمي',
                badge1: 'وسام الاستكشاف الصحراوي',
                badge2: '450 نقطة مكافآت',
                translatorTitle: 'المترجم الفوري والنظام 🌐',
                liveTranslator: 'المترجم الفوري المباشر',
                transPlaceholder: 'اكتب النص للترجمة المباشرة...',
                translateBtn: 'ترجمة',
                navHome: 'الرئيسية',
                navExplore: 'المغامرات',
                navPassport: 'الجواز',
                navProfile: 'المترجم',
                navSites: 'المواقع',
                navRobot: 'الروبوت',
                navSupport: 'الدعم',
                navLinks: 'الخدمات',
                sitesTitle: '🗺️ 17 موقعاً سياحياً جزائرياً',
                robotTitle: '🤖 الروبوت الذكي لتوجيه السياح',
                supportTitle: '🎧 الدعم الفني الذكي 24/7',
                linksTitle: '🔗 دليل الخدمات والنقل السريع',
                loginTitle: 'تسجيل الدخول',
                loginBtnText: 'تسجيل الدخول',
                sendCode: 'إرسال رمز التحقق',
                verifyBtn: 'تأكيد وتسجيل الدخول',
                loginStatus: 'تم إرسال رمز التحقق إلى رقمك',
                loginSuccess: 'تم تسجيل الدخول بنجاح!',
                loginError: 'رمز التحقق غير صحيح، حاول مجدداً',
                modal_hospitals_title: '🏥 المستشفيات والعيادات الطبية',
                modal_hospitals_item1: 'المركز الاستشفائي الجامعي (CHU)',
                modal_hospitals_desc1: 'طوارئ 24/7 وإحداثيات سريعة',
                modal_hospitals_item2: 'عيادات الإسعاف السياحي',
                modal_hospitals_desc2: 'خدمة طبية فورية باللغات الثلاث',
                modal_flights_title: '✈️ محطات الطيران والرحلات الجوية',
                modal_flights_item1: 'مطار هواري بومدين الدولي',
                modal_flights_desc1: 'حجز ومتابعة الرحلات الجوية',
                modal_ferry_title: '⛴️ الموانئ والباخرات السياحية',
                modal_ferry_item1: 'ميناء الجزائر / وهران البحري',
                modal_ferry_desc1: 'رحلات الباخرة والنقل البحري',
                modal_stations_title: '🚍 محطات النقل والقطارات',
                modal_stations_item1: 'المحطة المركزية للقطارات والحافلات',
                modal_stations_desc1: 'مواعيد وخطوط النقل البري',
                response_loading: '⏳ جاري تحليل الوجهة ومعالجة الخريطة...',
                response_success: 'تم تحديث الوجهة إلى {query} بنجاح. استمتع برحلتك الافتراضية!',
                twin_plan: 'مرحباً هواري، خطتك التلقائية الموصى بها عبر AI Twin: تيبازة 🏛️ -> شرشال 🏖️ -> الهقار 🏜️. الميزانية التقديرية: 250$ | الطقس: ممتاز | الدفع: عبر CPAY ROBOT AI 💳',
                twin_speak: 'تم إنشاء الخطة السياحية التلقائية المخصصة بنجاح بواسطة النسخة الرقمية الخاصة بك',
                ar_mode_activated: 'تم تفعيل وضع الواقع المعزز AR وإظهار الأسهم المضيئة فوق الكاميرا',
                emergency_alert: 'تم تنشيط زر الطوارئ وإرسال الإحداثيات فوراً إلى الخدمات المحلية والمستشفيات القريبة',
                translate_result: '[ترجمة هولوغرامية]: {text} (Translating to Local Dialect...)',
                modal_speak_hospitals: 'عرض قائمة المستشفيات والعيادات',
                modal_speak_flights: 'عرض قائمة محطات الطيران',
                modal_speak_ferry: 'عرض قائمة الموانئ والباخرات',
                modal_speak_stations: 'عرض قائمة محطات النقل',
                lang_changed_ar: 'تم تغيير اللغة إلى العربية',
                lang_changed_en: 'Language set to English',
                lang_changed_fr: 'Langue changée en Français',
                robot_greeting: 'مرحباً! أنا الروبوت الذكي المتخصص في السياحة الجزائرية. اسألني عن أي موقع.',
                robot_unknown: 'عذراً، لم أفهم سؤالك. يمكنك سؤالي عن أحد المواقع السياحية الجزائرية.',
                robot_site_info: '📍 {name} - {city}: {desc} (الإحداثيات: {lat}, {lng})',
            },
            en: {
                robotName: '3D Hologram Tour Robot',
                robotStatus: 'AI Twin Active Assistant',
                aiPlaceholder: 'Ask Hologram AI or search destination...',
                qHospitals: 'Hospitals',
                qFlights: 'Flights',
                qFerry: 'Ferries',
                qStations: 'Stations',
                twinTitle: 'Auto Planning (AI Twin Travel)',
                twinDesc: 'Analyze budget, time, and preferences for custom itinerary.',
                twinBtn: 'Generate Trip Plan 🚀',
                mapLabel: 'Algeria 3D View AR',
                arBtnText: 'AR Mode',
                exploreTitle: 'Discover Adventures 🏜️🌊',
                passportTitle: 'Digital Passport & Safety 🛡️',
                translatorTitle: 'Live Translator 🌐',
                navHome: 'Home',
                navExplore: 'Explore',
                navPassport: 'Passport',
                navProfile: 'Translator',
                navSites: 'Sites',
                navRobot: 'Robot',
                navSupport: 'Support',
                navLinks: 'Services',
                sitesTitle: '🗺️ 17 Algerian Tourist Sites',
                robotTitle: '🤖 AI Tourism Guide',
                supportTitle: '🎧 Smart Tech Support 24/7',
                linksTitle: '🔗 Transport & Service Links',
                loginTitle: 'Login',
                loginBtnText: 'Login',
                sendCode: 'Send Code',
                verifyBtn: 'Verify & Login'
            },
            fr: {
                robotName: 'Robot Touristique Hologramme 3D',
                robotStatus: 'Assistant AI Twin Actif',
                aiPlaceholder: 'Demandez à l\'Hologramme AI...',
                qHospitals: 'Hôpitaux',
                qFlights: 'Vols',
                qFerry: 'Bateaux',
                qStations: 'Gares',
                twinTitle: 'Planification Auto (AI Twin Travel)',
                twinDesc: 'Analyse du budget et temps pour circuit sur mesure.',
                twinBtn: 'Générer le Plan 🚀',
                mapLabel: 'Algérie Vue 3D AR',
                arBtnText: 'Mode AR',
                exploreTitle: 'Découvrir Aventures 🏜️🌊',
                passportTitle: 'Passeport Numérique & Sécurité 🛡️',
                translatorTitle: 'Traducteur En Direct 🌐',
                navHome: 'Accueil',
                navExplore: 'Aventures',
                navPassport: 'Passeport',
                navProfile: 'Traducteur',
                navSites: 'Sites',
                navRobot: 'Robot',
                navSupport: 'Support',
                navLinks: 'Services',
                sitesTitle: '🗺️ 17 Sites Touristiques Algériens',
                robotTitle: '🤖 Robot Guide Touristique',
                supportTitle: '🎧 Support Technique 24/7',
                linksTitle: '🔗 Guide Services et Transports',
                loginTitle: 'Connexion',
                loginBtnText: 'Connexion',
                sendCode: 'Envoyer Code',
                verifyBtn: 'Vérifier et Connecter'
            }
        };

        let currentLang = 'ar';
        let isSpeechEnabled = true;
        let isSatellite = true;
        let verificationCode = '';
        const algerianSites = {{ sites|tojson }};

        function getEl(id) { return document.getElementById(id); }

        function applyLanguage(lang) {
            const t = translations[lang] || translations['ar'];
            if (!t) return;
            if (getEl('robotName')) getEl('robotName').innerText = t.robotName || 'الروبوت السياحي';
            if (getEl('robotStatus')) getEl('robotStatus').innerText = t.robotStatus || 'AI Twin Active';
            if (getEl('aiQuery')) getEl('aiQuery').placeholder = t.aiPlaceholder || 'اسأل...';
            if (getEl('qHospitals')) getEl('qHospitals').innerText = t.qHospitals || 'مستشفيات';
            if (getEl('qFlights')) getEl('qFlights').innerText = t.qFlights || 'طيران';
            if (getEl('qFerry')) getEl('qFerry').innerText = t.qFerry || 'باخرة';
            if (getEl('qStations')) getEl('qStations').innerText = t.qStations || 'محطات';
            if (getEl('twinTitle')) getEl('twinTitle').innerText = t.twinTitle || 'التخطيط التلقائي';
            if (getEl('twinDesc')) getEl('twinDesc').innerText = t.twinDesc || 'تحليل الخطة...';
            if (getEl('twinBtn')) getEl('twinBtn').innerText = t.twinBtn || 'توليد الخطة';
            if (getEl('mapLocationLabel')) getEl('mapLocationLabel').innerText = t.mapLabel || 'خريطة 3D';
            if (getEl('arBtnText')) getEl('arBtnText').innerText = t.arBtnText || 'AR Mode';
            if (getEl('exploreTitle')) getEl('exploreTitle').innerText = t.exploreTitle || 'المغامرات';
            if (getEl('passportTitle')) getEl('passportTitle').innerText = t.passportTitle || 'الجواز';
            if (getEl('translatorTitle')) getEl('translatorTitle').innerText = t.translatorTitle || 'المترجم';
            if (getEl('navHome')) getEl('navHome').innerText = t.navHome || 'الرئيسية';
            if (getEl('navExplore')) getEl('navExplore').innerText = t.navExplore || 'المغامرات';
            if (getEl('navPassport')) getEl('navPassport').innerText = t.navPassport || 'الجواز';
            if (getEl('navProfile')) getEl('navProfile').innerText = t.navProfile || 'المترجم';
            if (getEl('navSites')) getEl('navSites').innerText = t.navSites || 'المواقع';
            if (getEl('navRobot')) getEl('navRobot').innerText = t.navRobot || 'الروبوت';
            if (getEl('navSupport')) getEl('navSupport').innerText = t.navSupport || 'الدعم';
            if (getEl('navLinks')) getEl('navLinks').innerText = t.navLinks || 'الخدمات';
            if (getEl('sitesTitle')) getEl('sitesTitle').innerText = t.sitesTitle || 'المواقع';
            if (getEl('robotTitle')) getEl('robotTitle').innerText = t.robotTitle || 'الروبوت';
            if (getEl('supportTitle')) getEl('supportTitle').innerText = t.supportTitle || 'الدعم الفني';
            if (getEl('linksTitle')) getEl('linksTitle').innerText = t.linksTitle || 'الروابط السريعة';
            if (getEl('loginTitle')) getEl('loginTitle').innerHTML = `<i class="fa-solid fa-user-lock"></i> ${t.loginTitle || 'تسجيل الدخول'}`;
            if (getEl('loginBtnText')) getEl('loginBtnText').innerText = t.loginBtnText || 'تسجيل الدخول';
            if (getEl('sendCodeBtn')) getEl('sendCodeBtn').innerText = t.sendCode || 'إرسال الرمز';
            if (getEl('verifyBtn')) getEl('verifyBtn').innerText = t.verifyBtn || 'تأكيد الدخول';
            window._translations = t;
        }

        function switchLanguage() {
            const newLang = document.getElementById('langSelect').value;
            if (newLang === currentLang) return;
            currentLang = newLang;
            applyLanguage(currentLang);
            const t = window._translations;
            const msg = currentLang === 'ar' ? t.lang_changed_ar : currentLang === 'en' ? t.lang_changed_en : t.lang_changed_fr;
            speakText(msg);
        }

        function speakText(text, lang = currentLang) {
            if (!isSpeechEnabled || !('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = lang === 'fr' ? 'fr-FR' : (lang === 'en' ? 'en-US' : 'ar-SA');
            utterance.pitch = 1.0;
            utterance.rate = 0.95;
            const avatar = getEl('robotAvatar');
            if (avatar) {
                utterance.onstart = () => avatar.classList.add('speaking');
                utterance.onend = () => avatar.classList.remove('speaking');
                utterance.onerror = () => avatar.classList.remove('speaking');
            }
            window.speechSynthesis.speak(utterance);
        }

        function stopSpeech() {
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
            if (getEl('robotAvatar')) getEl('robotAvatar').classList.remove('speaking');
        }

        function updateMap(query) {
            const mapFrame = getEl('gmapFrame');
            const mapTypeParam = isSatellite ? '&t=k' : '';
            mapFrame.src =
                `https://maps.google.com/maps?q=${encodeURIComponent(query)}&z=15${mapTypeParam}&ie=UTF8&iwloc=&output=embed`;
            const t = window._translations || translations[currentLang];
            getEl('mapLocationLabel').innerText = `${query} (${t.mapLabel ? t.mapLabel.split(' ').slice(1).join(' ') : '3D View'})`;
        }

        function askAIAndSpeak() {
            const query = getEl('aiQuery').value.trim();
            const res = getEl('aiResponse');
            if (!query) return;
            const t = window._translations || translations[currentLang];
            res.style.display = 'block';
            res.innerText = t.response_loading || 'جاري التحليل...';
            res.style.color = '#fbbf24';
            res.style.borderColor = 'rgba(251, 191, 36, 0.3)';
            setTimeout(() => {
                const responseText = (t.response_success || 'تم العثور على الوجهة: {query}').replace('{query}', query);
                res.innerText = responseText;
                res.style.color = '#4ade80';
                res.style.borderColor = 'rgba(16, 185, 129, 0.3)';
                speakText(responseText);
                updateMap(query);
            }, 500);
        }

        function runAITwin() {
            const res = getEl('aiResponse');
            const t = window._translations || translations[currentLang];
            res.style.display = 'block';
            res.innerText = t.twin_plan || 'تم توليد خطة السفر بنجاح.';
            res.style.color = '#a78bfa';
            res.style.borderColor = 'rgba(139, 92, 246, 0.3)';
            speakText(t.twin_speak || 'تم إنشاء الخطة تلقائياً');
        }

        function toggleARMode() {
            const t = window._translations || translations[currentLang];
            speakText(t.ar_mode_activated || 'تم تفعيل وضع AR');
            alert(t.ar_mode_activated || 'تم تفعيل وضع AR');
        }

        function triggerEmergency() {
            const t = window._translations || translations[currentLang];
            speakText(t.emergency_alert || 'تم إرسال طوارئ');
            alert('🚨 ' + (t.emergency_alert || 'تم إرسال استغاثة طوارئ سريعة'));
        }

        function translateLive() {
            const text = getEl('transInput').value.trim();
            if (!text) return;
            const t = window._translations || translations[currentLang];
            const result = (t.translate_result || '[ترجمة]: {text}').replace('{text}', text);
            getEl('transResult').innerText = result;
            speakText(text);
        }

        function selectAdventure(dest) {
            switchTab('home', document.querySelector('[data-screen="home"]'));
            getEl('aiQuery').value = dest;
            askAIAndSpeak();
        }

        function switchTab(screenId, btnElement) {
            document.querySelectorAll('.app-screen').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
            getEl(`screen-${screenId}`).classList.add('active');
            if (btnElement) btnElement.classList.add('active');
            if (screenId === 'sites') renderSites();
            if (screenId === 'robot') initRobotChat();
        }

        // ===== SERVICE MODAL =====
        const serviceData = {
            hospitals: {
                titleKey: 'modal_hospitals_title',
                items: [
                    { titleKey: 'modal_hospitals_item1', descKey: 'modal_hospitals_desc1', icon: 'fa-hospital' },
                    { titleKey: 'modal_hospitals_item2', descKey: 'modal_hospitals_desc2', icon: 'fa-user-doctor' }
                ],
                speakKey: 'modal_speak_hospitals'
            },
            flights: {
                titleKey: 'modal_flights_title',
                items: [{ titleKey: 'modal_flights_item1', descKey: 'modal_flights_desc1', icon: 'fa-plane' }],
                speakKey: 'modal_speak_flights'
            },
            ferry: {
                titleKey: 'modal_ferry_title',
                items: [{ titleKey: 'modal_ferry_item1', descKey: 'modal_ferry_desc1', icon: 'fa-ship' }],
                speakKey: 'modal_speak_ferry'
            },
            stations: {
                titleKey: 'modal_stations_title',
                items: [{ titleKey: 'modal_stations_item1', descKey: 'modal_stations_desc1', icon: 'fa-bus' }],
                speakKey: 'modal_speak_stations'
            }
        };

        function openModal(type) {
            const data = serviceData[type];
            if (!data) return;
            const t = window._translations || translations[currentLang];
            const titleText = t[data.titleKey] || 'تفاصيل الخدمة';
            getEl('modalTitle').innerHTML = `<i class="fa-solid fa-circle-info"></i> ${titleText}`;
            const modalBody = getEl('modalBody');
            modalBody.innerHTML = data.items.map(item => {
                const itemTitle = t[item.titleKey] || item.titleKey;
                const itemDesc = t[item.descKey] || item.descKey;
                return `
                    <div style="background:var(--glass-bg); border:1px solid var(--glass-border); padding:12px; border-radius:14px; display:flex; align-items:center; gap:12px;">
                        <i class="fa-solid ${item.icon}" style="font-size:1.3rem; color:var(--accent-cyan);"></i>
                        <div>
                            <h5 style="font-size:0.88rem;">${itemTitle}</h5>
                            <p style="font-size:0.75rem; color:var(--text-muted);">${itemDesc}</p>
                        </div>
                    </div>
                `;
            }).join('');
            getEl('serviceModal').classList.add('active');
            const speakMsg = t[data.speakKey] || 'عرض الخدمة';
            speakText(speakMsg);
        }

        function closeModal() {
            getEl('serviceModal').classList.remove('active');
            stopSpeech();
        }

        function closeModalOnOuter(e) {
            if (e.target.classList.contains('modal-overlay')) closeModal();
        }

        // ===== LOGIN MODAL =====
        function openLoginModal() {
            getEl('loginModal').classList.add('active');
            getEl('verificationArea').style.display = 'none';
            getEl('verifyBtn').style.display = 'none';
            getEl('loginStatus').innerText = '';
            getEl('sendCodeBtn').style.display = 'block';
            getEl('loginPhone').value = '';
            document.querySelectorAll('.code-input').forEach(inp => inp.value = '');
        }

        function closeLoginModal() {
            getEl('loginModal').classList.remove('active');
            stopSpeech();
        }

        function closeLoginModalOnOuter(e) {
            if (e.target.classList.contains('modal-overlay')) closeLoginModal();
        }

        function sendVerificationCode() {
            const phone = getEl('loginPhone').value.trim();
            if (!phone) {
                getEl('loginStatus').innerText = 'الرجاء إدخال رقم الهاتف أو البريد';
                return;
            }
            verificationCode = Math.floor(1000 + Math.random() * 9000).toString();
            console.log('رمز التحقق:', verificationCode);
            const t = window._translations || translations[currentLang];
            getEl('loginStatus').innerText = (t.loginStatus || 'تم إرسال رمز التحقق') + ' (' + verificationCode + ')';
            getEl('sendCodeBtn').style.display = 'none';
            getEl('verificationArea').style.display = 'flex';
            getEl('verifyBtn').style.display = 'block';
            document.querySelector('.code-input').focus();
        }

        function verifyLogin() {
            const inputs = document.querySelectorAll('.code-input');
            let entered = '';
            inputs.forEach(inp => entered += inp.value);
            const t = window._translations || translations[currentLang];
            if (entered === verificationCode) {
                getEl('loginStatus').innerHTML = `<span style="color:var(--accent-emerald);">${t.loginSuccess || 'تم تسجيل الدخول بنجاح!'}</span>`;
                getEl('loginBtnText').innerText = '👤 ' + getEl('loginPhone').value;
                setTimeout(() => closeLoginModal(), 1500);
            } else {
                getEl('loginStatus').innerHTML = `<span style="color:var(--accent-red);">${t.loginError || 'رمز التحقق غير صحيح، حاول مجدداً'}</span>`;
            }
        }

        // Auto-focus for verification inputs
        document.addEventListener('input', function(e) {
            if (e.target.classList.contains('code-input')) {
                if (e.target.value.length >= 1) {
                    const next = e.target.nextElementSibling;
                    if (next && next.classList.contains('code-input')) next.focus();
                }
            }
        });

        // ===== SITES SCREEN =====
        function renderSites() {
            const container = getEl('sitesContainer');
            if (!container) return;
            container.innerHTML = '';
            algerianSites.forEach(site => {
                const card = document.createElement('div');
                card.className = 'site-card';
                card.innerHTML = `
                    <i class="fa-solid fa-landmark"></i>
                    <h4>${site.name}</h4>
                    <p>${site.city}</p>
                    <p style="font-size:0.6rem; color:var(--text-muted);">${site.desc}</p>
                `;
                card.onclick = () => {
                    switchTab('home', document.querySelector('[data-screen="home"]'));
                    getEl('aiQuery').value = site.name + '، ' + site.city;
                    askAIAndSpeak();
                };
                container.appendChild(card);
            });
        }

        // ===== ROBOT CHAT =====
        let robotInitialized = false;

        function initRobotChat() {
            if (robotInitialized) return;
            const chatBox = getEl('chatBox');
            const t = window._translations || translations[currentLang];
            if (chatBox.children.length === 0) {
                const greeting = document.createElement('div');
                greeting.className = 'chat-msg bot';
                greeting.innerText = t.robot_greeting || 'مرحباً! أنا الروبوت الذكي المتخصص في السياحة الجزائرية.';
                chatBox.appendChild(greeting);
            }
            robotInitialized = true;
        }

        function sendRobotQuery() {
            const query = getEl('robotQuery').value.trim();
            if (!query) return;
            const chatBox = getEl('chatBox');
            const t = window._translations || translations[currentLang];

            const userMsg = document.createElement('div');
            userMsg.className = 'chat-msg user';
            userMsg.innerText = query;
            chatBox.appendChild(userMsg);
            getEl('robotQuery').value = '';

            let found = null;
            for (let site of algerianSites) {
                if (site.name.includes(query) || site.city.includes(query) || query.includes(site.name) || query.includes(site.city)) {
                    found = site;
                    break;
                }
            }

            const botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            if (found) {
                botMsg.innerText = (t.robot_site_info || '📍 {name} - {city}: {desc}')
                    .replace('{name}', found.name)
                    .replace('{city}', found.city)
                    .replace('{desc}', found.desc)
                    .replace('{lat}', found.lat)
                    .replace('{lng}', found.lng);
                speakText(botMsg.innerText);
            } else {
                botMsg.innerText = t.robot_unknown || 'عذراً لم أفهم سؤالك.';
                speakText(botMsg.innerText);
            }
            chatBox.appendChild(botMsg);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // ===== TECHNICAL SUPPORT CHAT =====
        function sendSupportQuery() {
            const query = getEl('supportQuery').value.trim();
            if (!query) return;
            const chatBox = getEl('supportChatBox');

            const userMsg = document.createElement('div');
            userMsg.className = 'chat-msg user';
            userMsg.innerText = query;
            chatBox.appendChild(userMsg);
            getEl('supportQuery').value = '';

            setTimeout(() => {
                const botMsg = document.createElement('div');
                botMsg.className = 'chat-msg bot';
                botMsg.innerText = `[الدعم الفني]: تم استلام استفسارك بخصوص (${query}). جاري المتابعة والتأكد من تقديم الإجابة الأكثر دقة لك عبر النظام.`;
                chatBox.appendChild(botMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
                speakText(botMsg.innerText);
            }, 600);
        }

        document.getElementById('robotQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); sendRobotQuery(); }
        });

        document.getElementById('supportQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); sendSupportQuery(); }
        });

        document.getElementById('aiQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); askAIAndSpeak(); }
        });

        document.getElementById('transInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); translateLive(); }
        });

        // ===== INIT =====
        applyLanguage('ar');
        document.getElementById('langSelect').value = 'ar';
        renderSites();
        console.log('✅ AI GLOBAL TOURISM V6 loaded successfully with Support & Link Directory.');
    </script>
</body>
</html>
"""

# ============================================================
# المسارات
# ============================================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, sites=ALGERIAN_SITES)

@app.route('/api/ai-process', methods=['POST'])
def ai_process():
    data = request.json or {}
    query = data.get('query', '').strip()
    lang = data.get('lang', 'ar')
    if not query:
        return jsonify({"status": "error", "reply": "الرجاء إدخال استعلام صحيح."})
    if lang == 'fr':
        reply = f"Hologramme AI analyse la destination: {query}. Navigation satellite 3D activée."
    elif lang == 'en':
        reply = f"Hologram AI processing destination: {query}. 3D Satellite navigation active."
    else:
        reply = f"الروبوت الهولوغرامي يحلل الموقع العالمي: {query}. تم عرض الخريطة والملاحة الفضائية 3D."
    return jsonify({"status": "success", "query": query, "reply": reply})

# ============================================================
# تشغيل الخادم على المنفذ 7000
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
