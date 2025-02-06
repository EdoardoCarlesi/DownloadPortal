from xxyears import create_app
from waitress import serve

application = create_app()

if __name__ == "__main__":
    #application.run()
    serve(app)
