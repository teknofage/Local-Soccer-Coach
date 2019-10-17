from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Local-Soccer-Coach')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
coaches = db.coaches
resumes = db.resumes
qualifications = db.qualifications
reviews = db.reviews
fields = db.fields
leagues = db.leagues


app = Flask(__name__)

#Coaches
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


@app.route('/coaches/')
def coaches_show():
    """Show a single coach."""
    allCoaches = coaches.find()
    print('********************')
    print(coaches)
    # coach_reviews = reviews.find({'coach_id': ObjectId(coach_id)})
    return render_template('coaches_show.html', allCoaches=allCoaches)







@app.route('/coach/<coach_id>')
def coach_show(coach_id):
    """Show a single coach."""
    coach = coaches.find_one({'_id': ObjectId(coach_id)})
    coach_reviews = reviews.find({'coach_id': ObjectId(coach_id)})
    return render_template('coach_show.html', coach=coach, reviews=coach_reviews)






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


@app.route('/coaches/reviews', methods=['POST'])
def coach_reviews_new():
    """Submit a new review."""
    review = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'coach_id': ObjectId(request.form.get('coach_id'))
    }
    print(review)
    review_id = reviews.insert_one(review).inserted_id
    return redirect(url_for('coaches_show', coach_id=request.form.get('coach_id')))


@app.route('/coaches/reviews/<review_id>', methods=['POST'])
def coach_reviews_delete(review_id):
    """Action to delete a review."""
    review = reviews.find_one({'_id': ObjectId(review_id)})
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('coaches_show', coach_id=review.get('coach_id')))

#Leagues

@app.route('/')
def leagues_index():
    """Show all leagues."""
    return render_template('leagues_index.html', leagues=leagues.find())


@app.route('/leagues', methods=['POST'])
def leagues_submit():
    """Submit a new league."""
    league = {
        'name': request.form.get('name'),
        'age_group': request.form.get('age_group'),
        'level': request.form.get('level').split(),
        'website': request.form.get('website').split(),
        'reviews': request.form.get('reviews')
    }
    league_id = leagues.insert_one(league).inserted_id
    return redirect(url_for('leagues_show', league_id=league_id))


@app.route('/leagues/new')
def leagues_new():
    """Create a new league."""
    return render_template('leagues_new.html', league={}, title='New league')


@app.route('/leagues/<league_id>')
def leagues_show(league_id):
    """Show a single league."""
    league = leagues.find_one({'_id': ObjectId(league_id)})
    league_reviews = reviews.find({'league_id': ObjectId(league_id)})
    return render_template('leagues_show.html', league=league, reviews=league_reviews)


@app.route('/leagues/<league_id>/edit')
def leagues_edit(league_id):
    """Show the edit form for a league."""
    league = leagues.find_one({'_id': ObjectId(league_id)})
    return render_template('leagues_edit.html', league=league, title='Edit league')


@app.route('/leagues/<league_id>', methods=['POST'])
def leagues_update(league_id):
    """Submit an edited league."""
    updated_league = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    leagues.update_one(
        {'_id': ObjectId(league_id)},
        {'$set': updated_league})
    return redirect(url_for('leagues_show', league_id=league_id))


@app.route('/leagues/<league_id>/delete', methods=['POST'])
def leagues_delete(league_id):
    """Delete one league."""
    leagues.delete_one({'_id': ObjectId(league_id)})
    return redirect(url_for('leagues_index'))


@app.route('/leagues/reviews', methods=['POST'])
def league_reviews_new():
    """Submit a new review."""
    review = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'league_id': ObjectId(request.form.get('league_id'))
    }
    print(review)
    review_id = reviews.insert_one(review).inserted_id
    return redirect(url_for('leagues_show', league_id=request.form.get('league_id')))


@app.route('/leagues/reviews/<review_id>', methods=['POST'])
def league_reviews_delete(review_id):
    """Action to delete a review."""
    review = reviews.find_one({'_id': ObjectId(review_id)})
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('leagues_show', league_id=review.get('league_id')))

#Fields

@app.route('/')
def fields_index():
    """Show all fields."""
    return render_template('fields_index.html', fields=fields.find())


@app.route('/fields', methods=['POST'])
def fields_submit():
    """Submit a new field."""
    field = {
        'name': request.form.get('name'),
        'number_of_pitches': request.form.get('number_of_pitches'),
        'turf': request.form.get('turf').split(),
        'location': request.form.get('location').split(),
        'reviews': request.form.get('reviews')
    }
    field_id = fields.insert_one(field).inserted_id
    return redirect(url_for('fields_show', field_id=field_id))


@app.route('/fields/new')
def fields_new():
    """Create a new field."""
    return render_template('fields_new.html', field={}, title='New field')


@app.route('/fields/<field_id>')
def fields_show(field_id):
    """Show a single field."""
    field = fields.find_one({'_id': ObjectId(field_id)})
    field_reviews = reviews.find({'field_id': ObjectId(field_id)})
    return render_template('fields_show.html', field=field, reviews=field_reviews)


@app.route('/fields/<field_id>/edit')
def fields_edit(field_id):
    """Show the edit form for a field."""
    field = fields.find_one({'_id': ObjectId(field_id)})
    return render_template('fields_edit.html', field=field, title='Edit field')


@app.route('/fields/<field_id>', methods=['POST'])
def fields_update(field_id):
    """Submit an edited field."""
    updated_field = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    fields.update_one(
        {'_id': ObjectId(field_id)},
        {'$set': updated_field})
    return redirect(url_for('fields_show', field_id=field_id))


@app.route('/fields/<field_id>/delete', methods=['POST'])
def fields_delete(field_id):
    """Delete one field."""
    fields.delete_one({'_id': ObjectId(field_id)})
    return redirect(url_for('fields_index'))


@app.route('/fields/reviews', methods=['POST'])
def field_reviews_new():
    """Submit a new review."""
    review = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'field_id': ObjectId(request.form.get('field_id'))
    }
    print(review)
    review_id = reviews.insert_one(review).inserted_id
    return redirect(url_for('fields_show', field_id=request.form.get('field_id')))


@app.route('/fields/reviews/<review_id>', methods=['POST'])
def field_reviews_delete(review_id):
    """Action to delete a review."""
    review = reviews.find_one({'_id': ObjectId(review_id)})
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('fields_show', field_id=review.get('field_id')))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))