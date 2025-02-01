import os
import flask
from flask import Flask

from xxyears import video
from xxyears import codes

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    DATABASE = os.path.join(app.instance_path, 'xxyears.db')
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=DATABASE,
    )

    print("App db: ", DATABASE)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        if not os.path.isdir(app.instance_path):
            os.makedirs(app.instance_path)
        else:
            print(f'Instance path already exists: {app.instance_path}')
    except OSError:
        print(f'Instance path does not exist: {app.instance_path}')

    # a simple page that says hello
    @app.route('/liechtenstein')
    def liechtenstein():
        return 'Hail to Liechtenstein!'

    @app.route('/')
    def index():
        return flask.render_template('video/index.html')

    from . import codes
    #app.register_blueprint(codes.bp)
    #app.add_url_rule('/redeem', endpoint='redeem', methods=['GET', 'POST'])
    app.add_url_rule('/', view_func=codes.redeem, methods=['GET', 'POST'])

    @app.route('/gdpr')
    def gdpr():
        return flask.render_template('gdpr.html')

    from . import db
    db.init_app(app)
    print('App intialized')

    from . import report
    report.init_report_command(app)
    print('Report generated successfully')

    from . import payment
    app.register_blueprint(payment.bp)
    app.add_url_rule('/payment', endpoint='payment.payment')
    app.add_url_rule('/payment/success', endpoint='payment.success')

    return app
