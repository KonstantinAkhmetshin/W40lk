from flask import Flask
from controllers.CharacterController import char_controller

# Create the Flask app
app = Flask(__name__)

# Register controllers (blueprints)
app.register_blueprint(char_controller, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)