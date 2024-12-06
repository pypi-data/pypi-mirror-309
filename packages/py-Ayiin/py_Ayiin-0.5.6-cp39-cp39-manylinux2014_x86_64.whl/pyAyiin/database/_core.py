# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import logging
import sqlite3

logger = logging.getLogger(__name__)


schemaXd = """
CREATE TABLE IF NOT EXISTS blacklistGcastGroup(
    userId INTEGER PRIMARY KEY,
    blGcast TEXT
);
CREATE TABLE IF NOT EXISTS blacklistGcastPrivate(
    userId INTEGER PRIMARY KEY,
    blGcast TEXT
);
CREATE TABLE IF NOT EXISTS blacklistFilter(
    chatId INTEGER,
    chatTitle TEXT,
    trigger TEXT
);
CREATE TABLE IF NOT EXISTS botBlacklist(
    userId INTEGER PRIMARY KEY,
    firstName TEXT,
    userName TEXT,
    reason TEXT,
    date DATETIME
);
CREATE TABLE IF NOT EXISTS botStarter(
    userId INTEGER PRIMARY KEY,
    firstName TEXT,
    date DATETIME,
    userName TEXT
);
CREATE TABLE IF NOT EXISTS botPms(
    userId INTEGER PRIMARY KEY,
    messageId INTEGER,
    firstName TEXT,
    replyId INTEGER,
    loggerId INTEGER,
    resultId INTEGER
);
CREATE TABLE IF NOT EXISTS broadcast(
    keyword TEXT PRIMARY KEY,
    chatIds TEXT
);
CREATE TABLE IF NOT EXISTS chatBot(
    chatId INTEGER PRIMARY KEY,
    status TEXT
);
CREATE TABLE IF NOT EXISTS filters(
    chatId INTEGER,
    trigger TEXT,
    string TEXT,
    msgId TEXT
);
CREATE TABLE IF NOT EXISTS gbanned(
    ubotId INTEGER PRIMARY KEY,
    userIds TEXT
);
CREATE TABLE IF NOT EXISTS handlers(
    ubotId INTEGER PRIMARY KEY,
    handler TEXT
);
CREATE TABLE IF NOT EXISTS gMutedUser(
    userId INTEGER PRIMARY KEY,
    gMuted TEXT
);
CREATE TABLE IF NOT EXISTS log(
    chatId INTEGER
);
CREATE TABLE IF NOT EXISTS mutedUser(
    userId INTEGER PRIMARY KEY,
    muted TEXT
);
CREATE TABLE IF NOT EXISTS notes(
    chatId INTEGER,
    keyword TEXT,
    reply TEXT,
    msgId TEXT
);
CREATE TABLE IF NOT EXISTS permitMode(
    ubotId INTEGER PRIMARY KEY,
    mode
);
CREATE TABLE IF NOT EXISTS permitMessage(
    ubotId INTEGER PRIMARY KEY,
    permitMsg TEXT
);
CREATE TABLE IF NOT EXISTS permitUser(
    ubotId INTEGER PRIMARY KEY,
    users TEXT
);
CREATE TABLE IF NOT EXISTS sudoHandlers(
    ubotId INTEGER PRIMARY KEY,
    handler TEXT
);
CREATE TABLE IF NOT EXISTS sudoer(
    ubotId INTEGER PRIMARY KEY,
    userId TEXT
);
CREATE TABLE IF NOT EXISTS variable(
    vars TEXT PRIMARY KEY,
    value TEXT
);
"""


class DatabaseXd:
    def __init__(self):
        self.conn: sqlite3.Connection = None
        self.path: str = "ayiinUserbot.db"
        self.is_connected: bool = False

    def connect(self):
        """
        KANG COPAS GAUSAH MAIN HAPUS KONTOL
        Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
        """
        conn = sqlite3.connect(self.path)

        conn.executescript(schemaXd)

        conn.execute("VACUUM")

        conn.commit()

        conn.row_factory = sqlite3.Row

        self.conn = conn
        self.is_connected: bool = True

        logger.info("Database Anda Telah Terhubung.")

    def close(self):
        """
        KANG COPAS GAUSAH MAIN HAPUS KREDIT KONTOL
        Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
        """
        self.conn.close()

        self.is_connected: bool = False

        logger.info("Database Anda Telah Ditutup.")

    def getConn(self) -> sqlite3.Connection:
        """
        KANG COPAS GAUSAH MAIN HAPUS KONTOL
        Copyright (C) 2023-present AyiinXd <https://github.com/AyiinXd>
        """
        if not self.is_connected:
            self.connect()

        return self.conn


db = DatabaseXd()
