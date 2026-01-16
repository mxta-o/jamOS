from flask import Flask
from routes.main_routes import main_bp
from routes.productivity_routes import productivity_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-change-this'
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(productivity_bp, url_prefix='/apps')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5002)
