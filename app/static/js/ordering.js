async function orderProduct(productId) {
    const btn = document.getElementById(`btn-${productId}`);
    const qtyBadge = document.getElementById(`qty-${productId}`);
    const orderQtyInput = document.getElementById(`order-qty-${productId}`);
    const quantity = parseInt(orderQtyInput.value, 10);
    if (isNaN(quantity) || quantity <= 0) {
        alert('Proszę wprowadzić prawidłową ilość do zamówienia.');
        return;
    }

    try {
        // Sending POST request to order the product
        const response = await fetch(`/api/products/${productId}/order?order_quantity=${quantity}`, {
            method: 'POST'
        });

        if (response.ok) {
            const data = await response.json();

            // Live actualization of the quantity badge
            qtyBadge.innerText = `${data.remaining} szt.`;

             if (data.remaining <= 0) {
                qtyBadge.classList.replace('bg-success', 'bg-danger');
                qtyBadge.innerText = "Brak w magazynie";
                btn.disabled = true;
             }

             alert(`Sukces: ${data.message}`);
        } else {
            const errorData = await response.json();
            alert(`Błąd: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Błąd sieci:', error);
        alert('Nie udało się połączyć z API');
    }
}