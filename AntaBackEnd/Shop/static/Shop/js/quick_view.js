function showQuickView(name, image, description, price, stock, category, prd_id) {
    const modal = document.getElementById('quick-view-modal');
    document.getElementById('quick-view-title').textContent = name;
    document.getElementById('quick-view-img').src = image;
    document.getElementById('quick-view-desc').textContent = description;
    document.getElementById('quick-view-price').textContent = price.toLocaleString() + ' CFA';
    document.getElementById('quick-view-category').textContent = category;
    document.getElementById('quantity').value = 1;
    document.getElementById('prd_id').value = prd_id;

    let stockHtml = '';
    if (stock > 10) {
        stockHtml = `<span class="text-success"><i class="fas fa-check-circle me-1"></i> En stock (${stock} unités)</span>`;
    } else if (stock > 0) {
        stockHtml = `<span class="text-warning"><i class="fas fa-exclamation-circle me-1"></i> Stock limité (${stock} unités)</span>`;
    } else {
        stockHtml = `<span class="text-danger"><i class="fas fa-times-circle me-1"></i> En rupture de stock</span>`;
    }
    document.getElementById('quick-view-stock').innerHTML = stockHtml;

    modal.style.display = 'flex';
}

function closeQuickView() {
    document.getElementById('quick-view-modal').style.display = 'none';
}

// Fonction pour ajouter depuis l'aperçu rapide
function addToCartFromQuickView() {
    const name = document.getElementById('quick-view-title').textContent;
    const priceText = document.getElementById('quick-view-price').textContent;
    const price = parseInt(priceText.replace(/\D/g, ''));
    const category = document.getElementById('quick-view-category').textContent;
    const image = document.getElementById('quick-view-img').src;
    const quantity = parseInt(document.getElementById('quantity').value);
    const prd_id = document.getElementById('prd_id').value;

    addToCart(name, price, category, image, quantity, prd_id);
}