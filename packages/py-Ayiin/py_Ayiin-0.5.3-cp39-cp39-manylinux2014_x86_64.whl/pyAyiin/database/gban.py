from json import dumps, loads
from typing import List

from ._core import db

conn = db.getConn()



# ========================×========================
#               GLOBAL BANNED DATABASE
# ========================×========================

def getGbanned() -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute("SELECT userIds FROM gbanned WHERE ubotId = ?", (3798,))
    try:
        row = cursor.fetchone()
        cursor.close()
        return loads(row[0])
    except:
        return []

def addGbanned(
    userId: int
):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    to_check = getGbanned()
    if userId not in to_check:
        to_check.append(userId)
        conn.execute("INSERT OR REPLACE INTO gbanned VALUES (?,?)", (3798, dumps(to_check)))
        conn.commit()


def delGbanned(
    userId: int
):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    to_check = getGbanned()
    if userId in to_check:
        to_check.remove(userId)
        conn.execute("INSERT OR REPLACE INTO gbanned VALUES (?,?)", (3798, dumps(to_check)))
        conn.commit()
        return True
    else:
        return False
