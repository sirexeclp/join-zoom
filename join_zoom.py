from configparser import ConfigParser
import sys
import subprocess
import os.path
from PyInquirer import prompt
import fire

def build_zoom_link(conf_id, password=""):
    return f"zoommtg://zoom.us/join?action=join&confno={conf_id}&pwd={password}"


def open_zoom(conf_id, password=""):
    zoom_link = build_zoom_link(conf_id, password)
    print(zoom_link)
    return subprocess.run(["xdg-open", zoom_link])

def get_info_from_config(name, config):    
    if name not in config.sections():
        print(f"No meeting with name {name}!")
        exit(-2)
    
    conf_id = config[name]["id"]
    pw = config[name]["pw"]
    return conf_id, pw


def main(name=None, conf_id=None, password=None):
    config = ConfigParser()
    config.read(os.path.expanduser("~/.zoom/config"))
    
    if not (conf_id and password):
        if not name:
            questions = [
                {
                    'type': 'list',
                    'choices':config.sections(), 
                    'name': 'meeting',
                    'message': 'Which Zoom meeting do you want to join:',
                }
            ]
            answers = prompt(questions)
            name = answers["meeting"]
        
        conf_id, pw = get_info_from_config(name=name, config=config)

    print("joining", name , "Meeting-ID:", conf_id)
    result = open_zoom(conf_id, pw)
    exit(result.returncode)


if __name__ == "__main__":
    fire.Fire(main)
