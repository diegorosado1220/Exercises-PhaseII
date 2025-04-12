from flask import Flask, jsonify, request
from flask_cors import CORS
from handler.championship import ChampionshipsHandler
from handler.exercise import ExerciseHandler


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "General Kenobi"


@app.route('/exercise', methods=['GET', 'POST'])
def handleExercise():
    if request.method == 'GET':
        return ExerciseHandler().getAllExercise()
    elif request.method == 'POST':
        return ExerciseHandler().createExercise(request.json)
    else:
        return jsonify("Unsupported method"), 405
    

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
    
    
@app.route('/championships', methods=['POST', 'GET'])
def handleChampionship():
    if request.method == 'GET':
        return ChampionshipsHandler().getAllChampionship()
    elif request.method == 'POST':
        return ChampionshipsHandler().createChampionship(request.json)
    else:
        return jsonify("Unsupported Method"), 405
    
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



if __name__ == '__main__':
    app.run(debug=True)