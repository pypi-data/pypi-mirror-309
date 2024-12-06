# Credits: @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# autopilot by @kenkan

import asyncio
import importlib
import logging
import os
import random
import sys
from pathlib import Path
from random import randint
from traceback import format_exc

from telethon.tl.functions.contacts import UnblockRequest
from telethon.errors import ChannelsTooMuchError
from telethon.tl.functions.channels import CreateChannelRequest, EditAdminRequest, EditPhotoRequest, InviteToChannelRequest
from telethon.tl.types import ChatPhotoEmpty, InputChatUploadedPhoto, ChatAdminRights
from telethon.utils import get_peer_id

import pyAyiin

from pyAyiin.config import var
# from AyiinXd import (
#     Ayiin,
#     CMD_HELP,
#     LOGS,
# )


new_rights = ChatAdminRights(
    add_admins=True,
    invite_users=True,
    change_info=True,
    ban_users=True,
    delete_messages=True,
    pin_messages=True,
    manage_call=True,
)


class Utils:
    async def chatTittle(self: "pyAyiin.pyAyiin", ctitle):
        string = ctitle
        font1 = list("𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ")
        font2 = list("𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅")
        font3 = list("𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩")
        font4 = list("𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵")
        font5 = list("𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ")
        font6 = list("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
        font26 = list("𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙")
        font27 = list("𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭")
        font28 = list("𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡")
        font29 = list("𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕")
        font30 = list("𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉")
        font1L = list("𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷")
        font2L = list("𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟")
        font3L = list("𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃")
        font4L = list("𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏")
        font5L = list("𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")
        font6L = list("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")
        font27L = list("𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳")
        font28L = list("𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇")
        font29L = list("𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻")
        font30L = list("𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯")
        font31L = list("𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣")
        normal = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        normalL = list("abcdefghijklmnopqrstuvwxyz")
        # small = list("ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘʀsᴛᴜᴠᴡxʏᴢ")
        cout = 0
        for XCB in font1:
            # string = string.replace(small[cout], normal[cout])
            string = string.replace(font1[cout], normal[cout])
            string = string.replace(font2[cout], normal[cout])
            string = string.replace(font3[cout], normal[cout])
            string = string.replace(font4[cout], normal[cout])
            string = string.replace(font5[cout], normal[cout])
            string = string.replace(font6[cout], normal[cout])
            string = string.replace(font26[cout], normal[cout])
            string = string.replace(font27[cout], normal[cout])
            string = string.replace(font28[cout], normal[cout])
            string = string.replace(font29[cout], normal[cout])
            string = string.replace(font30[cout], normal[cout])
            string = string.replace(font1L[cout], normalL[cout])
            string = string.replace(font2L[cout], normalL[cout])
            string = string.replace(font3L[cout], normalL[cout])
            string = string.replace(font4L[cout], normalL[cout])
            string = string.replace(font5L[cout], normalL[cout])
            string = string.replace(font6L[cout], normalL[cout])
            string = string.replace(font27L[cout], normalL[cout])
            string = string.replace(font28L[cout], normalL[cout])
            string = string.replace(font29L[cout], normalL[cout])
            string = string.replace(font30L[cout], normalL[cout])
            string = string.replace(font31L[cout], normalL[cout])
            cout += 1
        return string

    async def autoPilot(self: "pyAyiin.pyAyiin"):
        if not self.is_connected():
            try:
                await self.start()
            except:
                pass

        self.log.info("TUNGGU SEBENTAR. SEDANG MEMBUAT GROUP LOG USERBOT UNTUK ANDA")
        try:
            r = await self(
                CreateChannelRequest(
                    title="Aʏɪɪɴ-Usᴇʀʙᴏᴛ Lᴏɢs",
                    about="» Group log Created by: Ayiin-Userbot\n\n» Support : @AyiinChats\n» Support: @AyiinChannel",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError:
            self.log.info(
                "Channel dan Group Anda Melebihi batas, Hapus Salah Satu Dan Restart Lagi"
            )
            exit(1)
        except BaseException:
            self.log.info(
                "Terjadi kesalahan, Buat sebuah grup lalu isi id nya di config var BOTLOG_CHATID."
            )
            exit(1)
        chat = r.chats[0]
        channel = get_peer_id(chat)
        if isinstance(chat.photo, ChatPhotoEmpty):
            randomImage = random.choice([
                "assets/logs1.png",
                "assets/logs2.png",
            ])
            ll = await self.upload_file(randomImage)
            try:
                await self(
                    EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
                )
            except BaseException as er:
                self.log.exception(er)
        if not str(chat.id).startswith("-100"):
            Value_id = "-100" + str(chat.id)
        else:
            Value_id = str(chat.id)
        await self.setVarValue("BOTLOG_CHATID", Value_id)
        os.execvp(sys.executable, [sys.executable, "-m", "AyiinXd"])


    async def autoBot(self: "pyAyiin.pyAyiin"):
        if not self.is_connected():
            try:
                await self.start()
            except:
                pass

        await asyncio.sleep(15)
        try:
            await self.send_message(
                var.BOTLOG_CHATID,
                "**MOHON TUNGGU SEBENTAR, SEDANG MEMBUAT ASSISTANT BOT ANDA DI @BotFather**"
            )
            self.log.info("MOHON TUNGGU SEBENTAR, SEDANG MEMBUAT ASSISTANT BOT ANDA.")
            who = await self.get_me()
            name = f"{who.first_name} Assistant Bot"
            if who.username:
                username = f"{who.username}_bot"
            else:
                username = f"Ayiin{(str(who.id))[5:]}bot"
            bf = "@BotFather"
            await self(UnblockRequest(bf))
            await self.send_message(bf, "/cancel")
            await asyncio.sleep(1)
            await self.send_message(bf, "/start")
            await asyncio.sleep(1)
            await self.send_message(bf, "/newbot")
            await asyncio.sleep(1)
            isdone = (await self.get_messages(bf, limit=1))[0].text
            if isdone.startswith("That I cannot do."):
                self.log.info(
                    "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
                )
                sys.exit(1)
            await self.send_message(bf, name)
            await asyncio.sleep(1)
            isdone = (await self.get_messages(bf, limit=1))[0].text
            if not isdone.startswith("Good."):
                await self.send_message(bf, "My Assistant Bot")
                await asyncio.sleep(1)
                isdone = (await self.get_messages(bf, limit=1))[0].text
                if not isdone.startswith("Good."):
                    self.log.info(
                        "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
                    )
                    sys.exit(1)
            filogo = random.choice(
                [
                    "assets/robot1.png",
                    "assets/robot2.jpg",
                ]
            )
            await self.send_message(bf, username)
            await asyncio.sleep(3)
            isdone = (await self.get_messages(bf, limit=1))[0].text
            await self.send_read_acknowledge("botfather")
            await asyncio.sleep(3)
            if isdone.startswith("Sorry,"):
                ran = randint(1, 100)
                username = f"Ayiin{(str(who.id))[6:]}{str(ran)}bot"
                await self.send_message(bf, username)
                await asyncio.sleep(3)
                nowdone = (await self.get_messages(bf, limit=1))[0].text
                if nowdone.startswith("Done!"):
                    token = nowdone.split("`")[1]
                    await self.send_message(bf, "/setinline")
                    await asyncio.sleep(1)
                    await self.send_message(bf, f"@{username}")
                    await asyncio.sleep(1)
                    await self.send_message(bf, "Search")
                    await asyncio.sleep(3)
                    await self.send_message(bf, "/setuserpic")
                    await asyncio.sleep(1)
                    await self.send_message(bf, f"@{username}")
                    await asyncio.sleep(1)
                    await self.send_file(bf, filogo)
                    await asyncio.sleep(3)
                    await self.send_message(bf, "/setabouttext")
                    await asyncio.sleep(1)
                    await self.send_message(bf, f"@{username}")
                    await asyncio.sleep(1)
                    await self.send_message(bf, f"Managed With ✨ By {who.first_name}")
                    await asyncio.sleep(3)
                    await self.send_message(bf, "/setdescription")
                    await asyncio.sleep(1)
                    await self.send_message(bf, f"@{username}")
                    await asyncio.sleep(1)
                    await self.send_message(
                        bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @AyiinChannel ✨"
                    )
                    await self.send_message(
                        var.BOTLOG_CHATID,
                        f"**BERHASIL MEMBUAT ASSISTANT BOT ANDA DENGAN USERNAME @{username}**",
                    )
                    self.log.info(
                        f"BERHASIL MEMBUAT ASSISTANT BOT ANDA DENGAN USERNAME @{username}")
                    try:
                        await self(InviteToChannelRequest(int(var.BOTLOG_CHATID), [username]))
                        await asyncio.sleep(3)
                    except BaseException:
                        pass
                    try:
                        await self(EditAdminRequest(var.BOTLOG_CHATID, username, new_rights, "Assɪsᴛᴀɴᴛ Aʏɪɪɴ"))
                        await asyncio.sleep(3)
                    except BaseException:
                        pass
                    await self.send_message(
                        var.BOTLOG_CHATID,
                        "**SEDANG MERESTART USERBOT HARAP TUNGGU.**",
                    )
                    await self.setVarValue("BOT_TOKEN", token)
                    await self.setVarValue("BOT_USERNAME", f"{username}")
                    os.execvp(sys.executable, [sys.executable, "-m", "AyiinXd"])
                else:
                    self.log.info(
                        "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
                    )
                    sys.exit(1)
            elif isdone.startswith("Done!"):
                token = isdone.split("`")[1]
                await self.send_message(bf, "/setinline")
                await asyncio.sleep(1)
                await self.send_message(bf, f"@{username}")
                await asyncio.sleep(1)
                await self.send_message(bf, "Search")
                await asyncio.sleep(3)
                await self.send_message(bf, "/setuserpic")
                await asyncio.sleep(1)
                await self.send_message(bf, f"@{username}")
                await asyncio.sleep(1)
                await self.send_file(bf, filogo)
                await asyncio.sleep(3)
                await self.send_message(bf, "/setabouttext")
                await asyncio.sleep(1)
                await self.send_message(bf, f"@{username}")
                await asyncio.sleep(1)
                await self.send_message(bf, f"Managed With ✨ By {who.first_name}")
                await asyncio.sleep(3)
                await self.send_message(bf, "/setdescription")
                await asyncio.sleep(1)
                await self.send_message(bf, f"@{username}")
                await asyncio.sleep(1)
                await self.send_message(
                    bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @AyiinChannel ✨"
                )
                await self.send_message(
                    var.BOTLOG_CHATID,
                    f"**BERHASIL MEMBUAT ASSISTANT BOT ANDA DENGAN USERNAME @{username}**",
                )
                self.log.info(
                    f"BERHASIL MEMBUAT ASSISTANT BOT DENGAN USERNAME @{username}"
                )
                try:
                    await self(InviteToChannelRequest(int(var.BOTLOG_CHATID), [username]))
                    await asyncio.sleep(3)
                except BaseException:
                    pass
                try:
                    await self(EditAdminRequest(var.BOTLOG_CHATID, username, new_rights, "Assɪsᴛᴀɴᴛ Aʏɪɪɴ"))
                    await asyncio.sleep(3)
                except BaseException:
                    pass
                await self.send_message(
                    var.BOTLOG_CHATID,
                    "**SEDANG MERESTART USERBOT HARAP TUNGGU.**",
                )
                await self.setVarValue("BOT_TOKEN", token)
                await self.setVarValue("BOT_USERNAME", f"{username}")
                os.execvp(sys.executable, [sys.executable, "-m", "AyiinXd"])
            else:
                self.log.info(
                    "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
                )
                sys.exit(1)
        except BaseException:
            self.log.info(format_exc())


    def loadModule(
        self,
        path: str,
        exclude: list = [],
        display_module: bool = True
    ):
        listbin = []
        listbin.clear()

        if not os.path.exists(path):
            return print(f"No path found: {path}")

        modules = []
        modules.clear()

        for x in os.listdir(path):
            if x.endswith(".py"):
                if x not in ["__pycache__", "__init__.py"]:
                    modules.append(x.replace(".py", ""))

        py_path_raw = ".".join(path.split("/"))
        py_path = py_path_raw[0:len(py_path_raw) - 1]

        count = 0
        for x in modules:
            if x not in exclude:
                importlib.import_module(py_path + "." + x)
                count += 1
                listbin.append(x)

        if display_module:
            data = sorted(listbin)
            for x in data:
                print(x + " Loaded !")
        return count
