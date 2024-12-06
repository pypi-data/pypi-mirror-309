# Copyright (C) 2020 Adek Maulana
#
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#


import importlib.util
import aiofiles
import aiohttp
import asyncio
import hashlib
import importlib
import logging
import math
import os
import os.path
import re
import shlex
import sys
import time
from os.path import basename
from typing import Optional, Tuple, Union
from urllib.request import urlretrieve
from pathlib import Path


from emoji import get_emoji_regexp
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from html_telegraph_poster import TelegraphPoster
from PIL import Image
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    DocumentAttributeFilename,
)
from yt_dlp import YoutubeDL


from pyAyiin import ayiin, cmdHelp
from pyAyiin.exception import CancelProcess
from pyAyiin.utils import eod, eor

from .FastTelethon import download_file as downloadable


async def install_requirements():
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return ayiin.log.info(e)


def deEmojify(inputString):
    return get_emoji_regexp().sub("", inputString)


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def media_type(message):
    if message:
        if message.photo:
            return "Photo"
        if message.audio:
            return "Audio"
        if message.voice:
            return "Voice"
        if message.video_note:
            return "Round Video"
        if message.gif:
            return "Gif"
        if message.sticker:
            return "Sticker"
        if message.video:
            return "Video"
        if message.document:
            return "Document"
    return None



