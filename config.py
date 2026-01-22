

from functions.general import (
    load_json
)

#Loads Static Lists once at startup
MOD_LIST = load_json("mods.json")
MESSAGE_LIST = load_json("messages.json")

#Flags
TASK_FLAG = False

#Constants
seconds = 60
width = "500"
height = "800"

AUTOSAVE_TIMER = int(3 * seconds)
CHATBOX_LIMIT = 10
WINDOW_SIZE = f"{width}x{height}"

FIRST_AD = int(1 * seconds)
AD_LENGTH = int(1.5 * seconds)
AD_TIMER = int(30 * seconds)
AD_SPACING = int(2 * seconds)
AD_ALERT = int(AD_TIMER - AD_SPACING)
MESSAGE_DELAY = int(12 * seconds)