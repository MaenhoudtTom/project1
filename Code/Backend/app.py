# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from subprocess import check_output, call
from RPi import GPIO

import time
# import threading

#import code for hardware
from Klasses.Mcp import Mcp
# from Klasses.PCF8574 import PCF8574
from Klasses.LCD_display import LCD_display
from Klasses.MPU6050 import MPU6050
from Klasses.ulstrasonic import Ultrasonic
from Klasses.distribute import Distribute
from helpers.klasseknop import Button

#global variables
ip_address = 0
sensor_errors = []

#hardware declaration
ldr = Mcp(0)
display = LCD_display(13, 19)
mpu = MPU6050(0x68)
sonic = Ultrasonic(25, 24)
distribute = Distribute(12, 16, 20, 21, 18, 23)

#hardware functions
def setup():
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def get_IP_address():
        ip = check_output(['hostname', '--all-ip-addresses'])
        ip = ip[:15].decode(encoding='utf8')
        print(ip)
        return ip

def show_ip_lcd():
    global ip_address
    ip_address = get_IP_address()
    display.send_instruction(1)
    display.write_message(ip_address)

def read_ldr():
    value = ldr.read_channel(ldr.bus)
    return value

def read_mpu():
    x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = mpu.read_data()
    return x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden

def measure_distance():
    distance = sonic.measure_distance()
    return distance

# flask, socketio
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET!AJF;LAJFL;JAFOQWPYUTROQIRUKDSAJF;LKASFJ;LADSFJOGJPOQEGJ;OQEW'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

#custom endpoint
endpoint = '/api/v1'

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/sensors', methods=['GET'])
def sensors():
    data = DataRepository.read_sensors()
    if data is not None:
        return jsonify(sensors = data), 200
    else:
        return jsonify(message = 'ERROR: there were no sensors found!'), 404

