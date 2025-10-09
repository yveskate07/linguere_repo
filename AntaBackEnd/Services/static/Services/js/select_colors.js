// Sélection multiple de couleurs
const colorOptions = document.querySelectorAll('.color-option');
const selectedColorsInput = document.getElementById('selected-colors');
const selectedColorsDisplay = document.getElementById('selected-colors-display');
let selectedColors = [];

colorOptions.forEach(option => {
    option.addEventListener('click', function() {
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

function updateSelectedColorsDisplay() {
    selectedColorsDisplay.innerHTML = '';
    
    selectedColors.forEach(color => {
        let colorElement = document.createElement('div');
        colorElement.className = 'selected-color';
        colorElement.style.background = color;
        colorElement.setAttribute('data-color', color);
        
        // Ajouter un bouton pour supprimer la couleur
        colorElement.addEventListener('click', function(e) {
            e.stopPropagation();
            const colorToRemove = this.getAttribute('data-color');
            selectedColors = selectedColors.filter(c => c !== colorToRemove);
            selectedColorsInput.value = selectedColors.join(',');
            
            // Retirer la classe selected de l'option correspondante
            document.querySelectorAll('.color-option').forEach(opt => {
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