async def progress(
    current,
    total,
    gdrive,
    start,
    prog_type,
    file_name=None,
    is_cancelled=False
):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 15.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Uploading"
        elif "download" in prog_type.lower():
            status = "Downloading"
        else:
            status = "Unknown"
        progress_str = "`{0}` | `[{1}{2}] {3}%`".format(
            status,
            "".join("●" for _ in range(math.floor(percentage / 10))),
            "".join("○" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = (
            f"{progress_str}\n"
            f"`{humanbytes(current)} of {humanbytes(total)}"
            f" @ {humanbytes(speed)}`\n"
            f"**ETA :**` {time_formatter(eta)}`\n"
            f"**Duration :** `{time_formatter(elapsed_time)}`"
        )
        try:
            if file_name:
                await gdrive.edit(
                    f"**{prog_type}**\n\n"
                    f"**Nama File : **`{file_name}`**\nStatus**\n{tmp}"
                )
            else:
                await gdrive.edit(f"**{prog_type}**\n\n" f"**Status**\n{tmp}")
        except MessageNotModifiedError:
            pass



async def downloader(filename, file, event, taime, msg):
    with open(filename, "wb") as fk:
        result = await downloadable(
            client=event.client,
            location=file,
            out=fk,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


def humanbytes(size: Union[int, float]) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} hari, " if days else "")
        + (f"{str(hours)} jam, " if hours else "")
        + (f"{str(minutes)} menit, " if minutes else "")
        + (f"{str(seconds)} detik, " if seconds else "")
    )

    return tmp[:-2]


async def extract_time(yins, time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d", "w")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await yins.edit("Jumlah waktu yang ditentukan tidak valid.")
            return None
        if unit == "s":
            bantime = int(time.time() + int(time_num) * 1)
        elif unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        elif unit == "w":
            bantime = int(time.time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            await yins.edit(
                f"**Jenis waktu yang dimasukan tidak valid. Harap masukan** s, m , h , d atau w tapi punya: `{time_val[-1]}`"
            )
            return None
        return bantime
    await yins.edit(
        f"**Jenis waktu yang dimasukan tidak valid. Harap Masukan** s, m , h , d atau w tapi punya: `{time_val[-1]}`"
    )
    return None


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2**20,
        "MB": 2**20,
        "G": 2**30,
        "GB": 2**30,
        "T": 2**40,
        "TB": 2**40,
    }

    size = size.upper()
    if not re.match(r" ", size):
        size = re.sub(r"([KMGT])", r" \1", size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])


async def is_admin(chat_id, user_id):
    req_jo = await ayiin(GetParticipantRequest(channel=chat_id, user_id=user_id))
    chat_participant = req_jo.participant
    return isinstance(
        chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
    )


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot"""
    ayiin.log.info(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join("./temp/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        ayiin.log.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in ayiin.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def check_media(reply_message):
    if not reply_message or not reply_message.media:
        return False

    if reply_message.photo:
        data = reply_message.photo
    elif reply_message.document:
        if (
            DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
            in reply_message.media.document.attributes
        ):
            return False
        if (
            reply_message.gif
            or reply_message.video
            or reply_message.audio
            or reply_message.voice
        ):
            return False
        data = reply_message.media.document
    else:
        return False
    if not data or data is None:
        return False
    return data


async def run_cmd(cmd: list) -> Tuple[bytes, bytes]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await process.communicate()
    t_resp = out.strip()
    e_resp = err.strip()
    return t_resp, e_resp


# https://github.com/TeamUltroid/pyUltroid/blob/31c271cf4d35ab700e5880e952e54c82046812c2/pyUltroid/functions/helper.py#L154


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


def post_to_telegraph(title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "Ayiin-Userbot"
    auth_url = "https://github.com/AyiinXd/Ayiin-Userbot"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=auth_url,
        text=html_format_content,
    )
    return post_page["url"]


async def media_to_pic(event, reply):
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Round Video", "Gif", "Sticker", "Video"]:
        await eod(
            event,
            "**Saya tidak dapat mengekstrak gambar untuk memproses lebih lanjut ke media yang tepat**",
        )
        return None
    media = await reply.download_media(file="./temp")
    event = await eor(event, "`Transfiguration Time! Converting....`")
    file = os.path.join("./temp/", "meme.png")
    if mediatype == "Sticker" and media.endswith(".tgs"):
        await runcmd(
            f"lottie_convert.py --frame 0 -if lottie -of png '{media}' '{file}'"
        )
    elif (
        mediatype == "Sticker"
        and not media.endswith(".tgs")
        and media.endswith(".webp")
        or mediatype not in ["Sticker", "Round Video", "Video", "Gif"]
    ):
        im = Image.open(media)
        im.save(file)
    elif mediatype != "Sticker" or media.endswith(".tgs") or media.endswith(".webp"):
        extractMetadata(createParser(media))
        await runcmd(f"rm -rf '{file}'")
        await take_screen_shot(media, 0, file)
        if not os.path.exists(file):
            await eod(
                event,
                f"**Maaf. Saya tidak dapat mengekstrak gambar dari ini {mediatype}**",
            )
            return None
    await runcmd(f"rm -rf '{media}'")
    return [event, file, mediatype]


ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "noprogress": True,
    "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "extractor-args": "youtube:player_client=all",
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download_lagu(url: str) -> str:
    info = ydl.extract_info(url, download=False)
    ydl.download([url])
    return os.path.join("downloads", f"{info['id']}.{info['ext']}")


async def download_file(link, name):
    """for files, without progress callback with aiohttp"""
    if not aiohttp:
        urlretrieve(link, name)
        return name
    async with aiohttp.ClientSession() as ses:
        async with ses.get(link) as re_ses:
            file = await aiofiles.open(name, "wb")
            await file.write(await re_ses.read())
            await file.close()
    return name


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"plugins/{shortname}.py")
        name = "AyiinXd.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ayiin.log.info("Successfully imported " + shortname)
    else:

        path = Path(f"plugins/{shortname}.py")
        name = "plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.ayiin = ayiin
        mod.log = ayiin.log
        mod.cmdHelp = cmdHelp
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["AyiinXd.modules." + shortname] = mod
        ayiin.log.info("Successfully imported " + shortname)


def remove_plugin(shortname):
    try:
        try:
            for i in cmdHelp[shortname]:
                ayiin.remove_event_handler(i)
            del cmdHelp[shortname]

        except BaseException:
            name = f"plugins.{shortname}"

            for i in reversed(range(len(ayiin._event_builders))):
                ev, cb = ayiin._event_builders[i]
                if cb.__module__ == name:
                    del ayiin._event_builders[i]
    except BaseException:
        raise ValueError
