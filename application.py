from project import create_app
from flask_mail import Mail

application = app = create_app()
mail = Mail(app)

if __name__ == '__main__':
    application.run(debug=True)