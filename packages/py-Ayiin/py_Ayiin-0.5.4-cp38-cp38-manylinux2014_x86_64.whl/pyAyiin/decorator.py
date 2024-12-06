# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for managing events. One of the main components of the userbot."""

import inspect
import re
import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from functools import partial, wraps
from pathlib import Path
from time import gmtime, strftime
from traceback import format_exc
from typing import Callable, Literal, Optional, Union

from telethon import events

from pyAyiin import ayiin

from .config import var, DEVS
from .database.handler import getHandler
from .database.sudo import getSudo
from .database.sudoHandler import getSudoHandler


def ayiinCmd(
    pattern: str,
    devs: bool = False,
    sudo: bool = False,
    function: Optional[Callable] = None,
    only: Literal["groups", "private"] = None,
    disableEdited: bool = False,
    disableErrors: bool = False,
    **args
):
    global ayiin_reg
    global sudo_reg

    handler = getHandler()
    sudoHandler = getSudoHandler()
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if (
        pattern.startswith(r"\#")
        or not pattern.startswith(r"\#")
        and pattern.startswith(r"^")
    ):
        ayiin_reg = sudo_reg = re.compile(pattern)
    else:
        ayiin_ = "\\" + handler
        sudo_ = "\\" + sudoHandler
        ayiin_reg = re.compile(ayiin_ + pattern)
        sudo_reg = re.compile(sudo_ + pattern)

    def decorator(func):

        @wraps(func)
        async def wrapper(check):
            if only and only == "groups" and not check.is_group:
                await check.respond("Command can only be used in groups")
                return
            if only and only == "private" and check.is_group:
                await check.respond("Command can only be used in PMs")
                return
            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                ayiin.log.info(f"{e}")
                if not disableErrors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**✘ AYIIN-USERBOT ERROR REPORT ✘**\n\n"
                    link = "[Group Support](https://t.me/AyiinChats)"
                    text += "Jika mau, Anda bisa melaporkan error ini, "
                    text += f"Cukup forward saja pesan ini ke {link}.\n\n"

                    ftext = "========== DISCLAIMER =========="
                    ftext += "\nFile ini HANYA diupload di sini,"
                    ftext += "\nkami hanya mencatat fakta error dan tanggal,"
                    ftext += "\nkami menghormati privasi Anda."
                    ftext += "\nJika mau, Anda bisa melaporkan error ini,"
                    ftext += "\ncukup forward saja pesan ini ke @AyiinChats"
                    ftext += "\n================================\n\n"
                    ftext += "--------BEGIN USERBOT TRACEBACK LOG--------\n"
                    ftext += "\nTanggal : " + date
                    ftext += "\nChat ID : " + str(check.chat_id)
                    ftext += "\nUser ID : " + str(check.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(check.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                    command = 'git log --pretty=format:"%an: %s" -10'

                    ftext += "\n\n\n10 commits Terakhir:\n"

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    with open("error.log", "w+") as file:
                        file.write(ftext)

                    await ayiin.send_message(
                        var.BOTLOG_CHATID,
                        ftext,
                        link_preview=False,
                    )

        if ayiin:
            if not disableEdited:
                ayiin.add_event_handler(
                    wrapper,
                    events.MessageEdited(
                        pattern=ayiin_reg,
                        outgoing=True,
                        func=function,
                        **args,
                    ),
                )
            ayiin.add_event_handler(
                wrapper,
                events.NewMessage(
                    pattern=ayiin_reg,
                    outgoing=True,
                    func=function,
                    **args,
                ),
            )

        if sudo:
            sudoer = getSudo()
            if not disableEdited:
                ayiin.add_event_handler(
                    wrapper,
                    events.MessageEdited(
                        pattern=sudo_reg,
                        outgoing=True,
                        func=function,
                        from_users=sudoer
                    ),
                )
            ayiin.add_event_handler(
                wrapper,
                events.NewMessage(
                    pattern=sudo_reg,
                    incoming=True,
                    func=function,
                    from_users=sudoer
                ),
            )
        
        if devs:
            if not disableEdited:
                ayiin.add_event_handler(
                    wrapper,
                    events.MessageEdited(
                        pattern=ayiin_reg,
                        incoming=True,
                        func=function,
                        from_users=DEVS
                    ),
                )
            ayiin.add_event_handler(
                wrapper,
                events.NewMessage(
                    pattern=ayiin_reg,
                    incoming=True,
                    func=function,
                    from_users=DEVS
                ),
            )

        return wrapper

    return decorator


def ayiinHandler(
    **args,
):
    disable_edited = args.get("disable_edited", False)
    if "disable_edited" in args:
        del args["disable_edited"]

    def decorator(func):
        
        if not disable_edited:
            ayiin.add_event_handler(func, events.MessageEdited(**args))
        ayiin.add_event_handler(func, events.NewMessage(**args))
        # ayiin.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def asstCmd(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/!]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        if ayiin.bot:
            ayiin.bot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def chatAction(**args):
    def decorator(func):
        if ayiin:
            ayiin.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def callBack(**args):
    def decorator(func):
        if ayiin.bot:
            ayiin.bot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
