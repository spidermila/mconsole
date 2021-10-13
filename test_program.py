import curses

from mconsole import MConsole


def main(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)
    curses.mousemask(1)

    mc = MConsole(stdscr)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    main_menu = ['Mouse Test', 'Play Dices', 'Exit']
    yesno_menu = ['Yes', 'No']

    while True:
        choice = False
        while choice is False:
            stdscr.clear()
            choice = mc.menu_input(stdscr, main_menu, 'Main Menu')
            # print_center(stdscr, "You selected '{}'".format(choice))

        if choice.lower() == 'exit':
            stdscr.clear()
            yesno = mc.menu_input(stdscr, yesno_menu, 'Are you sure?')
            if yesno.lower() == 'yes':
                return
            else:
                pass

        if choice.lower() == 'mouse test':
            return

        if choice.lower() == 'play dices':
            return

        else:
            pass


if __name__ == '__main__':
    raise SystemExit(curses.wrapper(main))
