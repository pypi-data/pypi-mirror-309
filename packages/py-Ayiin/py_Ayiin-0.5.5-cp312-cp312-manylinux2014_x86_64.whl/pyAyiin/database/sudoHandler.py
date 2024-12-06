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

from ._core import db

conn = db.getConn()


# ========================×========================
#                SUDO HANDLER DATABASE
# ========================×========================


def getSudoHandler() -> str:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT handler FROM sudoHandlers WHERE ubotId = ?",
        ("ubotIds",),
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return str(row[0])
    except:
        return "$"


def addSudoHandler(command: str):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute("INSERT OR REPLACE INTO sudoHandlers VALUES (?,?)", ("ubotIds", command))
    conn.commit()


def delSudoHandler(command: str):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute("DELETE FROM sudoHandlers WHERE handler = ?", (command,))
    conn.commit()
