import peewee
from datetime import datetime


database = \
    peewee.SqliteDatabase('database.db')


class DataBase(peewee.Model):

    class Meta:
        database = database


class AbstractTable(DataBase):
    date_insert = peewee.DateTimeField(default=datetime.now)


class DatabaseWorker:
    """ Worker for database manage
    """

    def __init__(self, conn):
        self.connection = conn

    def select(self, columns=None, rows=None):
        """
        :param columns: [TableObject.columns1, TableObject.columns2] or None
        :param rows: TableObject.columns1  == 1 (expression)
        :return: list(tuples())
        """
        query = self.connection.select(*columns or '').where(rows).tuples()
        return [i for i in query]

    def insert(self, data):
        """
        :param data: list(dict())
                [
                    {"field_1": 1, "field_2": 1},
                    {"field_1": 2, "field_2": 3}
                ]
        :return: None
        """
        self.connection.insert_many(data).on_conflict('replace').execute()


if __name__ == '__main__':

    #Create Scheme
    class MyTable(AbstractTable):
        field_1 = peewee.IntegerField()
        field_2 = peewee.IntegerField()

    # Create Table
    database.create_tables([MyTable])

    # Working with database
    connection = DatabaseWorker(MyTable)

    connection.insert(
        [
            {"field_1": 1, "field_2": 1},
            {"field_1": 2, "field_2": 3}
        ]
    )
    print(connection.select(columns=[MyTable.id],rows=MyTable.id == 3))
