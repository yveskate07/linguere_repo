document.addEventListener("DOMContentLoaded", function () {

    // =========================================================================
    // UTILITAIRES
    // =========================================================================

    /**
     * Lit le JSONField (textarea caché) et retourne un tableau.
     * Si le contenu est invalide ou vide, retourne [].
     */
    function readJSON(textarea) {
        try {
            const parsed = JSON.parse(textarea.value);
            return Array.isArray(parsed) ? parsed : [];
        } catch {
            return [];
        }
    }

    /**
     * Sérialise un tableau en JSON et l'écrit dans le textarea caché.
     */
    function writeJSON(textarea, arr) {
        textarea.value = JSON.stringify(arr);
    }


    // =========================================================================
    // SYSTÈME DE TAGS — pour les champs de type "select"
    // =========================================================================

    function buildTagSystem(textarea) {

        let items = readJSON(textarea);

        const wrapper = document.createElement('div');
        wrapper.className = 'tag-system-wrapper';
        wrapper.style.cssText = `
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px;
            background: #fff;
            margin-top: 4px;
        `;

        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'tags-container';
        tagsContainer.style.cssText = `
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 8px;
            min-height: 32px;
        `;

        const inputRow = document.createElement('div');
        inputRow.style.cssText = 'display: flex; gap: 6px; align-items: center;';

        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Tapez une option et appuyez sur Entrée…';
        input.style.cssText = `
            flex: 1;
            padding: 6px 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 13px;
        `;

        const addBtn = document.createElement('button');
        addBtn.type = 'button';
        addBtn.textContent = '+ Ajouter';
        addBtn.style.cssText = `
            padding: 6px 12px;
            background: #417690;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            white-space: nowrap;
        `;

        inputRow.appendChild(input);
        inputRow.appendChild(addBtn);
        wrapper.appendChild(tagsContainer);
        wrapper.appendChild(inputRow);

        textarea.parentNode.insertBefore(wrapper, textarea);
        textarea.style.display = 'none';

        function renderTag(value) {
            const tag = document.createElement('span');
            tag.style.cssText = `
                display: inline-flex;
                align-items: center;
                gap: 4px;
                background: #e8f0fe;
                border: 1px solid #4a90d9;
                color: #1a3a5c;
                padding: 3px 8px;
                border-radius: 20px;
                font-size: 13px;
            `;
            tag.textContent = value;

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.textContent = '✕';
            removeBtn.title = 'Supprimer cette option';
            removeBtn.style.cssText = `
                background: none;
                border: none;
                color: #c0392b;
                cursor: pointer;
                font-size: 12px;
                padding: 0;
                line-height: 1;
            `;
            removeBtn.addEventListener('click', function () {
                items = items.filter(i => i !== value);
                writeJSON(textarea, items);
                tag.remove();
            });

            tag.appendChild(removeBtn);
            tagsContainer.appendChild(tag);
        }

        items.forEach(renderTag);

        function addItem() {
            const value = input.value.trim();
            if (!value) return;
            if (items.includes(value)) {
                input.style.borderColor = '#e74c3c';
                input.title = 'Cette option existe déjà';
                setTimeout(() => {
                    input.style.borderColor = '#ccc';
                    input.title = '';
                }, 1500);
                return;
            }
            items.push(value);
            writeJSON(textarea, items);
            renderTag(value);
            input.value = '';
            input.focus();
        }

        addBtn.addEventListener('click', addItem);
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addItem();
            }
        });
    }


    // =========================================================================
    // COLOR PICKER — pour les champs de type "multicolor"
    // =========================================================================

    function buildColorPicker(textarea) {

        let colors = readJSON(textarea);

        const wrapper = document.createElement('div');
        wrapper.className = 'color-picker-wrapper';
        wrapper.style.cssText = `
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px;
            background: #fff;
            margin-top: 4px;
        `;

        const swatchesContainer = document.createElement('div');
        swatchesContainer.style.cssText = `
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 10px;
            min-height: 36px;
        `;

        const inputRow = document.createElement('div');
        inputRow.style.cssText = 'display: flex; gap: 8px; align-items: center;';

        const colorInput = document.createElement('input');
        colorInput.type = 'color';
        colorInput.value = '#000000';
        colorInput.style.cssText = `
            width: 48px;
            height: 36px;
            border: 1px solid #ccc;
            border-radius: 4px;
            cursor: pointer;
            padding: 2px;
        `;

        const hexLabel = document.createElement('span');
        hexLabel.textContent = '#000000';
        hexLabel.style.cssText = `
            font-family: monospace;
            font-size: 13px;
            color: #555;
            min-width: 70px;
        `;
        colorInput.addEventListener('input', function () {
            hexLabel.textContent = colorInput.value.toUpperCase();
        });

        const addBtn = document.createElement('button');
        addBtn.type = 'button';
        addBtn.textContent = '+ Ajouter cette couleur';
        addBtn.style.cssText = `
            padding: 6px 12px;
            background: #417690;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            white-space: nowrap;
        `;

        inputRow.appendChild(colorInput);
        inputRow.appendChild(hexLabel);
        inputRow.appendChild(addBtn);
        wrapper.appendChild(swatchesContainer);
        wrapper.appendChild(inputRow);

        textarea.parentNode.insertBefore(wrapper, textarea);
        textarea.style.display = 'none';

        function renderSwatch(hexColor) {
            const swatch = document.createElement('div');
            swatch.style.cssText = `
                position: relative;
                display: inline-flex;
                flex-direction: column;
                align-items: center;
                gap: 2px;
            `;

            const circle = document.createElement('div');
            circle.style.cssText = `
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: ${hexColor};
                border: 2px solid #aaa;
                cursor: default;
            `;

            const label = document.createElement('span');
            label.textContent = hexColor.toUpperCase();
            label.style.cssText = `
                font-family: monospace;
                font-size: 10px;
                color: #555;
            `;

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.textContent = '✕';
            removeBtn.title = 'Supprimer cette couleur';
            removeBtn.style.cssText = `
                position: absolute;
                top: -4px;
                right: -4px;
                background: #c0392b;
                color: white;
                border: none;
                border-radius: 50%;
                width: 16px;
                height: 16px;
                font-size: 10px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 0;
                line-height: 1;
            `;
            removeBtn.addEventListener('click', function () {
                colors = colors.filter(c => c.toUpperCase() !== hexColor.toUpperCase());
                writeJSON(textarea, colors);
                swatch.remove();
            });

            swatch.appendChild(circle);
            swatch.appendChild(label);
            swatch.appendChild(removeBtn);
            swatchesContainer.appendChild(swatch);
        }

        colors.forEach(renderSwatch);

        addBtn.addEventListener('click', function () {
            const hex = colorInput.value.toUpperCase();
            if (colors.map(c => c.toUpperCase()).includes(hex)) {
                addBtn.textContent = '⚠ Déjà ajoutée !';
                setTimeout(() => { addBtn.textContent = '+ Ajouter cette couleur'; }, 1500);
                return;
            }
            colors.push(hex);
            writeJSON(textarea, colors);
            renderSwatch(hex);
        });
    }


    // =========================================================================
    // ORCHESTRATION
    // =========================================================================

    function applyWidget(row) {

        // FIX 1 : on cible select[name*="-field_type"] ET select[name="field_type"]
        // pour couvrir les lignes inline (préfixe dynamique) ET les cas edge
        const select = row.querySelector('select[name*="field_type"]');

        // FIX 2 : on cible aussi bien textarea que input[type=hidden] au cas où
        // Django rendrait le JSONField différemment selon la version
        const textarea = row.querySelector('textarea[name*="choices"], input[name*="choices"]');

        if (!select || !textarea) return;

        function refresh() {
            // FIX 3 : on compare select.value (valeur technique) au lieu du texte affiché
            // Plus robuste que selectedText — insensible aux changements de libellés
            const fieldType = select.value;

            // Supprimer tout widget précédemment injecté
            const existing = row.querySelector('.tag-system-wrapper, .color-picker-wrapper');
            if (existing) existing.remove();

            // Remettre le textarea visible avant de décider
            textarea.style.display = '';

            if (fieldType === 'select') {
                buildTagSystem(textarea);
            } else if (fieldType === 'multicolor') {
                buildColorPicker(textarea);
            } else {
                // text, integer, file, file_path, boolean → pas de choices
                // FIX 4 : on ne vide PAS textarea.value ici pour éviter
                // d'effacer des données si l'utilisateur change de type par erreur.
                // Le modèle Django gère déjà null/blank=True.
                textarea.style.display = 'none';
            }
        }

        refresh();
        select.addEventListener('change', refresh);
    }

    // FIX 5 : sélecteur élargi pour couvrir tous les cas de rendu Django admin
    // (tr.form-row seul, tr.dynamic-*, et tr sans classe sur certaines versions)
    function applyToAllRows() {
        const group = document.querySelector('#servicefield_set-group');
        if (!group) return;
        group.querySelectorAll('tr').forEach(function (row) {
            // Éviter les en-têtes et les lignes vides (pas de select dedans)
            if (row.querySelector('select[name*="field_type"]')) {
                applyWidget(row);
            }
        });
    }

    applyToAllRows();

    // MutationObserver pour les lignes ajoutées dynamiquement
    const inlineGroup = document.querySelector('#servicefield_set-group tbody');
    if (inlineGroup) {
        const observer = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                mutation.addedNodes.forEach(function (node) {
                    if (node.nodeType === 1 && node.tagName === 'TR') {
                        applyWidget(node);
                    }
                });
            });
        });
        observer.observe(inlineGroup, { childList: true });
    }

});