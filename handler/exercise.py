from flask import jsonify
from dao.exercise import exerciseDAO
from flask import jsonify

class ExerciseHandler:

    # This method maps the exercise data to a dictionary format.
    def map_to_dict(self, exercises):
        result = {}
        result["id"] = exercises[0]
        result["name"] = exercises[1]
        result["category"] = exercises[2]
        result["equipment"] = exercises[3]
        result["mechanic"] = exercises[4]
        result["force"] = exercises[5]
        result["level"] = exercises[6]
        result["alter_id"] = exercises[7]
        return result
    
    # This method maps the instructions data to a dictionary format.
    def map_to_dict_instructions(self, instructions):
        result = {}
        result["instruction_id"] = instructions[0]
        result["instruction_number"] = instructions[1]
        result["description"] = instructions[2]
        return result
    
    # This method maps the images data to a dictionary format.
    def map_to_dict_images(self, images):
        result = {}
        result["image_id"] = images[0]
        result["path"] = images[1]
        return result
    
    # This method maps the primary muscles data to a dictionary format.
    def map_to_dict_primary_muscles(self, primary_muscles):
        result = {}
        result["muscle_id"] = primary_muscles[0]
        result["name"] = primary_muscles[1] 
        return result
    
    # This method maps the secondary muscles data to a dictionary format.
    def map_to_dict_secondary_muscles(self, secondary_muscles):
        result = {}
        result["muscle_id"] = secondary_muscles[0]
        result["name"] = secondary_muscles[1]
        return result
    
    # This method maps the most performed exercises data to a dictionary format.
    def map_to_dict_most_performed(self, most_performed):
        result = {}
        result["exercise_id"] = most_performed[0]
        result["name"] = most_performed[1]
        result["sports_related"] = most_performed[2]
        return result
    
    # This method maps the exercises used by selected muscle data to a dictionary format.
    def map_to_dict_Exercise_By_Muscle(self, exercises):
        result = {}
        result["exercise_id"] = exercises[0]
        result["name"] = exercises[1]
        return result
    
    def map_to_dict_Most_Complex_Exercises(self, exercises):
        result = {}
        result["exercise_id"] = exercises[0]
        result["name"] = exercises[1]
        result["muscle_groups"] = exercises[2]
        return result
        
    
    # This method maps the exercise data to a dictionary format for the getExerciseById method.
    # It includes instructions, images, primary muscles, and secondary muscles.
    def map_to_dic_for_getExerciseById(self, exercise, instructions, images, primary_muscles, secondary_muscles):
        result = {}
        
        result["id"] = exercise[0]
        result["name"] = exercise[1]
        result["category"] = exercise[2]
        result["equipment"] = exercise[3]
        result["mechanic"] = exercise[4]
        result["force"] = exercise[5]
        result["level"] = exercise[6]
        result["alter_id"] = exercise[7]

        instructions_list = []
        if not instructions:
            instructions_list.append("Error, No Instructions found")
        else:
            for instruction in instructions:
                obj = self.map_to_dict_instructions(instruction)
                instructions_list.append(obj)
        
        images_list = []
        if not images:
            images_list.append("Error, No Images found")
        else:
            for image in images:
                obj = self.map_to_dict_images(image)
                images_list.append(obj)

        primary_muscles_list = []
        if not primary_muscles:
            primary_muscles_list.append("Error, No Primary muscles found")
        else:
            for primary_muscle in primary_muscles:
                obj = self.map_to_dict_primary_muscles(primary_muscle)
                primary_muscles_list.append(obj)


        secondary_muscles_list = []
        if not secondary_muscles:
            secondary_muscles_list.append("Error, No Secondary muscles found")
        else:
            for secondary_muscle in secondary_muscles:
                obj = self.map_to_dict_secondary_muscles(secondary_muscle)
                secondary_muscles_list.append(obj)


        result["instructions"] = instructions_list
        result["images"] = images_list
        result["primary_muscles"] = primary_muscles_list
        result["secondary_muscles"] = secondary_muscles_list

        return result
    
    # This method creates a new exercise in the database.
    def createExercise(self, json):

        name = json["name"]
        category = json["category"]
        equipment = json["equipment"]
        mechanic = json["mechanic"]
        force = json["force"]
        level = json["level"]
        alter_id = json["alter_id"]

        dao = exerciseDAO()
        exercise_id = dao.createExercise(name, category, equipment, mechanic, force, level, alter_id)
        if not exercise_id:
            return jsonify("Server Error"), 500
        
        elif name == "" or category == "" or equipment == "" or mechanic == "" or force == "" or level == "" or alter_id == "":
            return jsonify("Missing Parameters"), 400
        
        else:
            json["id"] = exercise_id
            return jsonify(json), 201

    # This methods gets all exercises from the database.
    def getAllExercise(self):
        dao = exerciseDAO()
        exercise_list = dao.getAllExercise()
        result_list = []
        for exercise in exercise_list:
            obj = self.map_to_dict(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200

    #This method gets an exercise by its ID from the database.
    def getExerciseById(self, id):
        dao = exerciseDAO()
        exercise = dao.getExerciseById(id)
        instructions = dao.getInstructionsById(id)
        images = dao.getImagesById(id)
        primary_muscles = dao.getPrimaryMuscleById(id)
        secondary_muscles = dao.getSecondaryMuscleById(id)
        
        if exercise is not None:
            result = self.map_to_dic_for_getExerciseById(exercise, instructions, images, primary_muscles, secondary_muscles)
            return jsonify(result), 200
        else:
            return jsonify(f"No Exercise found with id={id}"), 404

    #This method updates an exercise by its ID in the database.
    def updateExerciseById(self, json, id):

        name = json["name"]
        category = json["category"]
        equipment = json["equipment"]
        mechanic = json["mechanic"]
        force = json["force"]
        level = json["level"]
        alter_id = json["alter_id"]

        dao = exerciseDAO()
        updated = dao.updateExercise(id, name, category, equipment, mechanic, force, level, alter_id)

        if name == "" or category == "" or equipment == "" or mechanic == "" or force == "" or level == "" or alter_id == "":
            return jsonify("Missing Parameters"), 400
        else:
            if updated:
                exercise = dao.getExerciseForUpdate(id)
                result = self.map_to_dict(exercise)
                return jsonify(result), 200
            else:
                return jsonify("Not Found"), 404

    #This method deletes an exercise by its ID from the database.
    def deleteExerciseById(self, id):
        dao = exerciseDAO()
        deleted = dao.deleteExerciseById(id)
        if deleted == 0:
            return jsonify(f"Record with id={id}, does not exist"), 404
        elif deleted == 1:
            return jsonify(f"Deleted record with id={id}"), 200
        elif deleted == 2:
            return jsonify(f"Cannnot delete because its referenced"), 409
        else:
            return jsonify("Not Found"), 404
        
    #This method gets the most performed exercises.
    def getMostPerformed(self):
        dao = exerciseDAO()
        most_performed = dao.getMostPerformed()
        result = []
        if not most_performed:
            return jsonify("No Most Performed found"), 404
        else:
            for exercise in most_performed:
                obj = self.map_to_dict_most_performed(exercise)
                result.append(obj)
            return jsonify(result), 200
        
        
    #This method gets the exercises used by selected muscle
    def getExercisesByMuscle(self, muscleid):
        
        dao = exerciseDAO()
        exercises = dao.getExercisesByMuscle(muscleid)
        result = []
        for exercise in exercises:
            obj = self.map_to_dict_Exercise_By_Muscle(exercise)
            result.append(obj)
        if not result:
            return jsonify(f"No exercise found with muscle = '{muscleid}' "), 404
        else:
            return jsonify(result), 200
        
    #This method gets the most complex exercises.
    def getMostComplexExercises(self):
        dao = exerciseDAO()
        exercise_list = dao.getMostComplexExercises()
        result_list = []
        for exercise in exercise_list:
            obj = self.map_to_dict_Most_Complex_Exercises(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200

    #this method is to add instruction to exercise
    # POST /exercise/<exercise_id>/instruction
    def addInstructionToExercise(self, json, exercise_id):
        instruction_number = json["instruction_number"]
        description = json["description"]

        dao = exerciseDAO()
        instruction_id = dao.addInstruction(exercise_id, instruction_number, description)

        if instruction_id:
            result = {
                "instruction_id": instruction_id,
                "exercise_id": exercise_id,
                "instruction_number": instruction_number,
                "description": description
            }
            return jsonify(result), 201
        else:
            return jsonify("Insert Failed"), 500

    # DELETE /exercise/<exercise_id>/instruction/<instruction_id>
    # def deleteInstructionFromExercise(self, exercise_id, instruction_id):
    #     dao = exerciseDAO()
    #     success = dao.deleteInstruction(exercise_id, instruction_id)
    #
    #     if success:
    #         return '', 204
    #     else:
    #         return jsonify("Not Found"), 404

    # This method adds an image to an exercise
    def addImageToExercise(self, json, exercise_id):
        path = json["path"]
        dao = exerciseDAO()
        image_id = dao.addImageToExercise(exercise_id, path)

        if image_id:
            result = {
                "image_id": image_id,
                "exercise_id": exercise_id,
                "path": path
            }
            return jsonify(result), 201
        else:
            return jsonify("Insert Failed"), 500

