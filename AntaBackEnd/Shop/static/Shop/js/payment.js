// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner Orange Money par défaut
    //selectPayment('orange');

    // Événement pour le bouton de commande
    document.getElementById('checkout-button').addEventListener('click', getTotalPriceAndDisplayPaymentModal);
    //document.querySelector('.cart-count').addEventListener('click', toggleCartModal);
    //document.getElementById('close-cart').addEventListener('click', toggleCartModal);

    // Fermer le modal en cliquant à l'extérieur
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('payment-modal')) {
            closePaymentModal();
        }
    });
});


function getTotalPriceAndDisplayPaymentModal() {
    tr_Id = document.getElementById('payment-modal').getAttribute('data-transactionId');
    if (tr_Id) {
        socket.send(JSON.stringify({'type': 'get_order_datas', 'transaction_id': tr_Id}));
    }else{
        socket.send(JSON.stringify({'type': 'create_new_order'}));
    }
}

// Variables pour le paiement
let selectedPaymentMethod = 'orange'; // Par défaut Orange Money


// Fonction pour sélectionner le mode de paiement
/*function selectPayment(method) {
    selectedPaymentMethod = method;

    // Retirer la classe active de toutes les options
    document.querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('active');
    });

    // Ajouter la classe active à l'option sélectionnée
    const options = document.querySelectorAll('.payment-option');
    if (method === 'orange') {
        options[0].classList.add('active');
    } else if (method === 'wave') {
        options[1].classList.add('active');
    }
}*/

// Gestion de la soumission du formulaire de paiement
document.getElementById('payment-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Définition des champs obligatoires
    const requiredFields = ['first-name', 'last-name', 'email', 'address', 'city', 'payment-phone'];
    let isValid = true;
    let userData = {};

    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const value = field.value.trim();

        if (!value) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
            userData[fieldId] = value; // Ajout au dictionnaire JS
        }
    });

    // Champs optionnels
    const optionalFields = ['payment-code'];
    optionalFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            const value = field.value.trim();
            if (value) {
                userData[fieldId] = value;
            }
        }
    });

    if (!isValid) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return;
    }

    // Ajout des infos liées à la commande (depuis dataset)
    userData.transactionId = document.getElementById('payment-modal').dataset.transactionId;
    userData.amount = document.getElementById('payment-modal').dataset.totalPrice;
    userData.refCommande = document.getElementById('payment-modal').dataset.refCommande;

    
    // Envoi d'une requete ws au consumer avec type=payment_response
    socket.send(JSON.stringify({ 'type': 'prepayment_datas',
        'datas':userData
    }));

});

function gettingPaymentMethode(){
    // sending either Orange Money or Wave to the consumer with type=prepayment_datas, the key is paymentMethod
}

function emptyPaymentForm() {
    document.getElementById('payment-form').reset();
}

function conversionMultCinq(num) {
    if (num % 5 === 0) {
        return num; // C'est déjà un multiple de 5
    } else {
        return Math.ceil(num / 5) * 5; // Arrondi au multiple de 5 supérieur
    }
}