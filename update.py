from app import app, db, Team, Player, Pitcher
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sbteamdata

teamids = []

with app.app_context():
    query = db.session.query(Team.teamid.distinct().label("teamid"))

    for item in query:
        teamid = str(item)[1:]
        teamid = teamid[:-2]
        teamids.append(teamid)

    for tid in teamids:
        current_season = sbteamdata.get_current_season()
        seasons = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
        team = Team.query.filter_by(teamid=tid, season=current_season).first()

        if team and (team.time - datetime.now()).total_seconds() > -600:
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
    