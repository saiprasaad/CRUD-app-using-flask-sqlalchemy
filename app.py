from flask import Flask, render_template, request, redirect, url_for
from models import db, Student
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    students = []
    order = request.args.get('order')
    if order == 'asc':
        students = Student.query.order_by(Student._id).all()
    else:
        students = Student.query.order_by(desc(Student._id)).all()
    return render_template("index.html", students = students)

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        if 'name' not in request.form or 'email' not in request.form or 'password' not in request.form or 'gender' not in request.form or 'country' not in request.form or not request.form.getlist('hobby'):
            return render_template("create.html", error="Missing values of some fields")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']
        hobbies = ",".join(request.form.getlist("hobby"))
        student = Student(name=name, email=email, password=password, gender=gender, hobbies=hobbies, country=country)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("create.html")

@app.route("/update/<id>", methods = ["GET", "POST"])
def update_student(id):
    student_found = Student.query.filter_by(_id=id).first()
    if request.method == "GET":
        if student_found:
            return render_template("update.html", student = student_found)
        else:
            return redirect(url_for("home"))
    else:
        if 'name' not in request.form or 'email' not in request.form or 'password' not in request.form or 'gender' not in request.form or 'country' not in request.form or not request.form.getlist('hobby'):
            return render_template("update.html", error="Missing values of some fields")
        student_found.name = request.form['name']
        student_found.email = request.form['email']
        student_found.password = request.form['password']
        student_found.gender = request.form['gender']
        student_found.country = request.form['country']
        student_found.hobbies = ",".join(request.form.getlist("hobby"))
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/delete/<id>", methods = ["POST"])
def delete_student(id):
    student_found = Student.query.filter_by(_id=id).first()
    if student_found:
        Student.query.filter_by(_id=id).delete()
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)