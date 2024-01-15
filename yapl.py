import os
from json import loads as json_loads
from subprocess import Popen, DEVNULL
from curses import initscr, endwin, KEY_BACKSPACE, KEY_DOWN, KEY_UP, KEY_ENTER
from shlex import split as shlex_split

with open(os.path.expanduser("~/.config/yapl/yapl.json"), "r") as file:
    conf_json = json_loads(file.read())

    term_win = initscr()
    term_win.keypad(True)
    term_column = term_win.getmaxyx()[1]

    ## individual characters of search pattern
    search_buffer = []
    ## at this point, 'selected' variable is just the height of the terminal size
    selected = 2

    while True:

        search_str = "".join(search_buffer)
        sorted_apps = sorted(conf_json.items(), key=lambda x: x[0].lower().startswith(search_str), reverse=True)
        sorted_names = [x[0] for x in sorted_apps]

        term_win.addstr(0, 1, f"Search: {search_str}")

        for x, y in enumerate(sorted_names, 2): 

            if x == selected: 
                term_win.addstr(x, 1, f'>> {y}')
            else:
                term_win.addstr(x, 1, y)

        # move cursor to the first line and to the end of the line
        # the int 9 is the length of a single space indent and the string "Search: "
        # and add 9 to the length of the search buffer
        term_win.move(0, 9+len(search_buffer))

        term_win.refresh()
        char_input = term_win.getch()
        term_win.clear()

        ### EVENTS
        # why isnt there a standard way to deal with backspaces
        if char_input == 8 or char_input == 263 or char_input == 127 or char_input == KEY_BACKSPACE:
            if len(search_buffer) != 0:
                search_buffer.pop(-1)

            continue

        if char_input == 10 or char_input == 13 or char_input == KEY_ENTER:
            cmd = "nohup " + sorted_apps[selected-2][1].get("cmd")
            cmd = shlex_split(cmd)
            env_var = sorted_apps[selected-2][1].get("env_var", {})
            Popen(cmd, env={**os.environ.copy(), **env_var}, cwd=sorted_apps[selected-2][1].get("cwd"), stdout=DEVNULL, stderr=DEVNULL)
            break

        elif char_input == KEY_UP:
            if selected > 2:
                selected -= 1

        elif char_input == KEY_DOWN:
            if selected < len(sorted_apps)+1:
                selected += 1

        else:
            search_buffer.append(chr(char_input))

    endwin()
