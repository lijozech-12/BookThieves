import time
from flask import Flask, render_template,request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)

#######################MODELS ###############################

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    email =  db.Column(db.String(50))
    password = db.Column(db.String(50))
    about = db.Column(db.String(50))
    genres = db.Column(db.String(50))
    image = db.Column(db.String(50))


class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    possessor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(200))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    likes = db.Column(db.Integer, default= 0)
    genres = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    status = db.Column(db.Integer, default='Pending')
    
    



##########################ROUTES################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        data = User.query.filter_by(username=username,
                                    password=password).first()

        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('index'))

        return render_template('incorrectLogin.html')



@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'],
                        email=request.form['email']
                        password=request.form['password'], about=request.form['about'],
                        genres=request.form['genres'], image=request.form['image'],
                        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

######################################### MAIN ####################################


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)