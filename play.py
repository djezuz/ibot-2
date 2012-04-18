import sys
import json
import requests

root = 'http://dev.i.tv:2663'

level = sys.argv[1]
game_url = '{0}/minefield/levels/{1}/games'.format(root, level)

data = {'username': "smcquay", }
directions = ["up", "down", "left", "right"]

def move(gameid, direction):
    url = '{0}/minefield/{1}/moves'.format(root, gameid)
    print url
    return requests.post(url, data={'action': direction})

r = requests.post(game_url, data)
print r.text
game = json.loads(r.text)
game_id = game['gameId']
print requests.get('{0}/games/{1}/state.txt'.format(root, game_id)).text
sys.exit(0)
print game_id

if level == 'tiny':
    r = move(game['gameId'], 'down')
    print r.status_code, r.text
elif level == 'empty':
    for i in xrange(9):
        r = move(game['gameId'], 'down')
        r = move(game['gameId'], 'right')
        print r.status_code, r.text
