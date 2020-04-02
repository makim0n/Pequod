#!/usr/bin/python3

from sqlalchemy import *

SQLITE = 'sqlite'

class docker_index:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    meta = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self, layer):
        self.meta = MetaData()
        layer_table = Table(layer, self.meta,
                      Column('id', Integer, primary_key=True),
                      Column('filename', String),
                      Column('file_size', String),
                      Column('file_perm', String),
                      Column('owner', String),
                      Column('timestamp', String),
                      Column('file_content', String)
                      )
        self.meta.create_all(self.db_engine)
        return layer_table

    def insert_file_data(self, table, name, size, perm, own, ts, content):
        query = table.insert().values(filename=name, file_size=size, file_perm=perm, owner=own, timestamp=ts, file_content=content)
        print(query)
        conn = self.db_engine.connect()
        conn.execute(query)