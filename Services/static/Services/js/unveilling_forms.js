// Gestion de l'affichage du formulaire
document.getElementById('show-form-btn').addEventListener('click', function() {
    const formSection = document.getElementById('contact-form');
    formSection.style.display = 'block';
    this.style.display = 'none'; // Cache le bouton après clic
    
    // Animation pour le formulaire
    formSection.scrollIntoView({ behavior: 'smooth' });
    formSection.querySelector('.form-container').classList.add('animate__fadeInUp');
});