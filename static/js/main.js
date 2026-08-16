async function askAI() {
    const input = document.getElementById('aiQuery');
    const responseBox = document.getElementById('aiResponse');
    if (!input || !input.value.trim()) return;

    responseBox.innerText = "جاري البحث واستكشاف الوجهة...";

    try {
        const res = await fetch('/api/ai-process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: input.value })
        });
        const data = await res.json();
        responseBox.innerText = data.reply || data.message || "تم استلام الرد.";
    } catch (err) {
        responseBox.innerText = "حدث خطأ أثناء الاتصال بالمرشد الذكي.";
    }
}
