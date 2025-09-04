// Fonction pour mettre à jour l'affichage du panier
function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCountElement = document.querySelector('.cart-count');
    const totalPriceElement = document.getElementById('total-price');

    // Calculer les réductions selon les nouvelles règles
    const { discount, subtotal, gift } = calculateDiscounts();

    // Vider le conteneur
    cartItemsContainer.innerHTML = '';

    // Ajouter chaque article
    cart.forEach((item, index) => {
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <div class="cart-item-image">
                <img src="${item.image}" alt="${item.name}" loading="lazy">
            </div>
            <div class="cart-item-info">
                <h5>${item.name}</h5>
                <p>${item.price.toLocaleString()} CFA</p>
                <small>${item.category}</small>
            </div>
            <div class="cart-item-quantity">
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(${index}, -1, ${item.id})">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(${index}, 1, ${item.id})">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <div class="cart-item-actions">
                <span class="cart-item-total">${(item.price * item.quantity).toLocaleString()} CFA</span>
                <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${index}, ${item.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        cartItemsContainer.appendChild(itemElement);
    });

    // Ajouter la section des réductions/cadeaux
    if (discount > 0 || gift) {
        const discountElement = document.createElement('div');
        discountElement.className = 'cart-discounts';

        let discountHTML = '';
        if (discount > 0) {
            discountHTML += `
                <div class="discount-item">
                    <span>Réduction (10% sur kits Arduino/Robotique)</span>
                    <span class="text-danger">-${discount.toLocaleString()} CFA</span>
                </div>
            `;
        }

        if (gift) {
            discountHTML += `
                <div class="gift-item">
                    <span><i class="fas fa-gift text-success"></i> ${gift}</span>
                </div>
            `;
        }

        discountElement.innerHTML = discountHTML;
        cartItemsContainer.appendChild(discountElement);
    }

    // Mettre à jour le total
    const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.setAttribute('data-count', itemCount);
    cartCountElement.innerHTML = `<i class="fas fa-shopping-cart"></i> <span class="d-none d-md-inline">${subtotal.toLocaleString()} CFA</span>`;

    totalPriceElement.textContent = `${subtotal.toLocaleString()} CFA`;
    document.getElementById('total-amount').textContent = subtotal.toLocaleString();
}

// Fonction simplifiée sans réductions ni cadeaux
function calculateDiscounts() {
    // Retourne simplement le total sans aucune réduction
    return {
        discount: 0,
        subtotal: total,
        gift: ''
    };
}

function collectFilterData(){
    const disponibChecks = document.querySelectorAll('.disponib_checks');

    const categoryChecks = document.querySelectorAll('.category_checks');

    minPrice = document.getElementById('minPrice').value.trim();
    maxPrice = document.getElementById('maxPrice').value.trim();

    // Vérifier si les valeurs sont valides
    if (minPrice === '') {
        minPrice = 0;
        }

    if (maxPrice === '') {
        maxPrice = 0
        }

    // conversion de minPrice et maxPrice en entier avec ParseInt
    minPrice = parseInt(minPrice,10);
    maxPrice = parseInt(maxPrice,10);
    // Vérification de la validité des prix
    if (isNaN(minPrice) || isNaN(maxPrice)) {
        alert("Veuillez entrer des valeurs numériques valides pour les prix.");
        return;
    }
    if (minPrice > maxPrice) {
        alert("Le prix minimum ne peut pas être supérieure au prix maximum.");
        return;
    }

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

    const filters = {
            'categories': [],
            'price_range': [minPrice, maxPrice],
            'disponibility': [],
            'main_category': category
        };

    // Récupérer les catégories sélectionnées
    categoryChecks.forEach(function (checkbox) {
        if (checkbox.checked) {
            filters.categories.push(checkbox.value);
        }
    });

    // Récupérer les états de disponibilité sélectionnés
    disponibChecks.forEach(function (checkbox) {
        if (checkbox.checked) {
            filters.disponibility.push(checkbox.value);
        }
    });

    return filters;
}

