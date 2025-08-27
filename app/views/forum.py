from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from app.models import ForumTopic, ForumPost

@app.route('/forum/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            category_id = request.form.get('category')
            
            if not all([title, content, category_id]):
                flash('Alle felt må fylles ut', 'error')
                return render_template('forum/create_topic.html')
            
            # Generate slug from title
            import re
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
            topic = ForumTopic(
                title=title,
                slug=slug,
                content=content,
                category_id=category_id,
                author_id=current_user.id
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