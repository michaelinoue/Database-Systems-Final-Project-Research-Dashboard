import pymysql
import datetime

# mySQL
MYSQL_HOST = 'localhost'
MYSQL_UN = 'root'
MYSQL_PW = 'test_root'
MYSQL_DB = 'academicworld'

# MySQL Config 
try:
    db = pymysql.connect(host=MYSQL_HOST,
                         user=MYSQL_UN,
                         password=MYSQL_PW,
                         database=MYSQL_DB,
                         charset='utf8mb4',
                         port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
except:
    print("Error with MySQL connect ")
    db = None
UPDATE_KEYWORD = """UPDATE keyword
SET rating = {rating}, rating_date = '{rating_date}'
WHERE name = '{keyword}';"""

GET_RECENT = """SELECT name, rating
FROM keyword
WHERE rating_date IS NOT NULL 
ORDER BY rating_date DESC
LIMIT 10
"""

def execute_write(query):
    if db == None:
        return
    try: 
        with db.cursor() as cursor:
            cursor.execute('USE academicworld;')
            cursor.execute(query)
        db.commit()
    except pymysql.Error as e:
        print("Error with MySQ write: {}".format(e))
        return None
    
def execute_read(query):
    if db == None:
        return
    try: 
        with db.cursor() as cursor:
            cursor.execute('USE academicworld;')
            cursor.execute(query)
            result = cursor.fetchall()
            return result 
    except:
        print("Error with MySQL read")
        return None    

# add keyword rating and rating time to db
def rate_keyword(keyword, rating):
    now = datetime.datetime.utcnow()
    now_format = now.strftime('%Y-%m-%d %H:%M:%S')
    query = UPDATE_KEYWORD.format(rating=rating, rating_date=now_format, keyword=keyword)
    execute_write(query)

# add keyword rating and rating time to db
def get_recently_rated():
    return execute_read(GET_RECENT)