from config.pgconfig import pg_config
import psycopg2
from psycopg2 import errors


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
        
        state_variable = 0   
        
        # If state_value is 0 it means that record does not exist.
        # If state_value is 1 it means that record exists and it will be deleted.
        # If state_value is 2 it means that record exists but it cannot be deleted because of foreign key constraint.
        
        if exists:
            
            try:
                query = "delete from exercises where id = %s"
                cursor.execute(query, (id,))
                self.conn.commit()
                state_variable = 1
                
            except errors.ForeignKeyViolation as e:
                state_variable = 2
                self.conn.rollback()
                
            cursor.close()
            return state_variable
        else:
            cursor.close()
            return state_variable

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

    #This method updates an exercise in the database.
    def updateExercise(self, id, name, category, equipment, mechanic, force, level, alter_id):
        cursor = self.conn.cursor()
        pre_query = "SELECT 1 FROM exercises WHERE id = %s"
        cursor.execute(pre_query, (id,))
        exists = cursor.fetchone()
        if exists:
            query = "UPDATE exercises SET name = %s, category = %s, equipment = %s, mechanic = %s, force = %s, level = %s, alter_id = %s WHERE id = %s"
            cursor.execute(query, (name, category, equipment, mechanic, force, level, alter_id, id))
            self.conn.commit()
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    #This method gets an exercise for update by its ID from the database.
    def getExerciseForUpdate(self, id):
        cursor = self.conn.cursor()
        query = "SELECT id, name, category, equipment, mechanic, force, level, alter_id FROM exercises WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    #This method gets the most performed exercises from the database.
    def getMostPerformed(self):
        cursor = self.conn.cursor()
        query = """select exercises.id as exercise_id, exercises.name as name, count(distinct sport_exercises.sport) as sports_related
                from exercises join sport_exercises on exercises.id = sport_exercises.exercise
                group by exercises.id, exercises.name
                order by sports_related desc
                limit 5"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #This method gets Exercises by a selected muscle from the database.
    def getExercisesByMuscle(self, muscleid):
        cursor = self.conn.cursor()
        query =     """select distinct exercises.id as exercise_id, exercises.name as name
                    from exercises
                    join exercise_secondary_muscles on  exercises.id = exercise_secondary_muscles.exercise_id
                    join exercise_primary_muscles on exercises.id = exercise_primary_muscles.exercise_id
                    where lower(exercise_primary_muscles.muscle) = lower(%s) or lower(exercise_secondary_muscles.muscle) = lower(%s)
                    order by exercises.id"""
        cursor.execute(query, (muscleid, muscleid))
        result = cursor.fetchall()
        cursor.close
        return result
                    
                    
                    
                    
    