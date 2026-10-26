# Portfolio — Stephane Zoa

Portfolio de développeur Full-Stack (Cameroun) : fintech, mobile et IA. Application **Flask** rendue côté serveur, avec **Tailwind CSS** (CDN), **AOS** pour les animations d'apparition et du JavaScript natif pour les composants interactifs.

## Pages

| Route | Contenu |
|---|---|
| `/` | Accueil : hero avec vitrine animée de tous les projets, projets en vedette, expertise, contact |
| `/projects/projects` | Work : 24 projets filtrables (en ligne et locaux), avec stack, fonctionnalités et chiffres clés dans un modal |
| `/experience` | Parcours : hero animé et sentier chronologique des expériences, formation, compétences, langues |
| `/gallery` | Photothèque : événements, puis photos par événement avec visionneuse plein écran |
| `/skills` · `/testimonials` | Compétences et témoignages |
| `/contact/contact` | Formulaire de contact, envoyé par SMTP côté serveur |

## Démarrage rapide

Prérequis : Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # puis renseigner les valeurs
python run.py               # http://localhost:5001
```

## Configuration (`.env`)

Le fichier `.env` n'est **jamais versionné** (voir `.gitignore`). Modèle : [.env.example](.env.example).

| Variable | Rôle |
|---|---|
| `SECRET_KEY` | Clé de session Flask |
| `SMTP_HOST` / `SMTP_PORT` | Serveur d'envoi (SSL, port 465 par défaut) |
| `SMTP_EMAIL` / `SMTP_PASSWORD` | Compte d'envoi du formulaire de contact |
| `CONTACT_TO` | Adresse qui reçoit les messages (par défaut `SMTP_EMAIL`) |

## Contenu piloté par des données

Pas de base de données : le contenu vit dans des fichiers JSON et des dossiers d'images.

### Projets — `data/projects.json`

Chaque projet décrit : `title`, `subtitle`, `description`, `long_description`, `category`, `status`, `color`, `icon`, `image`, `demo`, `local`, ainsi que :

- `stack` : technologies **groupées** (Backend, Mobile, IA, Intégrations…) ;
- `features` : ce que fait l'application ;
- `metrics` : chiffres clés (`value` + `label`) ;
- `local: true` pour un projet non publié en ligne (badge « Projet local »).

Les captures vont dans `app/static/images/projects/`. Un projet sans image reçoit automatiquement une affiche (icône, chiffres, technologies).

Les projets mis en avant sur l'accueil sont listés dans `FEATURED_ON_HOME` ([app/routes/main.py](app/routes/main.py)). Tous les compteurs du site (nombre de projets, en production, locaux) sont calculés depuis ce fichier.

### Galerie — `data/gallery.json`

Un événement = un `id`, un `title`, une `category`, une `date`, un `location`, une `description` et, en option, un `cover`. Les photos sont **détectées automatiquement** dans `app/static/images/gallery/<id>/` (jpg, png, webp, avif, gif), triées par nom. Les photos s'affichent par lots de 24, avec chargement différé.

> Conseil : redimensionner les photos à ~1600 px de large avant de les déposer.

## Structure

```
app/
  __init__.py          application factory (charge .env)
  config.py            configuration
  routes/
    main.py            accueil, skills, expérience, témoignages, galerie
    projects.py        page Work
    contact.py         formulaire + envoi SMTP
  templates/           pages Jinja2 (base.html, home.html, gallery*.html, …)
  static/
    css/ js/           styles et scripts (gallery.js, main.js, …)
    images/            images, dont projects/ et gallery/
data/
  projects.json        les projets
  gallery.json         les événements de la galerie
run.py                 point d'entrée (port 5001)
```

## Notes

- Le CV est servi depuis `app/static/documents/CV_Stephane_Zoa.pdf` : ajouter ce fichier pour activer les boutons de téléchargement.
- Les animations respectent `prefers-reduced-motion` sur la page Expérience.
- Les captures de projets sont des captures d'écran des sites en ligne ; les projets locaux n'exposent que leur description, jamais de code ni d'identifiants.
