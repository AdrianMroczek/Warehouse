        document.addEventListener('DOMContentLoaded', () => {
            loadCategories();
            loadProducts();


        document.getElementById('applyFilters').addEventListener('click', () => {
            const filters = {
                name: document.getElementById('nameFilter').value,
                category_id: document.getElementById('categoryFilter').value,
                price: document.getElementById('priceFilter').value,
                status: document.getElementById('availabilityFilter').value
            };
            loadProducts(filters);
        });
    });

    async function loadCategories() {
        try {
            const response = await fetch('/api/categories');
            const categories = await response.json();
            const select = document.getElementById('categoryFilter');

            categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Błąd podczas pobierania kategorii:', error);
        }
    }

    async function loadProducts(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.name) params.append('name', filters.name);
            if (filters.category_id) params.append('category_id', filters.category_id);
            if (filters.price) params.append('max_price', filters.price);
            if (filters.status) params.append('status', filters.status);

            const response = await fetch(`/api/products?${params.toString()}`);

            if (response.status === 404) {
                alert("Nie znaleziono produktów dla wybranych filtrów.");
                return;
            }

            const products = await response.json();
            renderTable(products);
        } catch (error) {
            console.error('Błąd podczas pobierania produktów:', error);
        }
    }

    function renderTable(products) {
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';

    products.forEach(p => {
        const tr = document.createElement('tr');

        const badgeClass = p.quantity > 0 ? 'bg-success' : 'bg-danger';
        const badgeText = p.quantity > 0 ? `${p.quantity} szt.` : 'Brak w magazynie';
        const isBtnDisabled = p.quantity <= 0 ? 'disabled' : '';

        tr.innerHTML = `
            <td>${p.name}</td>
            <td>${p.category ? p.category.name : 'Brak'}</td>
            <td>${parseFloat(p.price).toFixed(2)} zł</td>
            <td>
                <span id="qty-${p.id}" class="badge ${badgeClass}">
                    ${badgeText}
                </span>
            </td>
            <td>
                <div class="input-group input-group-sm" style="max-width: 130px;">
                    <button onclick="orderProduct(${p.id})"
                        id="btn-${p.id}"
                        class="btn btn-sm btn-outline-primary"
                        ${isBtnDisabled}>
                    Zamów
                    </button>
                    <input type="number"
                           oninput="if(this.value > ${p.quantity}) this.value = ${p.quantity};"
                           id="order-qty-${p.id}" min="1" max="${p.quantity}" value="1"
                           class="form-control form-control-sm">
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}