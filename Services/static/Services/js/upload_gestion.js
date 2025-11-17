// Gestion de l'upload
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const ctaButton = dropArea.querySelector('.cta-button');

dropArea.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropArea.classList.add('active');
});

dropArea.addEventListener('dragleave', function () {
    dropArea.classList.remove('active');
});

dropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    dropArea.classList.remove('active');
    handleFile(e.dataTransfer.files[0]);
});

ctaButton.addEventListener('click', function () {
    fileInput.click();
});