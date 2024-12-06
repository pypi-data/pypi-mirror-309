import dotenv
import logging
import heroku3
import os
import time
import sys

from asyncio import get_event_loop
from logging import getLogger
from math import ceil
from pathlib import Path
from typing import Literal, List

from platform import python_version
from pytgcalls import PyTgCalls, __version__ as tgCallsVersion
from telethon import Button, __version__ as vsc
from telethon.sync import custom
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sync import TelegramClient
from telethon.tl.types import User


from .config import Config, var
from .connection import validateSession
from .lib import Lib
from .storage import Storage


def STORAGE(n):
    return Storage(Path("data") / n)

dotenv.load_dotenv(".env")

logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setLevel(logging.ERROR)
logging.getLogger("telethon.network.connection.connection").setLevel(logging.ERROR)

log = getLogger(__name__)

__copyright__ = "Copyright (C) 2022-present AyiinXd <https://github.com/AyiinXd>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.5.9"
loop = get_event_loop()
startTime = time.time()
cmdHelp = {}


class AyiinBot(TelegramClient, Config):
    me: User
    _telethonVersion: str = vsc
    _pythonVersion: str = python_version()
    _pyTgCallsVersion: str = tgCallsVersion
    _baseVersion: str = __version__
    _ch: str = "@AyiinProjects"
    _gc: str = "@AyiinChats"
    log: logging.Logger = log
    def __init__(
        self,
        apiId: int,
        apiHash: str
    ):
        super().__init__(
            "TG_BOT_TOKEN",
            api_id=apiId,
            api_hash=apiHash,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None,
        )

    def addHandler(self, callback, event = None):
        self.add_event_handler(
            callback,
            event
        )

    async def start(self):
        await super().start(bot_token=var.BOT_TOKEN)
        self.me = await self.get_me()
        self.log.info(f"Robot started as {self.me.first_name}")

    def stop(self):
        super().disconnect()

    def runUntilDisconnect(self):
        super().run_until_disconnected()


