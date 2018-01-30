from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db, Team, Player, Pitcher
import getcareerstats
import os
import sbteamdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

with app.app_context():
    db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tid = request.form['teamid']

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>', methods=['GET', 'POST'])
def stats(tid):
    current_season = sbteamdata.get_current_season()
    seasons = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
    team = Team.query.filter_by(teamid=tid, season=current_season).first()

    if team and (team.time - datetime.now()).total_seconds() > -3600:
        players = Player.query.filter_by(teamid=tid, season=current_season).all()
        pitchers = Pitcher.query.filter_by(teamid=tid, season=current_season).all()
        updated = team.time.strftime('Updated on %B %d at %I:%M %p')

    else:
        stats = sbteamdata.get_team_data(tid)

        team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
        players = Player.query.filter_by(teamid=tid, season=stats.season).all()
        pitchers = Pitcher.query.filter_by(teamid=tid, season=stats.season).all()

        for entry in team:
            if entry.season == int(stats.season):
                db.session.delete(entry)
                db.session.commit()

        new_entry = Team(datetime.now(), stats.season, tid, stats.name, stats.stars, stats.stadium,
                        stats.pl, stats.pl_position, stats.trained, stats.games, stats.ab, stats.hits,
                        stats.avg, stats.singles, stats.doubles, stats.triples, stats.hr,
                        stats.rbi, stats.so, stats.era, stats.slg, stats.wins, stats.losses,
                        stats.pct, stats.rs, stats.ra)
        db.session.add(new_entry)

        if players:
            for player in players:
                db.session.delete(player)
                db.session.commit()

        for player in stats.players:
            new_entry = Player(stats.season, tid, player.id, player.name, player.position, player.games,
                            player.ab, player.hits, player.avg, player.singles, player.doubles,
                            player.triples, player.hr, player.rbi, player.so, player.era, player.slg)
            db.session.add(new_entry)

        if pitchers:
            for player in pitchers:
                db.session.delete(player)
                db.session.commit()
        for player in stats.pitchers:
            new_entry = Pitcher(stats.season, tid, player.id, player.name, player.games,
                                player.so, player.era)
            db.session.add(new_entry)
        db.session.commit()

        team = Team.query.filter_by(teamid=tid, season=current_season).first()
        players = Player.query.filter_by(teamid=tid, season=current_season).all()
        pitchers = Pitcher.query.filter_by(teamid=tid, season=current_season).all()
        updated = team.time.strftime('Updated on %B %d at %I:%M %p')

    return render_template('stats.html', updated=updated, seasons=seasons, team=team, players=players, pitchers=pitchers)

@app.route('/refreshstats', methods=['POST'])
def refresh_stats():
    tid = request.form['tid']

    stats = sbteamdata.get_team_data(tid)

    team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
    players = Player.query.filter_by(teamid=tid, season=stats.season).all()
    pitchers = Pitcher.query.filter_by(teamid=tid, season=stats.season).all()

    for entry in team:
        if entry.season == int(stats.season):
            db.session.delete(entry)
            db.session.commit()

    new_entry = Team(datetime.now(), stats.season, tid, stats.name, stats.stars, stats.stadium,
                     stats.pl, stats.pl_position, stats.trained, stats.games, stats.ab, stats.hits,
                     stats.avg, stats.singles, stats.doubles, stats.triples, stats.hr,
                     stats.rbi, stats.so, stats.era, stats.slg, stats.wins, stats.losses,
                     stats.pct, stats.rs, stats.ra)
    db.session.add(new_entry)

    if players:
        for player in players:
            db.session.delete(player)
            db.session.commit()

    for player in stats.players:
        new_entry = Player(stats.season, tid, player.id, player.name, player.position, player.games,
                           player.ab, player.hits, player.avg, player.singles, player.doubles,
                           player.triples, player.hr, player.rbi, player.so, player.era, player.slg)
        db.session.add(new_entry)

    if pitchers:
        for player in pitchers:
            db.session.delete(player)
            db.session.commit()
    for player in stats.pitchers:
        new_entry = Pitcher(stats.season, tid, player.id, player.name, player.games,
                            player.so, player.era)
        db.session.add(new_entry)
    db.session.commit()

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>/<season>')
def seasonstats(tid, season):
    current_season = sbteamdata.get_current_season()

    if season != 'all' and int(current_season) == int(season):

        return redirect('/stats/{0}'.format(tid))

    else:
        if season == "all":
            team = Team.query.filter_by(teamid=tid).order_by(Team.season.asc()).all()
            players = Player.query.filter_by(teamid=tid).all()
            pitchers = Pitcher.query.filter_by(teamid=tid).all()
            stats = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).first()

            return render_template('allstats.html', team=team, stats=stats, players=players, pitchers=pitchers)

        else:
            team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
            players = Player.query.filter_by(teamid=tid, season=season).all()
            pitchers = Pitcher.query.filter_by(teamid=tid, season=season).all()

            for entry in team:
                if entry.season == int(season):
                    stats = entry

            return render_template('seasonstats.html', team=team, stats=stats, players=players, pitchers=pitchers)

@app.route('/stats/<tid>/career/<playerid>')
def careerstats(tid, playerid):
    current_season = sbteamdata.get_current_season()
    team = Team.query.filter_by(teamid=tid, season=current_season).first()
    teamavg = Team.query.filter_by(teamid=tid).order_by(Team.season.asc()).all()
    players = Player.query.filter_by(teamid=tid, season=current_season).all()
    seasons = Player.query.filter_by(teamid=tid, playerid=playerid).all()
    total = getcareerstats.get_career_stats(tid, playerid)

    return render_template('careerstats.html', total=total, seasons=seasons, team=team, playerid=playerid, players=players, teamavg=teamavg)

@app.route('/leaders')
def leaders():
    current_season = sbteamdata.get_current_season()

    teams = Team.query.filter_by(season=current_season).filter(Team.games >= 5)
    players = Player.query.filter_by(season=current_season).filter(Player.games >= 5)
    pitchers = Pitcher.query.filter_by(season=current_season).filter(Pitcher.games >= 5)

    return render_template('leaders.html', teams=teams, players=players, pitchers=pitchers)

@app.route('/gameleaders')
def gameleaders():
    current_season = sbteamdata.get_current_season()

    teams = Team.query.filter_by(season=current_season).filter(Team.games >= 5)
    players = Player.query.filter_by(season=current_season).filter(Player.games >= 5)
    pitchers = Pitcher.query.filter_by(season=current_season).filter(Pitcher.games >= 5)

    return render_template('gameleaders.html', teams=teams, players=players, pitchers=pitchers)

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
