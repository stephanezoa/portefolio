from flask import Blueprint, render_template

bp = Blueprint('projects', __name__)

@bp.route('/projects')
def projects():
    """Page des projets"""
    projects_data = [
        {
            'id': 1,
            'title': 'On-Demand Rides Made Simple',
            'subtitle': 'Ryde App',
            'description': 'A powerful, user-friendly app called Ryde built with React Native, Expo, & TailwindCSS for a fast, seamless ride-booking experience.',
            'long_description': 'Ryde is a comprehensive ride-sharing application that connects passengers with drivers in real-time. The app features GPS tracking, secure payments, ride history, and ratings system.',
            'image': 'ryde-app.png',
            'fallback': 'https://images.unsplash.com/photo-1555421689-d68471e189f2?w=800&h=600&fit=crop',
            'technologies': ['React Native', 'Expo', 'TailwindCSS', 'Firebase', 'Google Maps API'],
            'category': 'Mobile App',
            'github': 'https://github.com/yourusername/ryde-app',
            'demo': 'https://ryde-demo.com',
            'featured': True,
            'color': 'cyan'
        },
        {
            'id': 2,
            'title': 'The Library Management Platform',
            'subtitle': 'BookHub',
            'description': 'A modern platform to manage and discover books with intuitive UI and powerful search capabilities.',
            'long_description': 'BookHub is a comprehensive library management system that allows users to browse, borrow, and manage their reading lists. Features include advanced search, recommendations, and admin dashboard.',
            'image': 'library-platform.png',
            'fallback': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=600&fit=crop',
            'technologies': ['React', 'Node.js', 'MongoDB', 'Express', 'Redux'],
            'category': 'Web App',
            'github': 'https://github.com/yourusername/bookhub',
            'demo': 'https://bookhub-demo.com',
            'featured': True,
            'color': 'green'
        },
        {
            'id': 3,
            'title': 'YC Directory - A Startup Showcase App',
            'subtitle': 'Startup Connect',
            'description': 'Pitch your startup and connect with entrepreneurs in an innovative platform designed for the startup ecosystem.',
            'long_description': 'YC Directory is a platform where startups can showcase their products, connect with investors, and find co-founders. Features include pitch deck uploads, networking tools, and funding tracking.',
            'image': 'yc-directory.png',
            'fallback': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
            'technologies': ['Next.js', 'GraphQL', 'Firebase', 'Stripe', 'Vercel'],
            'category': 'Web App',
            'github': 'https://github.com/yourusername/yc-directory',
            'demo': 'https://yc-directory-demo.com',
            'featured': True,
            'color': 'purple'
        },
        {
            'id': 4,
            'title': 'E-Commerce Dashboard',
            'subtitle': 'ShopAdmin',
            'description': 'A comprehensive admin dashboard for managing e-commerce operations with real-time analytics.',
            'long_description': 'ShopAdmin provides store owners with powerful tools to manage products, orders, customers, and analytics. Features include inventory management, sales reports, and customer insights.',
            'image': 'ecommerce-dashboard.png',
            'fallback': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
            'technologies': ['Vue.js', 'Laravel', 'MySQL', 'Chart.js', 'Tailwind'],
            'category': 'Web App',
            'github': 'https://github.com/yourusername/shopadmin',
            'demo': 'https://shopadmin-demo.com',
            'featured': False,
            'color': 'orange'
        },
        {
            'id': 5,
            'title': 'Social Media Analytics Tool',
            'subtitle': 'SocialInsights',
            'description': 'Track and analyze your social media performance across multiple platforms in one dashboard.',
            'long_description': 'SocialInsights aggregates data from various social media platforms to provide comprehensive analytics, engagement metrics, and audience insights.',
            'image': 'social-analytics.png',
            'fallback': 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800&h=600&fit=crop',
            'technologies': ['React', 'Python', 'FastAPI', 'PostgreSQL', 'Docker'],
            'category': 'Analytics',
            'github': 'https://github.com/yourusername/socialinsights',
            'demo': 'https://socialinsights-demo.com',
            'featured': False,
            'color': 'pink'
        },
        {
            'id': 6,
            'title': 'Task Management System',
            'subtitle': 'TaskFlow',
            'description': 'Streamline your team\'s workflow with this intuitive task management and collaboration tool.',
            'long_description': 'TaskFlow helps teams organize projects, assign tasks, track progress, and collaborate effectively with features like kanban boards, time tracking, and team chat.',
            'image': 'task-management.png',
            'fallback': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=600&fit=crop',
            'technologies': ['Angular', 'Node.js', 'Socket.io', 'MongoDB', 'Redis'],
            'category': 'Productivity',
            'github': 'https://github.com/yourusername/taskflow',
            'demo': 'https://taskflow-demo.com',
            'featured': False,
            'color': 'blue'
        },
        {
            'id': 7,
            'title': 'Weather Forecast App',
            'subtitle': 'WeatherWise',
            'description': 'Get accurate weather forecasts with beautiful visualizations and location-based alerts.',
            'long_description': 'WeatherWise provides detailed weather information including hourly forecasts, 7-day outlook, radar maps, and severe weather alerts.',
            'image': 'weather-app.png',
            'fallback': 'https://images.unsplash.com/photo-1592210454359-9043f067919b?w=800&h=600&fit=crop',
            'technologies': ['React Native', 'TypeScript', 'OpenWeather API', 'Maps'],
            'category': 'Mobile App',
            'github': 'https://github.com/yourusername/weatherwise',
            'demo': 'https://weatherwise-demo.com',
            'featured': False,
            'color': 'cyan'
        },
        {
            'id': 8,
            'title': 'Fitness Tracker',
            'subtitle': 'FitTrack',
            'description': 'Monitor your workouts, track progress, and achieve your fitness goals with personalized plans.',
            'long_description': 'FitTrack helps users log workouts, track calories, monitor progress with charts, and get personalized workout recommendations based on their goals.',
            'image': 'fitness-tracker.png',
            'fallback': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&h=600&fit=crop',
            'technologies': ['Flutter', 'Dart', 'Firebase', 'HealthKit', 'ML Kit'],
            'category': 'Mobile App',
            'github': 'https://github.com/yourusername/fittrack',
            'demo': 'https://fittrack-demo.com',
            'featured': False,
            'color': 'green'
        },
        {
            'id': 9,
            'title': 'Recipe Sharing Platform',
            'subtitle': 'CookBook',
            'description': 'Discover, share, and save your favorite recipes in a beautiful, social cooking platform.',
            'long_description': 'CookBook allows users to share recipes, follow other cooks, create meal plans, and generate shopping lists automatically from recipes.',
            'image': 'recipe-platform.png',
            'fallback': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800&h=600&fit=crop',
            'technologies': ['React', 'Django', 'PostgreSQL', 'AWS S3', 'Elasticsearch'],
            'category': 'Web App',
            'github': 'https://github.com/yourusername/cookbook',
            'demo': 'https://cookbook-demo.com',
            'featured': False,
            'color': 'red'
        }
    ]
    
    # Filtrer les projets en vedette
    featured_projects = [p for p in projects_data if p.get('featured', False)]
    
    # Catégories disponibles
    categories = list(set([p['category'] for p in projects_data]))
    
    return render_template('projects.html', 
                         projects=projects_data,
                         featured_projects=featured_projects,
                         categories=categories)

@bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """Page de détail d'un projet"""
    return render_template('project_detail.html', project_id=project_id)