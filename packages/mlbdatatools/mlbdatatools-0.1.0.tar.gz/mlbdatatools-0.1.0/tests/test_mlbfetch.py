from mlbdatatools import mlbfetch

def test_players():
    all_players = mlbfetch.players()
    andrew_abbot = all_players[0]
    assert andrew_abbot.full_name == "Andrew Abbott"