from flask import Flask,render_template,request,redirect
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField,IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


app.config['MONGODB_SETTINGS'] = {
    'db': 'todoman',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)


class TodoModel(db.Document):
    num = db.IntField()
    task = db.StringField()
    summary = db.StringField()


class Post(FlaskForm):
    num= IntegerField("Enter the priority", validators=[DataRequired()])
    task = StringField("Enter the task" , validators=[DataRequired()])
    submit = SubmitField()


class Update(FlaskForm):
    task = StringField(validators=[DataRequired()])
    submit = SubmitField(label="Update")


@app.route("/",methods=['GET','POST'])
def create():
    form = Post()
    if form.validate_on_submit():
        try:
            task = TodoModel.objects.get(num=form.num.data)

        except:
            TodoModel(num=form.num.data, task=form.task.data).save()
            task = TodoModel.objects.order_by('num')
            return render_template("index.html", todo=task, form=form)

    task = TodoModel.objects.order_by('num')
    return render_template("index.html", todo=task, form=form)


@app.route('/update',methods=['GET', 'POST'])
def update():
    form = Update()
    todo_id = request.args.get("todo_id")
    if form.validate_on_submit():
        task = TodoModel.objects.get(num=todo_id)
        task.update(task=form.task.data)
        return redirect('/')
    return render_template("update.html",form=form,todo_id=todo_id)


@app.route('/delete',methods=["GET","POST"])
def delete():
    todo_id = request.args.get("todo_id")
    print(todo_id)
    TodoModel.objects.get(num=todo_id).delete()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

