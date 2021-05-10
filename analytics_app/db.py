import sqlite3
import click
import csv
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db

def close_db(e=None):
	db = g.pop('db',None)
	if db is not None:
		db.close()

def insert_csv_row(row):
	'''
	Sample CSV:
	Program Title, Program Genre, Program Network, Viewer Hometown, Number of Viewers
	Steelers Tonight!, Sports, CBS, Pittsburgh, 1000
	'''
	db=get_db()
	# insert each value into its respective database table
	if len(row) == 5:
		# if row matches the columns
		# store the data in variables
		program_title=row[0]
		program_genre=row[1]
		program_network=row[2]
		viewer_town=row[3]
		viewer_count=row[4]
		# initialize the id's we need to store the row into the viewers table
		program_title_id=None
		program_genre_id=None
		program_network_id=None
		viewer_town_id=None


		if not program_title:
			# if title is empty pass
			pass
		else:
			program_title_id=db.execute(
				'SELECT id FROM program WHERE title = ?', (program_title,)
			).fetchone()
			if program_title_id is not None:
				# if title already exist pass
				program_title_id=program_title_id[0]
				pass
			else:
				# title isn't empty and doesn't exist on the DB
				# insert title in the db
				db.execute(
					'INSERT INTO program (title) VALUES (?)', (program_title,)
				)
				db.commit()
				# store the id of the recently created program
				program_title_id=db.execute(
					'SELECT id FROM program WHERE title = ?', (program_title,)
				).fetchone()[0]

		if not program_genre:
			# if genre is empty pass
			pass
		else:
			program_genre_id=db.execute(
					'SELECT id FROM program_genre WHERE name = ?', (program_genre,)
				).fetchone()
			if program_genre_id is not None:
				# genre already exist in the DB pass
				program_genre_id=program_genre_id[0]
				pass
			else:
				# genre doesn't exist on the DB
				# insert genre in the db
				db.execute(
					'INSERT INTO program_genre (name) VALUES (?)', (program_genre,)
				)
				db.commit()
				# store the id of the recently created genre
				program_genre_id=db.execute(
					'SELECT id FROM program_genre WHERE name = ?', (program_genre,)
				).fetchone()[0]

		if not program_network:
			# if network empty pass
			pass
		else:
			program_network_id=db.execute(
				'SELECT id FROM program_network WHERE name = ?', (program_network,)
			).fetchone()

			if program_network_id is not None:
				# program netwok already exist
				program_network_id=program_network_id[0]
				pass
			else:
				# program network doesn't exist on the DB
				db.execute(
					'INSERT INTO program_network (name) VALUES (?)', (program_network,)
				)
				db.commit()
				# store the id of the recently created program network
				program_network_id=db.execute(
					'SELECT id FROM program_network WHERE name = ?', (program_network,)
				).fetchone()[0]

		if not viewer_town:
			# if town is empty
			pass
		else:
			viewer_town_id=db.execute(
				'SELECT id FROM town WHERE name = ?', (viewer_town,)
			).fetchone()
			if viewer_town_id is not None:
				# town exist in the DB
				viewer_town_id=viewer_town_id[0]
				pass
			else:
				# add town to db
				db.execute(
					'INSERT INTO town (name) VALUES (?)', (viewer_town,)
				)
				db.commit()
				# store the id of the recently created town
				viewer_town_id=db.execute(
					'SELECT id FROM town WHERE name = ?', (viewer_town,)
				).fetchone()[0]

		# all data required to insert the viewers information exists on DB
		# insert the row into the viewers table
		if not viewer_count:
			# if the number of viewers is empty pass
			pass
		else:
			if ((program_title_id is not None) and
				(program_network_id is not None) and
				(program_genre_id is not None) and
				(viewer_town_id is not None)):
			# if all ids for current row are set
				# check if a similar row doesn't exist on the db
				if db.execute(
						'SELECT id FROM viewers WHERE viewers_number = ? AND title_id = ? AND network_id = ? AND hometown_id = ? AND genre_id = ?', 
						(viewer_count,program_title_id,program_network_id,viewer_town_id,program_genre_id)
					).fetchone() is not None:

					click.echo("Skipped duplicated:%s" % (row,))
			
				else:
					# if it doesn't exist insert row on the db
					db.execute(
						'INSERT INTO viewers (viewers_number,title_id,network_id,hometown_id,genre_id) VALUES (?,?,?,?,?)', 
						(int(viewer_count),program_title_id,program_network_id,viewer_town_id,program_genre_id)
					)
					db.commit()

					click.echo("Inserted:%s" % (row,))



def init_db():
	db = get_db()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

	
	with open("%s/data.csv" % (current_app.root_path,), newline='') as f:
		reader=csv.reader(f,delimiter=',')
		# skip headers line
		next(reader)
		for row in reader:
			insert_csv_row(row)


@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear existing data and create new tables"""
	init_db()
	click.echo('Initialized the database, and imported all data from CSV')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)