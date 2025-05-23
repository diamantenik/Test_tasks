document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[name="city"]');
    input.addEventListener('input', async () => {
        const query = input.value;
        if (query.length < 2) return;

        const list = document.getElementById('suggestions');
        list.innerHTML = '';
        const cities = await fetch(`/static/cities.json`).then(r => r.json());
        const matched = cities.filter(c => c.toLowerCase().includes(query.toLowerCase())).slice(0, 5);
        matched.forEach(city => {
            const div = document.createElement('div');
            div.textContent = city;
            div.classList.add('suggestion');
            div.addEventListener('click', () => {
                input.value = city;
                list.innerHTML = '';
            });
            list.appendChild(div);
        });
    });
});
