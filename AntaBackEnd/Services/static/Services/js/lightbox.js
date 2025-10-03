// Lightbox simplifiée
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxClose = document.querySelector('.lightbox-close');
const lightboxPrev = document.querySelector('.lightbox-prev');
const lightboxNext = document.querySelector('.lightbox-next');
const lightboxCounter = document.getElementById('lightbox-counter');
const selectImageBtn = document.getElementById('select-image-btn');

let currentImageIndex = 0;
const images = Array.from(document.querySelectorAll('.gallery-item')).map(item => item.querySelector('img').src);
const previewImage = document.getElementById('preview-image');
const galleryItems = document.querySelectorAll('.gallery-item');

// Lightbox navigation
function updateLightboxImage() {
    lightboxImg.src = images[currentImageIndex];
    lightboxCounter.textContent = `${currentImageIndex + 1} / ${images.length}`;
}

// Ouvrir lightbox depuis la galerie
galleryItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        currentImageIndex = index;
        updateLightboxImage();
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
});

// Navigation lightbox
lightboxPrev.addEventListener('click', (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    updateLightboxImage();
});

lightboxNext.addEventListener('click', (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex + 1) % images.length;
    updateLightboxImage();
});

// Fermer lightbox et sélectionner l'image
lightboxClose.addEventListener('click', () => {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
});

// Sélectionner l'image et fermer la lightbox
selectImageBtn.addEventListener('click', () => {
    previewImage.src = images[currentImageIndex];
    galleryItems.forEach(item => item.classList.remove('selected'));
    galleryItems[currentImageIndex].classList.add('selected');
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
});

// Après la déclaration de selectImageBtn
const closeLightboxBtn = document.getElementById('close-lightbox-btn');

closeLightboxBtn.addEventListener('click', () => {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
});