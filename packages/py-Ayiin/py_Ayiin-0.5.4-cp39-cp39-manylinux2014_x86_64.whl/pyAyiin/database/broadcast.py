from json import dumps, loads
from typing import List

from ._core import db

con = db.getConn()


def getBroadcast(keyword) -> List[int]:
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = con.execute(
        '''
        SELECT chatIds FROM broadcast WHERE keyword = ?
        ''',
        (keyword,)
    )
    try:
        list_ = cursor.fetchone()
        cursor.close()
        return loads(list_[0])
    except:
        return []


def addBroadcast(keyword, chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    ok = getBroadcast(keyword)
    if chatId not in ok:
        ok.append(chatId)
        con.execute("""INSERT OR REPLACE INTO broadcast VALUES (?,?)""", (keyword, dumps(ok)))
        con.commit()


def delBroadcast(keyword, chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    ok = getBroadcast(keyword)
    if chatId in ok:
        ok.remove(chatId)
        con.execute("INSERT OR REPLACE INTO broadcast VALUES (?,?)", (keyword, dumps(ok)))
        con.commit()
