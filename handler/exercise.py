from flask import jsonify
from dao.exercise import exerciseDAO
from flask import jsonify

class ExerciseHandler:

    def getAllExercise(self):
        dao = exerciseDAO()
        exercise_list = dao.getAllExercise()
        result_list = []
        for exercise in exercise_list:
            obj = self.map_to_dict(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getExerciseById(self, id):
        dao = exerciseDAO()
        exercise = dao.getExerciseById(id)
        if not exercise:
            return jsonify("Not Found"), 404
        else:
            result = self.map_to_dict(exercise)
            return jsonify(result), 200

    def deleteExerciseById(self, id):
        dao = exerciseDAO()
        deleted = dao.deleteExerciseById(id)
        if deleted:
            return jsonify(f"Deleted record with id={id}"), 200
        else:
            return jsonify("Not Found"), 404

    def map_to_dict(self, exercises):
        result = {}
        #id, name, category, equipment, mechanic, force, level, alter_id
        result["id"] = exercises[0]
        result["name"] = exercises[1]
        result["category"] = exercises[2]
        result["equipment"] = exercises[3]
        result["mechanic"] = exercises[4]
        result["force"] = exercises[5]
        result["level"] = exercises[6]
        result["alter_id"] = exercises[7]
        return result