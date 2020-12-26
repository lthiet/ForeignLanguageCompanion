import configparser
import os
cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), 'config.ini'))
