import io
import re
import subprocess
import sys
import argparse

#https://github.com/shiena/ansicolor/blob/master/README.md
# costants for colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
GRAY = "\033[1;30m"
CLOSE = "\033[m"


def enable_verbose_logging():
    """Enable verbose logging mode.

    Returns:
        proc (Popen): Instance of the Popen class. 
    """
    try:
        subprocess.run("adb shell setprop log.tag.GAv4-SVC DEBUG".split(" "))
        proc = subprocess.Popen("adb logcat -v time -s GAv4-SVC".split(" "), stdout=subprocess.PIPE)
    except:
        print(f"Oops. There was an error. Make sure 'adb' is installed.")
        sys.exit(1)
    else:
        return proc


def no_arguments():
    """Shows event tags and screenview tags being saved to the database. That is, these hits will still be sent later.
    """
    proc = enable_verbose_logging()

    re_hit_saved = re.compile(r'Hit\ saved\ to\ database')
    re_event = re.compile(r't=event')
    re_screenview = re.compile(r't=screenview')

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if re_hit_saved.search(line):
            line = re.sub(r', ', r'\n', line)
            if re_event.search(line):
                print(f"{YELLOW}{line}{CLOSE}")
            elif re_screenview.search(line):
                print(f"{BLUE}{line}{CLOSE}")
            else:
                pass


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
                line = re.sub(r',\ ', r'\n', line)
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
                line = re.sub(r', ', r'\n', line)
                line = re.sub(term_match.group(), f"{BLUE}{term_match.group()}\033[m", line)
                print(line)
