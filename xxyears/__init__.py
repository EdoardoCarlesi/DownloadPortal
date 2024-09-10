import os
import flask
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'xxyears.sqlite'),
    )

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

    @app.route('/gdpr')
    def gdpr():
        return flask.render_template('gdpr.html')


    from . import db
    db.init_app(app)
    print('App intialized')

    from . import payment
    app.register_blueprint(payment.bp)
    app.add_url_rule('/payment', endpoint='payment.payment')
    app.add_url_rule('/payment/success', endpoint='payment.success')

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/auth', endpoint='auth.register')

    from . import video
    app.register_blueprint(video.bp)
    app.add_url_rule('/video', endpoint='video.play')
    
    return app
