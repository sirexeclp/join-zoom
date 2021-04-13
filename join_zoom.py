from configparser import ConfigParser
import sys
import subprocess
import webbrowser
import os
import os.path


def build_zoom_link(conf_id, password=""):
    return f"zoommtg://zoom.us/join?action=join&confno={conf_id}&pwd={password}"


def open_zoom(conf_id, password=""):
    zoom_link = build_zoom_link(conf_id, password)
    print(zoom_link)
    return open_url_cross_platform(zoom_link)


def open_url_windows(url):
    return os.startfile(url)


def open_url_mac(url):
    return subprocess.run(["open", url])


def open_url_linux(url):
    return subprocess.run(["xdg-open", url])


def open_url_cross_platform(url):
    """
    Adapted from https://stackoverflow.com/a/4217323
    """
    try:
        if sys.platform=="win32":
            return open_url_windows(url)
        elif sys.platform=='darwin':
            return open_url_mac(url)
        else:
            return open_url_linux(url)
    except OSError:
        return webbrowser.open_new_tab(url)


if __name__ == "__main__":
    print(r"""       _       _                                             
      (_)___  (_)___              ____  ____  ____  ____ ___ 
     / / __ \/ / __ \   ______   /_  / / __ \/ __ \/ __ `__ \
    / / /_/ / / / / /  /_____/    / /_/ /_/ / /_/ / / / / / /
 __/ /\____/_/_/ /_/             /___/\____/\____/_/ /_/ /_/ 
/___/                                                        
""")
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
    if hasattr(result, "returncode") and\
        type(result.returncode) == int:
        exit(result.returncode)

