// Mettre à jour l'aperçu lors de la sélection d'une image
document.getElementById('select-image-btn').addEventListener('click', updateSummary);
document.getElementById('file-input').addEventListener('change', function (event) {
    setTimeout(updateSummary, 100);
    handleFile(this.files[0]);

    const preview = document.getElementById('preview-image2');

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
