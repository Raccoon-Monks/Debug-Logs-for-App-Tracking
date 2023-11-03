import os

#https://github.com/shiena/ansicolor/blob/master/README.md
# costants for colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_GRAY = "\033[1;90m"
CLOSE = "\033[m"
DETECTIVE_EMOJI = "\U0001F575"


def title(txt: str):
    """Prints the title in the menu.

    Args:
        txt (str): Title to be printed.
    """
    print(f"{BLUE}" + "-" * 37 + f"{CLOSE}", end=f"\n{GREEN}")
    print(f"{DETECTIVE_EMOJI}  {txt}".center(37), end=f"{CLOSE}\n")
    print(f"{BLUE}" + "-" * 37 + f"{CLOSE}")


def options(platforms: list, msg: str = ""):
    """Prints the platforms to be chosen by the user.

    Args:
        platforms (list): list of available platforms.
        msg (str, optional): error message. Defaults to "".
    """
    print(f"{LIGHT_GRAY}After choosing the platform and \nthe logs are being displayed, to \nstop press 'CTRL + C'.{CLOSE}\n")
    print("Choose the platform:")
    for i, platform in enumerate(platforms):
        print(f"[{i}] - {platform}")
    print(msg)
    

def clear_screen():
    """Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def verbose_custom():
    """Prints text describing the purpose of the script.
    """
    text = f"Use this script to immediately observe \nthe triggering of events, helping you \nto verify that events are being sent. \nThe script only enables detailed \nlogging, allowing you to check that \nevents are being logged correctly by \nthe SDK. This includes both manually \nand automatically logged events.\n\nColor pattern: \n\t{BLUE}blue log{CLOSE} - screenview \n\t{YELLOW}yellow log{CLOSE} - event \n\t{LIGHT_GRAY}gray log{CLOSE} - automatic\n"
    print(text)


if __name__ == "__main__":
    title("Debug Logs")
    