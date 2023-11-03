import io
import re
import subprocess
import sys
import argparse

# costants for colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_GRAY = "\033[1;90m"
CLOSE = "\033[m"

def enable_verbose_logging():
    """Enable verbose logging mode.

    Returns:
        proc (Popen): Instance of the Popen class. 
    """
    try:
        #subprocess.run("adb shell setprop log.tag.FA VERBOSE".split(" "))
        subprocess.run("adb shell setprop log.tag.FA-SVC VERBOSE".split(" "))
        proc = subprocess.Popen("adb logcat -v time -s FA FA-SVC".split(" "), stdout=subprocess.PIPE)
    except:
        print(f"Oops. There was an error. Make sure 'adb' is installed.")
        sys.exit(1)
    else:
        return proc


def edit_log(log: str):
    """Edits the log to better organize key values.

    Args:
        log (str): log/record to be edited.

    Returns:
        log (str): edited log/record.
    """
    log = re.sub(r"\w+\[\{", r"Bundle[{\n", log)
    log = re.sub(r"\}\]", r"\n}]", log)
    log = re.sub(r", |,", r"\n", log)

    return log


def no_arguments():
    """Displays logs of events being logged. 
    """
    proc = enable_verbose_logging()

    re_registered_event = re.compile(r"Logging\ event:")
    screenview_event = re.compile(r'name=screen_view')
    automatic_event = re.compile(r'origin=auto')

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):

        if re_registered_event.search(line, re.IGNORECASE):
            line = edit_log(line)

            if screenview_event.search(line) and not automatic_event.search(line):
                print(f"{BLUE}{line}{CLOSE}")

            elif automatic_event.search(line):
                print(f"{LIGHT_GRAY}{line}{CLOSE}")
            else:
                print(f"{YELLOW}{line}{CLOSE}")


def with_arguments(args: argparse.Namespace):
    """Filters the logs/records based on arguments given by the user.

    Args:
        args (argparse.Namespace): Arguments passed by the user in the call to execute the script.
    """
    if args.pattern1 == None and args.pattern2 == None: # Only -v exists in the call
        no_arguments()

    elif args.pattern1 != None and args.pattern2 != None:
        proc = enable_verbose_logging()
        re_terms = re.compile(rf"{args.pattern1}|{args.pattern2}")

        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            check_terms = list(set(re_terms.findall(line, re.IGNORECASE)))
            
            if len(check_terms) == 2:
                check_terms.sort() # sort - alphabetically
                line = edit_log(line)

                line = re.sub(f"{check_terms[0]}", f"{BLUE}{check_terms[0]}{CLOSE}", line)
                line = re.sub(f"{check_terms[1]}", f"{GREEN}{check_terms[1]}{CLOSE}", line)
                print(line)

    elif args.pattern1 != None or args.pattern2 != None:
        proc = enable_verbose_logging()
        term = args.pattern1 if args.pattern1 != None else args.pattern2
        re_terms = re.compile(rf"{term}")
        
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            term_match = re_terms.search(line, re.IGNORECASE)         
            if term_match:
                line = edit_log(line)
                line = re.sub(term_match.group(), f"{BLUE}{term_match.group()}{CLOSE}", line)
                print(line)