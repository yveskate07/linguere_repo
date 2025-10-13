socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const type = data.type;

    if (type === "add_to_cart_result"){ // result after item added
            const count = document.getElementById('cart-count').getAttribute('data-count');
            document.getElementById('cart-count').setAttribute('data-count', parseInt(count, 10) + 1);

            document.getElementById('cart-count').innerHTML = `<i class="fas fa-shopping-cart"></i> 
                    <span class="d-none d-md-inline">
                            ${data.total_price} CFA
                    </span>`
        }else{
            if (type === "remove_item_result"){ // result after item removed

                    const cart_item = document.getElementById(data.html_id);
                    cart_item.remove();

                    document.getElementById('total-order-price').textContent = data.total_price
            }else{
                if (type==="quantity_changed"){ // result after item quantity changed
                    const idPrd = "quantity-value-"+ data.item_name
                    document.getElementById(idPrd).textContent = data.item_qtty;
                    document.getElementById("item-price-"+data.item_name).textContent = data.item_total;
                    document.getElementById('total-order-price').textContent = data.new_total
                }else{
                        if (type === "checkout_result"){
                            // Afficher le message de succès
                            showCheckoutSuccess(data);
                        }else{
                            if (type === "order_datas" || type === "order_created"){
                                // Mettre à jour le montant total dans le modal de paiement
                                //document.getElementById('total-amount').textContent = data.total_price;
                                /*document.getElementById('payment-modal').dataset.totalPrice = data.total_price.toLocaleString();
                                document.getElementById('payment-modal').dataset.refCommande = data.ref_commande;
                                document.getElementById('payment-modal').dataset.transactionId = data.transaction_id;
                                document.getElementById('payment-modal').dataset.clientName = data.client_name;

                                openPaymentModal();*/
                                // generer un lien whatsapp vers une discussion avec le numero +221773146662
                                const refOrder = data.ref_commande;
                                const phone = "221773146662";
                                const message = `Bonjour, je souhaite passer au paiement de la ${refOrder}`;
                                const whatsappUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
                                window.location.href = whatsappUrl;

                            }else{
                                if(type === "payment_confirmed" ){
                                    sweetMSG('Commande effectuée', 'Votre commande a été enregistrée avec succès.', 'success');
                                    emptyCartModal();
                                    emptyPaymentForm();
                                    closePaymentModal();
                                }else{
                                    if(type === "user_not_authenticated" ){
                                        window.location.href = "/login/";
                                    }else{
                                        if(type === "nothing" ){
                                            // ne rien faire
                                        }else{
                                            if(type === "process_payment" ){
                                                    const transactionId = document.getElementById('payment-modal').dataset.transactionId;
                                                    const amount = document.getElementById('payment-modal').dataset.totalPrice;
                                                    const refCommande = document.getElementById('payment-modal').dataset.refCommande;
                                                    const clientName = document.getElementById('payment-modal').dataset.clientName;
                                                    /*if(data.paymentMethod==='Orange Money'){
                                                        processPayment('ALL', transactionId, amount, refCommande, clientName);
                                                    }else{
                                                        processPayment('WAVE', transactionId, amount, refCommande, clientName);
                                                    }*/
                                                    socket.send(JSON.stringify({ 'type': 'payment_achieved', 
                                                        'datas':{'transactionId': transactionId},
                                                    }));
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }