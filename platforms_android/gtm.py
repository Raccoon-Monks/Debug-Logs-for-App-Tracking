import io
import re
import subprocess


def edit_log_firing_tag(log):
    """Edits the log to better organize key values.

    Args:
        log (str): log/record to be edited.

    Returns:
        log (str): edited log/record.
        color (str): color to print the log.
    """
    re_caputre_screenview = re.compile(r"vtp_trackType=TRACK_SCREENVIEW")
    re_capture_event = re.compile(r"vtp_trackType=TRACK_EVENT")
    color = "gray"
    if re_capture_event.search(log, re.IGNORECASE):
        color = "yellow"
    elif re_caputre_screenview.search(log, re.IGNORECASE):
        color = "blue"

    log = re.sub(r"V.*tag\ Properties: \{", "GTM Executing firing tag Properties: {\n  ", log)
    log = re.sub(r",\ vtp_", "\n  vpt_", log)
    log = re.sub(r"\},\ \{", "},\n    {", log)
    log = re.sub(r"dimension=\[\{", "dimension=[{\n    ", log)
    log = re.sub(r",\ function=", "\n  function=", log)
    log = re.sub(r",\ tag_id=", "\n  tag_id=", log)
    
    return log, color


def main():
    """Print the triggered tags.
    """
    subprocess.run("adb shell setprop log.tag.GoogleTagManager VERBOSE ".split(" "))
    proc = subprocess.Popen("adb logcat -v time -s GoogleTagManager".split(" "), stdout=subprocess.PIPE)

    re_firing_tag = re.compile(r"Executing\ firing\ tag")
    # Remember to add trigger impressions as well.
    re_evaluating_trigger = re.compile(r"Evaluating\ trigger\ Positive\ predicates")

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if re_firing_tag.search(line):
            line, color = edit_log_firing_tag(line)
            if color == "blue":
                print(f"\033[1;34m{line}\033[m")
            elif color == "yellow":
                print(f"\033[1;33m{line}\033[m")
            else:
                print(f"\033[1;90m{line}\033[m")


if __name__ == "__main__":
    main()