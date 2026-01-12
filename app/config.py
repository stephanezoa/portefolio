import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'
    TEMPLATES_AUTO_RELOAD = True
    
    # Dossiers
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    BLOG_DIR = os.path.join(DATA_DIR, 'blog')