from server.core.log import Log
from server.core import config

import sqlalchemy
from sqlalchemy.orm import Session, scoped_session, sessionmaker

log = Log.get_logger(__name__)


class Database:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            "sqlite:///" + config.data_dir + "/db.sqlite3"
        )
        self.engine.connect()
        self._scoped_session_factory = sessionmaker(bind=self.engine)

    def new_session(self):
        return Session(self.engine)

    def new_scoped_session(self):
        return scoped_session(self._scoped_session_factory)


db = Database()
