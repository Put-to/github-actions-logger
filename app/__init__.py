from flask import Flask
from app.extensions import init_app



def create_app():

    app = Flask(__name__)
    init_app(app)
    
    from app.webhook.routes import webhook
    app.register_blueprint(webhook)
    
    return app
