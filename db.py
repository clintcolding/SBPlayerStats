from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    name = db.Column(db.String)
    stars = db.Column(db.Integer)
    stadium = db.Column(db.String)
    pl = db.Column(db.String)
    pl_position = db.Column(db.String)
    trained = db.Column(db.String)
    games = db.Column(db.Integer)
    ab = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    avg = db.Column(db.String)
    singles = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)
    slg = db.Column(db.String)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    pct = db.Column(db.String)
    rs = db.Column(db.Integer)
    ra = db.Column(db.Integer)

    def __init__(self, time, season, teamid, name, stars, stadium, pl, pl_position,
                 trained, games, ab, hits, avg, singles, doubles, triples,
                 hr, rbi, so, era, slg, wins, losses, pct, rs, ra):
        self.time = time
        self.season = season
        self.teamid = teamid
        self.name = name
        self.stars = stars
        self.stadium = stadium
        self.pl = pl
        self.pl_position = pl_position
        self.trained = trained
        self.games = games
        self.ab = ab
        self.hits = hits
        self.avg = avg
        self.singles = singles
        self.doubles = doubles
        self.triples = triples
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self.era = era
        self.slg = slg
        self.wins = wins
        self.losses = losses
        self.pct = pct
        self.rs = rs
        self.ra = ra

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    name = db.Column(db.String)
    position = db.Column(db.String)
    games = db.Column(db.Integer)
    ab = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    avg = db.Column(db.String)
    singles = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)
    slg = db.Column(db.String)

    def __init__(self, season, teamid, playerid, name, position, games, ab, hits,
                 avg, singles, doubles, triples, hr, rbi, so, era, slg):
        self.season = season
        self.teamid = teamid
        self.playerid = playerid
        self.name = name
        self.position = position
        self.games = games
        self.ab = ab
        self.hits = hits
        self.avg = avg
        self.singles = singles
        self.doubles = doubles
        self.triples = triples
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self.era = era
        self.slg = slg

class Pitcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    name = db.Column(db.String)
    games = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)

    def __init__(self, season, teamid, playerid, name, games, so, era):
        self.season = season
        self.teamid = teamid
        self.playerid = playerid
        self.name = name
        self.games = games
        self.so = so
        self.era = era

class TeamGains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer)
    date = db.Column(db.String)
    time = db.Column(db.String)
    contact = db.Column(db.String)
    power = db.Column(db.String)
    skill = db.Column(db.String)
    run = db.Column(db.String)
    throw = db.Column(db.String)
    catch = db.Column(db.String)
    pitch = db.Column(db.String)
    total = db.Column(db.String)

    def __init__(self, tid, date, time, contact, power,
                 skill, run, throw, catch, pitch, total):
        self.tid = tid
        self.date = date
        self.time = time
        self.contact = contact
        self.power = power
        self.skill = skill
        self.run = run
        self.throw = throw
        self.catch = catch
        self.pitch = pitch
        self.total = total
