from ._core import db

con = db.getConn()


# ========================×========================
#              BLACKLIST FILTER DATABASE
# ========================×========================

def getChatBlacklist(chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = con.execute(
        '''
        SELECT * FROM blacklistFilter WHERE chatId = ?
        ''', (chatId,)
    )
    try:
        ok = cursor.fetchall()
        cursor.close()
        return ok
    except:
        return None


def addToBlacklist(chatId, chatTitle, trigger):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        INSERT INTO blacklistFilter (
            chatId,
            chatTitle,
            trigger
        )
        VALUES (?, ?, ?)
        ''',
        (chatId, chatTitle, trigger)
    )
    con.commit()


def updateToBlacklist(chatId, chatTitle, trigger):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        UPDATE blacklistFilter SET chatTitle = ?, trigger = ? WHERE chatId = ?
        ''',
        (chatId, chatTitle, trigger)
    )
    con.commit()


def rmFromBlacklist(chatId, trigger):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        DELETE FROM blacklistFilter WHERE chatId = ? AND trigger = ?
        ''',
        (chatId, trigger)
    )
    con.commit()
