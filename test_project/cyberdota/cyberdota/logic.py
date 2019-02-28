import urllib.request
import requests
import json
import mysql.connector
import re
from bs4 import BeautifulSoup

def if_win(idh):
	url = 'https://api.opendota.com/api/players/' + str(idh) + '/recentMatches'
	url = urllib.request.urlopen(url)
	data = json.loads(url.read())
	wins = []
	datas = wins
	six_loses = 0
	calc = 0
	for i in data:
		if i['player_slot'] < 100:
			if i['radiant_win'] == True:
				wins.append(1)
			else:
				wins.append(0)
		else:
			if i['radiant_win'] == True:
				wins.append(0)
			else:
				wins.append(1)
	while calc != 6:
		if wins[calc] == 0:
			six_loses += 1
		calc += 1
	six_wins = (datas[0] + datas[1] + datas[2] + datas[3] + datas[4] + datas[5]) * 100
	six_loses *= 100				
	return [wins, datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], six_wins, six_loses]

def wl(idh):
	url = 'https://api.opendota.com/api/players/' + str(idh) + '/wl'
	print(idh)
	url = urllib.request.urlopen(url)
	data = json.loads(url.read())
	win_lose = [data['win'], data['lose']]
	return win_lose

def recent_tournaments():
	url = 'https://dota2.ru/esport/tournaments/'
	url = urllib.request.urlopen(url)
	soup = BeautifulSoup(url, "lxml")
	soup = soup.find('div', {'class': 'esport-tournament-list'})
	soup = soup.find_next('div', {'class': 'esport-tournament-list'})
	name = 1
	summary = {}
	summary_t = []
	while soup.find_next('div', {'class': 'esport-tournament-list-single'}) != None:
		soup = soup.find_next('div', {'class': 'esport-tournament-list-single'})
		name = soup.find('div', {'class': 'title'})
		name = name.find('a')
		name = re.sub('[\r\n ]', '', name.get_text())
		date = soup.find('div', {'class': 'date'})
		date = date.find_next('div').get_text()
		prize = soup.find('div', {'class': 'prize'})
		prize = re.sub('[\r\n ]', '', prize.get_text())
		if prize != "Приглашениенаосновнойэтап":
			summary['name'] = name.strip()
			summary['date'] = date.strip()
			summary['prize'] = prize.strip()
			summary_t.append(summary)
		summary = {}
	print(summary_t) 
	return summary_t

def invites(idh):
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = '''
			SELECT team_id, date_in FROM teamplay
			WHERE player_id = {} and confirm = 'NONE'
	'''.format(idh)
	cursor.execute(text)
	invite = cursor.fetchall()
	names = []
	for i in invite:
		text = '''
			SELECT name FROM teams
			WHERE id = {}
		'''.format(i[0])
		cursor.execute(text)
		team_name = cursor.fetchall()
		if team_name != []:
			names.append(team_name[0][0])
	print(names)		
	return names