class pyAyiin(TelegramClient, Config, Lib):
    __module__ = "telethon"
    tgCalls: PyTgCalls
    bot: AyiinBot
    me: User
    _telethonVersion: str = vsc
    _pythonVersion: str = python_version()
    _pyTgCallsVersion: str = tgCallsVersion
    _baseVersion: str = __version__
    _help: dict = {}
    _ch: str = "@AyiinProjects"
    _devs: List[int] = [
        607067484, # Ayiin
        844432220, # Risman
        883761960, # Ari
        2130526178, # Alfa
        1663258664, # Kyy
    ]
    _gc: str = "@AyiinChats"
    _host: Literal['heroku', 'railway', 'qovery', 'windows', 'github actions', 'termux', 'vps']
    log: logging.Logger = log
    def __init__(
        self,
        apiId: int,
        apiHash: str,
        stringSession: str
    ):
        super().__init__(
            session=validateSession(stringSession),
            api_id=apiId,
            api_hash=apiHash,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None,
        )
        self.tgCalls = PyTgCalls(self)
        self.bot = AyiinBot(apiId, apiHash)
        self._host = self.where_hosted()
        self.log.info(f"pyAyiin v{self._baseVersion} by @AyiinXd")

    def addHandler(self, callback, event = None):
        self.add_event_handler(
            callback,
            event
        )

    async def start(self):
        await super().start()
        await self.tgCalls.start()
        self.me = await self.get_me()
        self.log.info(f"Userbot started as {self.me.first_name}")

    def stop(self):
        super().disconnect()

    def runUntilDisconnect(self):
        super().run_until_disconnected()

    async def updateRestartMsg(self, chatId, msgId):
        message = (
            f"**Ayiin-UserBot v`{var.BOT_VER}` is back up and running!**\n\n"
            f"**Telethon:** `{self._telethonVersion}`\n"
            f"**Python:** `{self._pythonVersion}`\n"
        )
        await self.edit_message(chatId, msgId, message)
        return True

    async def setVarValue(self, vars, value):
        if self._host == "heroku":
            if var.HEROKU_API_KEY and var.HEROKU_APP_NAME:
                Heroku = heroku3.from_key(var.HEROKU_API_KEY)
                happ = Heroku.app(var.HEROKU_APP_NAME)
                heroku_config = happ.config()
                if vars not in heroku_config:
                    heroku_config[vars] = value
                    self.log.info(f"Berhasil Menambahkan Vars {vars}")
                    return True
                else:
                    heroku_config[vars] = value
                    self.log.info(f"Berhasil Mengubah Vars {vars}")
                    return True
            else:
                self.log.info(
                    "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )
                return
        else:
            path = dotenv.find_dotenv()
            if not path:
                self.log.info(".env file not found.")
            if not dotenv.get_key(path, vars):
                dotenv.set_key(path, vars, value)
                self.log.info(f"Berhasil Menambahkan var {vars}")
                # Restart Bot
                args = [sys.executable, "-m", "pyAyiin"]
                os.execle(sys.executable, *args, os.environ)
            else:
                dotenv.set_key(path, vars, value)
                self.log.info(f"Berhasil Mengubah var {vars}")
                # Restart Bot
                args = [sys.executable, "-m", "pyAyiin"]
                os.execle(sys.executable, *args, os.environ)

    def where_hosted(self) -> Literal['heroku', 'railway', 'qovery', 'windows', 'github actions', 'termux', 'vps']:
        if os.getenv("DYNO"):
            return "heroku"
        if os.getenv("RAILWAY_STATIC_URL"):
            return "railway"
        if os.getenv("KUBERNETES_PORT"):
            return "qovery"
        if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
            return "windows"
        if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
            return "github actions"
        if os.getenv("ANDROID_ROOT"):
            return "termux"
        return "vps"

    def heroku(self):
        if self._host == "Heroku":
            if var.HEROKU_API_KEY and var.HEROKU_APP_NAME:
                try:
                    Heroku = heroku3.from_key(var.HEROKU_API_KEY)
                    HAPP = Heroku.app(var.HEROKU_APP_NAME)
                    self.log.info(f"Heroku App Configured")
                except BaseException as e:
                    self.log.error(e)
                    self.log.info(
                        f"Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku."
                    )
            else:
                self.log.info(
                    "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
                )

    def paginateHelp(self, page_number, loaded_modules, prefix):
        number_of_rows = 6
        number_of_cols = 2
        global looters
        looters = page_number
        helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
        helpable_modules = sorted(helpable_modules)
        modules = [
            custom.Button.inline(
                "{}".format(x),
                data="ub_modul_{}".format(x),
            )
            for x in helpable_modules
        ]
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
            )
        )
        if len(modules) % number_of_cols == 1:
            pairs.append((modules[-1],))
        max_num_pages = ceil(len(pairs) / number_of_rows)
        modulo_page = page_number % max_num_pages
        if len(pairs) > number_of_rows:
            pairs = pairs[
                modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
            ] + [
                (
                    custom.Button.inline(
                        "«", data="{}_prev({})".format(prefix, modulo_page)
                    ),
                    custom.Button.inline(
                        "×", data="{}_close({})".format(prefix, modulo_page)
                    ),
                    custom.Button.inline(
                        "»", data="{}_next({})".format(prefix, modulo_page)
                    ),
                )
            ]
        return pairs


    def buildKeyboard(self, buttons):
        keyb = []
        for btn in buttons:
            if btn[2] and keyb:
                keyb[-1].append(Button.url(btn[0], btn[1]))
            else:
                keyb.append([Button.url(btn[0], btn[1])])
        return keyb


ayiin = pyAyiin(var.API_KEY, var.API_HASH, var.STRING_SESSION)


if not var.BOTLOG_CHATID:
    loop.run_until_complete(ayiin.autoPilot())
if not var.BOT_TOKEN:
    loop.run_until_complete(ayiin.autoBot())
