import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
    )

from analytics_app.db import get_db

bp =  Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/', methods=(['GET']))
def view():

    db = get_db()
    rows = db.execute(
        'SELECT p.title as title, g.name as genre, n.name as network, t.name as hometown, viewers_number'
        ' FROM viewers v JOIN program p ON v.title_id = p.id'
        ' JOIN program_genre g ON v.genre_id = g.id'
        ' JOIN program_network n ON v.network_id = n.id'
        ' JOIN town t ON v.hometown_id = t.id'
    ).fetchall()

    return render_template('dashboard/view.html.j2', rows=rows)