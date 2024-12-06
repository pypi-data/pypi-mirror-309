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

from json import loads, dumps
from typing import List

from ._core import db

conn = db.getConn()


# ========================×========================
#                 SUDOER DATABASE
# ========================×========================

def getSudo() -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT userId FROM sudoer WHERE ubotId = ?",
        ("ubotIds",),
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return loads(row[0])
    except:
        return []


def addSudo(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getSudo()
    if userId not in x:
        x.append(userId)
        conn.execute("INSERT OR REPLACE INTO sudoer VALUES (?,?)", ("ubotIds", dumps(x)))
        conn.commit()
        return True
    else:
        return False


def delSudo(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = getSudo()
    if userId in x:
        x.remove(userId)
        conn.execute("INSERT OR REPLACE INTO sudoer VALUES (?,?)", ("ubotIds", dumps(x)))
        conn.commit()
        return True
    else:
        return False
