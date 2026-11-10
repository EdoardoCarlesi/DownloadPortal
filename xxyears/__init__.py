import hmac
import os
import flask
from flask import Flask, flash
from xxyears import video
from xxyears import codes
from xxyears import mail

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Signs the session cookie that carries a buyer's code. Must be set in the environment
    # and be identical across all gunicorn workers.
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise RuntimeError('SECRET_KEY environment variable must be set.')
    app.config['SECRET_KEY'] = secret_key
    
    """
    DATABASE = os.path.join(app.instance_path, 'xxyears.db')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=DATABASE,
    )
    #print("App db: ", DATABASE)

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
    """

    # a simple page that says hello
    @app.route('/liechtenstein')
    def liechtenstein():
        return 'Hail to Liechtenstein!'

    @app.route('/')
    def index():
        return flask.render_template('video/index.html')

    from . import codes
    app.add_url_rule('/', view_func=codes.redeem, methods=['GET', 'POST'])

    @app.route('/gdpr')
    def gdpr():
        return flask.render_template('gdpr.html')

    @app.route('/send-report')
    def send_report():
        # Disabled unless REPORT_TOKEN is set; caller must send it in the X-Report-Token header.
        expected = os.environ.get('REPORT_TOKEN')
        provided = flask.request.headers.get('X-Report-Token', '')
        if not expected or not hmac.compare_digest(provided.encode(), expected.encode()):
            flask.abort(404)
        mail.send_codes_report()
        #flash('Report sent successfully')
        return 'Report sent successfully'

    from . import db
    db.init_app(app)
    print('App intialized')

    from . import payment
    app.register_blueprint(payment.bp)
    app.add_url_rule('/payment', endpoint='payment.payment')
    app.add_url_rule('/payment/success', endpoint='payment.success')

    return app
