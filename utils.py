import configparser

def init_config():
    config = configparser.ConfigParser()
    config.read("config.cfg")
    return config

def save_config(config):
    with open("config.cfg", "w") as cfg:
        config.write(cfg)