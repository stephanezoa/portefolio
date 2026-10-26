from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import logging
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

bp = Blueprint('contact', __name__)

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_mail(name, email, message):
    """Envoie le message du formulaire via SMTP SSL (identifiants dans .env)."""
    user = os.environ['SMTP_EMAIL']
    msg = EmailMessage()
    msg['Subject'] = f'Portfolio — message de {name}'.replace('\n', ' ').replace('\r', ' ')
    msg['From'] = user
    msg['To'] = os.environ.get('CONTACT_TO', user)
    msg['Reply-To'] = email.replace('\n', '').replace('\r', '')
    msg.set_content(f'Nom : {name}\nEmail : {email}\n\n{message}')

    host = os.environ.get('SMTP_HOST', 'mail.stephanezoa.site')
    port = int(os.environ.get('SMTP_PORT', 465))
    with smtplib.SMTP_SSL(host, port, timeout=15) as server:
        server.login(user, os.environ['SMTP_PASSWORD'])
        server.send_message(msg)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Page de contact avec envoi d'email via EmailJS (côté client)
    """
    if request.method == 'POST':
        # Cette route peut rester pour la validation côté serveur si nécessaire
        # Mais l'envoi d'email se fera via EmailJS côté client
        
        # Récupération des données
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # Validation renforcée
        errors = []
        
        # Validation du nom
        if not name:
            errors.append('Le nom est obligatoire')
        elif len(name) < 2:
            errors.append('Le nom doit contenir au moins 2 caractères')
        elif len(name) > 100:
            errors.append('Le nom ne peut pas dépasser 100 caractères')
        
        # Validation de l'email
        if not email:
            errors.append('L\'email est obligatoire')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Veuillez entrer une adresse email valide')
        elif len(email) > 254:  # RFC 5321
            errors.append('L\'email ne peut pas dépasser 254 caractères')
        
        # Validation du message
        if not message:
            errors.append('Le message est obligatoire')
        elif len(message) < 10:
            errors.append('Le message doit contenir au moins 10 caractères')
        elif len(message) > 5000:
            errors.append('Le message ne peut pas dépasser 5000 caractères')

        # Affichage des erreurs
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('contact.contact'))

        # Log du message
        logger.info(f"📨 Nouveau message de {name} ({email[:3]}***@{email.split('@')[1]})")

        try:
            send_mail(name, email, message)
        except Exception as e:
            logger.error(f"❌ Envoi SMTP échoué : {e}")
            flash("Une erreur est survenue lors de l'envoi. Veuillez réessayer plus tard.", 'error')
            return redirect(url_for('contact.contact'))

        # Message de confirmation
        flash('✅ Merci pour votre message ! Je vous répondrai dans les plus brefs délais.', 'success')
        return redirect(url_for('contact.contact'))

    return render_template('contact.html')


@bp.route('/api/contact/validate', methods=['POST'])
def validate_contact():
    """
    API endpoint pour la validation côté serveur (optionnel)
    """
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        errors = []
        
        # Validation
        if not name or len(name) < 2:
            errors.append('Le nom doit contenir au moins 2 caractères')
        if not email or '@' not in email:
            errors.append('Email invalide')
        if not message or len(message) < 10:
            errors.append('Le message doit contenir au moins 10 caractères')
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"❌ Erreur validation : {str(e)}")
        return jsonify({'success': False, 'errors': ['Erreur de validation']}), 500