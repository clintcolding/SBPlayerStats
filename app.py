from flask import Flask, render_template, request, redirect, url_for
import sbteamdata

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tid = request.form['teamid']

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>', methods=['GET', 'POST'])
def stats(tid):
    myteamname = (sbteamdata.get_team_data(tid)).name
    stats = sbteamdata.get_team_data(tid)
    pitchers = sbteamdata.get_pitchers(tid)

    return render_template('stats.html', myteamname=myteamname, stats=stats, pitchers=pitchers)

if __name__ == '__main__':
    app.run(debug=True)
