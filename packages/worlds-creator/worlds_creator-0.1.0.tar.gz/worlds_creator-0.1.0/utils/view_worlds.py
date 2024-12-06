import curses
import os
import re
import subprocess

from .colors import BRIGHT_CYAN, BRIGHT_MAGENTA, RESET


def view_worlds():
    while True:
        os.system("clear")
        data_folder = os.path.join(os.getcwd(), "data")

        if not os.path.exists(data_folder):
            print("No worlds found. The 'data' folder does not exist.")
            return

        worlds = [f for f in os.listdir(data_folder) if f.endswith(".yaml")]
        if not worlds:
            print("No worlds found.")
            return

        max_name_length = max(len(f.replace(".yaml", "")) for f in worlds)

        for i, filename in enumerate(worlds, start=1):
            world_name = filename.replace(".yaml", "")
            file_path = os.path.join(data_folder, filename)

            with open(file_path, "r") as file:
                content = file.read()
                t_entries = re.findall(r"^T\d+\.", content, re.MULTILINE)
                task_blocks = " - ".join("#" for _ in t_entries)

                print(
                    f"{BRIGHT_MAGENTA}{i}. {world_name.ljust(max_name_length)}{RESET}"
                )
                print(f"{BRIGHT_CYAN}   {task_blocks}{RESET}\n")

        try:
            selection = input("")
            if selection == "":
                break

            index = int(selection) - 1
            if 0 <= index < len(worlds):
                file_path = os.path.join(data_folder, worlds[index])

                curses.wrapper(display_world_details, file_path)
                subprocess.run(["vim", file_path])

        except ValueError:
            print("Invalid selection. Please enter a number.")


def display_world_details(stdscr, file_path):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Light blue for '#'
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Purple for 'hello'
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    curses.curs_set(0)

    # Read the file content
    with open(file_path, "r") as file:
        content = file.read()

    # Find tasks like "T1.", "T2.", etc.
    tasks = re.findall(r"^T\d+\.", content, re.MULTILINE)

    # Prepare display lines
    display_lines = [
        ("World Details:", curses.color_pair(1)),
        ("Tasks:", curses.A_NORMAL),
    ] + [(task, curses.color_pair(4)) for task in tasks]

    selected_task = 0

    while True:
        stdscr.clear()

        # Display each line with appropriate color
        for i, (line, color) in enumerate(display_lines):
            if i == selected_task + 2:  # Highlight selected line (if needed)
                stdscr.addstr(i, 0, line, curses.color_pair(5))
            else:
                stdscr.addstr(i, 0, line, color)

        stdscr.refresh()

        # Navigation logic (up/down to select, Enter to exit)
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_task > 0:
            selected_task -= 1
        elif key == curses.KEY_DOWN and selected_task < len(tasks) - 1:
            selected_task += 1
        elif key == ord("\n"):
            break
