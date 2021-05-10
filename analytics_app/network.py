import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('network', __name__, url_prefix='/network')

@bp.route('/add', methods=('GET','POST'))
def add():
	db = get_db()
	error = None
	rows = list()
	if request.method == 'POST':
		# if user submits form validate input
		network_name = request.form['name']
		# get the db connection
		db = get_db()
		error = None

		if not network_name:
			# if network name is empty set error message
			error = 'network name required.'
		elif db.execute(
				'SELECT id FROM program_network WHERE name = ?', (network_name,)
		).fetchone() is not None:
			# if title already exist set error message
			error = 'Network {} already exist.'.format(network_name)

		if error is None:
			# if there are no errors insert the program network into the db
			db.execute(
				'INSERT INTO program_network (name) VALUES (?)', (network_name,)
			)
			db.commit()
			return redirect(url_for('network.add'))

		flash(error)
	elif request.method == 'GET':
		rows = db.execute(
		        'SELECT *'
		        ' FROM program_network'
    		).fetchall()


	return render_template('network/add.html.j2', rows=rows)