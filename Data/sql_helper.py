#===== Standard Library
#===== 3rd party
import pymysql
import pymysql.cursors
#===== Reader
#=========================================================================
# MODEL
class Sql_Helper:
    def __init__(self, conn):
        self.conn = conn
    
    def create_database(self, db_name):
        with self.conn.cursor() as cursor:
            sql = f'CREATE DATABASE IF NOT EXISTS {db_name};'
            print(sql)
            cursor.execute(sql)

    def create_table(self, db_name, table_name, column_tuples, primary_key):
         with self.conn.cursor() as cursor:
            sql = f'use {db_name}'
            cursor.execute(sql)
            
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            for tupl in column_tuples:
                sql = sql + f' {tupl[0]} {tupl[1]},'
            sql += f' PRIMARY KEY ({primary_key})'
            sql += ' );'
            cursor.execute(sql)
    
    def insert_row(self, db_name, table_name, col_val_tuples):
        with self.conn.cursor() as cursor:
            sql = f'use {db_name}'
            cursor.execute(sql)
            columns = [tupl[0] for tupl in col_val_tuples]
            values = [str(tupl[1]) if type(tupl[1])!=str else f"\'{tupl[1]}\'" for tupl in col_val_tuples]
            sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(values)});"
            cursor.execute(sql)
        self.conn.commit()
   
    def insert_ignore_row(self, db_name, table_name, col_val_tuples):
        with self.conn.cursor() as cursor:
            sql = f'use {db_name}'
            cursor.execute(sql)
            columns = [tupl[0] for tupl in col_val_tuples]
            values = [str(tupl[1]) if type(tupl[1])!=str else f"\'{tupl[1]}\'" for tupl in col_val_tuples]
            sql = f"INSERT IGNORE INTO {table_name} ({','.join(columns)}) VALUES ({','.join(values)});"
            cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, db_name, table_name):
        with self.conn.cursor() as cursor:
            sql = f"use {db_name};"
            cursor.execute(sql)
            sql = f"DROP TABLE {table_name}"
            cursor.execute(sql)
        self.conn.commit()
    
    def get_table(self, db_name, table_name):
        with self.conn.cursor() as cursor:
            sql = f"use {db_name}"
            cursor.execute(sql)
            
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            cursor_obj = cursor
        return cursor_obj

    def get_row(self, db_name, table_name, pkey_tupl):
        pkey_col = pkey_tupl[0]
        pkey_val = pkey_tupl[1]
        with self.conn.cursor() as cursor:
            sql = f'use {db_name};'
            cursor.execute(sql)
            sql = f"select * from {table_name} where {pkey_col}={pkey_val}"
            cursor.execute(sql)
            cursor_obj = cursor
        return cursor_obj

    def custom_sql(self, db_name, sql):
        with self.conn.cursor() as cursor:
            db_sql = f'use {db_name}'
            cursor.execute(db_sql)
            cursor.execute(sql)
            cursor_obj = cursor
        self.conn.commit()
        return cursor_obj
        