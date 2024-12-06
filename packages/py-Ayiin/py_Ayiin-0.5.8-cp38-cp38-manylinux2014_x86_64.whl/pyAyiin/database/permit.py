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
#                 PM PERMIT DATABASE
# ========================×========================

# ========================×========================
#               PM PERMIT MODE DATABASE
# ========================×========================
def getModePermit():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT mode FROM permitMode"
    )
    try:
        cur = cursor.fetchone()
        cursor.close()
        return cur[0]
    except:
        return None


def setModePermit(mode):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cek = getModePermit()
    if cek and cek[0] is not None:
        conn.execute("""UPDATE permitMode SET mode = ?""", (mode,))
    else:
        conn.execute("""INSERT INTO permitMode (mode) VALUES(?)""", (mode,))
    conn.commit()


# ========================×========================
#               PM PERMIT USER DATABASE
# ========================×========================
def isApproved() -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT users FROM permitUser WHERE ubotId = ?",
        (3798, ),
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    except:
        return []


def approve(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = isApproved()
    if userId not in x:
        x.append(userId)
        conn.execute("""INSERT OR REPLACE INTO permitUser(ubotId, users) VALUES (?,?)""", (3798, dumps(x)))
        conn.commit()


def disapprove(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = isApproved()
    if userId in x:
        x.remove(userId)
        conn.execute("""INSERT OR REPLACE INTO permitUser(ubotId, users) VALUES (?,?)""", (3798, dumps(x)))
        conn.commit()


# ========================×========================
#             PM PERMIT MESSAGE DATABASE
# ========================×========================
def getPermitMessage():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT permitMsg FROM permitMessage"
    )
    try:
        cur = cursor.fetchone()
        cursor.close()
        return cur[0]
    except:
        return None


def setPermitMessage(permit):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cek = getPermitMessage()
    if cek:
        conn.execute("""UPDATE permitMessage SET permit_msg = ?""", (permit,))
    else:
        conn.execute("""INSERT INTO permitMessage (permitMsg) VALUES(?)""", (permit,))
    conn.commit()


def delPermitMessage():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cek = getPermitMessage()
    if cek:
        conn.execute("DELETE from permitMessage")
        conn.commit()
        return True
    else:
        return False
