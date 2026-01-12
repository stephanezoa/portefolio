import os
import markdown
from datetime import datetime

def load_blog_posts():
    """Charge tous les articles de blog depuis le dossier data/blog"""
    blog_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'blog')
    posts = []
    
    if not os.path.exists(blog_dir):
        return posts
    
    for filename in os.listdir(blog_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parser le front matter (simplifié)
                lines = content.split('\n')
                metadata = {}
                content_start = 0
                
                if lines[0].strip() == '---':
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            content_start = i + 1
                            break
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                
                # Convertir le markdown en HTML
                html_content = markdown.markdown('\n'.join(lines[content_start:]))
                
                slug = filename.replace('.md', '')
                posts.append({
                    'slug': slug,
                    'title': metadata.get('title', slug),
                    'date': metadata.get('date', '2024-01-01'),
                    'author': metadata.get('author', 'Djembar Arafat'),
                    'description': metadata.get('description', ''),
                    'tags': metadata.get('tags', '').split(','),
                    'content': html_content
                })
    
    # Trier par date (plus récent d'abord)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def get_post_by_slug(slug):
    """Récupère un article spécifique par son slug"""
    posts = load_blog_posts()
    for post in posts:
        if post['slug'] == slug:
            return post
    return None