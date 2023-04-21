import json

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
CAMERAS_CONFIG_JSON_FILENAME = env.str("CAMERAS_CONFIG_JSON_FILENAME")

cameras_config: dict = json.load(open(CAMERAS_CONFIG_JSON_FILENAME, "r"))
