import sys
import argparse
from platforms_android import firebase, univesal_analytics, appsflyer, gtm
from interface import title, options, clear_screen, verbose_custom


def receive_arguments():
    """Receives and handles the arguments passed in the call to execute the script.

    Returns:
        [argparse.Namespace]: All arguments received.
    """
    parser = argparse.ArgumentParser(description="Activate detailed logging and immediately see the events being sent. Use arguments to filter events or other information.")
    parser.add_argument("-p1", "--pattern1", type=str, help="The first regular expression pattern.")
    parser.add_argument("-p2", "--pattern2", type=str, help="The second regular expression pattern.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    return parser.parse_args()


def user_choice(verbose: bool = False):
    """It displays the platforms (options) and receives the user's choice.

    Args:
        verbose (bool): Determines whether the programme description will be displayed to the user in the platform's choice menu.

    Returns:
        action (str): Index related to the platform option chosen by the user.
    """
    platforms = ["Firebase/GA4", "GA Universal", "AppsFlyer", "Google Tag Manager", "Quit"]
    action = ""
    msg = ""

    while action not in ["0", "1", "2", "3", "4"]:
        clear_screen()
        title("Debug Logs - Android")
        if verbose:
            verbose_custom()
        options(platforms, msg)

        action = input(str("Option: ")).strip()
        msg = "\033[31mInvalid option. Choose between 0, 1, 2, 3 or 4.\033[m"
        
    return action


if __name__ == "__main__":
    args = receive_arguments()
    action = user_choice(True) if args.verbose else user_choice()

    if (len(sys.argv) == 1):
        if action == "0":
            firebase.no_arguments()
        elif action == "1":
            univesal_analytics.no_arguments()
        # options without filter
        elif action == "2":
            appsflyer.appsFlyer()
        elif action == "3":
            gtm.main()
        elif action == "4":
            pass
    
    else:
        if action == "0":
            firebase.with_arguments(args)
        elif action == "1":
            univesal_analytics.with_arguments(args)
        # options without filter
        elif action == "2":
            appsflyer.appsFlyer()
        elif action == "3":
            gtm.main()
        elif action == "4":
            pass
    
    print("\033[1;32mFinished.\033[m")
    sys.exit(0)
