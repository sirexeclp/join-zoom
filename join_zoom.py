from configparser import ConfigParser
import sys
import subprocess
import webbrowser
import os
import os.path
from PyInquirer import prompt
import fire


def build_zoom_link(conf_id, password=""):
    return f"zoommtg://zoom.us/join?action=join&confno={conf_id}&pwd={password}"


def build_jitsi_link(url, room):
    return f"{url}/{room}"


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


def get_info_from_config(name, config):    
    if name not in config.sections():
        print(f"No meeting with name {name}!")
        exit(-2)
    
    conf_id = config[name]["id"]
    pw = config[name]["pw"]
    return conf_id, pw

def join_browser(name, config):
    url = config[name]["url"]
    browser = config[name]["browser"]
    print(url)
    return webbrowser.get(browser).open(url)


def join_zoom_from_config(name, config):
    info = get_info_from_config(name=name, config=config)
    return open_zoom(*info)


def open_entry(name, config):
    functions = {
        "zoom": join_zoom_from_config,
        "browser": join_browser
    }
    conf_type = config[name].get("type", "zoom")
    print("joining", name, "type:", conf_type) # , "Meeting-ID:", conf_id)
    return functions[conf_type](name=name, config=config)


def main(name=None, conf_id=None, password=None):
    print(r"""       _       _                                             
      (_)___  (_)___              ____  ____  ____  ____ ___ 
     / / __ \/ / __ \   ______   /_  / / __ \/ __ \/ __ `__ \
    / / /_/ / / / / /  /_____/    / /_/ /_/ / /_/ / / / / / /
 __/ /\____/_/_/ /_/             /___/\____/\____/_/ /_/ /_/ 
/___/                                                        
""")
    config = ConfigParser()
    config.read(os.path.expanduser("~/.zoom/config"))
    
    if not (conf_id and password):
        if not name:
            questions = [
                {
                    'type': 'list',
                    'choices':config.sections(), 
                    'name': 'meeting',
                    'message': 'Please select the meeting you want to join:',
                }
            ]
            answers = prompt(questions)
            name = answers["meeting"]
        
        result = open_entry(name=name, config=config)
        if hasattr(result, "returncode") and type(result.returncode) == int:
            exit(result.returncode)
        return

    result = open_zoom(conf_id, pw)
    if hasattr(result, "returncode") and type(result.returncode) == int:
        exit(result.returncode)


if __name__ == "__main__":
    fire.Fire(main)
