// Hop & Barley — behaviours for the Django templates.
// Auth, cart math and pagination are server-side now; JS only handles
// small progressive enhancements.

document.addEventListener('DOMContentLoaded', () => {

    // --- Каталог: надсилати форму фільтра, коли прапорець категорії перемикається ---
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.querySelectorAll('input[type="checkbox"]').forEach((box) => {
            box.addEventListener('change', () => filterForm.submit());
        });
    }

    // --- Сторінка товару: accordion ---
    document.querySelectorAll('.accordion-title').forEach((title) => {
        title.addEventListener('click', () => {
            title.closest('.accordion-item').classList.toggle('active');
        });
    });

    // --- Сторінка товару: кроковий індикатор кількості поруч із кнопкою «Додати до кошика» ---
    document.querySelectorAll('.quantity-counter').forEach((counter) => {
        const input = counter.querySelector('input[name="quantity"]');
        const label = counter.querySelector('.quantity-value');
        if (!input) return;
        counter.querySelectorAll('.quantity-btn').forEach((btn) => {
            btn.addEventListener('click', (event) => {
                event.preventDefault();
                const delta = btn.dataset.action === 'increase' ? 1 : -1;
                const max = parseInt(input.max || '99', 10);
                const next = Math.min(max, Math.max(1, parseInt(input.value, 10) + delta));
                input.value = String(next);
                if (label) label.textContent = String(next);
            });
        });
    });

    // --- Панель керування обліковим записом / адміністратором: вкладки ---
    const tabs = document.querySelectorAll('.account-tab[data-tab-target]');
    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            tabs.forEach((t) => t.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach((p) => p.classList.remove('active'));
            tab.classList.add('active');
            const pane = document.querySelector(tab.dataset.tabTarget);
            if (pane) pane.classList.add('active');
        });
    });

    // --- Автоматично приховувати миттєві повідомлення ---
    document.querySelectorAll('.flash-message').forEach((el) => {
        setTimeout(() => { el.classList.add('flash-message--hidden'); }, 4000);
    });
});
