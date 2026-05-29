// ============================================================================
// VALIDATION FORMULAIRE DE COMMANDE — Générique pour tous les services
// Utilise input_ids_json pour détecter les champs dynamiquement
// ============================================================================

(function () {
    'use strict';

    // -------------------------------------------------------------------------
    // UTILITAIRES UI
    // -------------------------------------------------------------------------

    const ERROR_CLASS = 'vf-error';
    const ERROR_MSG_CLASS = 'vf-error-msg';

    /**
     * Injecte le CSS de validation une seule fois dans le <head>.
     */
    function injectStyles() {
        if (document.getElementById('vf-styles')) return;
        const style = document.createElement('style');
        style.id = 'vf-styles';
        style.textContent = `
            .${ERROR_CLASS} {
                border: 2px solid #e74c3c !important;
                border-radius: 4px;
                background-color: #fff8f8 !important;
                animation: vf-shake 0.3s ease;
            }
            .${ERROR_MSG_CLASS} {
                color: #e74c3c;
                font-size: 12px;
                margin-top: 4px;
                display: flex;
                align-items: center;
                gap: 4px;
                animation: vf-fadein 0.2s ease;
            }
            .${ERROR_MSG_CLASS}::before {
                content: '⚠';
            }
            /* Pour les color-options et les option-group */
            .option-group.${ERROR_CLASS} {
                border: 2px solid #e74c3c !important;
                border-radius: 8px;
                padding: 8px;
                background-color: #fff8f8 !important;
            }
            /* Bandeau récapitulatif */
            #vf-summary-banner {
                position: fixed;
                top: 0; left: 0; right: 0;
                background: #e74c3c;
                color: white;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                box-shadow: 0 4px 12px rgba(231,76,60,0.4);
                animation: vf-slidein 0.3s ease;
            }
            #vf-summary-banner ul {
                margin: 4px 0 0 0;
                padding-left: 18px;
                font-weight: 400;
                font-size: 13px;
            }
            #vf-summary-banner .vf-close-banner {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                flex-shrink: 0;
                line-height: 1;
            }
            @keyframes vf-shake {
                0%, 100% { transform: translateX(0); }
                25%       { transform: translateX(-6px); }
                75%       { transform: translateX(6px); }
            }
            @keyframes vf-fadein {
                from { opacity: 0; transform: translateY(-4px); }
                to   { opacity: 1; transform: translateY(0); }
            }
            @keyframes vf-slidein {
                from { transform: translateY(-100%); }
                to   { transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Marque un élément comme invalide et affiche un message d'erreur en dessous.
     * @param {Element} el       — l'input/select/div à marquer
     * @param {string}  message  — le message d'erreur
     */
    function markError(el, message) {
        clearError(el);
        el.classList.add(ERROR_CLASS);

        const msg = document.createElement('div');
        msg.className = ERROR_MSG_CLASS;
        msg.dataset.vfFor = el.id || el.className;
        msg.textContent = message;

        // Insérer après l'élément ou après son parent .option-group
        const parent = el.closest('.option-group') || el.parentNode;
        parent.appendChild(msg);

        // Auto-nettoyage sur interaction
        const evts = el.tagName === 'SELECT' ? ['change'] : ['input', 'change'];
        evts.forEach(evt => {
            el.addEventListener(evt, () => clearError(el), { once: true });
        });
    }

    /**
     * Nettoie l'état d'erreur d'un élément.
     */
    function clearError(el) {
        el.classList.remove(ERROR_CLASS);
        const parent = el.closest('.option-group') || el.parentNode;
        parent.querySelectorAll('.' + ERROR_MSG_CLASS).forEach(m => m.remove());
    }

    /**
     * Affiche le bandeau d'erreurs récapitulatif en haut de page.
     */
    function showBanner(errors) {
        removeBanner();
        const banner = document.createElement('div');
        banner.id = 'vf-summary-banner';

        const left = document.createElement('div');
        left.innerHTML = `<strong>Formulaire incomplet (${errors.length} erreur${errors.length > 1 ? 's' : ''})</strong>
            <ul>${errors.map(e => `<li>${e}</li>`).join('')}</ul>`;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'vf-close-banner';
        closeBtn.textContent = '✕';
        closeBtn.type = 'button';
        closeBtn.addEventListener('click', removeBanner);

        banner.appendChild(left);
        banner.appendChild(closeBtn);
        document.body.prepend(banner);

        // Auto-disparition après 8 secondes
        setTimeout(removeBanner, 8000);
    }

    function removeBanner() {
        const b = document.getElementById('vf-summary-banner');
        if (b) b.remove();
    }

    /**
     * Scroll vers le premier élément en erreur.
     */
    function scrollToFirstError() {
        const first = document.querySelector('.' + ERROR_CLASS);
        if (first) {
            first.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }


    // -------------------------------------------------------------------------
    // VALIDATION — Section Image
    // -------------------------------------------------------------------------

    /**
     * Vérifie qu'une image a été sélectionnée (galerie ou upload).
     * L'upload a la priorité : si un fichier est uploadé, on ne bloque pas
     * même si img_path est vide.
     * Retourne un message d'erreur ou null.
     */
    function validateImage() {
        const imgPath  = document.getElementById('id_img_path');
        const fileInput = document.getElementById('id_img');

        const hasUpload  = fileInput && fileInput.files && fileInput.files.length > 0;
        const hasGallery = imgPath && imgPath.value.trim() !== '';

        if (!hasUpload && !hasGallery) {
            // Marquer visuellement la zone d'upload
            const dropArea = document.getElementById('drop-area');
            if (dropArea) markError(dropArea, 'Veuillez sélectionner ou importer une image.');
            return 'Image manquante : sélectionnez un motif dans la galerie ou importez votre design.';
        }
        return null;
    }


    // -------------------------------------------------------------------------
    // VALIDATION — Champs de personnalisation dynamiques
    // Utilise input_ids_json pour être générique (tous services confondus)
    // -------------------------------------------------------------------------

    function validatePersonnalisation() {
        const errors = [];
        const inputIdsEl = document.getElementById('input_ids');
        if (!inputIdsEl) return errors;

        let items;
        try { items = JSON.parse(inputIdsEl.value); }
        catch { return errors; }

        // Champs fixes toujours présents
        const SKIP = ['id_img_path', 'id_comment']; // comment = optionnel

        items.forEach(item => {
            const mainId = item.input_ids[0];
            if (SKIP.includes(mainId)) return;

            const el = document.getElementById(mainId);
            if (!el) return;

            // --- Champ MULTICOLOR ---
            if (item.type === 'multicolor' || el.dataset.type === 'multicolor') {
                const val = el.value.trim();
                let isEmpty = !val || val === '' || val === '[]' || val === 'null';
                if (!isEmpty) {
                    try { isEmpty = JSON.parse(val).length === 0; }
                    catch { isEmpty = true; }
                }
                if (isEmpty) {
                    // Marquer le conteneur de pastilles
                    const pickerContainer = document.querySelector(
                        `.color-options[id^="color-picker-"]`
                    );
                    const target = pickerContainer
                        ? pickerContainer.closest('.option-group') || pickerContainer
                        : el;
                    markError(target, `Veuillez sélectionner au moins une couleur pour "${item.sum_tit_cls}".`);
                    errors.push(`Couleurs manquantes : "${item.sum_tit_cls}"`);
                }
                return;
            }

            // --- Champ WIDTH/HEIGHT (dimensions) ---
            if (mainId === 'id_width') {
                const wEl = el;
                const hEl = item.input_ids[1] ? document.getElementById(item.input_ids[1]) : null;
                if (!wEl.value || parseInt(wEl.value) <= 0) {
                    markError(wEl, 'La largeur doit être supérieure à 0.');
                    errors.push('Largeur invalide.');
                }
                if (hEl && (!hEl.value || parseInt(hEl.value) <= 0)) {
                    markError(hEl, 'La hauteur doit être supérieure à 0.');
                    errors.push('Hauteur invalide.');
                }
                return;
            }

            // --- Champ QUANTITY ---
            if (mainId === 'id_quantity') {
                if (!el.value || parseInt(el.value) < 1) {
                    markError(el, 'La quantité doit être au moins 1.');
                    errors.push('Quantité invalide.');
                }
                return;
            }

            // --- Champ SELECT ---
            if (el.tagName === 'SELECT') {
                if (!el.value || el.value.trim() === '') {
                    markError(el, `Veuillez choisir une option pour "${item.sum_tit_cls}".`);
                    errors.push(`Champ non rempli : "${item.sum_tit_cls}"`);
                    return;
                }
                // Cas "Autre (Préciser)" : vérifier le champ _other
                if (el.value === 'Autre (Préciser)') {
                    const otherId = item.input_ids[1] || (mainId + '_other');
                    const otherEl = document.getElementById(otherId);
                    if (otherEl && otherEl.value.trim() === '') {
                        markError(otherEl, `Veuillez préciser votre choix pour "${item.sum_tit_cls}".`);
                        errors.push(`Précision manquante : "${item.sum_tit_cls}"`);
                    }
                }
                return;
            }

            // --- Champ TEXT / NUMBER générique ---
            if (el.type === 'text' || el.type === 'number' || el.tagName === 'TEXTAREA') {
                // On ne valide que si le champ est marqué required
                if (el.required && el.value.trim() === '') {
                    markError(el, `Veuillez renseigner "${item.sum_tit_cls}".`);
                    errors.push(`Champ non rempli : "${item.sum_tit_cls}"`);
                }
                return;
            }

            // --- Champ CHECKBOX (boolean) ---
            if (el.type === 'checkbox' && el.required && !el.checked) {
                markError(el, `Veuillez cocher "${item.sum_tit_cls}".`);
                errors.push(`Case à cocher manquante : "${item.sum_tit_cls}"`);
            }
        });

        return errors;
    }


    // -------------------------------------------------------------------------
    // VALIDATION — Champs de livraison
    // -------------------------------------------------------------------------

    function validateLivraison() {
        const errors = [];
        const isAuth = document.body.dataset.userId && document.body.dataset.userId !== '0';

        // Champs requis pour utilisateur non authentifié
        if (!isAuth) {
            [
                { id: 'id_client_name',    label: 'Nom complet' },
                { id: 'id_client_email',   label: 'Email' },
                { id: 'id_client_phone',   label: 'Téléphone' },
            ].forEach(({ id, label }) => {
                const el = document.getElementById(id);
                if (el && el.value.trim() === '') {
                    markError(el, `Veuillez renseigner votre ${label.toLowerCase()}.`);
                    errors.push(`${label} manquant(e).`);
                }
            });
        }

        // Adresse — requise pour tous
        const addrEl = document.getElementById('id_client_address');
        if (addrEl && addrEl.value.trim() === '') {
            markError(addrEl, 'Veuillez renseigner votre adresse.');
            errors.push('Adresse manquante.');
        }

        // Mode de livraison
        const deliveryEl = document.getElementById('id_delivery_mode');
        if (deliveryEl && deliveryEl.value.trim() === '') {
            markError(deliveryEl, 'Veuillez choisir un mode de livraison.');
            errors.push('Mode de livraison non choisi.');
        }

        // CGU
        const cguEl = document.getElementById('cgu_accept');
        if (cguEl && !cguEl.checked) {
            markError(cguEl, 'Veuillez accepter les conditions générales.');
            errors.push('Conditions générales non acceptées.');
        }

        return errors;
    }


    // -------------------------------------------------------------------------
    // ORCHESTRATION — Branchement sur le submit
    // -------------------------------------------------------------------------

    document.addEventListener('DOMContentLoaded', function () {
        injectStyles();

        const form = document.getElementById('form_customisation');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            // Nettoyer les anciennes erreurs
            form.querySelectorAll('.' + ERROR_CLASS).forEach(el => el.classList.remove(ERROR_CLASS));
            form.querySelectorAll('.' + ERROR_MSG_CLASS).forEach(el => el.remove());
            removeBanner();

            const allErrors = [];

            // 1. Image
            const imgError = validateImage();
            if (imgError) allErrors.push(imgError);

            // 2. Personnalisation
            const persoErrors = validatePersonnalisation();
            allErrors.push(...persoErrors);

            // 3. Livraison
            const livraisonErrors = validateLivraison();
            allErrors.push(...livraisonErrors);

            if (allErrors.length > 0) {
                e.preventDefault();
                showBanner(allErrors);
                scrollToFirstError();
            }
        });

        // Nettoyage du bandeau dès qu'un champ est modifié
        form.addEventListener('input', removeBanner);
        form.addEventListener('change', removeBanner);
    });

})();