(function () {
    // Filtres (catégorie + année) sur la liste des événements
    var cards = document.querySelectorAll('.event-card');
    if (cards.length) {
        var state = { category: 'all', year: 'all' };
        var empty = document.getElementById('gallery-empty');
        function apply() {
            var n = 0;
            cards.forEach(function (c) {
                var ok = (state.category === 'all' || c.dataset.category === state.category) &&
                         (state.year === 'all' || c.dataset.year === state.year);
                c.style.display = ok ? '' : 'none';
                if (ok) n++;
            });
            if (empty) empty.style.display = n ? 'none' : '';
        }
        document.querySelectorAll('.gallery-filter').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var group = btn.dataset.group;
                document.querySelectorAll('.gallery-filter[data-group="' + group + '"]')
                    .forEach(function (b) { b.classList.remove('active'); });
                btn.classList.add('active');
                state[group] = btn.dataset.value;
                apply();
            });
        });
    }

    // Grille de photos : "Afficher plus" + visionneuse
    var items = Array.prototype.slice.call(document.querySelectorAll('.photo-item'));
    if (!items.length) return;

    var BATCH = 24, shown = 0;
    var more = document.getElementById('load-more');
    function reveal() {
        items.slice(shown, shown + BATCH).forEach(function (el) { el.classList.remove('hidden'); });
        shown = Math.min(shown + BATCH, items.length);
        if (more) {
            more.style.display = shown >= items.length ? 'none' : '';
            more.textContent = 'Afficher plus (' + (items.length - shown) + ' restantes)';
        }
    }
    if (more) more.addEventListener('click', reveal);
    reveal();

    var lb = document.getElementById('lightbox');
    var img = document.getElementById('lb-img');
    var count = document.getElementById('lb-count');
    var idx = 0;
    function show(i) {
        idx = (i + items.length) % items.length;
        img.src = items[idx].dataset.src;
        count.textContent = (idx + 1) + ' / ' + items.length;
    }
    function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }
    items.forEach(function (el, i) {
        el.addEventListener('click', function () {
            show(i);
            lb.classList.add('open');
            document.body.style.overflow = 'hidden';
        });
    });
    document.getElementById('lb-close').onclick = close;
    document.getElementById('lb-prev').onclick = function () { show(idx - 1); };
    document.getElementById('lb-next').onclick = function () { show(idx + 1); };
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
        if (!lb.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') show(idx - 1);
        if (e.key === 'ArrowRight') show(idx + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
        x0 = null;
    });
})();
