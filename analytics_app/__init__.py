import os
from flask import Flask

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
			SECRET_KEY='dev',
			DATABASE=os.path.join(app.instance_path,'analytics.sqlite')
		)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	# db module
	from . import db
	db.init_app(app)

	# program blueprint
	from . import program
	app.register_blueprint(program.bp)

	# town blueprint
	from . import town
	app.register_blueprint(town.bp)

	# program network blueprint
	from . import network
	app.register_blueprint(network.bp)

	# program genre blueprint
	from . import genre
	app.register_blueprint(genre.bp)

	# program views blueprint
	from . import views
	app.register_blueprint(views.bp)

	# dashboard views blueprint
	from . import dashboard
	app.register_blueprint(dashboard.bp)
	app.add_url_rule('/', endpoint='index')

	return app