import pymysql

connection=None
dbCur=None


class DevStackDB:
    connection = None
    cur = None
    
    def __init__(self):
        self.connection = pymysql.connect(host='devstack-notice-db.c9j6jk8y4wgv.ap-northeast-2.rds.amazonaws.com', user='admin', password='spring1234', db='Devstack',charset='utf8', port=3306)
        self.dbCur = self.connection.cursor(pymysql.cursors.DictCursor)
        
    def runQuery(self, query):
        self.dbCur.execute(query)
        return self.dbCur.fetchall()

db = DevStackDB()

row = db.runQuery('SELECT * FROM Skill')
print(row)