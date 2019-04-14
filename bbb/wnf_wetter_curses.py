#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Zum Testen dieses Kommando unter Geany-Erstellen eintragen
# konsole -e sh -c "python ./%f"
# oder mit
# python "./%f"

# Literatur:
# http://de.wikibooks.org/wiki/Python_unter_Linux:_Curses#Curses_Funktionen

# Import curses module

import curses, datetime, time


def printStatus(w):
    w.erase()
    w.box()
    #w.addstr(1, 1, 'Weckzeit 1: %1' % (ini.weckZeit_1()))
    #w.addstr(2, 1, 'Weckzeit 2: %1' % (ini.weckZeit_2()))


def anzeige(stdscr):

    # Get the screen size
    max_y, max_x = stdscr.getmaxyx()

    # Calculate the clock position relative to the screen size
    clock_x = max_x - 28

    # Draw the clock
    # Ein Fenster kann mit curses.newwin(Höhe, Breite, Y0, X0) erzeugt werden.
    # Die Parameter sind ungewöhnlich, stehen hier Y-Werte vor den
    # betreffenden X-Werten. Das ist eine Besonderheit der Terminal-Bibliotheken
    # curses und ncurses und war schon immer so.
    clockWindow = curses.newwin(max_y, max_x, 0, 0)
    clockWindow.bkgd(' ', curses.color_pair(2))
    clockWindow.box()
    clockWindow.refresh()

    clockWindow.addstr(max_y - 2, 1, "Ende mit q")
    # Der EeePC hat ein Display von 100x30 Zeichen
    # BigFont Hoehe = 22 Breite = 16
    h = 22 + 2
    w = 16 * 8 + 4
    h = 24
    w = 83
    digiWindow = curses.newwin(h, w, int(round((max_y - h) / 2)), int(round((max_x - w) / 2)))
    digiWindow.bkgd(' ', curses.color_pair(1))
    digiWindow.box()
    t = "23:59:59"
    #printBigFontZeit(digiWindow, 1, 2, t)
    digiWindow.refresh()

    while True:
        dt = datetime.datetime.today()

        digiWindow.refresh()
        s = dt.strftime('mm:ss')
        clockWindow.addstr(1, 1, s)
        # Cursor parken
        clockWindow.addstr(max_y - 2, 1, "q-Quit s-Status u-Uhr n-Nacht ein/aus m-Musik ein/aus")
        # s = 'Max_X %d Max_Y %d' % (max_x,max_y)
        # clockWindow.addstr(max_y-2, 1, s)
        clockWindow.refresh()
        stdscr.nodelay(1)
        c = stdscr.getch()
        if c == ord('q'):
            curses.beep()
            break
        else:
            time.sleep(1)


def main(stdscr):
    stdscr = curses.initscr()
    # Usually curses applications turn off automatic echoing of keys to
    # the screen, in order to be able to read keys and only display them
    # under certain circumstances. This requires calling the noecho() function.
    curses.noecho()
    # Applications will also commonly need to react to keys instantly,
    # without requiring the Enter key to be pressed; this is called cbreak mode,
    # as opposed to the usual buffered input mode.
    curses.cbreak()
    # Terminals usually return special keys, such as the cursor keys or
    # navigation keys such as Page Up and Home, as a multibyte escape sequence.
    # While you could write your application to expect such sequences and
    # process them accordingly, curses can do it for you, returning a
    # special value such as curses.KEY_LEFT.
    # To get curses to do the job, you’ll have to enable keypad mode.
    stdscr.keypad(1)
    # Define global colour scheme
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)

    # Bring up the clock function

    anzeige(stdscr)

    # Terminating a curses application is much easier than starting one.
    # You’ll need to call

    curses.nocbreak();
    stdscr.keypad(0);
    curses.echo()
    # to reverse the curses-friendly terminal settings.
    # Then call the endwin() function to restore the terminal to its
    # original operating mode.
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
