# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Copyright (C) 2021 TeamUltroid for autobot
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
""" Userbot start point """

import sys

from importlib import import_module
from platform import python_version
from traceback import format_exc

from telethon import version
from telethon.tl.alltlobjects import LAYER

from pyAyiin import ayiin, loop, var


ON = '''
❏ ᴀʏɪɪɴ - ᴜsᴇʀʙᴏᴛ ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪғᴋᴀɴ
╭╼┅━━━━━╍━━━━━┅╾
├▹ ᴀʏɪɪɴ ᴠᴇʀsɪᴏɴ : {} •[{}]•
├▹ ᴜsᴇʀʙᴏᴛ ɪᴅ : {}
├▹ ᴜsᴇʀʙᴏᴛ ɴᴀᴍᴇ : {}
├▹ ᴀssɪsᴛᴀɴᴛ ɪᴅ : {}
├▹ ᴀssɪsᴛᴀɴᴛ ɴᴀᴍᴇ : {}
╰╼┅━━━━━╍━━━━━┅╾
'''


async def AyiinMain():
    await ayiin.start()
    await ayiin.bot.start()
    try:
        ayiin.loadModule("plugins/", display_module=False)
        ayiin.log.info(f"Python Version - {python_version()}")
        ayiin.log.info(f"Telethon Version - {version.__version__} [Layer: {LAYER}]")
        ayiin.log.info(f"Userbot Version - {var.BOT_VER}")
        ayiin.log.info("[✨ BERHASIL DIAKTIFKAN! ✨]")
        await ayiin.checking()
        await ayiin.send_message(var.BOTLOG_CHATID, ON.format(var.BOT_VER, ayiin._host, ayiin.me.id, ayiin.me.first_name, ayiin.bot.me.id, ayiin.bot.me.first_name))
    except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
        pass
    except BaseException as e:
        ayiin.log.info(str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        # ayiin.heroku()
        loop.run_until_complete(AyiinMain())
    except BaseException:
        ayiin.log.error(format_exc())
        sys.exit()

if len(sys.argv) not in (1, 3, 4):
    ayiin.stop()
else:
    try:
        ayiin.runUntilDisconnect()
    except ConnectionError:
        pass