def last_matches(idha):
	url = 'https://api.opendota.com/api/players/' + str(idha) + '/recentMatches'
	url = urllib.request.urlopen(url)
	datass = json.loads(url.read())
	data = []
	real_data = []
	i = 0
	while i != 6:
		data = {}
		data['id'] = datass[i]['match_id']
		data['hero_id'] = datass[i]['hero_id']
		data['kills'] = datass[i]['kills']
		data['assists'] = datass[i]['assists']
		data['deaths'] = datass[i]['deaths']
		data['duration'] = str(datass[i]['duration'] // 60) + ':' + str(datass[i]['duration'] % 60)
		if datass[i]['player_slot'] < 100:
			if datass[i]['radiant_win'] == True:
				data['win'] = 1
			else:
				data['win'] = 0
		else:
			if datass[i]['radiant_win'] == True:
				data['win'] = 0
			else:
				data['win'] = 1
		i += 1
		print(data['win'])
		real_data.append(data)
	return real_data[:4]

def changes():
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = """SELECT player_id, team_id, confirm
				FROM teamplay"""
	cursor.execute(text)
	change = cursor.fetchall()
	divise = len(change) - 3
	mas_t = []
	for i in change[divise:]:
		t = {}
		text = """SELECT personanname FROM players WHERE id = {}""".format(i[0])
		cursor.execute(text)
		t['p_name'] = cursor.fetchall()[0][0]
		text = """SELECT name FROM teams WHERE id = {}""".format(i[1])
		cursor.execute(text)
		t['t_name'] = cursor.fetchall()[0][0]	
		t['confirm'] = (i[2])
		mas_t.append(t)
	cnx.close()	
	return mas_t
	
def ratings():
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = """SELECT name, region, rating FROM teams"""
	cursor.execute(text)
	team = cursor.fetchall()
	gtr = len(team) * 10 // 13
	while gtr:
		for i in range(len(team) - gtr):
			if team[i][2] < team[i + gtr][2]:
				team[i], team[i + gtr] = team[i + gtr], team[i]
		gtr = gtr * 10 // 13
	full_team = []
	for i in team:
		t = {}
		t['name'], t['reg'], t['rate'] = i[0], i[1], i[2]
		full_team.append(t)
	return full_team

def last_six_games(idh):
	url = 'https://api.opendota.com/api/players/{}/recentMatches'.format(idh)
	url = urllib.request.urlopen(url)
	data = json.loads(url.read())
	i = 0
	games = []
	wins = 0
	loses = 0
	while i != 6:
		games.append(data[i])
		i += 1
	for i in games:
		if i['player_slot'] < 100:
			if i['radiant_win'] == True:
				wins += 1
			else:
				loses += 1
		else:
			if i['radiant_win'] == True:
				loses += 1
			else:
				wins += 1
	wins_p = str(wins / (wins + loses) * 100)
	loses_p = str(loses / (wins + loses) * 100)
	if len(wins_p) != 1 and wins_p[1] != '.':
		if int(wins_p[3]) >= 5:
			wins_p = int(wins_p[:2]) + 1
		else:
			wins_p = int(wins_p[:2])
	else:
		wins_p = wins_p[0]
	if len(loses_p) != 1 and loses_p[1] != '.':
		if int(loses_p[3]) >= 5:
			loses_p = int(loses_p[:2]) + 1
		else:
			loses_p = int(loses_p[:2])
	else:
		loses_p = loses_p[0]
	return [int(wins_p), int(loses_p)]

def match(match_id):
	url = "https://api.opendota.com/api/matches/{}".format(str(match_id))
	url = urllib.request.urlopen(url)
	data = json.loads(url.read())
	players_info = []
	player = {}
	for i in data['players']:
		try:
			player['name'] = i['personaname']
		except KeyError:
			player['name'] = 'Anonim'
		player['id'] = i['account_id']	
		player['hero'] = str(i['hero_id'])
		player['i0'] = i['item_0']
		player['i1'] = i['item_1']
		player['i2'] = i['item_2']
		player['i3'] = i['item_3']
		player['i4'] = i['item_4']
		player['i5'] = i['item_5']
		player['kills'] = i['kills']
		player['deaths'] = i['deaths']
		player['assists'] = i['assists']
		player['level'] = i['level']
		player['xpm'] = i['xp_per_min']
		player['gpm'] = i['gold_per_min']
		player['damage'] = i['hero_damage']
		player['heal'] = i['hero_healing']
		player['lh'] = i['last_hits']
		player['dn'] = i['denies']
		player['nw'] = i['total_gold']
		players_info.append(player)
		player = {}
	i = 0
	radiant = []
	dire = []
	while i != len(players_info):
		if i < 5:
			radiant.append(players_info[i])
		else:
			dire.append(players_info[i])
		i += 1 	
	return radiant, dire
match(4312920376)	


















