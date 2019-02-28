from cyberdota import logic
import json
import mysql.connector
import urllib.request

def teaminvite(team_id, player_id):
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = '''INSERT INTO teamplay (player_id, team_id, confirm) VALUES ({}, {}, "NONE")'''.format(str(player_id), str(team_id))
	cursor.execute(text)
	cnx.commit()
	cnx.close()
	result = {'result': "true"}
	return result

def teamsrating():
	result = logic.ratings()
	return result