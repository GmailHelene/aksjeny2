"""Investment guides routes"""
from flask import Blueprint, render_template, redirect, url_for
from ..utils.access_control import demo_access

investment_guides = Blueprint('investment_guides', __name__)

@investment_guides.route('/')
@investment_guides.route('/index')
@demo_access
def index():
    """Investment guides index page"""
    guides = [
        {
            'title': 'Teknisk Analyse for Nybegynnere',
            'description': 'Lær grunnleggende teknisk analyse og chart-mønstre',
            'category': 'technical',
            'difficulty': 'Beginner',
            'time_to_read': '15 min',
            'slug': 'teknisk-analyse-guide'
        },
        {
            'title': 'Fundamental Analyse',
            'description': 'Forstå selskapers finansielle data og verdsettelse',
            'category': 'fundamental', 
            'difficulty': 'Intermediate',
            'time_to_read': '25 min',
            'slug': 'fundamental-analyse-guide'
        },
        {
            'title': 'Warren Buffett Investeringsstrategi',
            'description': 'Lær fra verdens mest suksessfulle investor',
            'category': 'strategy',
            'difficulty': 'Advanced',
            'time_to_read': '30 min', 
            'slug': 'warren-buffett-strategi'
        },
        {
            'title': 'Risikohåndtering',
            'description': 'Hvordan minimere risiko og beskytte kapitalen din',
            'category': 'risk',
            'difficulty': 'Intermediate',
            'time_to_read': '20 min',
            'slug': 'risikohåndtering-guide'
        }
    ]
    
    return render_template('investment_guides/index.html',
                         guides=guides,
                         title='Investeringsguider')

@investment_guides.route('/<slug>')
@demo_access  
def guide_detail(slug):
    """Investment guide detail page"""
    # Map slugs to guide details
    guides_data = {
        'teknisk-analyse-guide': {
            'title': 'Teknisk Analyse for Nybegynnere',
            'content': 'Dette er en omfattende guide til teknisk analyse...',
            'category': 'technical'
        },
        'fundamental-analyse-guide': {
            'title': 'Fundamental Analyse',
            'content': 'Lær å analysere selskapers finansielle data...',
            'category': 'fundamental'
        },
        'warren-buffett-strategi': {
            'title': 'Warren Buffett Investeringsstrategi', 
            'content': 'Warren Buffetts viktigste investeringsprinsipper...',
            'category': 'strategy'
        },
        'risikohåndtering-guide': {
            'title': 'Risikohåndtering',
            'content': 'Viktige prinsipper for risikohåndtering...',
            'category': 'risk'
        }
    }
    
    guide = guides_data.get(slug)
    if not guide:
        return redirect(url_for('investment_guides.index'))
        
    return render_template('investment_guides/guide.html',
                         guide=guide,
                         slug=slug,
                         title=guide['title'])
