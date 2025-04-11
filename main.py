from flask import Flask, jsonify, request
from flask_cors import CORS

from handler.exercise import ExerciseHandler
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "General Kenobi"
@app.route('/exercise')
def handleExercise():
    if request.method == 'GET':
        return ExerciseHandler().getAllExercise()
    elif request.method == 'POST':
        return ExerciseHandler().insertExercise(request.json)

    else:
        return jsonify("Unsupported method"), 405

@app.route('/exercise/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleExerciseById(id):
    if request.method == 'DELETE':
        #return ExerciseHandler().deleteExerciseById(id)
        pass
    # elif request.method == 'PUT':
    #     return ExerciseHandler().updateExerciseById(request.json, id)
    elif request.method == 'GET':
        return ExerciseHandler().getExerciseById(id)
    else:
        return jsonify("Unsupported Method"), 405

if __name__ == '__main__':
    app.run(debug=True)