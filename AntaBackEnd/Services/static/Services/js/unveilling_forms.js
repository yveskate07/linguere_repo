// Gestion de l'affichage du formulaire
document.getElementById('show-form-btn1').addEventListener('click', function() {
    const formSection = document.getElementById('contact-form1');
    formSection.style.display = 'block';
    this.style.display = 'none'; // Cache le bouton après clic
    
    // Animation pour le formulaire
    formSection.scrollIntoView({ behavior: 'smooth' });
    formSection.querySelector('.form-container').classList.add('animate__fadeInUp');
});

document.getElementById('show-form-btn2').addEventListener('click', function() {
    const formSection = document.getElementById('contact-form2');
    formSection.style.display = 'block';
    this.style.display = 'none'; // Cache le bouton après clic
    
    // Animation pour le formulaire
    formSection.scrollIntoView({ behavior: 'smooth' });
    formSection.querySelector('.form-container').classList.add('animate__fadeInUp');
});