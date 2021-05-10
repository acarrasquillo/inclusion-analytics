import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
    )

from analytics_app.db import get_db

bp =  Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/', methods=(['GET','POST']))
def view():
    db = get_db()
    rows = list()
    genre_id=None
    town_id_list=None
    filter_count_sum=None
    form_towns=list()
    # return the genre and towns to allow the data to be filtered by selecting them on a form.
    genres=db.execute(
                'SELECT *'
                ' FROM program_genre'
        ).fetchall()

    towns=db.execute(
                'SELECT *'
                ' FROM town'
        ).fetchall()

    if request.method == 'GET':
        # display all the data on the viewers table
        rows = db.execute(
            'SELECT p.title as "Program Title", g.name as "Program Genre", n.name as "Program Network", t.name as "Viewer Hometown", "viewers_number" as "Number of Viewers"'
            ' FROM viewers v JOIN program p ON v.title_id = p.id'
            ' JOIN program_genre g ON v.genre_id = g.id'
            ' JOIN program_network n ON v.network_id = n.id'
            ' JOIN town t ON v.hometown_id = t.id'
        ).fetchall()

    if request.method == 'POST':
        # filter the data by genre and selected towns
        # extract the genre and towns the user want to filter by
        if "genre" in request.form:
            genre_id = request.form['genre']

        form_towns = [v for k,v in request.form.items() if k.startswith("town")]
        # construct the db query section for the respective filters
        if len(form_towns) > 0:
            town_id_list='('
            for form_town in form_towns:
                # if not the last element in the list add a comma
                print(form_town)
                if form_town != form_towns[-1]:
                    town_id_list+=f'{form_town},'
                else:
                    town_id_list+=f'{form_town}'

            town_id_list+=')'

        if ((genre_id is not None) and (town_id_list is not None)):
            rows = db.execute(
                'SELECT p.title as "Program Title", g.name as "Program Genre", n.name as "Program Network", t.name as "Viewer Hometown", "viewers_number" as "Number of Viewers"'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.genre_id = {genre_id} AND v.hometown_id IN {town_id_list}'
            ).fetchall()
            filter_count_sum = db.execute(
                'SELECT sum(viewers_number) as total_viewers'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.genre_id = {genre_id} AND v.hometown_id IN {town_id_list}'
            ).fetchone()
        elif genre_id is not None:
            rows = db.execute(
                'SELECT p.title as "Program Title", g.name as "Program Genre", n.name as "Program Network", t.name as "Viewer Hometown", "viewers_number" as "Number of Viewers"'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.genre_id = {genre_id}'
            ).fetchall()
            filter_count_sum = db.execute(
                'SELECT sum(viewers_number) as total_viewers'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.genre_id = {genre_id}'
            ).fetchone()
        elif town_id_list is not None:
            rows = db.execute(
                'SELECT p.title as "Program Title", g.name as "Program Genre", n.name as "Program Network", t.name as "Viewer Hometown", "viewers_number" as "Number of Viewers"'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.hometown_id IN {town_id_list}'
            ).fetchall()
            filter_count_sum = db.execute(
                'SELECT sum(viewers_number) as total_viewers'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
                f' WHERE v.hometown_id IN {town_id_list}'
            ).fetchone()
        else:
            rows = db.execute(
                'SELECT p.title as "Program Title", g.name as "Program Genre", n.name as "Program Network", t.name as "Viewer Hometown", "viewers_number" as "Number of Viewers"'
                ' FROM viewers v JOIN program p ON v.title_id = p.id'
                ' JOIN program_genre g ON v.genre_id = g.id'
                ' JOIN program_network n ON v.network_id = n.id'
                ' JOIN town t ON v.hometown_id = t.id'
            ).fetchall()

    return render_template('dashboard/view.html.j2', rows=rows, genres=genres, towns=towns,filtered_genre=genre_id,filtered_towns=form_towns,filter_count_sum=filter_count_sum)