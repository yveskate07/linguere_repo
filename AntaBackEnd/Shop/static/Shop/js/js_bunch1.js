function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Est-ce que ce cookie commence par le nom qu'on cherche ?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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
function processPayment() {
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

    console.log('---processPayment called---')

    const paymentMethod1 = document.getElementById('selected-payment').value;
    let paymentMethod2;
    
    if(paymentMethod1==='wave'){
        paymentMethod2 = 'WALLET';
    }else{
        paymentMethod2 = 'MOBILE_MONEY';
    }

    fetch("/shop/create-payment/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // si CSRF activé
        },
        body: JSON.stringify({
            metadata: paymentMethod1,
            channels: paymentMethod2, // MOBILE_MONEY, WALLET
            notify_url: document.body.getAttribute('data-notify-url'),
            return_url: document.body.getAttribute('data-return-url')
        }),
        })
        .then(response => response.json())
        .then(data => {
        if (data.code === "201") {
            const paymentUrl = data.data.payment_url;
            window.location.href = paymentUrl; // Redirige l’utilisateur vers CinetPay
        }else {
            sweetMSG('Erreur','Erreur lors du paiement. Veuillez réessayer.', 'error');
            return
        }
        })
        .catch(console.error);

}