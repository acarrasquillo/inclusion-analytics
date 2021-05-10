import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('views', __name__, url_prefix='/views')

@bp.route('/add', methods=('GET','POST'))
def add():
	db = get_db()
	error = None
	if request.method == 'POST':
		# if user submits form validate input
		views_count = request.form['count']
		views_hometown_id = request.form['town']
		views_program_id = request.form['program']
		views_program_genre_id = request.form['genre']
		views_program_network_id = request.form['network']
		# get the db connection

		if not (views_count and 
			views_hometown_id and views_program_id and 
			views_program_genre_id and views_program_network_id):
			# if required values are empty set error message
			error = 'Viewers count, viewers hometown, program title, program genre and program network are required.'
		elif db.execute(
				'SELECT id FROM viewers WHERE viewers_number = ? AND title_id = ? AND network_id = ? AND hometown_id = ? AND genre_id = ?', 
				(views_count,views_program_id,views_program_network_id,views_hometown_id,views_program_genre_id)
		).fetchone() is not None:
			# if title already exist set error message
			error = 'Views with the same values already exist'

		if error is None:
			# if there are no errors insert the program genre into the db
			db.execute(
				'INSERT INTO viewers (viewers_number,title_id,network_id,hometown_id,genre_id) VALUES (?,?,?,?,?)', 
				(views_count,views_program_id,views_program_network_id,views_hometown_id,views_program_genre_id)
			)
			db.commit()
			return redirect(url_for('views.add'))

		flash(error)
	if request.method == 'GET':
		rows = db.execute(
		        'SELECT *'
		        ' FROM viewers'
    		).fetchall()

	return render_template('views/add.html.j2', rows=rows)