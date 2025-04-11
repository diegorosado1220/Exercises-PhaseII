from config.pgconfig import pg_config
import psycopg2


class exerciseDAO():

    def __init__(self):
        url = "dbname = %s password = %s host = %s port = %s user= %s" % \
              (pg_config['database'],
               pg_config['password'],
               pg_config['host'],
               pg_config['port'],
               pg_config['user']
               )

        self.conn = psycopg2.connect(url)

    def getAllExercise(self):
        cursor = self.conn.cursor()
        query = "select id, name, category, equipment, mechanic, force, level, alter_id from exercises"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def deleteExerciseById(self, id):
        cursor = self.conn.cursor()
        pre_query = "select 1 from exercises where id = %s"
        cursor.execute(pre_query, (id,))
        exists = cursor.fetchone()
        if exists:
            query = "delete from exercises where id = %s"
            cursor.execute(query, (id,))
            self.conn.commit()
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    def getExerciseByID(self, id):
        cursor = self.conn.cursor()
        query = "select id, name, category, equipment, mechanic, force, level, alter_id from exercises where id = %s"
        cursor.execute(query, id)
        result = cursor.fetchone()
        cursor.close()
        return result