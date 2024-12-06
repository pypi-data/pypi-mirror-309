import os
from dotenv import load_dotenv
from base64 import b64decode


load_dotenv(".env")


def strToBool(value: str = None):
    if value:
        return value.lower() in ("yes", "true", "t", "1")
    else:
        return False


DEVS = [
    607067484, # Ayiin
    844432220, # Risman
    883761960, # Ari
    2130526178, # Alfa
    1663258664, # Kyy
]


GCAST_BLACKLIST = [
    -1001718852988,  # AyiinChats <- New
    -1001675396283,  # AyiinChats
    -1001473548283,  # SharingUserbot
    -1001361294038,  # UltroidSupportChat
    -1001387666944,  # PyrogramChat
    -1001109500936,  # TelethonChat
    -1001050982793,  # Python
    -1001256902287,  # DurovsChat
    -1001433238829,  # TedeSupport
    -1001642830120,  # Aditya Discus
    -1001476936696,  # AnosSupport
    -1001327032795,  # UltroidSupport
    -1001294181499,  # UserBotIndo
    -1001419516987,  # VeezSupportGroup
    -1001459812644,  # GeezSupportGroup
    -1001296934585,  # X-PROJECT BOT
    -1001481357570,  # UsergeOnTopic
    -1001459701099,  # CatUserbotSupport
    -1001109837870,  # TelegramBotIndonesia
    -1001752592753,  # Skyzusupport
    -1001788983303,  # KayzuSupport
    -1001380293847,  # NastySupport
    -1001692751821,  # RamSupport
    -1001267233272,  # PocongUserbot
    -1001500063792,  # Trident
    -1001687155877,  # CilikSupport
    -1001578091827,  # PrimeSupport
    -1001704645461,  # Jamet No Support
    -1001662510083,  # MutualanDestra
    -1001347414136,  # ArunaMutualan
    -1001572486389,  # PluviaMusicGroup
    -1001608701614,  # UputtSupport
    -1001812143750,  # Kynan Support
]


class Config:
    # Telegram App KEY and HASH
    API_KEY = int(os.environ.get("API_KEY") or 0)
    API_HASH = str(os.environ.get("API_HASH") or None)

    # Inline bot helper
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

    SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
    BL_CHAT = {int(x) for x in os.environ.get("BL_CHAT", "").split()}
    BLACKLIST_GCAST = {
        int(x) for x in os.environ.get(
            "BLACKLIST_GCAST",
            "").split()}

    # For Blacklist Group Support
    BLACKLIST_CHAT = os.environ.get("BLACKLIST_CHAT", None)
    if not BLACKLIST_CHAT:
        BLACKLIST_CHAT = [-1001473548283, -1001675396283, -1001718852988]

    # Userbot Session String
    STRING_SESSION = os.environ.get("STRING_SESSION", None)

    # Logging channel/group ID configuration.
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0"))

    # Load or No Load modules
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()

    # Bleep Blop, this is a bot ;)
    PM_AUTO_BAN = strToBool(os.environ.get("PM_AUTO_BAN", "True"))
    PM_LIMIT = int(os.environ.get("PM_LIMIT", 6))

    # Custom Handler command
    CMD_HANDLER = os.environ.get("CMD_HANDLER") or "."
    SUDO_HANDLER = os.environ.get("SUDO_HANDLER", r"$")

    # Support
    GROUP = os.environ.get("GROUP", "AyiinChats")
    CHANNEL = os.environ.get("CHANNEL", "AyiinChannel")

    # Heroku Credentials for updater.
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

    # JustWatch Country
    WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "ID")

    # Github Credentials for updater and Gitupload.
    GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)

    # Custom (forked) repo URL for updater.
    UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO_URL", "https://github.com/AyiinXd/Ayiin-Userbot.git")

    # Custom Name Sticker Pack
    S_PACK_NAME = os.environ.get("S_PACK_NAME", None)

    # SQL Database URI
    DB_URI = os.environ.get("DATABASE_URL", None)
    DATABASE_PATH = os.path.join("ayiin.db")

    # OCR API key
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

    # remove.bg API key
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "jK9nGhjQPtd2Y5RhwMwB5EMA")

    # Chrome Driver and Headless Google Chrome Binaries
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER") or "/usr/bin/chromedriver"
    GOOGLE_CHROME_BIN = os.environ.get(
        "GOOGLE_CHROME_BIN") or "/usr/bin/google-chrome"

    # OpenWeatherMap API Key
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", "Jakarta")

    # Anti Spambot Config
    ANTI_SPAMBOT = strToBool(os.environ.get("ANTI_SPAMBOT", "False"))
    ANTI_SPAMBOT_SHOUT = strToBool(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

    # untuk perintah teks costum .alive
    ALIVE_TEKS_CUSTOM = os.environ.get(
        "ALIVE_TEKS_CUSTOM",
        "Hey, Saya pengguna Ayiin-Userbot")

    # Default .alive name
    ALIVE_NAME = os.environ.get("ALIVE_NAME", "AyiinXd")

    # Custom Emoji Alive
    ALIVE_EMOJI = os.environ.get("ALIVE_EMOJI", "✧")

    # Custom Emoji Alive
    INLINE_EMOJI = os.environ.get("INLINE_EMOJI", "✵")

    # Custom icon HELP
    ICON_HELP = os.environ.get("ICON_HELP", "⍟")

    # Time & Date - Country and Time Zone
    COUNTRY = str(os.environ.get("COUNTRY", "ID"))
    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

    # Clean Welcome
    CLEAN_WELCOME = strToBool(os.environ.get("CLEAN_WELCOME", "True"))

    # Zipfile module
    ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

    # bit.ly module
    BITLY_TOKEN = os.environ.get("BITLY_TOKEN", None)

    # Bot version
    BOT_VER = os.environ.get("BOT_VER", "5.0.0")

    # Default .alive logo
    ALIVE_LOGO = (os.environ.get("ALIVE_LOGO")
                or "https://telegra.ph/file/940f21be8d8863b6c70ae.jpg")

    INLINE_PIC = (os.environ.get("INLINE_PIC")
                or "https://telegra.ph/file/9f8e73d387f25b7f27ce5.jpg")

    # Picture For VCPLUGIN
    PLAY_PIC = (os.environ.get("PLAY_PIC")
                or "https://telegra.ph/file/6213d2673486beca02967.png")

    QUEUE_PIC = (os.environ.get("QUEUE_PIC")
                or "https://telegra.ph/file/d6f92c979ad96b2031cba.png")

    DEFAULT = list(map(int, b64decode("MTkwNTA1MDkwMw==").split()))

    TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY", "./downloads/")

    # Deezloader
    DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN", None)

    # NSFW Detect DEEP AI
    DEEP_AI = os.environ.get("DEEP_AI", None)


var = Config()
