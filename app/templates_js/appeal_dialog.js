(function () {
    var appealId = window.DIALOG_APPEAL_ID;
    var profile = window.DIALOG_PROFILE || {};

    var thread = document.getElementById('thread');
    var input = document.getElementById('replyText');
    var btn = document.getElementById('replyBtn');
    var title = document.getElementById('threadTitle');
    var sub = document.getElementById('threadSub');
    var badge = document.getElementById('threadBadge');

    function node(tag, cls, text) {
        var el = document.createElement(tag);
        if (cls) el.className = cls;
        if (text !== undefined && text !== null) el.textContent = String(text);
        return el;
    }

    function fmtTime(iso) {
        if (!iso) return '';
        var d = new Date(iso);
        if (isNaN(d.getTime())) return '';
        return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }) +
            ' ' + d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    }
    function setBadge(data) {
        var last = data.messages[data.messages.length - 1];
        var lastMod = null;
        for (var i = data.messages.length - 1; i >= 0; i--) {
            if (data.messages[i].kind === 'moderator') { lastMod = data.messages[i]; break; }
        }

        badge.className = 'chat-badge';
        if (!lastMod) {
            badge.textContent = 'waiting for moderator';
            return;
        }
        badge.textContent = lastMod.reaction ? 'accepted' : 'rejected';
        badge.className = 'chat-badge ' + (lastMod.reaction ? 'ok': 'no');

        if (last && last.kind === 'moderator') input.placeholder = 'Write your reply…';
        else input.placeholder = 'Write a message…';
    }

    function render(data) {
        title.textContent = 'Dialog · № ' + data.root_id;
        sub.textContent = (data.table_name || '') + ' · ' + data.messages.length + ' messages · ' + (profile.email || '');
        setBadge(data);

        thread.innerHTML = '';
        
        if (!data.messages.length) {
            thread.appendChild(node('p', 'chat-empty', 'No messages yet'));
            return;
        }

        data.messages.forEach(function (message) {
            var bubble = node('div', 'msg ' + (message.kind === 'user' ? 'user' : 'mod'));
            
            var who = node('div', 'who');
            who.appendChild(node('span', null, message.kind === 'user' ? 'You': 'Moderator'));
            if (message.reaction !== null && message.reaction !== undefined) {
                who.appendChild(node('span', 'react ' + (message.reaction ? 'yes' : 'no'),
                    message.reaction ? 'accepted' : 'rejected'));
            }
            bubble.appendChild(who);

            bubble.appendChild(node('div', 'body', message.text || '-'));

            var foot = node('div', 'foot');
            foot.appendChild(node('span', null, message.email || ''));
            foot.appendChild(node('span', null, fmtTime(message.created_at)));
            bubble.appendChild(foot);

            thread.appendChild(bubble);
        });

        thread.scrollTop = thread.scrollHeight;
    }

    function showError(text) {
        thread.innerHTML = '';
        thread.appendChild(node('p', 'chat-error', text));
    }

    async function load() {
        try {
            var res = await fetch('/appeal_admid_check/api/dialog?appeal_id=' + appealId);
            var data = await res.json().catch(function () { return {}; });
            if (!res.ok) {
                showError(data.message || ('Error ' + res.status));
                return;
            }
            render(data);
        } catch (err) {
            showError('Load failed:' + err);
        }
    }

    async function send() {
        var text = input.value;

        btn.disabled = true;
        btn.textContent = 'Sending…';

        try {
            var res = await fetch('/appeal_admid_check/api/dialog/reply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ appeal_id: appealId, text: text })
            });
            var data = await res.json().catch(function () { return {}; });
            if (!res.ok) {
                alert('Error: ' + (data.message || res.status));
                return;
            }
            input.value = '';
            input.style.height = '';
            render(data);
        } catch (err) {
            alert('Send failed: ' + err);
        } finally {
            btn.disabled = false;
            btn.textContent = 'Send';
            input.focus();
        }
    }

    btn.addEventListener('click', send);

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (!btn.disabled) send();
        }
    });

    input.addEventListener('input', function () {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 150) + 'px';
    });

    load();
})();