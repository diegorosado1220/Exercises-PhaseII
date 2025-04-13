from flask import Flask, jsonify, request
from flask_cors import CORS
from handler.championship import ChampionshipsHandler
from handler.exercise import ExerciseHandler


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "General Kenobi"


#This route handles the /exercise endpoint for GET and POST requests.
@app.route('/exercise', methods=['GET', 'POST'])
def handleExercise():
    if request.method == 'GET':
        return ExerciseHandler().getAllExercise()
    elif request.method == 'POST':
        return ExerciseHandler().createExercise(request.json)
    else:
        return jsonify("Unsupported method"), 405
    
    
#This route handles the /exercise/<id> endpoint for GET, PUT, and DELETE requests.
@app.route('/exercise/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleExerciseById(id):
    if request.method == 'DELETE':
        return ExerciseHandler().deleteExerciseById(id)
        
    elif request.method == 'PUT':
        return ExerciseHandler().updateExerciseById(request.json, id)
    
    elif request.method == 'GET':
        return ExerciseHandler().getExerciseById(id)
    
    else:
        return jsonify("Unsupported Method"), 405
    
    
#This route handles the /exercises/most-performed endpoint for GET requests.
# It retrieves the most performed exercises from the database.
@app.route('/exercises/most-performed', methods=['GET'])
def handleExercisesMostPerformed():
    if request.method == 'GET':
        return ExerciseHandler().getMostPerformed()
    else:
        return jsonify("Unsupported method"), 405
    
    
#This route handles the /exercises/muscle-group/<muscleid> endpoint for GET requests.
# It retrieves exercises by a selected muscle from the database.
@app.route('/exercises/muscle-group/<string:muscleid>', methods=['GET'])
def handleExercisesByMucle(muscleid):
    if request.method == 'GET':
        return ExerciseHandler().getExercisesByMuscle(muscleid)
    else:
        return jsonify("Unsupported method"), 405
    
    
#This route handles the /exercises/most-complex endpoint for GET requests.
# It retrieves the most complex exercises from the database. 
@app.route('/exercises/most-complex', methods=['GET'])
def handleComplexExercises():
    if request.method == 'GET':
        return ExerciseHandler().getMostComplexExercises()
    else:
        return jsonify("Unsupported method"), 405
    


# This route handles the /championships endpoint for GET and POST requests.
@app.route('/championships', methods=['POST', 'GET'])
def handleChampionship():
    if request.method == 'GET':
        return ChampionshipsHandler().getAllChampionship()
    elif request.method == 'POST':
        return ChampionshipsHandler().createChampionship(request.json)
    else:
        return jsonify("Unsupported Method"), 405


# This route handles the /championships/<id> endpoint for GET, PUT, and DELETE requests.
@app.route('/championships/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleChampionshipById(id):
    if request.method == 'DELETE':
        return ChampionshipsHandler().deleteChampionshipById(id)
    elif request.method == 'PUT':
        return ChampionshipsHandler().updateChampionshipById(request.json, id)
    elif request.method == 'GET':
        return ChampionshipsHandler().getChampionshipById(id)
    else:
        return jsonify("Unsupported Method"), 40


# Add an instruction to a specific exercise
@app.route('/exercise/<int:exercise_id>/instruction', methods=['POST'])
def addInstructionToExercise(exercise_id):
    return ExerciseHandler().addInstructionToExercise(request.json, exercise_id)


# Delete an instruction from a specific exercise
@app.route('/exercise/<int:exercise_id>/instruction/<int:instruction_id>', methods=['DELETE'])
def deleteInstructionFromExercise(exercise_id, instruction_id):
    return ExerciseHandler().deleteInstructionFromExercise(exercise_id, instruction_id)


# Add image to an exercise
@app.route('/exercise/<int:exercise_id>/image', methods=['POST'])
def addImageToExercise(exercise_id):
    return ExerciseHandler().addImageToExercise(request.json, exercise_id)


# Add primary muscle to an exercise
@app.route('/exercise/<int:exercise_id>/primary-muscle', methods=['POST'])
def addPrimaryMuscleToExercise(exercise_id):
    return ExerciseHandler().addPrimaryMuscleToExercise(request.json, exercise_id)

#Delete a primary muscle from an exercise
@app.route('/exercise/<int:exercise_id>/primary-muscle/<int:primary_muscle_id>', methods=['DELETE'])
def deletePrimaryMuscleFromExercise(exercise_id, primary_muscle_id):
    return ExerciseHandler().deletePrimaryMuscleFromExercise(exercise_id, primary_muscle_id)


# Add secondary muscle to an exercise
@app.route('/exercise/<int:exercise_id>/secondary-muscle', methods=['POST'])
def addSecondaryMuscleToExercise(exercise_id):
    return ExerciseHandler().addSecondaryMuscleToExercise(request.json, exercise_id)


if __name__ == '__main__':
    app.run(debug=True)