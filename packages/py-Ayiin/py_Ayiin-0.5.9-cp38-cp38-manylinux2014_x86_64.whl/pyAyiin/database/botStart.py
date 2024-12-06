from ._core import db

conn = db.getConn()


def getStarterDetails(userId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        '''
        SELECT * FROM botStarter WHERE userId = ?
        ''',
        (userId,)
    )
    try:
        user = cursor.fetchone()
        cursor.close()
        return user
    except:
        return None


def addStarterToDb(
    userId,
    first_name,
    date,
    username,
):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    to_check = getStarterDetails(userId)
    if not to_check:
        conn.execute(
            '''
            INSERT INTO botStarter (
                userId,
                first_name,
                date,
                username
            )
            VALUES (?, ?, ?, ?)
            ''',
            (userId, first_name, date, username)
        )
    else:
        conn.execute(
            '''
            UPDATE botStarter 
            SET first_name = ?, date = ?, username = ?
            WHERE userId = ?
            ''',
            (first_name, date, username, userId)
        )
    conn.commit()


def delStarterFromDb(userId):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute(
        '''
        DELETE FROM botStarter WHERE userId = ?
        ''',
        (userId,)
    )
    conn.commit()


def getAllStarters():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        '''
        SELECT * FROM botStarter
        '''
    )
    return cursor.fetchall()
