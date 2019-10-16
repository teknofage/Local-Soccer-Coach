from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Local Soccer Coach')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
coaches = db.coaches
resumes = db.resumes
qualifications = db.qualifications
reviews = db.reviews
fields = db.fields
leagues = db.leagues


app = Flask(__name__)


@app.route('/')
def coaches_index():
    """Show all coaches."""
    return render_template('coaches_index.html', coaches=coaches.find())


@app.route('/coaches', methods=['POST'])
def coaches_submit():
    """Submit a new coach."""
    coach = {
        'name': request.form.get('name'),
        'resume': request.form.get('resume'),
        'qualifications': request.form.get('qualifications').split(),
        'reviews': request.form.get('reviews')
    }
    coach_id = coaches.insert_one(coach).inserted_id
    return redirect(url_for('coaches_show', coach_id=coach_id))


@app.route('/coaches/new')
def coaches_new():
    """Create a new coach."""
    return render_template('coaches_new.html', coach={}, title='New Coach')


@app.route('/coaches/<coach_id>')
def coaches_show(coach_id):
    """Show a single coach."""
    coach = coaches.find_one({'_id': ObjectId(coach_id)})
    coach_comments = comments.find({'coach_id': ObjectId(coach_id)})
    return render_template('coaches_show.html', coach=coach, comments=coach_comments)


@app.route('/coaches/<coach_id>/edit')
def coaches_edit(coach_id):
    """Show the edit form for a coach."""
    coach = coaches.find_one({'_id': ObjectId(coach_id)})
    return render_template('coaches_edit.html', coach=coach, title='Edit coach')


@app.route('/coaches/<coach_id>', methods=['POST'])
def coaches_update(coach_id):
    """Submit an edited coach."""
    updated_coach = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    coaches.update_one(
        {'_id': ObjectId(coach_id)},
        {'$set': updated_coach})
    return redirect(url_for('coaches_show', coach_id=coach_id))


@app.route('/coaches/<coach_id>/delete', methods=['POST'])
def coaches_delete(coach_id):
    """Delete one coach."""
    coaches.delete_one({'_id': ObjectId(coach_id)})
    return redirect(url_for('coaches_index'))


@app.route('/coaches/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'coach_id': ObjectId(request.form.get('coach_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('coaches_show', coach_id=request.form.get('coach_id')))


@app.route('/coaches/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('coaches_show', coach_id=comment.get('coach_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))