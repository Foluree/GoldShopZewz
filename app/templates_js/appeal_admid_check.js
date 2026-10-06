(function () {
    const buttons = document.querySelectorAll('.cat-btn');
    const cards = document.querySelectorAll('.card');
    const shown = document.getElementById('shownCount');
    const empty = document.getElementById('emptyHint');

    function apply(cat) {
        let count = 0;
        cards.forEach(function (card) {
            const visible = (cat === 'All' || card.dataset.category === cat);
            card.style.display = visible ? '' : 'none';
            if (visible) count++;
        });
        shown.textContent = String(count);
        empty.style.display = count ? 'none' : 'block';
    }

    buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            buttons.forEach(function (b) { b.classList.toggle('active', b === btn); });
            apply(btn.dataset.cat);
        });
    });
    
    function showModeration(card, data, answer) {
        const badge = card.querySelector('.card-badge');
        if (badge) {
            badge.textContent = data.reaction ? 'Accepted' : 'Rejected';
            badge.className = 'card-badge ' + (data.reaction ? 'badge-accept' : 'badge-reject');
        }

        const block = card.querySelector('.card-answer');
        if (block) {
            block.hidden = false;
            const plate = block.querySelector('[data-answer-plate]');
            if (plate) {
                plate.textContent = answer || '- (without reason) -';
                plate.className = 'textplate ' + (data.reaction ? 'accept': 'reject');
            }
            const mail = block.querySelector('[data-answer-mail]');
            if (mail) mail.textContent = data.moderator_email || '';
        }
    }

    async function moderate(card, btn) {
        const appealId = Number(card.dataset.appealId);
        const accepted = btn.classList.contains('btn-accept');
        const field = btn.closest('.action').querySelector('textarea');
        const answer = field ? field.value.trim() : '';
        const label = btn.textContent;

        const cardButtons = card.querySelectorAll('.action-btn');
        cardButtons.forEach(function (b) { b.disabled = true; });
        btn.textContent = 'Saving...';

        try {
            const res = await fetch('/appeal_admid_check/api/moderate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ appeal_id: appealId, reaction: accepted, answer: answer })
            });
            const data = await res.json().catch(function () { return {}; });
            if (!res.ok) {
                alert('Error: ' + (data.message || res.status));
                return;
            }
            if (field) field.value = '';
            showModeration(card, data, answer);
        } catch (err) {
            alert('Send failed: ' + err);
        } finally {
            cardButtons.forEach(function (b) { b.disabled = false; });
            btn.textContent = label;
        }
    }

    cards.forEach(function (card) {
        card.querySelectorAll('.action-btn').forEach(function (btn) {
            btn.addEventListener('click', function () { moderate(card, btn); });
        });
    });

    apply('All');
})();