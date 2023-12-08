from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String,nullable = False)
    description = db.Column(db.String,nullable = False)


with app.app_context():
    db.create_all()

@app.route("/",methods = ["GET","POST"])
def greet():

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        todo = Todo(title=title,description=desc)
        db.session.add(todo)
        db.session.commit()

    todoList = Todo.query.all()
    return render_template('index.html', todoList = todoList)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>",methods = ["GET","POST"])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo = todo)

app.run(debug=True)