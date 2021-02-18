from flask import Flask, jsonify
from flask import render_template
from flask_table import Table, Col
from pony.orm import *
from flask import request
import json
import collections

app = Flask(__name__)

db = Database()
db.bind(provider="sqlite", filename="discgolf.db", create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def db_getData(id):
    course = db.select(
        "name, location, holeNumber, par, length FROM hole INNER JOIN course ON hole.course_id = course.courseID AND courseID = "
        + str(id)
    )
    return course


@db_session
def db_getName():
    courseName = db.select("courseID, name FROM course")
    return courseName


@db_session
def db_getGameData():
    game = db.select(
        "SELECT holenumber,par,LENGTH, score, name FROM score inner join hole on score.hole_id = hole.holeID INNER JOIN game on score.game_id = game.gameID inner join player on score.player_id = player.playerID AND score.game_id=2"
    )
    return game


@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/game")
def game():
    """Gets and format data for game scores table"""
    game = db_getGameData()

    headers = ["Holenumber", "Lenght", "Par"]

    for x in game:
        if x.holeNumber == 1:
            headers.append(x.name)

    gameData = []
    gameData.append([])
    skip = False    #Holenumber, par and length are needed only one time per hole.  
    tmp = 1
    y = 0
    for i in game:

        if i.holeNumber > tmp:
            tmp = i.holeNumber
            skip = False
            y = y + 1
            gameData.append([])

        if skip == False:
            gameData[y].append(i.holeNumber)
            gameData[y].append(i.length)
            gameData[y].append(i.par)
            skip = True

        if tmp == i.holeNumber:
            gameData[y].append(i.score)

    return render_template("game.html", table=gameData, headers=headers)


@app.route("/api/name", methods=["GET"])
""" Returns course names and id's in JSON format"""
def api_select():
    name = db_getName()
    objects_list = []
    for row in name:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        objects_list.append(d)

    j = json.dumps(objects_list)
    return j


@app.route("/api/courses", methods=["GET"])
""" Returns data from courses for datatable"""
def api_id():
    results = []
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided. Please specify an id."

    results = db_getData(id)
    return jsonify({"data": results})


@app.route("/courses")
def courses():
    return render_template("courses.html")


if __name__ == "__main__":
    app.run()
