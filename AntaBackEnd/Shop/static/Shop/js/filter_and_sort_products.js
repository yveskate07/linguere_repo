document.addEventListener('DOMContentLoaded', function () {
    
    // Sélectionner tous les éléments à surveiller
    const categoryChecks = document.querySelectorAll('.category_checks');
    const priceRange = document.querySelector('.price-range');
    const disponibChecks = document.querySelectorAll('.disponib_checks');
    const filterSection = document.querySelector('.filter-section');
    var sortSelect = document.getElementById('sort-select');

    sortSelect.addEventListener('change', function(){
        
        let pageN = document.body.dataset.pageNumber;
        let pageLabel = document.body.dataset.pageLabel;

        let form = document.createElement("form");
        form.method = "POST";
        form.action = document.body.dataset.url;

        // page
        let page = document.createElement('input');
        page.name = 'page';
        page.value = pageN;

        // tri croissant/decroissant
        let sort_choice = document.createElement('input');
        sort_choice.name = 'sort-choice';
        sort_choice.value = document.getElementById('sort-select').value;

        // filtres
        let minPrice_ = document.getElementById('minPrice').value.trim();
        let maxPrice_ = document.getElementById('maxPrice').value.trim();

        // Vérifier si les valeurs sont valides
        if (minPrice_ === '') {
            document.getElementById('minPrice').value = 0;
            }

        if (maxPrice_ === '') {
            document.getElementById('maxPrice').value = 0
            }

        // conversion de minPrice et maxPrice en entier avec ParseInt
        minPrice_ = parseInt(minPrice_,10);
        maxPrice_ = parseInt(maxPrice_,10);
        // Vérification de la validité des prix
        if (isNaN(minPrice_) || isNaN(maxPrice_)) {
            alert("Veuillez entrer des valeurs numériques valides pour les prix.");
            return;
        }
        if (minPrice_ > maxPrice_) {
            alert("Le prix minimum ne peut pas être supérieure au prix maximum.");
            return;
        }

        // filtre prix min-max
        let minPrice = document.createElement('input');
        minPrice.name = 'min-price';
        minPrice.value = document.getElementById('minPrice').value
        let maxPrice = document.createElement('input');
        maxPrice.name = 'max-price';
        maxPrice.value = document.getElementById('maxPrice').value
        
        const category_checks = document.querySelectorAll('.category_checks');
        const disponib_checks = document.querySelectorAll('.disponib_checks');

        let categoryChecks_list_selected = [];
        console.log('category_checks is ', category_checks)
        category_checks.forEach(function (checkbox) {
            if (checkbox.checked) {
                // joindres toutes les valeurs en les separant par ', '
                categoryChecks_list_selected.push(checkbox.value);
            }
        });

        let disponibChecks_list_selected = [];
        // Récupérer les états de disponibilité sélectionnés
        disponib_checks.forEach(function (checkbox) {
            if (checkbox.checked) {
                disponibChecks_list_selected.push(checkbox.value);
            }
        });

        // filtres stock
        let disponibChecks = document.createElement('select');
        disponibChecks.name = 'disponib-checks';
        disponibChecks.multiple = true;
        const stocks = ['En stock','Stock limité','Rupture de stock']
        stocks.forEach(stock => {
            let option = document.createElement('option');
            if(disponibChecks_list_selected.includes(stock)){
                option.selected = true;
            }
            option.value = stock;
            option.textContent = stock
            disponibChecks.appendChild(option);
        })

        // filtres categorie
        let categoryChecks = document.createElement('select');
        categoryChecks.name = 'category-checks';
        categoryChecks.multiple = true;
        const categories = ['Kits Arduino','Composants IoT','Robotique','Capteurs']
        categories.forEach(cat => {
            let option = document.createElement('option');
            if(categoryChecks_list_selected.includes(cat)){
                option.selected = true;
            }
            option.value = cat;
            option.textContent = cat
            categoryChecks.appendChild(option);
        })

        let page_label = document.createElement('input');
        page_label.name = 'page-label';
        page_label.value = pageLabel;

        const csrftoken = getCookie('csrftoken');

        // Créer le champ hidden pour le CSRF
        let csrfInput = document.createElement('input');
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";  // Django exige ce nom exact
        csrfInput.value = csrftoken;

        // Ajouter les champs au formulaire
        form.appendChild(page);
        form.appendChild(sort_choice);
        form.appendChild(minPrice);
        form.appendChild(maxPrice);
        form.appendChild(categoryChecks);
        form.appendChild(disponibChecks);
        form.appendChild(page_label);
        form.appendChild(csrfInput);

        document.body.appendChild(form);
        form.submit();
    });

    // Fonction pour insérer ou mettre à jour le bouton de filtres
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

});

