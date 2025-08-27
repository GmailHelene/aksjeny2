from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import app, db
from ..models import ForumTopic

@app.route('/forum/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            category = request.form.get('category')
            
            if not all([title, content, category]):
                flash('Alle felt må fylles ut', 'error')
                return render_template('forum/create_topic.html')
            
            topic = ForumTopic(
                title=title,
                content=content,
                category=category,
                user_id=current_user.id
            )
            db.session.add(topic)
            db.session.commit()
            flash('Innlegg opprettet!', 'success')
            return redirect(url_for('forum.view_topic', topic_id=topic.id))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Create topic error: {str(e)}")
            flash('Det oppstod en feil ved opprettelse av innlegg. Prøv igjen.', 'error')
    
    return render_template('forum/create_topic.html')