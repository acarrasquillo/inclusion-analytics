import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('genre', __name__, url_prefix='/genre')

@bp.route('/add', methods=('GET','POST'))
def add():
	db = get_db()
	error = None
	rows = list()
	if request.method == 'POST':
		# if user submits form validate input
		genre_name = request.form['name']
		# get the db connection
		if not genre_name:
			# if genre name is empty set error message
			error = 'genre name required.'
		elif db.execute(
				'SELECT id FROM program_genre WHERE name = ?', (genre_name,)
		).fetchone() is not None:
			# if genre already exist set error message
			error = 'Genre {} already exist.'.format(genre_name)

		if error is None:
			# if there are no errors insert the program genre into the db
			db.execute(
				'INSERT INTO program_genre (name) VALUES (?)', (genre_name,)
			)
			db.commit()
			return redirect(url_for('genre.add'))

		flash(error)
	elif request.method == 'GET':
		rows = db.execute(
		        'SELECT *'
		        ' FROM program_genre'
    		).fetchall()


	return render_template('genre/add.html.j2',rows=rows)