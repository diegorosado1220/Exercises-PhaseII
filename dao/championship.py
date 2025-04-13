#Here is where the connection to the database is made and contains the logic for the SportsTracker DAO.

from config.pgconfig import pg_config
import psycopg2
from psycopg2 import errors

class PartDAO():
    def __init__(self):
        url = "dbname = %s password = %s host = %s port = %s user= %s" % \
              (pg_config['database'],
               pg_config['password'],
               pg_config['host'],
               pg_config['port'],
               pg_config['user']
               )

        self.conn = psycopg2.connect(url)
        
    # This method gets all championships from the database.
    def getAllChampionship(self):
        cursor = self.conn.cursor()
        query = "SELECT id, name, winner_team, winner_year FROM championships"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    # This method creates a new championship in the database.
    def createChampionShip(self, name, winner_team, winner_year):
        cursor = self.conn.cursor()
        query = "INSERT INTO championships (name, winner_team, winner_year) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (name, winner_team, winner_year))
        championship_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return championship_id
    
    # This method deletes a championship by its ID from the database.
    def deleteChampionById(self, id):
        cursor = self.conn.cursor()
        pre_query = "SELECT 1 FROM championships WHERE id = %s"
        cursor.execute(pre_query, (id,))
        exists = cursor.fetchone()
        if exists:
            query = "DELETE FROM championships WHERE id = %s"
            cursor.execute(query, (id,))
            self.conn.commit()
            cursor.close()
            return True
        else:
            cursor.close()
            return False
        
    # This method updates a championship by its ID in the database.
    # It takes the championship details as parameters and returns the ID of the updated championship.
    def updateChampionship(self, id, name, winner_team, winner_year):
        cursor = self.conn.cursor()
        pre_query = "SELECT 1 FROM championships WHERE id = %s"
        cursor.execute(pre_query, (id,))
        exists = cursor.fetchone()
        
        state_variable = 0   
        
        # If state_value is 0 it means that record does not exist.
        # If state_value is 1 it means that record exists and it will be updated.
        # If state_value is 2 it means that record exists but it cannot be updated because of missing parameters.
        
        if exists:
            
            try:
                query = "UPDATE championships SET name = %s, winner_team = %s, winner_year = %s WHERE id = %s"
                cursor.execute(query, (name, winner_team, winner_year, id))
                self.conn.commit()
                state_variable = 1
                
            except errors.InvalidTextRepresentation:
                state_variable= 2
                self.conn.rollback()
                
            cursor.close()
            return state_variable
        else:
            cursor.close()
            return state_variable
        
    # This method gets a championship by its ID from the database.
    def getChampionshipForUpdate(self, id):
        cursor = self.conn.cursor()
        query = "SELECT id, name, winner_team, winner_year FROM championships WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    # This method gets a championship by its ID from the database.
    def getChampionshipById(self, id):
        cursor = self.conn.cursor()
        query = "SELECT id, name, winner_year, winner_team FROM championships WHERE id = %s" 
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
     #This method gets the winner team by its ID from the database for the getChampionshipById method.
    def getWinnerTeamById(self, id):
        cursor = self.conn.cursor()
        
        getwinner_team_id_query = "select winner_team from championships where id = %s"
        cursor.execute(getwinner_team_id_query, (id,))
        winner_team_id = cursor.fetchone()
        
        query = "SELECT id, name FROM teams WHERE id = %s"
        cursor.execute(query, (winner_team_id,))
        result = cursor.fetchone()
        
        cursor.close()
        return result
        
        
        
    