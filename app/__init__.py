from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enregistrer les blueprints
    from app.routes import main, projects, contact  #blog
    
    app.register_blueprint(main.bp, url_prefix='/')
    app.register_blueprint(projects.bp, url_prefix='/projects')
    app.register_blueprint(contact.bp, url_prefix='/contact')
    #app.register_blueprint(blog.bp, url_prefix='/blog')
    
    return app