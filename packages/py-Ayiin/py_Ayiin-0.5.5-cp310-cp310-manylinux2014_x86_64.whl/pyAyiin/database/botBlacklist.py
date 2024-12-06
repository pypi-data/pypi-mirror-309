from ._core import db

conn = db.getConn()



# ========================×========================
#               BLACKLIST USER DATABASE
# ========================×========================
def checkIsBlacklist(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        '''
        SELECT * FROM botBlacklist WHERE userId = ?
        ''', (userId,)
    )
    try:
        ok = cursor.fetchone()
        cursor.close()
        return ok
    except:
        return None


def addUserToBl(
    userId: int,
    firstName: str,
    userName: str,
    reason: str,
    date: str
):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    to_check = checkIsBlacklist(userId)
    if not to_check:
        conn.execute(
            '''
            INSERT INTO bot_starter (
                userId,
                firstName,
                userName,
                reason,
                date
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (userId, firstName, userName, reason, date)
        )
    else:
        conn.execute(
            '''
            UPDATE bot_starter 
            SET firstName = ?, userName = ?, reason = ?, date = ?
            WHERE userId = ?
            ''',
            (firstName, userName, reason, date, userId)
        )
    conn.commit()


def remUserFromBl(userId: int):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute(
        '''
        DELETE FROM botBlacklist WHERE userId = ?
        ''', (userId,)
    )


def getBlUsers():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    get = conn.execute(
        '''
        SELECT * FROM botBlacklist
        '''
    )
    return get.fetchall()
