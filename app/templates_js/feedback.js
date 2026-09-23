(function() {
    const c = document.getElementById('stars');
    for (let i = 0; i < 120; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        s.style.left = Math.random()*100 + '%';
        s.style.top = Math.random()*100 + '%';
        s.style.setProperty('--dur', (1.5 + Math.random()*3) + 's');
        s.style.animationDelay = Math.random()*4 + 's';
        s.style.width = s.style.height = (1 + Math.random()*2) + 'px';
        c.appendChild(s);
    }
})();

(function() {
    const c = document.getElementById('particles');
    for (let i = 0; i < 20; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.left = Math.random()*100 + '%';
        p.style.bottom = '-10px';
        p.style.setProperty('--s', (2 + Math.random()*3) + 'px');
        p.style.setProperty('--dur', (6 + Math.random()*10) + 's');
        p.style.setProperty('--del', Math.random()*12 + 's');
        c.appendChild(p);
    }
})();

let mountainShown = false, templeShown = false, godsShown = false;

function showMountain() {
    const el = document.getElementById('mountain');
    const btn = document.getElementById('btn-mountain');
    if (!mountainShown) {
        el.classList.add('show');
        btn.classList.add('active');
        mountainShown = true;
    } else {
        el.classList.remove('show');
        btn.classList.remove('active');
        mountainShown = false;
    }
}

function showTemple() {
    const el = document.getElementById('temple');
    const btn = document.getElementById('btn-temple');
    if (!templeShown) {
        if (!mountainShown) showMountain();
        el.classList.add('show');
        btn.classList.add('active');
        templeShown = true;
    } else {
        el.classList.remove('show');
        btn.classList.remove('active');
        templeShown = false;
    }
}

function showGods() {
    const el = document.getElementById('gods');
    const btn = document.getElementById('btn-gods');
    if (!godsShown) {
        if (!mountainShown) showMountain();
        if (!templeShown) showTemple();
        el.classList.add('show');
        btn.classList.add('active');
        godsShown = true;
    } else {
        el.classList.remove('show');
        btn.classList.remove('active');
        godsShown = false;  
    }
}

async function sendAppeal() {
    const btn = document.getElementById('sendBtn');
    const message = document.getElementById('message');
    const appealType = document.getElementById('appealType');

    const text = message.value.trim();
    const type = appealType.value;

    if (!text) {
        alert('Please write yours appeal before send.');
        return;
    }
    if (!type) {
        alert('Please select type appeal.');
        return;
    }

    btn.disabled = true;
    btn.style.transform = 'scale(1.3) rotate(15deg)';
    btn.style.boxShadow = '0 0 50px rgba(19, 16, 11, 0.8)';

    try {
        const res = await fetch('/feedback/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_name: type, appeal: text }),
        });
        const data = await res.json();
        if (!res.ok) {
            alert('Error: ' + (data.message || res.status));
            return;
        }
        message.value = '';
        alert('🗳️ Yours appeal accepted (id ' + data.appeal_id + ') and will reviewed gods Olympys.');
    } catch (err) {
        alert('Send failed: ' + err);
    } finally {
        btn.disabled = false;
        setTimeout(() => {
            btn.style.transform = '';
            btn.style.boxShadow = '';
        }, 400);
    }
}