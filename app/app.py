from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

db = SQLAlchemy(app)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100), nullable=False)
    track_id = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    playlists = Playlist.query.all()
    return render_template('index.html', playlists=playlists)

@app.route('/help')
def help():
    return render_template('help.html')



if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()

