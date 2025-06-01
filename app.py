from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    memo = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    GENRE_CHOICES = [
        ('work', '仕事'),
        ('private', 'プライベート'),
        ('other', 'その他'),
    ]

    PRIORITY_CHOICES = [
        (1, '低'),
        (2, 'やや低'),
        (3, '中'),
        (4, 'やや高'),
        (5, '高'),
    ]

    def get_genre_display(self):
        genre_dict = dict(self.GENRE_CHOICES)
        return genre_dict.get(self.genre, self.genre)

    def get_priority_display(self):
        priority_dict = dict(self.PRIORITY_CHOICES)
        return priority_dict.get(self.priority, str(self.priority))

    def __repr__(self):
        return f'<Task {self.title}>'

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField('タスク名', validators=[DataRequired(), Length(max=200)], 
                       render_kw={'class': 'form-control'})
    memo = TextAreaField('メモ', render_kw={'class': 'form-control', 'rows': 3})
    genre = SelectField('ジャンル', choices=Task.GENRE_CHOICES, 
                       render_kw={'class': 'form-control'})
    priority = RadioField('重要度', choices=Task.PRIORITY_CHOICES, coerce=int)
    submit = SubmitField('保存', render_kw={'class': 'btn btn-primary'})

@app.route('/')
def task_list():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('task_list.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def task_create():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            memo=form.memo.data,
            genre=form.genre.data,
            priority=form.priority.data
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task_list'))
    return render_template('task_form.html', form=form, title='新規タスク作成')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def task_update(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('task_list'))
    return render_template('task_form.html', form=form, task=task, title='タスク編集')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def task_delete(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('task_list'))
    return render_template('task_confirm_delete.html', task=task)

@app.route('/toggle/<int:id>', methods=['POST'])
def task_toggle(id):
    task = Task.query.get_or_404(id)
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'success', 'is_completed': task.is_completed})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
