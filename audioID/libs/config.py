import json
import os.path

dirPath = os.path.dirname(os.path.realpath(__file__))
CONFIG_DEFAULT_FILE = f'{dirPath}/../config.json'
CONFIG_DEVELOPMENT_FILE = f'{dirPath}/../config-development.json'

# load config from multiple files,
# and return merged result
def get_config():
  defaultConfig = {"env": "unknown"}

  # print(os.getcwd())
  # print(CONFIG_DEFAULT_FILE)
  # print(f'Config debug: {parse_config(CONFIG_DEFAULT_FILE)}')

  mergedConfig = merge_configs(
    defaultConfig,
    parse_config(CONFIG_DEFAULT_FILE),
    parse_config(CONFIG_DEVELOPMENT_FILE)
  )

  mergedConfig['db.file'] = f'{dirPath}/../{mergedConfig["db.file"]}'

  return mergedConfig

# parse config from specific filename
# will return empty config if file not exists, or isn't readable
def parse_config(filename):
  config = {}

  if os.path.isfile(filename):
    f = open(filename, 'r')
    config = json.load(f)
    f.close()

  return config

# @merge multiple dicts into one
def merge_configs(*configs):
  z = {}

  for config in configs:
    z.update(config)

  return z
