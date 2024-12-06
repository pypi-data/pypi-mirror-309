# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from json import dumps, loads
from typing import List

from ._core import db

conn = db.getConn()


# ========================×========================
#              BLACKLIST GCAST DATABASE
# ========================×========================


# ========================×========================
#              GCAST GROUP DATABASE
# ========================×========================

def getGcastGroup() -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT blGcast FROM blacklistGcastGroup WHERE userId = ?", (3798,)
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return loads(row[0])
    except:
        return []


def addGcastGroup(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getGcastGroup()
    if chatId not in x:
        x.append(chatId)
        conn.execute("INSERT OR REPLACE INTO blacklistGcastGroup(userId, blGcast) VALUES (?,?)", (3798, dumps(x)))
        conn.commit()


def delGcastGroup(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getGcastGroup()
    if chatId in x:
        x.remove(chatId)
        conn.execute("INSERT OR REPLACE INTO blacklistGcastGroup(userId, blGcast) VALUES (?,?)", (3798, dumps(x)))
        conn.commit()


# ========================×========================
#              GCAST PRIVATE DATABASE
# ========================×========================

def getGcastPrivate() -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT blGcast FROM blacklistGcastPrivate WHERE userId = ?", (3798,)
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return loads(row[0])
    except:
        return []

def addGcastPrivate(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getGcastPrivate()
    if chatId not in x:
        x.append(chatId)
        conn.execute("INSERT OR REPLACE INTO blacklistGcastPrivate(userId, blGcast) VALUES (?,?)", (3798, dumps(x)))
        conn.commit()

def delGcastPrivate(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getGcastPrivate()
    if chatId in x:
        x.remove(chatId)
        conn.execute("INSERT OR REPLACE INTO blacklistGcastPrivate(userId, blGcast) VALUES (?,?)", (3798, dumps(x)))
        conn.commit()
