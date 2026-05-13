function handleFile(file) {
    if (file && (file.type.startsWith('image/') || file.name.endsWith('.svg'))) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else if (file && file.name.endsWith('.dst')) {
        previewImage.src = 'https://via.placeholder.com/320x320/CCCCCC/808080?Text=Fichier+DST';
        alert('Le fichier DST est un format de broderie, la prévisualisation peut ne pas être exacte.');
    } else if (file) {
        alert('Format de fichier non supporté. Veuillez utiliser une image (PNG, JPG, SVG) ou un fichier DST.');
    }
}

// Mettre à jour l'aperçu lors de la sélection d'une image
document.getElementById('file-input').addEventListener('change', function (event) {
    handleFile(this.files[0]);

    const preview = document.getElementById('preview-image');

    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
        preview.src = '#';
    }
});

