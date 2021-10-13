import curses


class ScreenSettings:
    verbose = 1
    blank_character = ' '


class MConsole:
    def __init__(self, stdscr):
        self._y_max, self._x_max = stdscr.getmaxyx()
        self._screen = []
        self._windows = []
        for y in range(self._y_max):
            self._screen.append([])
            for x in range(self._x_max):
                self._screen[y].append(ScreenSettings.blank_character)

    def size_refresh(self, stdscr):
        self.log(
            'screen refreshed, original size: ' +
            str(self._x_max) + ' x ' +
            str(self._y_max) + ' - array size ' +
            str(len(self._screen[0])) + ' x ' + str(len(self._screen)),
        )
        self._y_max, self._x_max = stdscr.getmaxyx()

        # if rows were removed:
        if self._y_max < len(self._screen):
            for y in range(self._y_max, len(self._screen)):
                self.log('removing row: ' + str(self._y_max))
                self._screen.pop(self._y_max)

        for y in range(self._y_max):
            if y > len(self._screen) - 1:  # if rows were added:
                self.log('adding row y: ' + str(y))
                self._screen.append([])
            if len(self._screen[y]) > self._x_max:  # if a column was removed:
                for x in range(self._x_max, len(self._screen[y])):
                    self.log(
                        'removing column: ' +
                        str(y) + ' x ' + str(self._x_max),
                    )
                    self._screen[y].pop(self._x_max)
            else:
                for x in range(self._x_max):
                    if x > len(self._screen[y]) - 1:  # if a column was added
                        self.log('adding column: ' + str(y))
                        self._screen[y].append(ScreenSettings.blank_character)

        self.log(
            'screen refreshed, new size: ' +
            str(self._x_max) + ' x ' +
            str(self._y_max) + ' - array size ' +
            str(len(self._screen[0])) +
            ' x ' + str(len(self._screen)),
        )

    def clear(self, stdscr):
        stdscr.clear()

    def create_window(self, name, xpos, ypos, height, width):
        self._windows.append(Window(name, xpos, ypos, height, width))

    def resize_window(self):
        pass

    def menu_input(self, stdscr, menu, title):
        curses.mouseinterval(0)
        curses.mousemask(-1)
        current_row = 0
        while 1:
            self.print_menu(stdscr, current_row, menu, title)
            key = stdscr.getch()
            if key == curses.KEY_RESIZE:
                stdscr.clear()
                return False
            elif key == curses.KEY_MOUSE:
                _, m_x, m_y, _, mouse_state = curses.getmouse()

                stdscr.clear()
                stdscr.addstr(0, 0, str(mouse_state))

                if mouse_state == 2097152 and current_row < len(menu)-1:
                    current_row += 1
                elif mouse_state == 2097152 and current_row == len(menu)-1:
                    current_row = 0
                elif mouse_state == 65536 and current_row > 0:
                    current_row -= 1
                elif mouse_state == 65536 and current_row == 0:
                    current_row = len(menu)-1
                row_clicked = find_menu_row_by_coords(stdscr, m_x, m_y, menu)
                # stdscr.addstr(1, 1, "clicked")
                # stdscr.getch()
                if -1 < row_clicked == current_row:
                    return menu[current_row]
                elif -1 < row_clicked != current_row:
                    current_row = row_clicked

            elif key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_UP and current_row == 0:
                current_row = len(menu)-1
            elif key == curses.KEY_DOWN and current_row < len(menu)-1:
                current_row += 1
            elif key == curses.KEY_DOWN and current_row == len(menu)-1:
                current_row = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return menu[current_row]

    def print_menu(self, stdscr, selected_row_idx, menu, title):
        h, w = stdscr.getmaxyx()
        self.log(f'{h=}, {w=}')
        # print title
        try:
            stdscr.addstr(h//2 - len(menu)//2 - 2, w//2 - len(title)//2, title)
            for idx, row in enumerate(menu):
                x = w//2 - len(row)//2
                y = h//2 - len(menu)//2 + idx
                if idx == selected_row_idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, row)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, row)
        except Exception as e:
            self.log(f'{e}')
            self.log('not able to print to screen')
        stdscr.refresh()

    def log(self, message):
        if ScreenSettings.verbose == 1:
            f = open('cursetest.log', 'a')
            f.write(str(message) + '\n')
            f.close()
        else:
            pass


class Window:
    def __init__(self, name, xpos, ypos, height, width):
        self._name = name
        self._xpos = xpos
        self._ypos = ypos
        self._height = height
        self._width = width
        self._members = []

    def add_member(self, type, *args):
        self._members.append(locals()[type](*args))

    def center_member(self):
        pass


class TextField:
    def __init__(self, text):
        self._text = text


class MenuWithTitle:
    def __init__(self, title, items):
        self._title = title
        self._items = items


class Menu:
    def __init__(self, items):
        self._items = items


def print_to_row_relative(stdscr, row, position, text, clearscreen=False):
    """parameters: stdscr, row, position, text, clear_screen(default=False)"""

    # TODO - pridat kontrolu velikosti displeje - at nekresli mimo

    position = position.lower()
    y = row
    text = text.split('\n')
    i = 0
    if position == 'center':
        if clearscreen:
            stdscr.clear()
        h, w = stdscr.getmaxyx()
        for t in text:
            x = w//2 - len(text[i])//2
            stdscr.addstr(y + i, x, t)
            i += 1
            # stdscr.refresh()
    elif position == 'left':
        if clearscreen:
            stdscr.clear()
        x = 0
        for t in text:
            stdscr.addstr(y + i, x, text)
            i += 1
            # stdscr.refresh()
    elif position == 'right':
        if clearscreen:
            stdscr.clear()
        h, w = stdscr.getmaxyx()
        for t in text:
            x = w - len(text[i]) - 1
            stdscr.addstr(y + i, x, text)
            i += 1
    else:
        return False


def print_to_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def find_menu_row_by_coords(stdscr, m_x, m_y, menu):
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x_min = w//2 - len(row)//2
        _x_max = x_min + len(row)
        y = h//2 - len(menu)//2 + idx
        if x_min <= m_x < _x_max and m_y == y:
            # log('returning ' + str(idx))
            return idx
    return -1
