from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Person, Record
from datetime import datetime
from forms import *

WTF_CSRF_ENABLED = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

engine = create_engine('sqlite:///records.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index/')
def coverPage():
    return render_template('/index.html')

@app.route('/login')
def loginPage():
    return render_template('/login.html', methods=['GET','POST'])

@app.route('/register')
def registerPage():
    return render_template('/register.html', methods=['GET','POST'])

@app.route('/<int:id>/', methods=['GET'])
def showRecord(id):
    q = session.query(Record).filter_by(id=id).one()
    return render_template('/show.html', methods=['GET'], item=q)

@app.route('/<int:id>/edit/', methods=['GET','POST'])
def editRecord(id):
    q = session.query(Record)
    if request.method == 'POST':
            if request.form['subject']:
                print(request.form['subject'])
                print(q)
                q.subject = request.form['subject']
            if request.form['start_time']:
                q.start_time = request.form['start_time']
            if request.form['stop_time']:
                q.stop_time = request.form['stop_time']
            if request.form['total_minutes']:
                q.total_minutes = request.form['total_minutes']
            if request.form['goal']:
                q.goal= request.form['goal']
            if request.form['comments']:
                q.comments = request.form['comments']
            session.add(q)
            session.commit()
            return redirect(url_for('coverPage'))
    else:
        return render_template('/edit.html', item=q)

@app.route('/success', methods=['GET'])
def success(id):
    return render_template('/success.html')

@app.route('/new',methods=['GET','POST'])
def submit():
    form = CreateEntryForm()
    form.meta.csrf = False

    if form.validate_on_submit():
        q = Record()
        sq =session.query(func.count(Record.id))
        print(sq)


        q.subject = form.subject.data
        q.start_time = func.now()
        q.stop_time = func.now()
        q.total_minutes = 0
        q.goal = form.goal.data
        q.comments = form.comments.data
        session.add(q)
        session.commit()
        flash("Record created!")


        return redirect(url_for('coverPage'))

    return render_template('/new.html', form=form)

@app.route('/records')
def records():
    return render_template('/records.html', items=session.query(Record).all())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
