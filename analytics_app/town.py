import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('town', __name__, url_prefix='/town')

@bp.route('/add', methods=('GET','POST'))
def add():
	if request.method == 'POST':
		# if user submits form validate input
		town_name = request.form['name']
		# get the db connection
		db = get_db()
		error = None

		if not town_name:
			# if town name is empty set error message
			error = 'Town name required.'
		elif db.execute(
				'SELECT id FROM town WHERE name = ?', (town_name,)
		).fetchone() is not None:
			# if title already exist set error message
			error = 'Town {} already exist.'.format(town_name)

		if error is None:
			# if there are no errors insert the twon into the db
			db.execute(
				'INSERT INTO town (name) VALUES (?)', (town_name,)
			)
			db.commit()
			return redirect(url_for('town.add'))

		flash(error)

	return render_template('town/add.html.j2')