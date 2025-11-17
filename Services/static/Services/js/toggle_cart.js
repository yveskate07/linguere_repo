// Gestion des modales
function toggleCartModal() {
    const cartModal = document.getElementById('cart-modal');
    if (cartModal.style.display === 'block') {
        cartModal.style.display = 'none';
    } else {
        cartModal.style.display = 'block';
    }
}