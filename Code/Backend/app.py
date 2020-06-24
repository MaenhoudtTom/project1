# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from subprocess import check_output, call
from RPi import GPIO

import time
# import threading

# import code for hardware
from Klasses.Mcp import Mcp
# from Klasses.PCF8574 import PCF8574
from Klasses.LCD_display import LCD_display
from Klasses.MPU6050 import MPU6050
from Klasses.ulstrasonic import Ultrasonic
from Klasses.distribute import Distribute
from helpers.klasseknop import Button

#global variables
sensor_errors_saving_data = []
sensor_errors = []

# hardware declaration
ldr = Mcp(0)
display = LCD_display(13, 19)
mpu = MPU6050(0x68)
sonic = Ultrasonic(25, 24)
distribute = Distribute(12, 16, 20, 21, 18)

# hardware functions
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)


def get_IP_address():
    ips = check_output(['hostname', '--all-ip-addresses'])
    space = str(ips).find(' ') - 1
    lan_ip = ips[:space].decode(encoding='utf8')
    wan_ip = ips[space:].decode(encoding='utf8')
    print(lan_ip)
    print(wan_ip)
    return lan_ip, wan_ip


def show_ip_lcd():
    lan_ip, wan_ip = get_IP_address()
    if wan_ip:
        display.send_instruction(1)
        display.write_message(wan_ip)
        print('boot message')
        display.send_instruction(0x40 | 128)
        display.write_message("Booted")
    else:
        display.send_instruction(1)
        display.write_message(lan_ip)
        print('boot message')
        display.send_instruction(0x40 | 128)
        display.write_message("Booted")

def read_ldr():
    value = ldr.read_channel(ldr.bus)
    return value


def read_mpu():
    x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = mpu.read_data()
    return x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden


def measure_distance():
    distance = sonic.measure_distance()
    return distance

def log_sensor_data():
    dis_cards = True
    values_gyro_x = []
    values_gyro_y = []
    values_gyro_z = []

    id_ldr = DataRepository.read_id_sensor('LDR')['id']
    id_gyroscopeX = DataRepository.read_id_sensor('GyroscopeX')['id']
    id_gyroscopeY = DataRepository.read_id_sensor('GyroscopeY')['id']
    id_gyroscopeZ = DataRepository.read_id_sensor('GyroscopeZ')['id']
    id_sonic = DataRepository.read_id_sensor('Ultrasonic sensor')['id']

    # print(id_ldr)
    # print(id_gyroscopeX)
    # print(id_gyroscopeY)
    # print(id_gyroscopeZ)
    # print(id_sonic)

    value_ldr = read_ldr()
    print(value_ldr)

    #store values from gyro for x amount of seconds to detect changes
    end_time = time.time() + 3
    while time.time() < end_time:
        x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = read_mpu()
        # print(x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden)
        values_gyro_x.append(x_waarde_gyro_in_graden)
        values_gyro_y.append(y_waarde_gyro_in_graden)
        values_gyro_z.append(z_waarde_gyro_in_graden)
        # print('while')

    #calculate average
    # print('calculating')
    average_gyro_x = sum(values_gyro_x) / len(values_gyro_x)
    average_gyro_y = sum(values_gyro_y) / len(values_gyro_y)
    average_gyro_z = sum(values_gyro_z) / len(values_gyro_z)
    print(average_gyro_x)
    print(average_gyro_y)
    print(average_gyro_z)
    # print('done calculating')
    
    value_sonic = measure_distance()
    print(value_sonic)

    #check values before logging data into database
    if value_ldr is not None:
        data_ldr = DataRepository.create_sensor_data(id_ldr, value_ldr)
        # print(data_ldr)
        if data_ldr is None:
            sensor_errors_saving_data.append('ldr')
            # print('ldr')
    else:
        sensor_errors.append('ldr')

    if x_waarde_gyro_in_graden is not None and y_waarde_gyro_in_graden is not None and z_waarde_gyro_in_graden is not None:
        data_gyroscopeX = DataRepository.create_sensor_data(
        id_gyroscopeX, average_gyro_x)
        # print(data_gyroscopeX)
        data_gyroscopeY = DataRepository.create_sensor_data(
            id_gyroscopeY, average_gyro_y)
        # print(data_gyroscopeY)
        data_gyroscopeZ = DataRepository.create_sensor_data(
            id_gyroscopeZ, average_gyro_z)
        # print(data_gyroscopeZ)
        if data_gyroscopeX is None or data_gyroscopeY is None or data_gyroscopeZ is None:
            print('gyroscope')
            sensor_errors_saving_data.append(
                'gyroscope')

    if value_sonic is not None:
        data_sonic = DataRepository.create_sensor_data(id_sonic, value_sonic)
        # print(data_sonic)
        if data_sonic is None:
            sensor_errors_saving_data.append('Ultrasonic sensor')
    else:
        sensor_errors.append('Ultrasonic sensor')

    #check if sensor values indicate that it is ok to distribute cards
    if (value_ldr < 800) or (average_gyro_x < 0.20 or average_gyro_x > 0.35) or (average_gyro_y < 0.10 or average_gyro_y > 0.35) or (average_gyro_z < 0.20 or average_gyro_z > 0.35):
        dis_cards = False
        socketio.emit('B2F_error_according_to_sensors')

    #check if cards are placed
    if value_sonic > 7.5:
        socketio.emit('B2F_no_cards_placed')
    
    # print(sensor_errors)

    if len(sensor_errors) != 0:
        socketio.emit('B2F_error_sensors', sensor_errors)
    
    if len(sensor_errors_saving_data) != 0:
        socketio.emit('B2F_error_saving_data', sensor_errors_saving_data)

    return dis_cards

