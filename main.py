from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Person, Record

app = Flask(__name__)

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
    q = session.query(Record).filter_by(id=id).one()
    if request.method == 'POST':
            if request.form['subject']:
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

@app.route('/new', methods=['POST', 'GET'])
def createRecord():
    q = session.query(Record)
    if request.method == 'POST':
        if request.form['subject']:
            q.subject = request.form['subject']
        if request.form['start_time']:
            q.start_time = request.form['start_time']
        if request.form['stop_time']:
            q.stop_time = request.form['stop_time']
        if request.form['goal']:
            q.goal = request.form['goal']
        if request.form['comments']:
            q.comments = request.form['comments']
        q.total_minutes = 0
        session.add(q)
        session.commit()
        return redirect(url_for('showRecord', id=q.id))
    else:
        return render_template('new.html', methods=['POST', 'GET'])



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