function getProductsPage(pageNumber) {


    const filters = collectFilterData();

    const pageRange = JSON.parse(document.getElementById('pagination-list').getAttribute('data-page-range'))

    document.getElementById('pagination-list').setAttribute('data-page-number',pageNumber);
    //document.getElementById('pagination-list').setAttribute('data-page-range',pageRange);

    const selectedValue = document.getElementById('sort-select').value;
    // Envoie une requête WebSocket pour obtenir les produits de la page demandée
    const data = {
        'type': 'product_page',
        'page_number': pageNumber,
        'list_page_range':pageRange,
        'filters': filters,
        'sort': selectedValue === 'none' ? null : selectedValue
    };

    socket.send(JSON.stringify(data));
}

function openPaymentModal() {
    if (cart.length === 0) { // utiliser sweet alert
        alert('Votre panier est vide. Ajoutez des produits avant de passer commande.');
        return;
    }

    // Mettre à jour le montant total dans le modal
    document.getElementById('total-amount').textContent = total.toLocaleString();

    // Réinitialiser le formulaire
    document.getElementById('payment-form').reset();

    // Afficher le modal
    document.getElementById('payment-modal').style.display = 'block';
    document.getElementById('cart-modal').style.display = 'none';
}

function closePaymentModal() {
    document.getElementById('payment-modal').style.display = 'none';
}

// Fonction pour simuler le processus de paiement
function processPayment(paymentMethod, transactionId, amount, refCommande, clientName) {
    /*const { discount, subtotal, gift } = calculateDiscounts();
    const phoneNumber = document.getElementById('mobile-number').value;
    const paymentCode = document.getElementById('payment-code').value;

    // Message de confirmation
    let confirmationMessage = `Paiement ${selectedPaymentMethod === 'orange' ? 'Orange Money' : 'Wave'} de ${subtotal.toLocaleString()} CFA effectué avec succès!`;

    // Informations client
    const customerName = `${document.getElementById('first-name').value} ${document.getElementById('last-name').value}`;
    confirmationMessage += `\n\nMerci ${customerName} pour votre commande !`;*/

    /*var axios = require('axios');

    var data = JSON.stringify({
      "apikey": "YOUR_APIKEY",
      "site_id": "YOUR_SITEID",
      "transaction_id":  transactionId, 
      "amount": conversionMultCinq(amount),
      "currency": "XOF",
      "description": " TEST INTEGRATION ",
      "notify_url": "{% url 'notify' %}",
      "return_url": "{% url 'arduino' 1 %}",
      "channels": 'ALL',
      "metadata": refCommande,
      "lang": "FR",
      "invoice_data": {
        "Nom Client": clientName,
        "Moyen de paiement": 'CINETPAY',
        "Montant payé": amount.toLocaleString() + " CFA",
      }
    });

    var config = {
      method: 'post',
      url: 'https://api-checkout.cinetpay.com/v2/payment',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    };

    axios(config)
    .then(function (response) {
      // traitement au cas où le paiement est un succès. 
      // afficher un sweet alert de succès
      console.log(JSON.stringify(response.data));
      socket.send(JSON.stringify({'response': response.data, 'type': 'payment_response', 'transaction_id': transactionId}));
    })
    .catch(function (error) {
      // traitement au cas où le paiement est un echec.
      console.log(error);
    });*/

    fetch("/create-payment/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // si CSRF activé
        },
        body: JSON.stringify({
            transaction_id: transactionId,
            amount: amount,
            metadata: refCommande,
            channels: paymentMethod, // MOBILE_MONEY, ALL
            notify_url: "{% url 'notify' %}",
            return_url: "{% url 'arduino' 1 %}",
            invoice_data: {
                "Nom Client": clientName,
                "Moyen de paiement": 'CINETPAY',
                "Montant payé": amount.toLocaleString() + " CFA"}
        }),
        })
        .then(response => response.json())
        .then(data => {
        if (data.code === "201") {
            const paymentUrl = data.data.payment_url;
            window.location.href = paymentUrl; // Redirige l’utilisateur vers CinetPay
        }else {
            sweetMSG('Erreur','Erreur lors de la création du paiement. Veuillez réessayer.', 'error');
            return
        }
        })
        .catch(console.error);

    // Réinitialiser le panier
    cart = [];
    total = 0;
    updateCartDisplay();

    // Fermer le modal
    closePaymentModal();

    // Réinitialiser les formulaires
    document.getElementById('customer-info-form').reset();
    document.getElementById('payment-form').reset();
}