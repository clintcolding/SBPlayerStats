from flask import Flask, render_template, request
import sbteamdata

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def my_form():
    return render_template('index.html')

@app.route('/teamstats', methods=['POST'])
def my_form_post():
    tid = request.form['teamid']

    myteamname = (sbteamdata.get_team_data(tid)).name
    stats = sbteamdata.get_team_data(tid)
    pitchers = sbteamdata.get_pitchers(tid)

    return render_template('teamstats.html', myteamname=myteamname, stats=stats, pitchers=pitchers)

if __name__ == '__main__':
    app.run(debug=True)
