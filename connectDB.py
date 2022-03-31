import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

connection=None
dbCur=None


class DevStackDB:
    connection = None
    cur = None
    
    def __init__(self):
        self.connection = pymysql.connect(host=os.environ.get('AWS_MARIADB_HOST'), user=os.environ.get('AWS_MARIADB_USER'), password=os.environ.get('AWS_MARIADB_PASSWORD'), db='Devstack',charset='utf8', port=3306)
        self.dbCur = self.connection.cursor(pymysql.cursors.DictCursor)
        
    def runQuery(self, query):
        self.dbCur.execute(query)
        return self.dbCur.fetchall()

db = DevStackDB()

row = db.runQuery('SELECT * FROM Skill')
print(row)