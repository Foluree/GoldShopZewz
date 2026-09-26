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
    
    apply('All');
})();