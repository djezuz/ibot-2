#!/usr/bin/python

import curses

class guy():
    def __init__(self, y, x):
        self.wt = 3
        self.ht = 3
        self.win = curses.newwin(y, x, 0, 0)
        self.x = 1
        self.y = 1
        self.d = 0
        self.draw()

    def move_vert(self, delta):
        if delta > 0:
            self.d = 0
        else:
            self.d = 1
        self.y -= delta
        if(self.y <= 1):
            self.y = 1
        elif(self.y > self.max_y - self.ht - 1):
            self.y = self.max_y - self.ht - 1

    def move_horz(self, delta):
        if delta < 0:
            self.d = 2
        else:
            self.d = 3

        self.x += delta

        if(self.x <= 1):
            self.x = 1
        elif(self.x > self.max_x - self.wt - 1):
            self.x = self.max_x - self.wt - 1

    def reset(self):
        self.x = 1
        self.y = 1

    def draw(self, msg=None):
        self.win.clear()
        self.win.border()
        if msg is None:
            msg = ''
        for c, s in enumerate(msg.split('\n')):
            self.win.addstr(c + 1, 1, s,
                    curses.color_pair(1))
        self.win.refresh()

    @property
    def max_x(self):
        return self.win.getmaxyx()[1]

    @property
    def max_y(self):
        return self.win.getmaxyx()[0]

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.start_color()

    curses.noecho()
    curses.cbreak()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    ofile = open('/tmp/output.log', 'a')

    xy = stdscr.getmaxyx()
    g = guy(xy[0], xy[1])
    while True:
        c = stdscr.getch()

        direction = ''
        if c == ord('w') or c == ord('k'):
            g.move_vert(1)
            direction = 'up'
        elif c == ord('s') or c == ord('j'):
            g.move_vert(-1)
            direction = 'down'
        elif c == ord('a') or c == ord('h'):
            g.move_horz(-1)
            direction = 'left'
        elif c == ord('d') or c == ord('l'):
            g.move_horz(1)
            direction = 'right'
        elif c == ord('q'):
            break
        ofile.write('{0}\n'.format(direction))
        g.draw(direction)
        ofile.flush()

    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
