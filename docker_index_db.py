#!/usr/bin/python3

from sqlalchemy import *
#from sqlalchemy import Table, Column, Integer, String, BLOB, MetaData, ForeignKey

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
        try:
            self.meta.create_all(self.db_engine)
            #print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # def execute_query(self, query=''):
    #     if query == '' : return
    #     print (query)
    #     with self.db_engine.connect() as connection:
    #         try:
    #             connection.execute(query)
    #         except Exception as e:
    #             print(e)

    def insert_file_data(self, layer, name, size, perm, own, ts, content):
        # Insert Data
        #query = "INSERT INTO '{}'(filename, file_size, file_perm, owner, timestamp, file_content) " \
        #        "VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(\
        #                layer, name, size, perm, own, ts, content)
        #query = (text("INSERT INTO :filelayer(filename, file_size, file_perm, owner, timestamp, file_content) VALUES (:filename, :filesize, :fileperm, :fileown, :filets, :filecontent);"), filelayer=layer, filename=name, filesize=size, fileperm=perm, fileown=own, filets=ts, filecontent=content)
        print(type(self.meta))
        print(self.meta)
        print(type(self.meta.tables))
        print(self.meta.tables)
        print(type(self.meta.tables[layer]))
        print(self.meta.tables[layer])
        query = self.meta.tables[layer].insert().values(filename=name, file_size=size, file_perm=perm, owner=own, timestamp=ts, file_content=content)
        print(query)
        conn = self.db_engine.connect()
        conn.execute(query)