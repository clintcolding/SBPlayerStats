from app import app, db, Team, Player, Pitcher
import sbteamdata

def get_career_stats(tid, playerid):

    with app.app_context():
        players = Player.query.filter_by(teamid=tid, playerid=playerid).all()

    name = ""
    position = ""
    games = 0
    ab = 0
    hits = 0
    singles = 0
    doubles = 0
    triples = 0
    hr = 0
    rbi = 0
    so = 0
    era = 0
    slg = 0

    for player in players:
        name = player.name
        position = player.position
        games += player.games
        ab += player.ab
        hits += player.hits
        singles += player.singles
        doubles += player.doubles
        triples += player.triples
        hr += player.hr
        rbi += player.rbi
        so += player.so
        if "-" not in player.era:
            era = era + float(player.era)

    if ab == "0":
        avg = 0
    else:
        avg = hits / ab
        avg = format(avg, '.3f')
        if avg[0] == "0":
            avg = avg[1:]

    totalbases = int(singles) + (int(doubles)*2) + (int(triples)*3) + (int(hr)*4)

    if ab == "0":
        slg = 0
    else:
        slg = (totalbases / int(ab))
        slg = format(slg, '.3f')
        if slg[0] == "0":
            slg = slg[1:]

    player = sbteamdata.Player(playerid, name, position, games, ab, hits,
                               avg, singles, doubles, triples, hr, rbi, so, era)

    player.slg = player.compute_slg()

    return player
