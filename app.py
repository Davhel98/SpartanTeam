from flask import Flask, render_template, request, jsonify, make_response
import json
import os
from Team_Halo import fetch_kd_ratio, balance_teams

app = Flask(__name__)

@app.route('/')
def index():
    gamertags = request.cookies.get('gamertags')
    if gamertags:
        gamertags = json.loads(gamertags)
    else:
        gamertags = []
    return render_template('index.html', gamertags=gamertags)

@app.route('/search', methods=['GET'])
def search():
    gamertag = request.args.get('gamertag')
    if not gamertag:
        return jsonify({'error': 'No gamertag provided'}), 400

    kd_ratio = fetch_kd_ratio(gamertag)
    if kd_ratio == 0.0:
        return jsonify({'error': 'Failed to fetch data for gamertag'}), 400

    gamertags = request.cookies.get('gamertags')
    if gamertags:
        gamertags = json.loads(gamertags)
    else:
        gamertags = []

    if gamertag not in gamertags:
        gamertags.append(gamertag)

    response = make_response(jsonify({'gamertag': gamertag}))
    response.set_cookie('gamertags', json.dumps(gamertags))
    return response

@app.route('/import', methods=['POST'])
def import_gamertags():
    data = request.json
    gamertags = data.get('gamertags')

    if not gamertags:
        return jsonify({'error': 'No gamertags provided'}), 400

    valid_gamertags = []
    for gamertag in gamertags:
        kd_ratio = fetch_kd_ratio(gamertag)
        if kd_ratio != 0.0:
            valid_gamertags.append(gamertag)

    response = make_response(jsonify({'gamertags': valid_gamertags}))
    response.set_cookie('gamertags', json.dumps(valid_gamertags))
    return response

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    gamertags = data.get('gamertags')
    team_size = int(data.get('team_size'))

    if not gamertags or not team_size:
        return jsonify({'error': 'Invalid input'}), 400

    kd_ratios = {tag: fetch_kd_ratio(tag) for tag in gamertags}
    team1, team2 = balance_teams(kd_ratios, team_size)

    return jsonify({'team1': team1, 'team2': team2})

if __name__ == '__main__':
    app.run(debug=True)