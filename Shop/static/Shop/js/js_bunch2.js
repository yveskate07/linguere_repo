// Initialisation AOS
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });

    // Fonction pour extraire le prix numérique d'un élément de prix
    function extractPrice(priceElement) {
        const priceText = priceElement.textContent;
        return parseInt(priceText.replace(/\D/g, '')) || 0;
    }

    // Fonction pour mettre à jour l'affichage des valeurs de prix
    function updatePriceValues() {
        const priceRange = document.querySelector('.price-range');
        const priceValues = document.querySelectorAll('.price-values span');
        priceValues[1].textContent = parseInt(priceRange.value).toLocaleString() + ' CFA';
    }

    // Écouteur d'événement pour le menu déroulant de tri
    document.addEventListener('DOMContentLoaded', function() {

        // Initialiser les autres fonctions comme avant
        if (typeof AOS !== 'undefined') {
            AOS.init({ duration: 800, easing: 'ease-in-out', once: true });
        }
    });

    // Fonction pour les filtres
    function toggleFilter(id) {
        const filter = document.getElementById(id);
        const icon = filter.previousElementSibling.querySelector('i');
        filter.classList.toggle('show');
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-up');
    }