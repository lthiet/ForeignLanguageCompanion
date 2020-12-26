import configparser
import os
print('hi')
cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), 'config.ini'))
