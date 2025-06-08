// Sélection de couleur
// Sélection multiple de couleurs
const colorOptions = document.querySelectorAll('.group1');
const colorOptions2 = document.querySelectorAll('.group2');
const selectedColorsInput = document.getElementById('selected-colors1');
const selectedColorsInput2 = document.getElementById('selected-colors2');
const selectedColorsDisplay = document.getElementById('selected-colors-display1');
const selectedColorsDisplay2 = document.getElementById('selected-colors-display2');
let selectedColors = [];
let selectedColors2 = [];

colorOptions.forEach(option => {
    option.addEventListener('click', function () {
        const color = this.getAttribute('data-color');

        // Vérifier si la couleur est déjà sélectionnée
        const colorIndex = selectedColors.indexOf(color);

        if (colorIndex === -1) {
            // Ajouter la couleur
            selectedColors.push(color);
            this.classList.add('selected');
        } else {
            // Retirer la couleur
            selectedColors.splice(colorIndex, 1);
            this.classList.remove('selected');
        }

        // Mettre à jour le champ caché
        selectedColorsInput.value = selectedColors.join(',');

        // Mettre à jour l'affichage
        updateSelectedColorsDisplay();
    });
});

colorOptions2.forEach(option => {
    option.addEventListener('click', function () {
        const color = this.getAttribute('data-color');

        // Vérifier si la couleur est déjà sélectionnée
        const colorIndex = selectedColors2.indexOf(color);

        if (colorIndex === -1) {
            // Ajouter la couleur
            selectedColors2.push(color);
            this.classList.add('selected');
        } else {
            // Retirer la couleur
            selectedColors2.splice(colorIndex, 1);
            this.classList.remove('selected');
        }

        // Mettre à jour le champ caché
        selectedColorsInput2.value = selectedColors2.join(',');

        // Mettre à jour l'affichage
        updateSelectedColorsDisplay2();
    });
});

function updateSelectedColorsDisplay() {
    selectedColorsDisplay.innerHTML = '';

    selectedColors.forEach(color => {
        const colorElement = document.createElement('div');
        colorElement.className = 'selected-color';
        colorElement.style.background = color;
        colorElement.setAttribute('data-color', color);

        // Ajouter un bouton pour supprimer la couleur
        colorElement.addEventListener('click', function (e) {
            e.stopPropagation();
            const colorToRemove = this.getAttribute('data-color');
            selectedColors = selectedColors.filter(c => c !== colorToRemove);
            selectedColorsInput.value = selectedColors.join(',');

            // Retirer la classe selected de l'option correspondante
            document.querySelectorAll('.group1').forEach(opt => {
                if (opt.getAttribute('data-color') === colorToRemove) {
                    opt.classList.remove('selected');
                }
            });

            updateSelectedColorsDisplay();
        });

        selectedColorsDisplay.appendChild(colorElement);
    });
    updateSummary();
}

function updateSelectedColorsDisplay2() {
    selectedColorsDisplay2.innerHTML = '';


    selectedColors2.forEach(color => {
        const colorElement = document.createElement('div');
        colorElement.className = 'selected-color';
        colorElement.style.background = color;
        colorElement.setAttribute('data-color', color);

        // Ajouter un bouton pour supprimer la couleur
        colorElement.addEventListener('click', function (e) {
            e.stopPropagation();
            const colorToRemove = this.getAttribute('data-color');
            selectedColors2 = selectedColors2.filter(c => c !== colorToRemove);
            selectedColorsInput2.value = selectedColors2.join(',');

            // Retirer la classe selected de l'option correspondante
            document.querySelectorAll('.group2').forEach(opt => {
                if (opt.getAttribute('data-color') === colorToRemove) {
                    opt.classList.remove('selected');
                }
            });

            updateSelectedColorsDisplay2();
        });

        selectedColorsDisplay2.appendChild(colorElement);
    });
    updateSummary2();
}
