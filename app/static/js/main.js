/* =================================
   MAIN JAVASCRIPT
   ================================= */

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Portfolio loaded successfully!');
    
    // Initialiser AOS si disponible
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100,
            easing: 'ease-in-out'
        });
    }
    
    // Mobile Menu
    initMobileMenu();
    
    // Smooth Scroll
    initSmoothScroll();
    
    // Flash Messages
    initFlashMessages();
});

// ======= MOBILE MENU =======
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeMenu = document.getElementById('close-menu');
    
    if (!mobileMenuBtn || !mobileMenu) return;
    
    // Ouvrir le menu
    mobileMenuBtn.addEventListener('click', function() {
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    // Fermer le menu
    if (closeMenu) {
        closeMenu.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Fermer en cliquant sur un lien
    const menuLinks = mobileMenu.querySelectorAll('a');
    menuLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
    
    // Fermer avec Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// ======= SMOOTH SCROLL =======
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#' || href === '#!') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const headerHeight = document.querySelector('header')?.offsetHeight || 0;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ======= FLASH MESSAGES =======
function initFlashMessages() {
    const flashContainer = document.getElementById('flash-container');
    
    if (!flashContainer) return;
    
    // Auto-hide après 5 secondes
    setTimeout(function() {
        flashContainer.style.transition = 'opacity 0.5s ease';
        flashContainer.style.opacity = '0';
        
        setTimeout(function() {
            flashContainer.remove();
        }, 500);
    }, 5000);
}

// ======= SCROLL HEADER EFFECT =======
let lastScroll = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
        header?.classList.add('scrolled');
    } else {
        header?.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// ======= LOG SUCCESS =======
console.log('✅ Main.js loaded successfully');