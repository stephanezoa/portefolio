import json
import os

from flask import Blueprint, render_template, current_app

bp = Blueprint('projects', __name__)

@bp.route('/projects')
def projects():
    """Page des projets (data/projects.json)"""
    with open(os.path.join(current_app.config['DATA_DIR'], 'projects.json'), encoding='utf-8') as f:
        projects_data = json.load(f)

    featured_projects = [p for p in projects_data if p.get('featured', False)]
    categories = sorted({p['category'] for p in projects_data})

    return render_template('projects.html',
                           projects=projects_data,
                           featured_projects=featured_projects,
                           categories=categories)


@bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """Page de détail d'un projet"""
    return render_template('project_detail.html', project_id=project_id)