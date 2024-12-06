from ._core import db

con = db.getConn()


def getNote(chatId, keyword):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT * FROM notes WHERE chatId = ? AND keyword = ?
        ''', (chatId, keyword)
    )
    try:
        raw = cur.fetchone()
        cur.close()
        return raw
    except:
        return None


def getNotes(chatId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT * FROM notes WHERE chatId = ?
        ''', (chatId,)
    )
    return cur.fetchall()


def addNote(chatId, keyword, reply, msgId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        INSERT INTO notes (
            chatId,
            keyword,
            reply,
            msgId
        )
        VALUES (?, ?, ?, ?)
        ''',
        (chatId, keyword, reply, msgId)
    )
    con.commit()


def updateNote(chatId, keyword, reply, msgId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        UPDATE notes 
        SET reply = ?, msgId = ? 
        WHERE chatId = ? AND keyword = ?
        ''',
        (reply, msgId, chatId, keyword)
    )
    con.commit()


def rmNote(chatId, keyword):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        DELETE FROM notes WHERE chatId = ? AND keyword = ?
        ''',
        (chatId, keyword)
    )
