

from functions.general import (
    load_json
)

#Loads Static Lists once at startup
MOD_LIST = load_json("mods.json")
MESSAGE_LIST = load_json("messages.json")
CHAT_STATS = load_json("chatters.json")
HOARD = load_json("hoard.json")

#Flags
TASK_FLAG = False

#Constants
seconds = 60
width = "500"
height = "800"

AUTOSAVE_TIMER = int(3 * seconds)
CHATBOX_LIMIT = 10
WINDOW_SIZE = f"{width}x{height}"

MESSAGE_DELAY = int(12 * seconds)