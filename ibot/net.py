import sys
import json
import requests


class Network(object):

    root = 'http://dev.i.tv:2663'
    data = {'username': "smcquay", }

    def __init__(self, level, data=None):
        if data is None:
            self.data = Network.data
        self.game_url = '{0}/minefield/levels/{1}/games'.format(Network.root, level)
        try:
            r = requests.post(self.game_url, self.data)
            game = json.loads(r.text)
            self.game_id = game['gameId']
            self._parse_state(game['state'])
        except requests.exceptions.ConnectionError:
            self.game_id = None

    def _parse_state(self, state):
        self.loc = state['player']
        self.mines = state['mines']
        self.target = state['target']
        self.mode = state['mode']
        self.max_x = state['size']['w']
        self.max_y = state['size']['h']

    def move(self, direction):
        url = '{0}/minefield/{1}/moves'.format(Network.root, self.game_id)
        try:
            r = requests.post(url, data={'action': direction})
            r = json.loads(r.text)
            self._parse_state(r)
        except requests.exceptions.ConnectionError:
            pass

    @property
    def map(self):
        try:
            r = requests.get('{0}/games/{1}/state.txt'.format(Network.root, self.game_id))
            m = r.text
        except requests.exceptions.ConnectionError:
            pass
            m = 'There is a problem with the server'
        return m

    @property
    def x(self):
        return self.loc['x']

    @property
    def y(self):
        return self.loc['y']

    def __str__(self):
        return self.map

usage = """\
ibot <level>
    where level is one of the following:
        tiny - all the demos solve this for you, move once to win (hint, go down)
        empty - a large map with no mines
        easy - a few stationary mines always in the same place
        muchosMines - lots of mines with deadly traps
        randomMines - a random assortment of mines to avoid
        movingTarget - Your goal keeps shifting, can you hit it?
        blackAnts - the mines grow legs and move each time you do (they can't move onto your square)
        heatSeeking - a single mine heads straight for you, watch out!
        puppyGuard - a few mines patrol the way to your goal, can you get past?
        armyAnts - the ultimate challenge, tons of mines move randomly without regard to your position
"""

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print usage
        sys.exit(1)

    level = sys.argv[1]

    net = Network(level)
    print net
    if level == 'tiny':
        net.move('down')
        print net
    elif level == 'empty':
        for i in xrange(9):
            net.move('down')
            net.move('right')
            print net
