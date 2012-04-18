#!/usr/bin/python

import curses
import sys

from ibot.net import Network, usage


class GUI():
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.direction = ''
        self.net = Network(puzzle)

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.start_color()

        curses.noecho()
        curses.cbreak()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        y, x = self.stdscr.getmaxyx()
        self.win = curses.newwin(y, x, 0, 0)
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def move(self, direction):
        self.direction = direction
        self.net.move(direction)

    def draw(self):
        self.win.clear()
        self.win.border()
        for c, s in enumerate(self.net.map.split('\n')):
            self.win.addstr(c + 1, 1, s,
                    curses.color_pair(1))
        self.win.refresh()

    def run(self):
        c = self.stdscr.getch()
        self.draw()

        while True:
            c = self.stdscr.getch()

            if c == ord('w') or c == ord('k'):
                self.move('up')
            elif c == ord('s') or c == ord('j'):
                self.move('down')
            elif c == ord('a') or c == ord('h'):
                self.move('left')
            elif c == ord('d') or c == ord('l'):
                self.move('right')
            elif c == ord('q'):
                break
            self.draw()


def main():
    if len(sys.argv) != 2:
        print usage
        sys.exit(1)
    puzzle = sys.argv[1]
    with GUI(puzzle) as g:
        g.run()
if __name__ == "__main__":
    main()
