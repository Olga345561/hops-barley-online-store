document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.querySelectorAll('input[type="checkbox"]').forEach((box) => {
            box.addEventListener('change', () => filterForm.submit());
        });
    }
    document.querySelectorAll('.flash-message').forEach((el) => {
        setTimeout(() => { el.classList.add('flash-message--hidden'); }, 4000);
    });
});