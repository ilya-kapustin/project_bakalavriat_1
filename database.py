import sqlite3
import pandas as pd


engine = sqlite3.connect('database.db')


class DatabaseWorker:
    """ Worker for database manage
    """

    def __init__(self, conn=None):
        self.connection = conn or engine
        self.data = None

    def select(self, table, columns=None, where=None):
        """
        :param table: name table
        :param columns: list columns
        :param where: filter expressions
        :return: pd.DataFrame
        """
        to_str = lambda x: ','.join(x)

        self.data = pd.read_sql(f"""select {to_str(columns or '*')} 
                             from {table} 
                             where  {to_str(where or '1')}""", self.connection)
        print(self.data)

    def insert_from_csv(self, path):
        """
        :param path: path to csv file
        :return: None
        """
        data = pd.read_csv(path)
        self.insert(data, path.split("/")[-1].split(".")[0])

    def insert(self, data, table):
        """
        :param data: pd.DataFrame
        :param table: name table
        :return: None
        """
        data.to_sql(table, self.connection, if_exists='append', index=False)


if __name__ == '__main__':
    # Working with database
    #connection = DatabaseWorker(engine)

    #connection.insert_from_csv("file.csv")
    #print(connection.select(table="file"))
