import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

class DevStackDB:
    connection = None
    cur = None
    
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.environ.get('AWS_MARIADB_HOST'),
            user=os.environ.get('AWS_MARIADB_USER'),
            password=os.environ.get('AWS_MARIADB_PASSWORD'),
            db='Devstack',
            charset='utf8mb4',
            port=3306)
        self.dbCur = self.connection.cursor(pymysql.cursors.DictCursor)
        
    def runQuery(self, query):
        self.dbCur.execute(query)
        return self.dbCur.fetchall(), self.dbCur.lastrowid

    def runQueryWithParameter(self, query, data):
        self.dbCur.execute(query, data)
        return self.dbCur.fetchall()
    
    def close(self):
        self.dbCur.close()
        