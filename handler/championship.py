from flask import jsonify
from dao.championship import PartDAO

class ChampionshipsHandler:
    
    
    # This method maps the championship data to a dictionary format.
    def map_to_dict(self, championship):
        result = {}
        result["id"] = championship[0]
        result["name"] = championship[1]
        result["winner_team"] = championship[2]
        result["winner_year"] = championship[3]
        return result
    
    
    # This method maps the winner team data to a dictionary format.
    def map_to_dict_teams(self, winnerTeam):
        result = {}
        result["team_id"] = winnerTeam[0]
        result["name"] = winnerTeam[1]
        return result
    
    # This method maps is for getTeamsWithMostChampionships Method
    def map_to_dict_teams(self, team):
        result = {}
        result["team_id"] = team[0]
        result["name"] = team[1]
        result["total_wins"] = team[2]
        return result
    
    
    # This method maps the championship data for update to a dictionary format.
    def map_to_dic_for_update(self, championship, winnerTeam):
        result = {}
        result["id"] = championship[0]
        result["name"] = championship[1]
        result["winner_year"] = championship[2]
        result["winner_team"] = self.map_to_dict_teams(winnerTeam)
        return result
    
    
    #This method gets all championships from the database.
    def getAllChampionship(self):
        dao = PartDAO()
        championship_list = dao.getAllChampionship()
        result = []
        for championship in championship_list:
            obj = self.map_to_dict(championship)
            result.append(obj)
        return jsonify(result), 200
    
    
    #This method creates a new championship in the database.
    def createChampionship(self, json):
        
        name = json["name"]
        winner_team = json["winner_team"]
        winner_year = json["winner_year"]
        
        dao = PartDAO()
        championship_id = dao.createChampionShip(name, winner_team, winner_year)
        if name == "" or winner_team == "" or winner_year == "":
            return jsonify("Missing Parameters"), 400
        else:
            if not championship_id:
                return jsonify("Server Error"), 500
            else:
                json["id"] = championship_id
                return jsonify(json), 201
        
        
    #This method deletes a championship by its ID from the database.
    def deleteChampionshipById(self, id):
        dao = PartDAO()
        deleted = dao.deleteChampionById(id)
        if deleted:
            return jsonify(f"Deleted record with id={id}"), 200
        else:
            return jsonify("Not Found"), 404
    
    
    # This method updates a championship by its ID in the database.
    # It takes the championship details as parameters and returns the updated championship.
    def updateChampionshipById(self, json, id):

        name = json["name"]
        winner_team = json["winner_team"]
        winner_year = json["winner_year"]
        
        dao = PartDAO()
        updated = dao.updateChampionship(id, name, winner_team, winner_year)
        
        if name == "":
            return jsonify("Missing Parameters"), 400
        else:
            if updated == 0:
                return jsonify(f"Record with id={id}, does not exist"), 404
            elif updated == 1:
                championship = dao.getChampionshipForUpdate(id)
                result = self.map_to_dict(championship)
                return jsonify(result), 200
            elif updated == 2:
                return jsonify("Missing Parameters"), 400
            else:
                return jsonify("Not Found"), 404
        
        
    # This method gets a championship by its ID from the database.
    def getChampionshipById(self, id):
        
        dao = PartDAO()
        championship = dao.getChampionshipById(id)
        winnerTeam = dao.getWinnerTeamById(id)
        if championship and winnerTeam:
            result = self.map_to_dic_for_update(championship, winnerTeam)
            return jsonify(result), 200
        elif championship and not winnerTeam:
            return jsonify("Not Winner Team found with id={id}"), 404
        else:
            return jsonify("Not Found"), 404
        
        
    # This method gets the teams with the most championships from the database.
    def getTeamsWithMostChampionships(self):
        dao = PartDAO()
        teams = dao.getTeamsWithMostChampionShips()
        result = []
        for team in teams:
            obj = self.map_to_dict_teams(team)
            result.append(obj)
        return jsonify(result), 200        
        
    
    