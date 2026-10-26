import json
import os
from datetime import datetime

from flask import Blueprint, render_template, current_app, abort

bp = Blueprint('main', __name__)

FEATURED_ON_HOME = ['Père Nkap', 'Mboa News', 'TOURISM237', 'HR-Skills Pay']


def _load_projects():
    with open(os.path.join(current_app.config['DATA_DIR'], 'projects.json'), encoding='utf-8') as f:
        return json.load(f)


@bp.route('/')
def home():
    """Page d'accueil"""
    projects = _load_projects()
    by_title = {p['title']: p for p in projects}
    featured = [by_title[t] for t in FEATURED_ON_HOME if t in by_title]

    # Vitrine du hero : vedettes d'abord, puis les autres projets avec capture, puis les projets locaux
    rest = [p for p in projects if p['title'] not in FEATURED_ON_HOME]
    showcase = featured + [p for p in rest if p['image']] + [p for p in rest if not p['image']]
    return render_template('home.html', featured_projects=featured, showcase_projects=showcase,
                           total_projects=len(projects))


@bp.route('/skills')
def skills():
    """Page des compétences"""
    skills_data = [
        {
            'name': 'React Developer',
            'icon': 'fa-react',
            'color': 'cyan',
            'description': 'Expert in building modern React applications'
        },
        {
            'name': 'Mobile App Developer',
            'icon': 'fa-mobile-alt',
            'color': 'blue',
            'description': 'Creating cross-platform mobile experiences'
        },
        {
            'name': 'Backend Developer',
            'icon': 'fa-server',
            'color': 'green',
            'description': 'Building scalable server-side solutions'
        },
        {
            'name': 'Interactive Developer',
            'icon': 'fa-cube',
            'color': 'purple',
            'description': 'Crafting engaging user interactions'
        },
        {
            'name': 'Project Manager',
            'icon': 'fa-project-diagram',
            'color': 'red',
            'description': 'Leading teams to successful delivery'
        }
    ]
    return render_template('skills.html', skills=skills_data)

@bp.route('/experience')
def experience():
    """Page d'expérience professionnelle"""
    experiences = [
        {
            'title': 'Frontend Developer',
            'company': 'Hostinger',
            'period': 'January 2023 – Present',
            'description': 'Developed and maintained user-facing features for the Hostinger websites.',
            'responsibilities': [
                'Collaborated closely with UX/UI designers to ensure seamless user experiences',
                'Optimized web applications for maximum speed and scalability',
                'Implemented responsive designs and cross-browser compatibility'
            ],
            'technologies': ['React', 'TypeScript', 'Next.js', 'TailwindCSS'],
            'icon': 'fa-code',
            'color': 'cyan'
        },
        {
            'title': 'Full Stack Developer',
            'company': 'Appwrite',
            'period': 'June 2020 – December 2023',
            'description': 'Led the development of Docker\'s web applications with a focus on scalability.',
            'responsibilities': [
                'Architected and implemented scalable microservices architecture',
                'Worked with backend engineers to integrate APIs seamlessly',
                'Contributed to open-source projects'
            ],
            'technologies': ['React', 'Node.js', 'Docker', 'MongoDB', 'Redis'],
            'icon': 'fa-server',
            'color': 'purple'
        },
        {
            'title': 'React Native Developer',
            'company': 'Docker',
            'period': 'March 2019 – May 2020',
            'description': 'Built cross-platform mobile applications with React Native.',
            'responsibilities': [
                'Built cross-platform mobile apps using React Native',
                'Improved app performance through code optimization',
                'Coordinated with product team for feature implementation'
            ],
            'technologies': ['React Native', 'Expo', 'JavaScript', 'Firebase'],
            'icon': 'fa-react',
            'color': 'blue'
        }
    ]
    return render_template('experience.html', experiences=experiences, total_projects=len(_load_projects()),
                           years_active=datetime.now().year - 2019)

@bp.route('/testimonials')
def testimonials():
    """Page des témoignages"""
    testimonials_data = [
        {
            'name': 'Esther Howard',
            'role': 'CEO, TechStart',
            'avatar': 'EH',
            'rating': 5,
            'text': 'I can\'t say enough good things about Adrian. He was able to take our complex project requirements and turn them into a beautiful website.',
            'company': 'appwrite'
        },
        {
            'name': 'Guy Hawkins',
            'role': 'CTO, InnovateCo',
            'avatar': 'GH',
            'rating': 5,
            'text': 'Collaborating with Adrian was an absolute pleasure. His professionalism, promptness, and dedication to delivering exceptional results were evident throughout our project.',
            'company': 'hostinger'
        },
        {
            'name': 'Wade Warren',
            'role': 'Product Manager',
            'avatar': 'WW',
            'rating': 5,
            'text': 'Working with Adrian was a fantastic experience. He transformed our outdated website into a modern, user-friendly platform.',
            'company': 'docker'
        },
        {
            'name': 'Floyd Miles',
            'role': 'Senior Developer',
            'avatar': 'FM',
            'rating': 5,
            'text': 'Adrian\'s expertise in web development is truly impressive. He delivered a robust and scalable solution that perfectly met our needs.',
            'company': 'appwrite'
        },
        {
            'name': 'Marvin McKinney',
            'role': 'Startup Founder',
            'avatar': 'MM',
            'rating': 5,
            'text': 'Adrian is a pleasure to work with. He turned our outdated website into a fresh, intuitive platform.',
            'company': 'docker'
        },
        {
            'name': 'Albert Flores',
            'role': 'Lead Designer',
            'avatar': 'AF',
            'rating': 5,
            'text': 'Adrian is great to work with. He understood our requirements perfectly and delivered a website that exceeded our expectations.',
            'company': 'hostinger'
        }
    ]
    return render_template('testimonials.html', testimonials=testimonials_data)

IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')


def _load_events():
    """Charge data/gallery.json. Les photos sont détectées automatiquement dans
    static/images/gallery/<id>/ ; une liste 'photos' dans le JSON n'est plus nécessaire."""
    path = os.path.join(current_app.config['DATA_DIR'], 'gallery.json')
    with open(path, encoding='utf-8') as f:
        events = json.load(f)

    root = os.path.join(current_app.static_folder, 'images', 'gallery')
    for event in events:
        event['date_obj'] = datetime.strptime(event['date'], '%Y-%m-%d')
        folder = os.path.join(root, event['id'])
        names = sorted(n for n in os.listdir(folder) if n.lower().endswith(IMAGE_EXTS)) if os.path.isdir(folder) else []
        event['photos'] = [f"{event['id']}/{n}" for n in names]
        cover = event.get('cover')
        event['cover_photo'] = f"{event['id']}/{cover}" if cover in names else (event['photos'][0] if names else None)
    events.sort(key=lambda e: e['date_obj'], reverse=True)
    return events


@bp.route('/gallery')
def gallery():
    """Photothèque : liste des événements (une carte par événement)"""
    events = _load_events()
    return render_template(
        'gallery.html',
        events=events,
        categories=sorted({e['category'] for e in events}),
        years=sorted({e['date_obj'].year for e in events}, reverse=True),
        total_photos=sum(len(e['photos']) for e in events),
    )


@bp.route('/gallery/<event_id>')
def gallery_event(event_id):
    """Détail d'un événement : toutes ses photos"""
    events = _load_events()
    pos = next((i for i, e in enumerate(events) if e['id'] == event_id), None)
    if pos is None:
        abort(404)
    return render_template(
        'gallery_event.html',
        event=events[pos],
        newer=events[pos - 1] if pos > 0 else None,
        older=events[pos + 1] if pos < len(events) - 1 else None,
    )
