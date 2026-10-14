import json
import sqlite3
from contextlib import contextmanager


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class Store:
    def __init__(self, path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('CREATE TABLE IF NOT EXISTS records(kind TEXT, id TEXT, value TEXT, PRIMARY KEY(kind,id))')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=15)
        try:
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def put(self, kind, key, value, con=None):
        if con is None:
            with self.connect() as db:
                self.put(kind, key, value, db)
            return
        con.execute('INSERT OR REPLACE INTO records VALUES (?,?,?)', (kind, key, dumps(value)))

    def get(self, kind, key, con=None):
        if con is None:
            with self.connect() as db:
                return self.get(kind, key, db)
        row = con.execute('SELECT value FROM records WHERE kind=? AND id=?', (kind, key)).fetchone()
        return json.loads(row[0]) if row else None

    def all(self, kind):
        with self.connect() as db:
            return [json.loads(r[0]) for r in db.execute('SELECT value FROM records WHERE kind=? ORDER BY rowid', (kind,))]