function filter_sort_form_datas(pageN, pageLabel) {
        let form = document.createElement("form");
        form.method = "POST";
        form.action = document.body.dataset.url;

        // page
        let page = document.createElement('input');
        page.name = 'page';
        page.value = pageN;

        // tri croissant/decroissant
        let sort_choice = document.createElement('input');
        sort_choice.name = 'sort-choice';
        sort_choice.value = document.getElementById('sort-select').value;

        // filtres
        let minPrice_ = document.getElementById('minPrice').value.trim();
        let maxPrice_ = document.getElementById('maxPrice').value.trim();

        // Vérifier si les valeurs sont valides
        if (minPrice_ === '') {
            document.getElementById('minPrice').value = 0;
            }

        if (maxPrice_ === '') {
            document.getElementById('maxPrice').value = 0
            }

        // conversion de minPrice et maxPrice en entier avec ParseInt
        minPrice_ = parseInt(minPrice_,10);
        maxPrice_ = parseInt(maxPrice_,10);
        // Vérification de la validité des prix
        if (isNaN(minPrice_) || isNaN(maxPrice_)) {
            alert("Veuillez entrer des valeurs numériques valides pour les prix.");
            return;
        }
        if (minPrice_ > maxPrice_) {
            alert("Le prix minimum ne peut pas être supérieure au prix maximum.");
            return;
        }

        // filtre prix min-max
        let minPrice = document.createElement('input');
        minPrice.name = 'min-price';
        minPrice.value = document.getElementById('minPrice').value
        let maxPrice = document.createElement('input');
        maxPrice.name = 'max-price';
        maxPrice.value = document.getElementById('maxPrice').value
        
        const category_checks = document.querySelectorAll('.category_checks');
        const disponib_checks = document.querySelectorAll('.disponib_checks');

        let categoryChecks_list_selected = [];
        console.log('category_checks is ', category_checks)
        category_checks.forEach(function (checkbox) {
            if (checkbox.checked) {
                // joindres toutes les valeurs en les separant par ', '
                categoryChecks_list_selected.push(checkbox.value);
            }
        });

        let disponibChecks_list_selected = [];
        // Récupérer les états de disponibilité sélectionnés
        disponib_checks.forEach(function (checkbox) {
            if (checkbox.checked) {
                disponibChecks_list_selected.push(checkbox.value);
            }
        });

        // filtres stock
        let disponibChecks = document.createElement('select');
        disponibChecks.name = 'disponib-checks';
        disponibChecks.multiple = true;
        const stocks = ['En stock','Stock limité','Rupture de stock']
        stocks.forEach(stock => {
            let option = document.createElement('option');
            if(disponibChecks_list_selected.includes(stock)){
                option.selected = true;
            }
            option.value = stock;
            option.textContent = stock
            disponibChecks.appendChild(option);
        })

        // filtres categorie
        let categoryChecks = document.createElement('select');
        categoryChecks.name = 'category-checks';
        categoryChecks.multiple = true;
        const categories = ['Kits Arduino','Composants IoT','Robotique','Capteurs']
        categories.forEach(cat => {
            let option = document.createElement('option');
            if(categoryChecks_list_selected.includes(cat)){
                option.selected = true;
            }
            option.value = cat;
            option.textContent = cat
            categoryChecks.appendChild(option);
        })

        let page_label = document.createElement('input');
        page_label.name = 'page-label';
        page_label.value = pageLabel;

        const csrftoken = getCookie('csrftoken');

        // Créer le champ hidden pour le CSRF
        let csrfInput = document.createElement('input');
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";  // Django exige ce nom exact
        csrfInput.value = csrftoken;

        // Ajouter les champs au formulaire
        form.appendChild(page);
        form.appendChild(sort_choice);
        form.appendChild(minPrice);
        form.appendChild(maxPrice);
        form.appendChild(categoryChecks);
        form.appendChild(disponibChecks);
        form.appendChild(page_label);
        form.appendChild(csrfInput);

        document.body.appendChild(form);
        form.submit();
    }