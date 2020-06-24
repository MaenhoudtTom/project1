from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # CREATE methods

    @staticmethod
    def create_game(name, description, carddecks, rulesetid):
        sql = 'insert into Games(Name, Description, CardDecks, RulesetID) values(%s, %s, %s, %s)'
        params = [name, description, carddecks, rulesetid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_ruleset(playerinfoid, cardsperplayer, keepremainingcards):
        sql = 'insert into Rulesets(PlayerInfoID, CardsPerPlayer, KeepRemainingCards) values(%s, %s, %s)'
        params = [playerinfoid, cardsperplayer, keepremainingcards]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_playerinfo(minimumage, minimumplayers, maximumplayers=None):
        sql = 'insert into PlayerInfo(MinimumAge, MinimumPlayers, MaximumPlayers) values(%s, %s, %s)'
        params = [minimumage, minimumplayers, maximumplayers]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_sensor_data(sensorID, value):
        sql = 'insert into History(SensorID, Value) values(%s, %s)'
        params = [sensorID, value]
        return Database.execute_sql(sql, params)

    # READ methods

    @staticmethod
    def read_games():
        sql = "SELECT * from Games order by Name Asc"
        return Database.get_rows(sql)

    @staticmethod
    def read_game_by_id(id):
        sql = "SELECT * from Games where ID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_playerinfo_by_data(age, minimumplayers, maximumplayers):
        sql = "select ID from PlayerInfo where MinimumAge = %s and MinimumPlayers = %s and MaximumPlayers = %s"
        params = [age, minimumplayers, maximumplayers]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_ruleset_by_data(cardsperplayer, playerinfoid):
        sql = "select ID from Rulesets where CardsPerPlayer = %s and PlayerInfoID = %s"
        params = [cardsperplayer, playerinfoid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_sensors():
        sql = "SELECT * from Sensors"
        return Database.get_rows(sql)

    @staticmethod
    def read_id_sensor(name):
        sql = "select id from Sensors where name = %s"
        params = [name]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_sensor_by_id(id):
        sql = "SELECT * from Sensors where ID = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_history_by_sensorID(sensorID):
        sql = "select Name, Type, Description, Unit, Value, Date from Sensors join History on Sensors.id = History.sensorid where sensorID = %s order by Date desc LIMIT 25"
        params = [sensorID]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_games_with_rulesets_and_playerinfo():
        sql = "select Name, Description, CardDecks, CardsPerPlayer, KeepRemainingCards, MinimumAge, MinimumPlayers, MaximumPlayers from Games join Rulesets on Games.RuleSetID = Rulesets.ID join PlayerInfo on Rulesets.PlayerInfoID = PlayerInfo.ID"
        return Database.get_rows(sql)

    @staticmethod
    def read_game_with_ruleset_and_playerinfo_by_id(gameID):
        sql = "select Name, Description, CardDecks, CardsPerPlayer, KeepRemainingCards, MinimumAge, MinimumPlayers, MaximumPlayers, RulesetID, PlayerInfoID from Games join Rulesets on Games.RuleSetID = Rulesets.ID join PlayerInfo on Rulesets.PlayerInfoID = PlayerInfo.ID where Games.ID = %s"
        params = [gameID]
        return Database.get_rows(sql, params)

    # UPDATE methods

    @staticmethod
    def update_game_by_id(gameID, name, description, cardDecks, rulesetID):
        sql = 'update Games set name = %s, description = %s, carddecks = %s, rulesetid = %s where id = %s'
        params = [name, description, cardDecks, rulesetID, gameID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_ruleset_by_id(rulesetID, playerInfoID, cardsPerPlayer):
        sql = 'update Rulesets set playerInfoID = %s, cardsPerPlayer = %s where id = %s'
        params = [playerInfoID, cardsPerPlayer, rulesetID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_playerinfo_by_id(playerInfoID, minimumAge, minimumPlayers, maximumPlayers):
        sql = 'update PlayerInfo set minimumAge = %s, minimumPlayers = %s, maximumPlayers = %s where id = %s'
        params = [minimumAge, minimumPlayers, maximumPlayers, playerInfoID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_sensor_by_id(sensorID, name, sensorType, unit, description):
        sql = 'update Sensors set name = %s, type = %s, unit = %s, description = %s where id = %s'
        params = [name, sensorType, unit, description, sensorID]
        return Database.execute_sql(sql, params)

    # DELETE methods

    @staticmethod
    def delete_ruleset(id):
        sql = 'delete from Rulesets where id = %s'
        params = [id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def delete_game(id):
        sql = 'delete from Games where id = %s'
        params = [id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def delete_playerinfo(id):
        sql = 'delete from PlayerInfo where id = %s'
        params = [id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def delete_history(id):
        sql = 'delete from History where id = %s'
        params = [id]
        return Database.execute_sql(sql, params)