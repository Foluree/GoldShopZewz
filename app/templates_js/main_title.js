async function buy(offerId) {
const shopId = 1;
const res = await fetch('/api/order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ offer_id: offerId, shop_id: shopId, quantity: 1 })
});

const data = await res.json();
document.getElementById('status').textContent = data.message;
}