# flask, socketio
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET!AJF;LAJFL;JAFOQWPYUTROQIRUKDSAJF;LKASFJ;LADSFJOGJPOQEGJ;OQEW'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# custom endpoint
endpoint = '/api/v1'

# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@app.route(endpoint + '/sensors', methods=['GET'])
def sensors():
    data = DataRepository.read_sensors()
    if data is not None:
        return jsonify(sensors=data), 200
    else:
        return jsonify(message='ERROR: there were no sensors found!'), 404


@app.route(endpoint + '/sensors/<sensor_id>', methods=['GET', 'PUT'])
def sensor(sensor_id):
    if request.method == 'GET':
        data = DataRepository.read_sensor_by_id(sensor_id)
        if data is not None:
            return jsonify(sensor=data), 200
        else:
            return jsonify(message=f'ERROR: there is no sensor with this id: {sensor_id}'), 404
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_sensor_by_id(
            sensor_id, gegevens['name'], gegevens['sensorType'], gegevens['unit'], gegevens['description'])
        if data is not None:
            if data > 0:
                return jsonify(message='Sensor is succesfull updated'), 200
            elif data == 0:
                return jsonify(message='There wasn\'t anything to update.'), 200
        else:
            return jsonify(message='ERROR: there went something wrong with updating the sensor.'), 404

@app.route(endpoint + '/sensordata/<sensor_id>', methods=['GET', 'DELETE'])
def sensordata_by_id(sensor_id):
    if request.method == 'GET':
        data = DataRepository.read_history_by_sensorID(sensor_id)
        if data is not None:
            return jsonify(sensordata=data), 200
        else:
            return jsonify(message=f'ERROR: there is no sensor with this id: {sensor_id}!'), 404


