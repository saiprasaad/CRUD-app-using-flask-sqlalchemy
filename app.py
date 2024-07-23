from flask import Flask, jsonify
from todo_bp import todo_bp
from todo_model import db

app = Flask(__name__)
app.register_blueprint(todo_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret@1234'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)