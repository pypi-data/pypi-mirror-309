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
#                   MUTED DATABASE
# ========================×========================

def cekMute(userId: int) -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT muted FROM mutedUser WHERE userId = ?", (userId,)
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return loads(row[0])
    except:
        return []


def addMute(userId: int, targetId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = cekMute(userId)
    if targetId not in x:
        x.append(targetId)
        conn.execute(
            "INSERT OR REPLACE INTO mutedUser VALUES (?,?)", (userId, dumps(x))
        )
        conn.commit()


def delMute(userId: int, targetId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = cekMute(userId)
    if targetId in x:
        x.remove(targetId)
        conn.execute(
            "INSERT OR REPLACE INTO mutedUser VALUES (?,?)", (userId, dumps(x))
        )
        conn.commit()


# ========================×========================
#               GLOBAL MUTED DATABASE
# ========================×========================

def cekGmute(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT gMuted FROM gMutedUser WHERE userId = ?", (userId,)
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    except:
        return []


def addGmute(userId: int, targetId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = cekGmute(userId)
    if targetId not in x:
        x.append(targetId)
        conn.execute(
            "INSERT OR REPLACE INTO gMutedUser VALUES (?,?)", (userId, dumps(x))
        )
        conn.commit()


def delGmute(userId: int, targetId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = cekGmute(userId)
    if targetId in x:
        x.remove(targetId)
        conn.execute(
            "INSERT OR REPLACE INTO gMutedUser VALUES (?,?)", (userId, dumps(x))
        )
        conn.commit()
