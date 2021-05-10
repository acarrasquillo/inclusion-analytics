import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

from analytics_app.db import get_db

bp =  Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/', methods=(['GET']))
def view():

	db = get_db()
    views = db.execute(
        'SELECT v.id, p.name, g.name, n.name, t.name,viewers_number'
        ' FROM views v JOIN program p ON v.title_id = p.id' 
        ' JOIN program_genre g ON v.genre_id = g.id'
        ' JOIN program_netwok n ON v.network_id = n.id'
        ' JOIN town t ON v.hometown_id = t.id'
        ' ORDER BY created DESC'
    ).fetchall()

	return render_template('dashboard/view.html.j2')