from configparser import ConfigParser
import sys
import subprocess
import webbrowser
import os
import os.path
from PyInquirer import prompt
import fire
import pyperclip
from pathlib import Path
import itertools

def add_browsers_win():
    x64_apps = os.environ.get("PROGRAMFILES", "C:\\Program Files")
    x86_apps = os.environ.get("PROGRAMFILES(x86)", "C:\\Program Files (x86)")
    local_apps = os.environ["LOCALAPPDATA"]
    
    app_dirs = [x64_apps, x86_apps, local_apps]
    browsers = [("firefox", "Mozilla Firefox\\firefox.exe"),
        	    ("opera", "Opera\\launcher.exe"),
                ("opera", "Programs\\Opera\\launcher.exe"),
                ("chrome", "Google\\Chrome\\Application\\chrome.exe")
            ]

    for app_dir, (name, browser_path) in itertools.product(app_dirs, browsers):
        path = Path(app_dir) / browser_path
        if path.exists():
            webbrowser.register(name, None, webbrowser.BackgroundBrowser(str(path)))


if sys.platform[:3] == "win":
    add_browsers_win()


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


def join(name=None, conf_id=None, password=None):
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
                    'choices': [s for s in config.sections() if not s.startswith(".")], 
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


class AddConfig:

    def __init__(self):
        self.config_path = os.path.expanduser("~/.zoom/config")
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def zoom(self, name, conf_id, password):
        self.config[name] = {
            "type":"zoom",
            "id": conf_id,
            "password":password
            }

    def browser(self, name, url, browser):
        self.config[name] = {
            "type": "browser",
            "url": url,
            "browser": browser
        }

    def __del__(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)


class NewHandler:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.zoom/config")
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def jitsi(self, room):
        url = self.config[".default"]["jitsi"]
        browser = self.config[".default"]["browser"]
        full_url = f"{url}/{room}"
        print(full_url)
        webbrowser.get(browser).open(full_url)
        pyperclip.copy(full_url)
    
    def default_jitsi(self, url):
        if ".default" not in self.config:
            self.config[".default"] = {}    

        self.config[".default"].update({
            "jitsi": url
        })

    def default_browser(self, name):
        if ".default" not in self.config:
            self.config[".default"] = {}
        
        self.config[".default"].update({
            "browser": name
        })

    def __del__(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)



class CLI:
    def __init__(self):
        self.add = AddConfig()
        self.new = NewHandler()

    def __call__(self, *args, **kwargs):
        join(*args, **kwargs)
    
    def join(self, name=None, conf_id=None, password=None):
        join(name=name, conf_id=conf_id, password=password)
    

if __name__ == "__main__":
    fire.Fire(CLI)
