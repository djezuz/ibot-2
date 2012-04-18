import sys
import json
import requests

from pprint import pprint as pp, pformat as pf


class Network(object):

    root = 'http://dev.i.tv:2663'
    data = {'username': "smcquay", }

    def __init__(self, level, data=None):
        if data is None:
            self.data = Network.data
        self.game_url = '{0}/minefield/levels/{1}/games'.format(Network.root, level)
        r = requests.post(self.game_url, self.data)
        game = json.loads(r.text)
        self.game_id = game['gameId']
        self._parse_state(game['state'])

    def _parse_state(self, state):
        self.loc    = state['player']
        self.mines  = state['mines']
        self.target = state['target']
        self.mode   = state['mode']
        self.max_x  = state['size']['w']
        self.max_y  = state['size']['h']

    def move(self, direction):
        url = '{0}/minefield/{1}/moves'.format(Network.root, self.game_id)
        r = requests.post(url, data={'action': direction})
        r = json.loads(r.text)
        self._parse_state(r)
        # 200 {"mode":"won","size":{"w":2,"h":2},"player":{"x":0,"y":1},"target":{"x":0,"y":1},"mines":[]}

    @property
    def map(self):
        r = requests.get('{0}/games/{1}/state.txt'.format(Network.root, self.game_id))
        return r.text

    @property
    def x(self):
        return self.loc['x']

    @property
    def y(self):
        return self.loc['y']


    def __str__(self):
        return self.map


usage = """\
net.py <tiny|empty|easy>
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
