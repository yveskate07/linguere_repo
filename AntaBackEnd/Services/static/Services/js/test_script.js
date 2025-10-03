// Back to Top Button
        const backToTopButton = document.querySelector('.back-to-top');
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('active');
            } else {
                backToTopButton.classList.remove('active');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Dropdown menu animation
        const dropdowns = document.querySelectorAll('.dropdown');
        
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('mouseenter', () => {
                const menu = dropdown.querySelector('.dropdown-menu');
                menu.style.display = 'block';
                menu.classList.add('animate__animated', 'animate__fadeIn');
            });
            
            dropdown.addEventListener('mouseleave', () => {
                const menu = dropdown.querySelector('.dropdown-menu');
                menu.style.display = 'none';
                menu.classList.remove('animate__animated', 'animate__fadeIn');
            });
        });


function updateSummary() {
    const summaryContainer = document.getElementById('summary-container');
    const supportType = document.getElementById('support-type');
    const otherSupport = document.getElementById('other-support');
    const width = document.getElementById('width');
    const height = document.getElementById('height');
    const selectedColors = document.getElementById('selected-colors');
    const quantity = document.getElementById('quantity');
    const specialNotes = document.getElementById('special-notes');
    const previewImage = document.getElementById('preview-image').src;
        
    // Déterminer le type de support
    let supportText = supportType.options[supportType.selectedIndex].text;
    if (supportType.value === 'autre' && otherSupport.value) {
        supportText = otherSupport.value;
    }
        
        // Préparer les couleurs sélectionnées
        let colorsHtml = '';
        if (selectedColors.value) {
            colorsHtml = selectedColors.value.split(',').map(color => {
                return `<span class="color-swatch" style="background: ${color}"></span>`;
            }).join('');
        }
        
        // Créer le HTML de l'aperçu
        summaryContainer.innerHTML = `
            <div class="summary-item">
                <h4><i class="fas fa-tshirt"></i> Support</h4>
                <p>${supportText}</p>
            </div>
            
            <div class="summary-item">
                <h4><i class="fas fa-ruler-combined"></i> Dimensions</h4>
                <p>${width.value} cm × ${height.value} cm</p>
            </div>
            
            <div class="summary-item">
                <h4><i class="fas fa-palette"></i> Couleurs</h4>
                <p>${colorsHtml || 'Aucune couleur sélectionnée'}</p>
            </div>
            
            <div class="summary-item">
                <h4><i class="fas fa-boxes"></i> Quantité</h4>
                <p>${quantity.value} pièce(s)</p>
            </div>
            
            ${specialNotes.value ? `
            <div class="summary-item">
                <h4><i class="fas fa-clipboard-list"></i> Instructions</h4>
                <p>${specialNotes.value}</p>
            </div>
            ` : ''}
        `;
    }