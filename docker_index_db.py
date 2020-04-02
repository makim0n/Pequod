#!/usr/bin/python3

from sqlalchemy import *

SQLITE = 'sqlite'

class docker_index:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        """
        Constructor of the class docker_index.

        :param dbtype: Type of the database (i.e. SQLite).
        :type dbtype: str
        :param username: Username for database connection.
        :type username: str
        :param password: Password for database connection.
        :type password: str
        :param dbname: Database name.
        :type dbname: str
        """
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self, layer):
        """
        Create the database.

        :param layer: Layer name, used as table name.
        :type layer: str
        :return: The SQLAlchemy table object of the corresponding table.
        :rtype: SQLAlchemy table object
        """
        meta = MetaData()
        layer_table = Table(layer, meta,
                      Column('id', Integer, primary_key=True),
                      Column('filename', String),
                      Column('file_size', String),
                      Column('file_perm', String),
                      Column('owner', String),
                      Column('timestamp', String),
                      Column('file_content', String)
                      )
        meta.create_all(self.db_engine)
        return layer_table

    def insert_file_data(self, table, name, size, perm, own, ts, content):
        """
        Insert data in the database in the right table.

        :param table: SQLAlchemy table of the associated layer.
        :type table: SQLAlchemy table object
        :param name: Name of the file or directory found in the layer.
        :type name: str
        :param size: Size of the file or directory found in the layer.
        :type size: str
        :param perm: Permission of the file or directory found in the layer.
        :type perm: str
        :param own: Owner of the file or directory found in the layer.
        :type own: str
        :param ts: Timestamp (epoch format) of the file or directory found in the layer.
        :type ts: str
        :param content: Raw content of the file or directory found in the layer.
        :type content: str
        """
        query = table.insert().values(filename=name, file_size=size, file_perm=perm, owner=own, timestamp=ts, file_content=content)
        conn = self.db_engine.connect()
        conn.execute(query)