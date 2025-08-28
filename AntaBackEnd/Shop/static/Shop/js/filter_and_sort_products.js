document.addEventListener('DOMContentLoaded', function () {
    
    // Sélectionner tous les éléments à surveiller
    const categoryChecks = document.querySelectorAll('.category_checks');
    const priceRange = document.querySelector('.price-range');
    const disponibChecks = document.querySelectorAll('.disponib_checks');
    const filterSection = document.querySelector('.filter-section');
    var sortSelect = document.getElementById('sort-select');

    // Fonction pour collecter les données des filtres
    /*function collectAndSendFilterData() {
        const data = {
            'categories': [],
            'price_range': [0, parseInt(priceRange.value)],
            'disponibility': []
        };

        // Récupérer les catégories sélectionnées
        categoryChecks.forEach(function(checkbox) {
            if (checkbox.checked) {
                data.categories.push(checkbox.id);
            }
        });

        // Récupérer la plage de prix (min est fixé à 0, max est la valeur du range)
        // Si vous avez aussi un input pour le prix min, vous devrez l'ajouter ici

        // Récupérer les états de disponibilité sélectionnés
        disponibChecks.forEach(function(checkbox) {
            if (checkbox.checked) {
                data.disponibility.push(checkbox.id);
            }
        });
        return data;
    }

    function collectSortData() {
        const selectedValue = sortSelect.value;
        const data = {
            'type': 'sort',
            'sort': selectedValue === 'none' ? null : selectedValue
        };

        return data;
    }*/

    // Fonction pour insérer ou mettre à jour le bouton
    function updateDisplayButton() {
        // Vérifier si le bouton existe déjà
        let showBtn = document.getElementById("showBtn");

        if (showBtn.style.display == "none") {
            showBtn.style.display = 'block';
        }

    }

    // Ajouter des écouteurs d'événements pour les cases à cocher de catégorie
    categoryChecks.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateDisplayButton);
    });

    // Ajouter un écouteur d'événements pour le range de prix
    document.getElementById('minPrice').addEventListener('change', updateDisplayButton);
    document.getElementById('maxPrice').addEventListener('change', updateDisplayButton);

    // Ajouter des écouteurs d'événements pour les cases à cocher de disponibilité
    disponibChecks.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateDisplayButton);
    });


    // Fonction pour collecter les données des filtres et les envoyer par websocket
    function collectAndSendFilterData() {
        
        const data = {
            'type': 'filter',
            'filters': collectFilterData()
        };

        socket.send(JSON.stringify(data));
    }

    // Fonction pour collecter la requete de tri et l'envoyer par websocket
    function collectSortData() {

        url = window.location.href;
        var category;
        if (url.includes('installations')) {
            category='installation';
        }else{
            if (url.includes('machine')){
                category='machine' 
            }else{
                category='arduino'
            }
        }

        const selectedValue = sortSelect.value;
        const data = {
            'type': 'sort',
            'main_category': category,
            'sort': selectedValue === 'none' ? null : selectedValue
        };

        socket.send(JSON.stringify(data));
    };

    // Écouteur d'événement pour détecter les changements
    sortSelect.addEventListener('change', function () {
        const sortData = collectSortData();
        // envoi de la requete par ws
    });
 document.getElementById("showBtn").addEventListener('click', function () {
        // Collecter les données des filtres et les envoyer au backend
        collectAndSendFilterData();
        });
});