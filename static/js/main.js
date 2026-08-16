// ==========================================
// CPAY ROBOT AI V5 - FRONTEND INTERACTION LOGIC
// ==========================================

let isSpeechEnabled = true;
let currentLang = 'ar';

// 1. التنقل بين الشاشات
function switchTab(screenId, btnElement) {
    document.querySelectorAll('.app-screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    
    const targetScreen = document.getElementById(`screen-${screenId}`);
    if (targetScreen) targetScreen.classList.add('active');
    if (btnElement) btnElement.classList.add('active');
}

// 2. إرسال الاستفسار إلى خادم Flask
async function askAIAndSpeak() {
    const inputElem = document.getElementById('aiQuery');
    const query = inputElem ? inputElem.value.trim() : '';
    if (!query) return;

    const resElem = document.getElementById('aiResponse');
    if (resElem) {
        resElem.style.display = 'block';
        resElem.innerText = "جاري الاتصال بالخادم وتحليل الطلب...";
    }

    try {
        const response = await fetch('/api/ai-process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, lang: currentLang })
        });

        const data = await response.json();
        const replyText = data.reply || data.message;

        if (resElem) resElem.innerText = replyText;
        speakText(replyText);

        const iframe = document.getElementById('gmapFrame');
        if (iframe) {
            iframe.src = `https://maps.google.com/maps?q=${encodeURIComponent(query)}&z=12&t=k&ie=UTF8&iwloc=&output=embed`;
        }
    } catch (err) {
        console.error("API Error:", err);
        if (resElem) resElem.innerText = "حدث خطأ أثناء الاتصال بالخادم.";
    }
}

// 3. تحويل النص إلى صوت
function speakText(text, lang = currentLang) {
    if (!isSpeechEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang === 'fr' ? 'fr-FR' : (lang === 'en' ? 'en-US' : 'ar-SA');
    utterance.pitch = 1.0;
    utterance.rate = 0.95;

    const avatar = document.getElementById('robotAvatar');
    utterance.onstart = () => { if (avatar) avatar.classList.add('speaking'); };
    utterance.onend = () => { if (avatar) avatar.classList.remove('speaking'); };

    window.speechSynthesis.speak(utterance);
}

// 4. تغيير اللغة
function switchLanguage() {
    const langSelect = document.getElementById('langSelect');
    if (langSelect) {
        currentLang = langSelect.value;
        const msg = currentLang === 'fr' ? "Langue changée" : (currentLang === 'en' ? "Language updated" : "تم تغيير اللغة");
        speakText(msg);
    }
}

