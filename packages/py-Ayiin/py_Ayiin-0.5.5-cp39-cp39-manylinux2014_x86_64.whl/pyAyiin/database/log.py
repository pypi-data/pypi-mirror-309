from ._core import db

conn = db.getConn()


# ========================×========================
#               PM PERMIT USER DATABASE
# ========================×========================
def isApprovedLog(chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        "SELECT chatId FROM log WHERE chatId = ?", (chatId,)
    )
    try:
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    except:
        return None


def approveLog(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = isApprovedLog(chatId)
    if x:
        conn.execute("""UPDATE log SET chatId = ?""", (chatId,))
    else:
        conn.execute("""INSERT INTO log (chatId) VALUES(?)""", (chatId,))
    conn.commit()


def disapproveLog(chatId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    x = isApprovedLog(chatId)
    if x:
        conn.execute("""DELETE FROM log""")
    conn.commit()