@app.route(endpoint + '/sensors/<sensor_id>', methods=['GET', 'PUT'])
def sensor(sensor_id):
    if request.method == 'GET':
        data = DataRepository.read_sensor_by_id(sensor_id)
        if data is not None:
            return jsonify(sensor = data), 200
        else:
            return jsonify(message = f'ERROR: there is no sensor with this id: {sensor_id}'), 404
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_sensor_by_id(sensor_id, gegevens['name'], gegevens['sensorType'], gegevens['unit'], gegevens['description'])
        if data is not None:
            if data > 0:
                return jsonify(message = 'Sensor is succesfull updated'), 200
            elif data == 0:
                return jsonify(message = 'There wasn\'t anything to update.'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with updating the sensor.'), 404

@app.route(endpoint + '/sensordata', methods=['GET', 'POST'])
def sensordata():
    if request.method == 'GET':
        data = DataRepository.read_sensors_with_history()
        if data is not None:
            return jsonify(sensordata = data), 200
        else:
            return jsonify(message = 'ERROR: there were no sensordata found!'), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.create_sensor_data(gegevens['sensorID'], gegevens['value'])
        if data is not None:
            return jsonify(historyID = data), 201
        else:
            return jsonify(message = 'ERROR: please try again'), 400

@app.route(endpoint + '/sensordata/<sensor_id>', methods=['GET', 'DELETE'])
def sensordata_by_id(sensor_id):
    if request.method == 'GET':
        data = DataRepository.read_history_by_sensorID(sensor_id)
        if data is not None:
            return jsonify(sensordata = data), 200
        else:
            return jsonify(message = f'ERROR: there is no sensor with this id: {sensor_id}!'), 404

@app.route(endpoint + '/sensordata/delete/<history_id>', methods=['DELETE'])
def deleteHistory(history_id):
    data = DataRepository.delete_history(history_id)
    if data is not None:
        if data > 0:
            return jsonify(message = 'The value is succesfull deleted.'), 200
        elif data == 0:
            return jsonify(message = 'No value has been deleted.'), 200
    else:
        return jsonify(message = 'ERROR: there went something wrong with deleting the value.'), 404

@app.route(endpoint + '/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        data = DataRepository.read_games()
        if data is not None:
            return jsonify(games = data), 200
        else:
            return jsonify(message = 'ERROR: there were no games found!'), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.create_game(gegevens['name'], gegevens['description'], gegevens['cardDecks'], gegevens['rulesetID'])
        if data is not None:
            return jsonify(gameid = data), 201
        else:
            return jsonify(message = 'ERROR: please try again!'), 400

@app.route(endpoint + '/gamesWithRules', methods=['GET'])
def gamesWithRules():
    data = DataRepository.read_games_with_rulesets_and_playerinfo()
    if data is not None:
        return jsonify(games = data), 200
    else:
        return jsonify(message = 'ERROR: please try again!'), 404

@app.route(endpoint + '/gamesWithRules/<game_id>', methods=['GET'])
def gameWithRules(game_id):
    data = DataRepository.read_game_with_ruleset_and_playerinfo_by_id(game_id)
    if data is not None:
        return jsonify(game = data), 200
    else:
        return jsonify(message = f'ERROR: there is no game with this id: {game_id}'), 404

@app.route(endpoint + '/games/<game_id>', methods=['GET', 'PUT', 'DELETE'])
def game(game_id):
    if request.method == 'GET':
        data = DataRepository.read_game_by_id(game_id)
        if data is not None:
            return jsonify(game = data), 200
        else:
            return jsonify(message = f'ERROR: there is no game with this id: {game_id}'), 404
    elif request.method == 'PUT': 
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_game_by_id(game_id, gegevens['name'], gegevens['description'], gegevens['cardDecks'], gegevens['rulesetID'])
        if data is not None:
            if data > 0:
                return jsonify(gameID = data), 200
            elif data == 0:
                return jsonify(message = 'There wasn\'t anything to update.'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with updating the game.'), 404
    elif request.method == 'DELETE':
        data = DataRepository.delete_game(game_id)
        if data is not None:
            if data > 0:
                return jsonify(message = 'The game has been deleted.'), 200
            elif data == 0:
                return jsonify(message = 'No game has been deleted.'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with deleting the game'), 404

@app.route(endpoint + '/rulesets', methods=['GET', 'POST'])
def rulesets():
    if request.method == 'GET':
        data = DataRepository.read_rulesets()
        if data is not None:
            return jsonify(rulesets = data), 200
        else:
            return jsonify(message = 'ERROR: there were no rulesets found!'), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.create_ruleset(gegevens['playerInfoID'], gegevens['cardsPerPlayer'])
        if data is not None:
            return jsonify(ruleset = data), 201
        else:
            return jsonify(message = 'ERROR: please try again!'), 404

@app.route(endpoint + '/rulesets/<ruleset_id>', methods=['GET', 'PUT', 'DELETE'])
def ruleset(ruleset_id):
    if request.method == 'GET':
        data = DataRepository.read_ruleset_by_id(ruleset_id)
        if data is not None:
            return jsonify(ruleset = data), 200
        else:
            return jsonify(message = f'ERROR: there is no ruleset with this id: {ruleset_id}'), 404
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_ruleset_by_id(ruleset_id, gegevens['playerInfoID'], gegevens['cardsPerPlayer'])
        if data is not None:
            if data > 0:
                return jsonify(rulesetID = data), 200
            elif data == 0:
                return jsonify(message = 'There wasn\'t anything to update'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with updating the ruleset'), 404
    elif request.method == 'DELETE':
        data = DataRepository.delete_ruleset(ruleset_id)
        if data is not None:
            if data > 0:
                return jsonify(message = 'The ruleset is succesfull deleted'), 200
            elif data == 0:
                return jsonify(message = 'No ruleset has been deleted.'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with deleting the ruleset.'), 404

@app.route(endpoint + '/playerinfo', methods=['GET', 'POST'])
def playerinfo():
    if request.method == 'GET':
        data = DataRepository.read_playerinfo()
        if data is not None:
            return jsonify(playerInfo = data), 200
        else:
            return jsonify(message = 'ERROR: there was no playerinfo found!'), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.create_playerinfo(gegevens['minimumAge'], gegevens['minimumPlayers'], gegevens['maximumPlayers'])
        if data is not None:
            return jsonify(playerinfo = data), 201
        else:
            return jsonify(message = 'ERROR: please try again!'), 404

@app.route(endpoint + '/playerinfo/<playerinfo_id>', methods=['GET', 'PUT', 'DELETE'])
def playerinformation(playerinfo_id):
    if request.method == 'GET':
        data = DataRepository.read_playerinfo_by_id(playerinfo_id)
        if data is not None:
            return jsonify(playerinfo = data), 200
        else:
            return jsonify(message = f'ERROR: there is no playerinfo with this id: {playerinfo_id}'), 404
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_playerinfo_by_id(playerinfo_id, gegevens['minimumAge'], gegevens['minimumPlayers'], gegevens['maximumPlayers'])
        if data is not None:
            if data > 0:
                return jsonify(message = 'Playerinfo succesfull updated.'), 200
            elif data == 0:
                return jsonify(message = 'There wasn\'t anything to update.'), 200
        else:
            return jsonify(message = 'ERROR: there wen\'t something wrong with updating the playerinfo.'), 404
    elif request.method == 'DELETE':
        data = DataRepository.delete_playerinfo(playerinfo_id)
        if data is not None:
            if data > 0:
                return jsonify(message = 'The playerinfo is succesfull deleted.'), 200
            elif data == 0:
                return jsonify(message = 'No playerinfo has been deleted.'), 200
        else:
            return jsonify(message = 'ERROR: there went something wrong with deleting the playerinfo.'), 404 

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
#     # # Send to the client!
#     # vraag de status op van de lampen uit de DB
#     status = DataRepository.read_status_lampen()
#     socketio.emit('B2F_status_lampen', {'lampen': status})

@socketio.on('F2B_log_sensor_data')
def log_sensor_data():
    id_ldr = DataRepository.read_id_sensor('LDR')['id']
    id_accelerometerX = DataRepository.read_id_sensor('AccelerometerX')['id']
    id_accelerometerY = DataRepository.read_id_sensor('AccelerometerY')['id']
    id_accelerometerZ = DataRepository.read_id_sensor('AccelerometerZ')['id']
    id_gyroscopeX = DataRepository.read_id_sensor('GyroscopeX')['id']
    id_gyroscopeY = DataRepository.read_id_sensor('GyroscopeY')['id']
    id_gyroscopeZ = DataRepository.read_id_sensor('GyroscopeZ')['id']
    id_sonic = DataRepository.read_id_sensor('Ultrasonic sensor')['id']

    # print(id_ldr)
    # print(id_accelerometerX)
    # print(id_accelerometerY)
    # print(id_accelerometerZ)
    # print(id_gyroscopeX)
    # print(id_gyroscopeY)
    # print(id_gyroscopeZ)
    # print(id_sonic)

    value_ldr = read_ldr()
    # print(value_ldr)
    x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = read_mpu()
    # print(x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden)
    value_sonic = measure_distance()
    # print(value_sonic)

    data_ldr = DataRepository.create_sensor_data(id_ldr, value_ldr)
    # print(data_ldr)
    data_accelerometerX = DataRepository.create_sensor_data(id_accelerometerX, x_waarde_accelero_in_g)
    # print(data_accelerometerX)
    data_accelerometerY = DataRepository.create_sensor_data(id_accelerometerY, y_waarde_accelero_in_g)
    # print(data_accelerometerY)
    data_accelerometerZ = DataRepository.create_sensor_data(id_accelerometerZ, z_waarde_accelero_in_g)
    # print(data_accelerometerZ)
    data_gyroscopeX = DataRepository.create_sensor_data(id_gyroscopeX, x_waarde_gyro_in_graden)
    # print(data_gyroscopeX)
    data_gyroscopeY = DataRepository.create_sensor_data(id_gyroscopeY, y_waarde_gyro_in_graden)
    # print(data_gyroscopeY)
    data_gyroscopeZ = DataRepository.create_sensor_data(id_gyroscopeZ, z_waarde_gyro_in_graden)
    # print(data_gyroscopeZ)
    data_sonic = DataRepository.create_sensor_data(id_sonic, value_sonic)
    # print(data_sonic)

    print('data created')

    if data_ldr is None:
        sensor_errors.append('Something went wrong getting data from LDR.')
        print('error ldr')
    elif data_accelerometerX is None or data_accelerometerY is None or data_accelerometerZ is None:
        sensor_errors.append('Something went wrong getting data from the accelerometer.')
        print('error accelero')
    elif data_gyroscopeX is None or data_gyroscopeY is None or data_gyroscopeZ is None:
        print('error gyro')
        sensor_errors.append('Something went wrong getting data from the gyroscope.')
    # print(sensor_errors)

    if len(sensor_errors) == 0:
        print('sending message to front')
        socketio.emit('B2F_logged_data')
    else:
        socketio.emit('B2F_error_logging_data', jsonify(sensor_errors))

@socketio.on('F2B_distribute_cards')
def distribute_card(player_info, cards_per_player):
    for i in range(cards_per_player):
        distribute.distribute_card()

@socketio.on('F2B_change_game')
def change_game(game_data):
    game_id = game_data['ID']
    name = game_data['Name']
    desc = game_data['Description']
    decks = int(game_data['CardDecks'])
    cards = int(game_data['CardsPerPlayer'])
    age = int(game_data['MinimumAge'])
    min_players = int(game_data['MinimumPlayers'])
    max_players = int(game_data['MaximumPlayers'])
    playerinfoid = int(game_data['PlayerInfoID'])
    rulesetid = int(game_data["RulesetID"])

    print(game_id)
    print(name)
    print(desc)
    print(decks)
    print(cards)
    print(age)
    print(min_players)
    print(max_players)
    print(playerinfoid)
    print(rulesetid)
    print('-------------')

    existing_playerinfoid = DataRepository.read_playerinfo_by_data(age, min_players, max_players)

    if existing_playerinfoid is not None:
        playerinfoid = int(existing_playerinfoid["ID"])

    existing_rulesetid = DataRepository.read_ruleset_by_data(cards, playerinfoid)

    if existing_rulesetid is not None:
        rulesetid = int(existing_rulesetid["ID"])

    game = DataRepository.update_game_by_id(game_id, name, desc, decks, rulesetid)
    ruleset = DataRepository.update_ruleset_by_id(rulesetid, playerinfoid, cards)
    playerinfo = DataRepository.update_playerinfo_by_id(playerinfoid, age, min_players, max_players)

    print(rulesetid)
    print(playerinfoid)
    print(game)
    print(ruleset)
    print(playerinfo)
    
    socketio.emit('B2F_changed_game')

@socketio.on('F2B_create_game')
def create_game(game_data):
    name = game_data['Name']
    desc = game_data['Description']
    decks = int(game_data['CardDecks'])
    cards = int(game_data['CardsPerPlayer'])
    age = int(game_data['MinimumAge'])
    min_players = int(game_data['MinimumPlayers'])
    max_players = int(game_data['MaximumPlayers'])
    playerinfoid = 0
    rulesetid = 0

    existing_playerinfoid = DataRepository.read_playerinfo_by_data(age, min_players, max_players)

    if existing_playerinfoid is not None:
        playerinfoid = int(existing_playerinfoid["ID"])
    else:
        playerinfoid = DataRepository.create_playerinfo(age, min_players, max_players)
        

    existing_rulesetid = DataRepository.read_ruleset_by_data(cards, playerinfoid)

    if existing_rulesetid is not None:
        rulesetid = int(existing_rulesetid["ID"])
    else:
        rulesetid = DataRepository.create_ruleset(playerinfoid, cards, 0)

    gameid = DataRepository.create_game(name, desc, decks, rulesetid)

    socketio.send('B2F_game_created')

@socketio.on('F2B_delete_game')
def delete_game(game_id):
    data = DataRepository.delete_game(game_id['ID'])
    socketio.emit('B2F_game_deleted')

@socketio.on('F2B_shutdown')
def shutdown():
    call("sudo shutdown -h now", shell=True)

if __name__ == '__main__':
    try:
        setup()
        show_ip_lcd()
        # socketio.run(app, host=f'{ip_address}', port=5000, debug=False)
        socketio.run(app, host='0.0.0.0', debug=False)
    except KeyboardInterrupt as e:
        print('Quitting.....')
    finally:
        GPIO.cleanup()
        print("Programm has been closed")

