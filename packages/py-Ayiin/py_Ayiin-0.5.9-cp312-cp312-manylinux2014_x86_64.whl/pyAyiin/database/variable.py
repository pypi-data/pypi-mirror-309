from ._core import db

conn = db.getConn()


def cekVar():
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cursor = conn.execute(
        '''
        SELECT * FROM variable
        '''
    )
    return cursor.fetchall()

def getVar(var):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cur = conn.execute(
        '''
        SELECT value FROM variable WHERE vars = ?
        ''', (var,)
    )
    try:
        raw = cur.fetchone()
        cur.close()
        return raw[0]
    except:
        return None


def setVar(var, value):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    cek = getVar(var)
    if cek:
        conn.execute(
            '''
            UPDATE variable SET value = ? WHERE vars = ?
            ''', (value, var)
        )
    else:
        conn.execute(
            '''
            INSERT INTO variable (vars, value) VALUES (?,?)
            ''', (var, value)
        )
    conn.commit()


def delVar(var):
    """
    KANG COPAS GAUSAH MAIN HAPUS KONTOL
    Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
    """
    conn.execute(
    """
    DELETE FROM variable WHERE vars = ?
    """, (var,)
    )
    conn.commit()
