from flask import Blueprint, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import threading
import logging

bp = Blueprint('contact', __name__)

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email_async(name, email, message):
    """
    Wrapper asynchrone pour l'envoi d'emails (non-bloquant)
    """
    thread = threading.Thread(target=send_emails, args=(name, email, message))
    thread.daemon = True
    thread.start()

def send_emails(name, email, message):
    """
    Envoie deux emails :
    1. Notification au propriétaire du site
    2. Accusé de réception à l'expéditeur
    """
    try:
        # Configuration SMTP
        smtp_server = "mail.stephanezoa.online"
        smtp_port = 465
        sender_email = 'contact@stephanezoa.online'
        sender_password = "fA2-pekm9$H!1EA"
        
        if not sender_password:
            logger.error("⚠️ SMTP_PASSWORD non défini")
            return False

        # Connexion au serveur SMTP (réutilisée pour les deux emails)
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
            server.login(sender_email, sender_password)
            
            # 1️⃣ Email de notification (pour vous)
            notification_sent = send_notification_email(server, sender_email, name, email, message)
            
            # 2️⃣ Accusé de réception (pour l'expéditeur)
            confirmation_sent = send_confirmation_email(server, sender_email, email, name)
            
            if notification_sent and confirmation_sent:
                logger.info(f"✅ Emails envoyés avec succès à {email}")
                return True
            else:
                logger.warning(f"⚠️ Envoi partiel pour {email}")
                return False
                
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"❌ Erreur d'authentification SMTP : {str(e)}")
        return False
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"❌ Serveur SMTP déconnecté : {str(e)}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"❌ Erreur SMTP : {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Erreur inattendue : {type(e).__name__} - {str(e)}")
        return False

def send_notification_email(server, sender_email, name, email, message):
    """
    Email de notification pour le propriétaire du site (design amélioré)
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🔔 Nouveau message de {name} | Portfolio'
        msg['From'] = sender_email
        msg['To'] = sender_email
        msg['Reply-To'] = email

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; }}
                .email-wrapper {{ max-width: 650px; margin: 0 auto; }}
                .email-container {{ background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
                .header {{ background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #a855f7 100%); padding: 50px 40px; text-align: center; position: relative; }}
                .header::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>'); opacity: 0.3; }}
                .header h1 {{ color: #ffffff; font-size: 32px; font-weight: 700; margin-bottom: 10px; position: relative; z-index: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
                .header .icon {{ font-size: 60px; margin-bottom: 15px; display: block; animation: bounce 2s infinite; }}
                @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
                .content {{ padding: 40px; }}
                .badge {{ display: inline-block; background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; padding: 8px 20px; border-radius: 50px; font-size: 14px; font-weight: 600; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3); }}
                .sender-info {{ background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 30px; border-radius: 15px; margin: 25px 0; border-left: 5px solid #06b6d4; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
                .info-row {{ margin: 15px 0; display: flex; align-items: center; }}
                .info-label {{ font-weight: 600; color: #475569; min-width: 100px; font-size: 15px; }}
                .info-value {{ color: #1e293b; font-size: 15px; }}
                .info-value a {{ color: #06b6d4; text-decoration: none; font-weight: 600; }}
                .info-value a:hover {{ text-decoration: underline; }}
                .message-box {{ background: #ffffff; border: 2px solid #e2e8f0; padding: 30px; border-radius: 15px; margin: 25px 0; box-shadow: inset 0 2px 10px rgba(0,0,0,0.02); }}
                .message-box h3 {{ color: #1e293b; margin-bottom: 15px; font-size: 18px; display: flex; align-items: center; gap: 10px; }}
                .message-text {{ color: #475569; line-height: 1.8; font-size: 15px; white-space: pre-wrap; word-wrap: break-word; }}
                .cta-section {{ text-align: center; margin: 35px 0; padding: 30px; background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%); border-radius: 15px; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 16px; box-shadow: 0 10px 25px rgba(6, 182, 212, 0.3); transition: all 0.3s ease; }}
                .cta-button:hover {{ transform: translateY(-2px); box-shadow: 0 15px 35px rgba(6, 182, 212, 0.4); }}
                .footer {{ background: #f8fafc; padding: 30px 40px; text-align: center; border-top: 3px solid #e2e8f0; }}
                .footer p {{ color: #64748b; font-size: 13px; margin: 8px 0; }}
                .footer .brand {{ color: #1e293b; font-weight: 700; font-size: 15px; margin-top: 15px; }}
                .divider {{ height: 2px; background: linear-gradient(90deg, transparent, #06b6d4, transparent); margin: 25px 0; }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="email-container">
                    <div class="header">
                        <span class="icon">📬</span>
                        <h1>Nouveau Message Reçu</h1>
                    </div>
                    <div class="content">
                        <div style="text-align: center;">
                            <span class="badge">📩 PORTFOLIO CONTACT</span>
                        </div>
                        
                        <div class="sender-info">
                            <div class="info-row">
                                <span class="info-label">👤 Nom :</span>
                                <span class="info-value"><strong>{name}</strong></span>
                            </div>
                            <div class="divider"></div>
                            <div class="info-row">
                                <span class="info-label">📧 Email :</span>
                                <span class="info-value"><a href="mailto:{email}">{email}</a></span>
                            </div>
                            <div class="divider"></div>
                            <div class="info-row">
                                <span class="info-label">🕒 Date :</span>
                                <span class="info-value">{datetime.now().strftime('%d/%m/%Y à %H:%M')}</span>
                            </div>
                        </div>

                        <div class="message-box">
                            <h3>
                                <span style="font-size: 24px;">💬</span>
                                <span>Message</span>
                            </h3>
                            <div class="message-text">{message}</div>
                        </div>

                        <div class="cta-section">
                            <p style="color: #475569; margin-bottom: 20px; font-size: 15px;">Répondez rapidement à {name}</p>
                            <a href="mailto:{email}?subject=Re: Votre message depuis mon portfolio" class="cta-button">
                                ✉️ Répondre Maintenant
                            </a>
                        </div>
                    </div>
                    <div class="footer">
                        <p>📨 Message automatique envoyé depuis votre portfolio</p>
                        <p style="color: #94a3b8; font-size: 12px;">Un accusé de réception a été automatiquement envoyé à {email}</p>
                        <p class="brand">© 2026 Stephane Zoa • Tous droits réservés</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
NOUVEAU MESSAGE PORTFOLIO
{'='*60}

De: {name}
Email: {email}
Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}

MESSAGE:
{message}

{'='*60}
Répondre: mailto:{email}
        """

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        server.send_message(msg)
        logger.info(f"✅ Notification envoyée à {sender_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur notification email : {str(e)}")
        return False

def send_confirmation_email(server, sender_email, recipient_email, recipient_name):
    """
    Accusé de réception pour l'expéditeur (design premium)
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'✅ Message bien reçu | Stephane Zoa'
        msg['From'] = sender_email
        msg['To'] = recipient_email

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%); padding: 40px 20px; }}
                .email-wrapper {{ max-width: 650px; margin: 0 auto; }}
                .email-container {{ background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); padding: 50px 40px; text-align: center; position: relative; }}
                .header::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 50%); }}
                .checkmark {{ width: 80px; height: 80px; margin: 0 auto 20px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 50px; position: relative; z-index: 1; animation: scaleIn 0.5s ease-out; }}
                @keyframes scaleIn {{ from {{ transform: scale(0); }} to {{ transform: scale(1); }} }}
                .header h1 {{ color: #ffffff; font-size: 32px; font-weight: 700; margin-bottom: 10px; position: relative; z-index: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
                .header p {{ color: rgba(255,255,255,0.95); font-size: 16px; position: relative; z-index: 1; }}
                .content {{ padding: 40px; }}
                .greeting {{ font-size: 24px; color: #1e293b; font-weight: 600; margin-bottom: 20px; }}
                .message-card {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 30px; border-radius: 15px; margin: 25px 0; border-left: 5px solid #06b6d4; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
                .message-card p {{ color: #475569; line-height: 1.8; font-size: 15px; margin: 12px 0; }}
                .highlight-box {{ background: #ffffff; border: 2px dashed #06b6d4; padding: 25px; border-radius: 12px; margin: 25px 0; text-align: center; }}
                .highlight-box .icon {{ font-size: 40px; margin-bottom: 15px; }}
                .highlight-box h3 {{ color: #1e293b; font-size: 20px; margin-bottom: 10px; }}
                .highlight-box p {{ color: #64748b; font-size: 14px; line-height: 1.6; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 30px 0; }}
                .info-card {{ background: #ffffff; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #e2e8f0; transition: all 0.3s; }}
                .info-card:hover {{ border-color: #06b6d4; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(6, 182, 212, 0.2); }}
                .info-card .icon {{ font-size: 32px; margin-bottom: 10px; }}
                .info-card h4 {{ color: #1e293b; font-size: 14px; font-weight: 600; margin-bottom: 5px; }}
                .info-card p {{ color: #64748b; font-size: 13px; }}
                .social-section {{ background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 30px; border-radius: 15px; margin: 30px 0; text-align: center; }}
                .social-section h3 {{ color: #92400e; margin-bottom: 15px; font-size: 18px; }}
                .social-links {{ display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-top: 20px; }}
                .social-btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; background: #ffffff; color: #1e293b; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s; }}
                .social-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }}
                .footer {{ background: #f8fafc; padding: 30px 40px; text-align: center; border-top: 3px solid #e2e8f0; }}
                .footer p {{ color: #64748b; font-size: 13px; margin: 8px 0; }}
                .footer .brand {{ color: #1e293b; font-weight: 700; font-size: 15px; margin-top: 15px; }}
                .divider {{ height: 2px; background: linear-gradient(90deg, transparent, #06b6d4, transparent); margin: 25px 0; }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="email-container">
                    <div class="header">
                        <div class="checkmark">✓</div>
                        <h1>Message bien reçu !</h1>
                        <p>Je reviendrai vers vous très bientôt</p>
                    </div>
                    <div class="content">
                        <p class="greeting">Bonjour {recipient_name},</p>
                        
                        <div class="message-card">
                            <p><strong>Merci pour votre message !</strong> 🙏</p>
                            <p>Je vous confirme la bonne réception de votre demande envoyée le <strong>{datetime.now().strftime('%d/%m/%Y à %H:%M')}</strong>.</p>
                            <p>Je m'efforce de répondre à tous les messages dans les <strong>24-48 heures</strong>. Votre demande est importante pour moi et je la traiterai avec attention.</p>
                        </div>

                        <div class="highlight-box">
                            <div class="icon">⏱️</div>
                            <h3>Délai de réponse</h3>
                            <p>Je reviendrai vers vous sous <strong>24 à 48 heures</strong><br>En cas d'urgence, contactez-moi via WhatsApp</p>
                        </div>

                        <div class="info-grid">
                            <div class="info-card">
                                <div class="icon">📧</div>
                                <h4>Email</h4>
                                <p>contact@stephanezoa.online</p>
                            </div>
                            <div class="info-card">
                                <div class="icon">📱</div>
                                <h4>WhatsApp</h4>
                                <p>+237 686 002 112</p>
                            </div>
                        </div>

                        <div class="social-section">
                            <h3>🔗 Restons connectés</h3>
                            <p style="color: #92400e; font-size: 14px; margin-bottom: 10px;">Suivez mon actualité et mes projets</p>
                            <div class="social-links">
                                <a href="#" class="social-btn">
                                    <span>💼</span> LinkedIn
                                </a>
                                <a href="#" class="social-btn">
                                    <span>🐙</span> GitHub
                                </a>
                                <a href="https://wa.me/237686002112" class="social-btn">
                                    <span>💬</span> WhatsApp
                                </a>
                            </div>
                        </div>

                        <div class="divider"></div>
                        
                        <p style="color: #64748b; font-size: 14px; text-align: center; line-height: 1.6;">
                            En attendant ma réponse, n'hésitez pas à consulter mes projets sur mon portfolio<br>
                            ou à me contacter directement via WhatsApp pour toute urgence.
                        </p>
                    </div>
                    <div class="footer">
                        <p>📩 Ceci est un accusé de réception automatique</p>
                        <p style="color: #94a3b8; font-size: 12px;">Merci de ne pas répondre directement à cet email</p>
                        <p class="brand">© 2026 Stephane Zoa • Développeur Full Stack</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
MESSAGE BIEN REÇU !
{'='*60}

Bonjour {recipient_name},

Merci pour votre message ! Je vous confirme sa bonne réception.

📅 Date de réception : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
⏱️ Délai de réponse : 24-48 heures

Je reviendrai vers vous très bientôt.

CONTACT DIRECT:
📧 Email : contact@stephanezoa.online
📱 WhatsApp : +237 686 002 112

Cordialement,
Stephane Zoa
Développeur Full Stack

{'='*60}
Ceci est un accusé de réception automatique
© 2026 Djembar Arafat
        """

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        server.send_message(msg)
        logger.info(f"✅ Accusé de réception envoyé à {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur accusé de réception : {str(e)}")
        return False


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Page de contact avec envoi d'email asynchrone (non-bloquant)
    """
    if request.method == 'POST':
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

        # Log sécurisé (sans afficher l'email complet)
        logger.info(f"📨 Nouveau message de {name} ({email[:3]}***@{email.split('@')[1]})")

        try:
            # Envoi asynchrone (non-bloquant) ✅
            send_email_async(name, email, message)
            
            # Réponse immédiate à l'utilisateur
            flash('✅ Merci pour votre message ! Je vous répondrai dans les plus brefs délais. Un accusé de réception a été envoyé à votre adresse email.', 'success')
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du lancement de l'envoi : {str(e)}")
            flash('⚠️ Une erreur est survenue. Veuillez réessayer ou me contacter via WhatsApp au +237 686 002 112.', 'error')

        return redirect(url_for('contact.contact'))

    return render_template('contact.html')