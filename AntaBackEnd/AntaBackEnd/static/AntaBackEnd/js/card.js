// JavaScript pour gérer l'ouverture/fermeture du panier
    document.addEventListener('DOMContentLoaded', function() {
        const cartCount = document.getElementById('cart-count');
        const cartModal = document.getElementById('cart-modal');
        const closeCart = document.getElementById('close-cart');
        const cartOverlay = document.getElementById('cart-overlay');

        cartCount.addEventListener('click', function() {
            cartModal.classList.add('active');
            cartOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        closeCart.addEventListener('click', function() {
            cartModal.classList.remove('active');
            cartOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });

        cartOverlay.addEventListener('click', function() {
            cartModal.classList.remove('active');
            cartOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    });