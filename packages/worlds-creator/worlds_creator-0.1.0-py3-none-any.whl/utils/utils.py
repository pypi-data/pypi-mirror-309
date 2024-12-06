from .colors import BRIGHT_CYAN, BRIGHT_MAGENTA, RESET, YELLOW


def print_main_menu_text():
    print(
        f"{BRIGHT_MAGENTA}1. View Worlds{RESET}\n"
        f"{BRIGHT_CYAN}2. Create World{RESET}\n"
        f"{YELLOW}x. Exit{RESET}"
    )
