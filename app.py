from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sbteamdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

class Recent(db.Model):
    teamid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)

    def __init__(self, teamid, time):
        self.teamid = teamid
        self.time = time

@app.route('/')
def index():
    recent = Recent.query.order_by(Recent.time.desc()).limit(10)
    return render_template('index.html', recent=recent)

@app.route('/search', methods=['POST'])
def search():
    tid = request.form['teamid']
    
    team = Recent.query.filter_by(teamid=tid).first()

    if team:
        team.time = datetime.now()
    else:
        new_entry = Recent(tid, datetime.now())
        db.session.add(new_entry)
    db.session.commit()

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>', methods=['GET', 'POST'])
def stats(tid):
    myteamname = (sbteamdata.get_team_data(tid)).name
    stats = sbteamdata.get_team_data(tid)
    pitchers = sbteamdata.get_pitchers(tid)

    return render_template('stats.html', myteamname=myteamname, stats=stats, pitchers=pitchers)

if __name__ == '__main__':
    app.run(debug=True)
