import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('program', __name__, url_prefix='/program')

@bp.route('/add', methods=('GET','POST'))
def add():
	if request.method == 'POST':
		# if user submits form validate input
		title = request.form['title']
		# get the db connection
		db = get_db()
		error = None

		if not title:
			# if title is empty set error message
			error = 'Program title required.'
		elif db.execute(
				'SELECT id FROM program WHERE title = ?', (title,)
		).fetchone() is not None:
			# if title already exist set error message
			error = 'Program {} already exist.'.format(title)

		if error is None:
			# if there are no errors insert the program into the db
			db.execute(
				'INSERT INTO program (title) VALUES (?)', (title,)
			)
			db.commit()
			return redirect(url_for('program.add'))

		flash(error)

	return render_template('program/add.html.j2')