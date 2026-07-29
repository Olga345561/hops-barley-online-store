document.addEventListener('DOMContentLoaded', function() {
    const calcBtn = document.getElementById('calculate-btn');
    if (calcBtn) {
        calcBtn.addEventListener('click', function() {
            // Замінюємо кому на крапку на випадок введення з української розкладки
            const ogVal = document.getElementById('og-input').value.replace(',', '.');
            const fgVal = document.getElementById('fg-input').value.replace(',', '.');

            const og = parseFloat(ogVal);
            const fg = parseFloat(fgVal);
            const resultDiv = document.getElementById('calc-result');
            const abvSpan = document.getElementById('abv-value');

            if (isNaN(og) || isNaN(fg) || og <= fg) {
                alert('Please enter the correct values ​​(OG must be greater than FG, e.g. 1.050 and 1.010).');
                return;
            }

            const abv = (og - fg) * 131.25;
            abvSpan.textContent = abv.toFixed(2);
            resultDiv.style.display = 'block';
        });
    }
});