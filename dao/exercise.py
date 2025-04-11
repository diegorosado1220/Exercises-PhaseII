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

    # This method creates a new exercise in the database.
    # It takes the exercise details as parameters and returns the ID of the created exercise.
    def createExercise(self, name, category, equipment, mechanic, force, level, alter_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO exercises (name, category, equipment, mechanic, force, level, alter_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"
        cursor.execute(query, (name, category, equipment, mechanic, force, level, alter_id))
        exercise_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return exercise_id

    #This method gets all exercises from the database.
    def getAllExercise(self):
        cursor = self.conn.cursor()
        query = "select id, name, category, equipment, mechanic, force, level, alter_id from exercises"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #This method deletes an exercise by its ID from the database.
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

    #This method gets an exercise by its ID from the database.
    def getExerciseById(self, id):
        cursor = self.conn.cursor()
        query = "select id, name, category, equipment, mechanic, force, level, alter_id from exercises where id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    #This method gets the instructions of an exercise by its ID from the database.
    def getInstructionsById(self, id):
        
        cursor = self.conn.cursor()
        get_Exercise_Id_query = "select id from exercises where id = %s"
        cursor.execute(get_Exercise_Id_query, (id,))
        exercise_id = cursor.fetchone()
        
        query = "select id, instruction_number, instruction from exercise_instructions where exercise_id = %s"
        cursor.execute(query, (exercise_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #This method gets the images of an exercise by its ID from the database.
    def getImagesById(self, id):
        
        cursor = self.conn.cursor()
        get_Exercise_Id_query = "select id from exercises where id = %s"
        cursor.execute(get_Exercise_Id_query, (id,))
        exercise_id = cursor.fetchone()
        
        query = "select id, image_path from exercise_images where exercise_id = %s"
        cursor.execute(query, (exercise_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #This method gets the primary muscles of an exercise by its ID from the database.
    def getPrimaryMuscleById(self, id):
        
        cursor = self.conn.cursor()
        get_Exercise_Id_query = "select id from exercises where id = %s"
        cursor.execute(get_Exercise_Id_query, (id,))
        exercise_id = cursor.fetchone()
        
        query = "select id, muscle from exercise_primary_muscles where exercise_id = %s"
        cursor.execute(query, (exercise_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #This method gets the secondary muscles of an exercise by its ID from the database.
    def getSecondaryMuscleById(self, id):
        
        cursor = self.conn.cursor()
        get_Exercise_Id_query = "select id from exercises where id = %s"
        cursor.execute(get_Exercise_Id_query, (id,))
        exercise_id = cursor.fetchone()
        
        query = "select id, muscle from exercise_secondary_muscles where exercise_id = %s"
        cursor.execute(query, (exercise_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    