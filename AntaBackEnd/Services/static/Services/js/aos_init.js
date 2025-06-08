// Initialize AOS
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

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

// Cart Counter Animation
const cartCount = document.querySelector('.cart-count');
let count = 0;

// Simulate adding items to cart (for demo)
setInterval(() => {
    if (count < 5) {
        count++;
        cartCount.setAttribute('data-count', count);

        // Add animation
        cartCount.classList.add('animate__animated', 'animate__bounceIn');
        setTimeout(() => {
            cartCount.classList.remove('animate__animated', 'animate__bounceIn');
        }, 1000);
    }
}, 5000);

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

// Search bar focus effect
const searchInput = document.querySelector('.search-bar input');

searchInput.addEventListener('focus', () => {
    searchInput.parentElement.classList.add('animate__animated', 'animate__pulse');
});

searchInput.addEventListener('blur', () => {
    searchInput.parentElement.classList.remove('animate__animated', 'animate__pulse');
});