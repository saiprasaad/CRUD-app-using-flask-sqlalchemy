from flask import Blueprint, render_template, session, abort, request, redirect, url_for
from todo_model import db, User, Todo

todo_bp = Blueprint('todo', __name__)

@todo_bp.route("/")
def home():
    if 'user' not in session or 'userid' not in session:
        return redirect(url_for('todo.login'))
    todos = Todo.query.filter_by(userid=int(session['userid'])).all()
    return render_template('todo_list.html', todos = todos)

@todo_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not username or len(username) == 0 or not password or len(password) == 0:
            return render_template('login.html', error = 'Missing required fields')
        else:
            u = User.query.filter_by(username=username).first()
            if not u:
                return render_template('login.html', error = 'Username does not exists')
            elif u.password != password:
                return render_template('login.html', error = 'Incorrect credentials') 
            else:
                session['user'] = username
                session['userid'] = u.id
                return redirect(url_for('todo.home'))

@todo_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not username or len(username) == 0 or not password or len(password) == 0:
            return render_template('register.html', error = 'Missing required fields')
        else:
            u = User(username=username, password=password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('todo.login'))
        
@todo_bp.route('/logout')
def logout():
    session.pop('user')
    session.pop('userid')
    return redirect(url_for('todo.login'))


@todo_bp.route("/add-todo", methods = ["GET", "POST"])
def addTodo():
    if 'user' not in session or 'userid' not in session:
        return redirect(url_for('todo.login'))
    if request.method == "GET":
        return render_template('addtodo.html')
    else:
        text = request.form['content']
        if not text or len(text) == 0:
            return render_template('addtodo.html', error = 'Missing required fields') 
        else:
            t = Todo(text=text, userid=int(session['userid']))
            db.session.add(t)
            db.session.commit()
            return redirect(url_for('todo.home')) 
        
@todo_bp.route("/delete-todo/<id>")
def deleteTodo(id):
    if 'user' not in session or 'userid' not in session:
        return redirect(url_for('todo.login'))
    Todo.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('todo.home')) 

@todo_bp.route("/update-todo/<id>", methods = ['GET', 'POST'])
def updateTodo(id):
    if 'user' not in session or 'userid' not in session:
        return redirect(url_for('todo.login'))
    todo = Todo.query.filter_by(id=id).first()
    if not todo:
        abort(404, 'Todo does not exists')
    if todo.userid != int(session['userid']):
        abort(401, 'Unauthorized')
    if request.method == 'GET':
        return render_template('updatetodo.html', todo = todo)
    else:
        text = request.form['content']
        if not text or len(text) == 0:
            return render_template('updatetodo.html', error = 'Missing required fields', todo = todo) 
        else:
            todo.text = text
            db.session.commit()
            return redirect(url_for('todo.home'))
    
    