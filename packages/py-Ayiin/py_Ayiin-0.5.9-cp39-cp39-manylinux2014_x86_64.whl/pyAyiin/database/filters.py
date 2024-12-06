from ._core import db

conn = db.getConn()


def addFilter(chatId, trigger, string, msgId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute(
        "INSERT OR REPLACE INTO filters(chatId, trigger, string, msgId) VALUES(?, ?, ?, ?)",
        (chatId, trigger, string, msgId),
    )
    conn.commit()


def delFilter(chatId, trigger):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute(
        "DELETE from filters WHERE chatId = ? AND trigger = ?", (chatId, trigger)
    )
    conn.commit()


def getAllFilters(chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute("SELECT * FROM filters WHERE chatId = ?", (chatId,))
    return cursor.fetchall()