@app.route(endpoint + '/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        data = DataRepository.read_games()
        if data is not None:
            return jsonify(games=data), 200
        else:
            return jsonify(message='ERROR: there were no games found!'), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.create_game(
            gegevens['name'], gegevens['description'], gegevens['cardDecks'], gegevens['rulesetID'])
        if data is not None:
            return jsonify(gameid=data), 201
        else:
            return jsonify(message='ERROR: please try again!'), 404

@app.route(endpoint + '/gamesWithRules/<game_id>', methods=['GET'])
def gameWithRules(game_id):
    data = DataRepository.read_game_with_ruleset_and_playerinfo_by_id(game_id)
    if data is not None:
        return jsonify(game=data), 200
    else:
        return jsonify(message=f'ERROR: there is no game with this id: {game_id}'), 404


@app.route(endpoint + '/games/<game_id>', methods=['GET', 'PUT', 'DELETE'])
def game(game_id):
    if request.method == 'GET':
        data = DataRepository.read_game_by_id(game_id)
        if data is not None:
            return jsonify(game=data), 200
        else:
            return jsonify(message=f'ERROR: there is no game with this id: {game_id}'), 404
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)

        data = DataRepository.update_game_by_id(
            game_id, gegevens['name'], gegevens['description'], gegevens['cardDecks'], gegevens['rulesetID'])
        if data is not None:
            if data > 0:
                return jsonify(gameID=data), 200
            elif data == 0:
                return jsonify(message='There wasn\'t anything to update.'), 200
        else:
            return jsonify(message='ERROR: there went something wrong with updating the game.'), 404
    elif request.method == 'DELETE':
        data = DataRepository.delete_game(game_id)
        if data is not None:
            if data > 0:
                return jsonify(message='The game has been deleted.'), 200
            elif data == 0:
                return jsonify(message='No game has been deleted.'), 200
        else:
            return jsonify(message='ERROR: there went something wrong with deleting the game'), 404

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_distribute_cards')
def distribute_card(data):
    players = int(data['Players'])
    cards = int(data['CardsPerPlayer'])
    decks = int(data['CardDecks'])
    print(f'{players} players')
    print(f'{cards} cards')
    print(f'{decks} decks')
    disc_cards = log_sensor_data()
    print(disc_cards)
    if disc_cards == True:
        socketio.emit('B2F_distributing')
        # print('message sent')
        distribute.distribute_card(players, cards)
        distribute.remove_remaining_cards(players, cards, decks)

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

    existing_playerinfoid = DataRepository.read_playerinfo_by_data(
        age, min_players, max_players)

    if existing_playerinfoid is not None:
        playerinfoid = int(existing_playerinfoid["ID"])

    existing_rulesetid = DataRepository.read_ruleset_by_data(
        cards, playerinfoid)

    if existing_rulesetid is not None:
        rulesetid = int(existing_rulesetid["ID"])

    game = DataRepository.update_game_by_id(
        game_id, name, desc, decks, rulesetid)
    ruleset = DataRepository.update_ruleset_by_id(
        rulesetid, playerinfoid, cards)
    playerinfo = DataRepository.update_playerinfo_by_id(
        playerinfoid, age, min_players, max_players)

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

    existing_playerinfoid = DataRepository.read_playerinfo_by_data(
        age, min_players, max_players)

    if existing_playerinfoid is not None:
        playerinfoid = int(existing_playerinfoid["ID"])
    else:
        playerinfoid = DataRepository.create_playerinfo(
            age, min_players, max_players)

    existing_rulesetid = DataRepository.read_ruleset_by_data(
        cards, playerinfoid)

    if existing_rulesetid is not None:
        rulesetid = int(existing_rulesetid["ID"])
    else:
        rulesetid = DataRepository.create_ruleset(playerinfoid, cards, 0)

    gameid = DataRepository.create_game(name, desc, decks, rulesetid)

    socketio.emit('B2F_game_created')


@socketio.on('F2B_delete_game')
def delete_game(game_id):
    data = DataRepository.delete_game(game_id['ID'])
    socketio.emit('B2F_game_deleted')


@socketio.on('F2B_shutdown')
def shutdown():
    print('shutdown')
    call("sudo shutdown -h now", shell=True)


if __name__ == '__main__':
    try:
        setup()
        show_ip_lcd()
        socketio.run(app, host='0.0.0.0', debug=False)
        
    except KeyboardInterrupt as e:
        print('Quitting.....')
    finally:
        GPIO.cleanup()
        print("Programm has been closed")
