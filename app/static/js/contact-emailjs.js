// ========================================
// Configuration EmailJS
// ========================================
// ÉTAPE 1: Créer un compte sur https://www.emailjs.com/
// ÉTAPE 2: Récupérer vos clés dans le dashboard EmailJS
// ÉTAPE 3: Remplacer les valeurs ci-dessous

const EMAILJS_CONFIG = {
    publicKey: 'RdQ_W5S6f3vXW0tkK',        // Ex: 'user_abc123xyz'
    serviceID: 'service_cyl26vu',        // Ex: 'service_gmail'
    templateID: 'VOTRE_TEMPLATE_ID'       // Ex: 'template_contact'
};

// ========================================
// Initialisation EmailJS
// ========================================
(function() {
    emailjs.init(EMAILJS_CONFIG.publicKey);
})();

// ========================================
// Gestion du formulaire de contact
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('form[action*="contact.contact"]');
    
    if (!contactForm) {
        console.warn('Formulaire de contact non trouvé');
        return;
    }

    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Récupérer les données du formulaire
        const formData = {
            name: contactForm.querySelector('#name').value.trim(),
            email: contactForm.querySelector('#email').value.trim(),
            message: contactForm.querySelector('#message').value.trim()
        };

        // Validation côté client
        if (!validateForm(formData)) {
            return;
        }

        // Désactiver le bouton d'envoi
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalHTML = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="inline-block animate-spin mr-2">⏳</span>
            <span>Sending...</span>
        `;

        try {
            // Envoyer l'email via EmailJS
            const response = await emailjs.send(
                EMAILJS_CONFIG.serviceID,
                EMAILJS_CONFIG.templateID,
                {
                    from_name: formData.name,
                    from_email: formData.email,
                    message: formData.message,
                    to_name: 'Djembar Arafat',
                    reply_to: formData.email,
                    date: new Date().toLocaleString('fr-FR', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                }
            );

            console.log('✅ Email envoyé avec succès:', response);

            // Afficher notification de succès
            showToast('success', '✅ Message sent successfully! I\'ll get back to you soon.');

            // Réinitialiser le formulaire
            contactForm.reset();

            // Animation de confettis (optionnel)
            createConfetti();

        } catch (error) {
            console.error('❌ Erreur lors de l\'envoi:', error);
            
            // Afficher notification d'erreur
            showToast(
                'error', 
                '⚠️ Oops! Something went wrong. Please try WhatsApp or call me directly.'
            );

        } finally {
            // Réactiver le bouton
            submitButton.disabled = false;
            submitButton.innerHTML = originalHTML;
        }
    });
});

// ========================================
// Validation du formulaire
// ========================================
function validateForm(data) {
    const errors = [];

    // Validation du nom
    if (!data.name || data.name.length < 2) {
        errors.push('Name must be at least 2 characters');
    } else if (data.name.length > 100) {
        errors.push('Name cannot exceed 100 characters');
    }

    // Validation de l'email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!data.email) {
        errors.push('Email is required');
    } else if (!emailRegex.test(data.email)) {
        errors.push('Please enter a valid email address');
    } else if (data.email.length > 254) {
        errors.push('Email cannot exceed 254 characters');
    }

    // Validation du message
    if (!data.message || data.message.length < 10) {
        errors.push('Message must be at least 10 characters');
    } else if (data.message.length > 5000) {
        errors.push('Message cannot exceed 5000 characters');
    }

    // Afficher les erreurs
    if (errors.length > 0) {
        showToast('error', errors.join('<br>'));
        return false;
    }

    return true;
}

// ========================================
// Système de notifications Toast (moderne)
// ========================================
function showToast(type, message) {
    // Supprimer les toasts existants
    const existingToasts = document.querySelectorAll('.custom-toast');
    existingToasts.forEach(toast => toast.remove());

    // Créer le toast
    const toast = document.createElement('div');
    toast.className = `custom-toast custom-toast-${type}`;
    
    const icon = type === 'success' 
        ? '<i class="fas fa-check-circle"></i>' 
        : '<i class="fas fa-exclamation-circle"></i>';
    
    toast.innerHTML = `
        <div class="custom-toast-content">
            <div class="custom-toast-icon">${icon}</div>
            <div class="custom-toast-message">${message}</div>
            <button class="custom-toast-close" onclick="this.closest('.custom-toast').remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Ajouter au DOM
    document.body.appendChild(toast);

    // Animation d'entrée
    setTimeout(() => toast.classList.add('show'), 10);

    // Suppression automatique après 6 secondes
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 6000);
}

// ========================================
// Animation de confettis (succès)
// ========================================
function createConfetti() {
    const colors = ['#06b6d4', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        
        document.body.appendChild(confetti);

        // Supprimer après l'animation
        setTimeout(() => confetti.remove(), 4000);
    }
}

// ========================================
// Injection des styles CSS
// ========================================
const style = document.createElement('style');
style.textContent = `
    /* Toast Notifications */
    .custom-toast {
        position: fixed;
        top: 20px;
        right: 20px;
        min-width: 350px;
        max-width: 500px;
        background: rgba(17, 24, 39, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        transform: translateX(120%);
        transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        z-index: 9999;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .custom-toast.show {
        transform: translateX(0);
    }

    .custom-toast-success {
        border-left: 4px solid #10b981;
    }

    .custom-toast-error {
        border-left: 4px solid #ef4444;
    }

    .custom-toast-content {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 20px;
    }

    .custom-toast-icon {
        font-size: 24px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }

    .custom-toast-success .custom-toast-icon {
        color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }

    .custom-toast-error .custom-toast-icon {
        color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }

    .custom-toast-message {
        flex: 1;
        color: #e5e7eb;
        font-size: 14px;
        line-height: 1.6;
        padding-top: 4px;
    }

    .custom-toast-close {
        background: none;
        border: none;
        color: #9ca3af;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        transition: all 0.2s;
        border-radius: 4px;
    }

    .custom-toast-close:hover {
        color: #fff;
        background: rgba(255, 255, 255, 0.1);
    }

    /* Confetti Animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        z-index: 9998;
        animation: confettiFall linear forwards;
        opacity: 0.9;
        border-radius: 2px;
    }

    @keyframes confettiFall {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }

    /* Loading Animation */
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .animate-spin {
        animation: spin 1s linear infinite;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .custom-toast {
            min-width: auto;
            max-width: calc(100% - 40px);
            left: 20px;
            right: 20px;
        }
    }

    /* Dark theme adjustments */
    @media (prefers-color-scheme: dark) {
        .custom-toast {
            background: rgba(17, 24, 39, 0.98);
        }
    }
`;
document.head.appendChild(style);