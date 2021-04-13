from configparser import ConfigParser
import sys
import subprocess
import os.path

def build_zoom_link(conf_id, password=""):
    return f"zoommtg://zoom.us/join?action=join&confno={conf_id}&pwd={password}"


def open_zoom(conf_id, password=""):
    zoom_link = build_zoom_link(conf_id, password)
    print(zoom_link)
    return subprocess.run(["xdg-open", zoom_link])


if __name__ == "__main__":
    config = ConfigParser()
    config.read(os.path.expanduser("~/.zoom/config"))

    if len(sys.argv) != 2:
        print("Use: python3 join-zoom.py <meeting-name>")
        exit(-1)

    name = sys.argv[1]
    if name not in config.sections():
        print(f"No meeting with name {name}!")
        exit(-2)

    conf_id = config[name]["id"]
    pw = config[name]["pw"]

    print("joining", name , "Meeting-ID:", conf_id)

    result = open_zoom(conf_id, pw)
    exit(result.returncode)

