socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const type = data.type;

    if (type === "display_products") { // filter products 
        
        const pagination = data.pagination; // pour la pagination
        const productGrid = document.querySelector('.product-grid');
        const products = data.products; // car le backend envoie directement un tableau
        productGrid.innerHTML = ""; // on vide le contenu actuel

                if (data.length === 0) {
                    productGrid.innerHTML = "<h2>Rien à afficher ici</h2>";
                    return;
                }

                products.forEach(product => {
                    const productCard = document.createElement('div');
                    productCard.className = 'product-card';
                    productCard.setAttribute('data-aos', 'fade-up');
                    productCard.setAttribute('data-category', product.category);

                    let badgeHTML = '';
                    if (product.badge === "Nouveau") {
                        badgeHTML = `<span class="product-badge">Nouveau</span>`;
                    } else if (product.badge === "Promo") {
                        badgeHTML = `<span class="product-badge" style="background: #27ae60;">Promo</span>`;
                    } else if (product.badge === "Top ventes") {
                        badgeHTML = `<span class="product-badge" style="background: #9b59b6;">Top vente</span>`;
                    }

                    const imageName = product.image.url;
                    const description = product.description || "Pas de description.";
                    let stockText;
                    if (product.disponibility === 'En stock'){
                        stockText = `<p class="product-stock in-stock"><i class="fas fa-check-circle me-1"></i> En stock: (${product.stock})</p>`;
                    }else{
                        if (product.disponibility === 'Rupture de stock'){
                            stockText = `<p class="product-stock out-of-stock"><i class="fas fa-times-circle me-1"></i> Rupture de stock</p>`;
                    }else{
                        stockText = `<p class="product-stock low-stock"><i class="fas fa-exclamation-circle me-1"></i> Stock limité: (${product.stock})</p>`;
                    }
                }
                    productCard.innerHTML = `
                    ${badgeHTML}
                    <img src='${imageName}' alt="${product.name}">
                    <div class="quick-view">
                        <button class="quick-view-btn" onclick="showQuickView('${product.name}', '${imageName}', '${description.replace(/'/g, "\\'")}', ${product.price}, ${product.stock}, '${product.category}')">
                            <i class="fas fa-eye me-1"></i> Aperçu rapide
                        </button>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">${product.name}</h3>
                        <p class="product-description">${description}.</p>
                        <p class="product-price">${product.price} FCFA</p>
                        ${stockText}
                        <button class="add-to-cart-button" onclick="addToCart('${product.name}', ${product.price}, '${product.category}', '${imageName}',1, ${product.id})">
                            <i class="fas fa-cart-plus"></i> Ajouter au panier
                        </button>
                        <div class="product-meta">
                            <span class="product-rating">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star-half-alt"></i>
                            </span>
                            <span class="product-sku">REF: ${product.id}</span>
                        </div>
                    </div>`;

                    productGrid.appendChild(productCard);
                });

                //console.log("Pagination data:", pagination);

                let pag_link = document.getElementById('pagination-list');
                let html1, html2, html3;

                page_range = document.getElementById('pagination-list').getAttribute('data-page-range');

                if (pagination.has_previous) {
                    html1 = `<li class="page-item">
                                <button class="page-link" onclick="getProductsPage(${pagination.number-1}, ${page_range})">&laquo;</button>
                            </li>`;
                }else{
                    html1 = `<li class="page-item disabled">
                                <span class="page-link">&laquo;</span>
                            </li>`;
                }
                html2 = "";
                pagination.page_range.forEach(i => {
                    const classes = (i === pagination.number) ? 'page-item active' : 'page-item';
                    html2 += `<li class="${classes}">
                                <button class="page-link" onclick="getProductsPage(${i}, ${page_range})">${i}</button>
                            </li>`;
                });
                if (pagination.has_next) {
                    html3 = `<li class="page-item">
                                <button class="page-link" onclick="getProductsPage(${pagination.number+1}, ${page_range})">&raquo;</button>
                            </li>`;
                } else {
                    html3 = `<li class="page-item disabled"><span class="page-link">&raquo;</span></li>`;
                }

                pag_link.innerHTML = html1 + html2 + html3;

    } else {
        if (type === "add_to_cart_result"){ // result after item added
            const count = document.getElementById('cart-count').getAttribute('data-count');
            document.getElementById('cart-count').setAttribute('data-count', parseInt(count, 10) + 1);

            document.getElementById('cart-count').innerHTML = `<i class="fas fa-shopping-cart"></i> 
                    <span class="d-none d-md-inline">
                            ${data.total_price} CFA
                    </span>`
        }else{
            if (type === "remove_item_result"){ // result after item removed
                document.getElementById('cart-count').setAttribute('data-count', data.new_qtty);

                document.getElementById('cart-count').innerHTML = `<i class="fas fa-shopping-cart"></i> 
                        <span class="d-none d-md-inline">
                                ${data.new_total} CFA
                        </span>`
            }else{
                if (type==="quantity_changed"){ // result after item quantity changed
                    document.getElementById('cart-count').setAttribute('data-count', data.new_qtty);

                    document.getElementById('cart-count').innerHTML = `<i class="fas fa-shopping-cart"></i> 
                            <span class="d-none d-md-inline">
                                    ${data.new_total} CFA
                            </span>`;

                    document.getElementById('quantity-value').textContent = data.item_qtty;
                }else{
                        if (type === "checkout_result"){
                            // Afficher le message de succès
                            showCheckoutSuccess(data);
                        }else{
                            if (type === "order_datas" || type === "order_created"){
                                // Mettre à jour le montant total dans le modal de paiement
                                //document.getElementById('total-amount').textContent = data.total_price;
                                document.getElementById('payment-modal').dataset.totalPrice = data.total_price.toLocaleString();
                                document.getElementById('payment-modal').dataset.refCommande = data.ref_commande;
                                document.getElementById('payment-modal').dataset.transactionId = data.transaction_id;
                                document.getElementById('payment-modal').dataset.clientName = data.client_name;

                                openPaymentModal();
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
        /*let toastEl = document.getElementById("success-toast");
        let toast = new bootstrap.Toast(toastEl);
        document.getElementById("toast-msg").textContent = data.message; 
        toast.show();*/
        }

