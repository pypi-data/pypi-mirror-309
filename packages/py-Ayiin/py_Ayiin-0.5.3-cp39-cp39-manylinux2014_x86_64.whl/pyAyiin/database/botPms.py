from ._core import db

con = db.getConn()


def getUserId(messageId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT * FROM botPms WHERE messageId = ?
        ''', (messageId,)
    )
    try:
        cur.fetchone()
        cur.close()
        return cur[0]
    except:
        return None


def addUserToDb(
    userId,
    messageId,
    firstName,
    replyId,
    loggerId,
    resultId
):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    check = getUserId(messageId)
    if check:
        con.execute(
            '''
            UPDATE botPms 
            SET messageId = ?, firstName = ?, replyId = ?, loggerId = ?, resultId = ?
            WHERE userId = ?
            ''',
            (messageId, firstName, replyId, loggerId, resultId, userId)
        )
    else:
        con.execute(
            '''
            INSERT INTO botPms (
                userId,
                messageId,
                firstName,
                replyId,
                loggerId,
                resultId
                
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (userId, messageId, firstName, replyId, loggerId, resultId)
        )


def delUserFromDb(messageId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    con.execute(
        '''
        DELETE FROM botPms WHERE messageId = ?
        ''', (messageId,)
    )
    con.commit()


def getUserReply(replyId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT replyId FROM botPms WHERE replyId = ?
        ''', (replyId,)
    )
    try:
        cur.fetchone()
        cur.close()
        return cur[0]
    except:
        return None


def getUserResults(resultId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT resultId FROM botPms WHERE resultId = ?
        ''', (resultId,)
    )
    try:
        cur.fetchone()
        cur.close()
        return cur[0]
    except:
        return None


def getUserLogging(loggerId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = con.execute(
        '''
        SELECT loggerId FROM botPms WHERE loggerId = ?
        ''', (loggerId,)
    )
    try:
        cur.fetchone()
        cur.close()
        return cur[0]
    except:
        return None
