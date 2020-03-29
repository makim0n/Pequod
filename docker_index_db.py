#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

SQLITE = 'sqlite'

class docker_index:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self, layer):
        metadata = MetaData()
        layer_table = Table(layer, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('filename', String),
                      Column('file_size', String),
                      Column('file_perm', String),
                      Column('owner', String),
                      Column('date', String),
                      Column('timestamp', String)
                      )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)
