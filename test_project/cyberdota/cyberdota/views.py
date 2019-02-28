from django.shortcuts import render
from django import forms
from django.utils.translation import ugettext as _
from bs4 import BeautifulSoup
from django.shortcuts import redirect
from cyberdota import logic
from cyberdota import api
from django.http import JsonResponse
import http.cookies
import urllib.request
import requests
import mysql.connector
import json	 



class PlayersRegistrationForm(forms.Form):
    idha = forms.CharField(label=_(u'idha'))
    region = forms.CharField(label=_(u'region'))
    lang = forms.CharField(label=_(u'lang'))
class TeamRegistrationForm(forms.Form):
	idha = forms.CharField(label=_(u'idha'))
	region = forms.CharField(label=_(u'region'))
	lang = forms.CharField(label=_(u'lang'))
class LoginForm(forms.Form):
	pers = forms.CharField(label=_(u'pers'))
	idha = forms.IntegerField(label=_(u'idha'))
class SearchForm(forms.Form):
	name = forms.CharField(label=_(u'name'))
class AddForm(forms.Form):
	name = forms.CharField(label=_(u'name'))
class InviteForm(forms.Form):
	succes = forms.CharField(label=_(u'Succes'))


def welcome_page(request):
	return render(request, 'welcome_page.html')

def registration(request):
	form = PlayersRegistrationForm(data=request.POST)
	print(form.is_valid())
	if request.method == 'POST' and form.is_valid():
		steam_id = form.cleaned_data.get('idha', None)
		reg = form.cleaned_data.get('region', None)
		langg = form.cleaned_data.get('lang', None)

		url = 'https://api.opendota.com/api/players/' + str(steam_id)
		url = urllib.request.urlopen(url)
		datass = json.loads(url.read())
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		text = '''
			INSERT INTO players(account_id, personanname, avatar, rank, region, lang)
			VALUES ({},'{}','{}',{},'{}','{}')
		'''.format(steam_id, 'VADIM', datass['profile']['avatar'], datass['rank_tier'], reg, langg)
		cursor.execute(text)
		cnx.commit()	
		cnx.close()
		return render(request, 'test.html')
	else:
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		country = '''SELECT name FROM country'''
		cursor.execute(country)
		country = cursor.fetchall()
		cnt = []
		for i in country:
			cnt.append(i[0])
		print(cnt)
		return render(request, 'registration.html', {'country': cnt})	

def main_page(request):
	if request.session.get('login') != None:
		return redirect('http://127.0.0.1:8090/profile/{}'.format(request.session.get('login')))
	else:
		return redirect('http://127.0.0.1:8090/login')			
	return render(request, 'main.html')

def login(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		person = form.cleaned_data.get('pers', None)
		steamid = form.cleaned_data.get('idha', None)
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		text = '''
			SELECT account_id FROM players
			WHERE personanname = '{}'
		'''.format(person)
		cursor.execute(text)
		results = cursor.fetchone()
		cnx.close()
		if results[0] == steamid:
			request.session['login'] = steamid
			return redirect("http://127.0.0.1:8090/main")
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')

def search_choice(request):
	return render(request, 'search_choice.html')

def search_auto(request):
	if request.session.get('login') != None:
		name = request.session['login']
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		stats = '''
			SELECT rank, region, lang, team FROM players
			WHERE account_id = '{}'
		'''.format(request.session['login'])
		cursor.execute(stats)
		stats = cursor.fetchone()
		if stats[3] != None:	
			text = ''' SELECT id, account_id FROM players
					   WHERE rank <= {} + 5 and region = '{}' and lang = '{}' and account_id != {}
					   ORDER BY abs({} - rank)
					   '''.format(stats[0], stats[1], stats[2], str(request.session['login']), stats[0])
			cursor.execute(text)
			res_row = cursor.fetchall()

			res_b = []			
			for i in res_row:
				res = {}
				url = 'https://api.opendota.com/api/players/{}'.format(str(i[1]))
				url = urllib.request.urlopen(url)
				datass = json.loads(url.read())
				res['id'] = i[0]
				res['name'] = datass['profile']['personaname']
				res['rank'] = datass['rank_tier']
				if res['rank'] == None:
					res['rank'] = 'No rank'
				else:
					cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
					cursor = cnx.cursor()
					text = '''SELECT name FROM ranks WHERE rank_id = {}'''.format(str(res['rank']))
					cursor.execute(text)
					res['rank'] = cursor.fetchall()[0][0]
				res_b.append(res)
			cnx.close()
			print(res_b)
			return render(request, 'search.html', {'res_b': res_b, 'team_id': stats[3]})
		else:
			return render(request, 'test.html')
	else:
		return redirect('http://127.0.0.1:8090/login')		

def create_team(request):
	form = TeamRegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		name = form.cleaned_data.get('idha', None)
		region = form.cleaned_data.get('region', None)
		lang = form.cleaned_data.get('lang', None)
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		text = ''' INSERT INTO teams (name, region, lang)
				   VALUES ('{}','{}','{}')	
				   '''.format(name, region, lang)
		cursor.execute(text)
		cnx.commit()
		cnx.close()
		return render(request, 'create_complite.html', {'name': name})
	else:
		return render(request, 'create_team.html')


def add(request, team, account_id):
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = ''' INSERT INTO teamplay (player_id, team_id) VALUES {}, {}'''.format(str(account_id), str(team))



def invite(request):
	form = InviteForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		name = form.cleaned_data.get('name', None)
		return render(request, 'main.html')


def menu(request):
	if request.session.get('login') != None:
		wl = logic.if_win(request.session['login'])
		i = 0
		matches = logic.last_matches(request.session['login'])
		while i != len(matches):
			matches[i]['win'] = wl[i]
			i+=1
		changes = logic.changes()
		rating = logic.ratings()
		if_login = True
		data = logic.recent_tournaments()		
		return render(request, 'main_menu.html', {'data': data, 'matches': matches, 'wl': wl, 'changes': changes, 'rating': rating, 'if_login': if_login})
	else:
		changes = logic.changes()
		rating = logic.ratings()
		data = logic.recent_tournaments()
		if_login = False		
		return render(request, 'main_menu.html', {'data': data, 'changes': changes, 'rating': rating, 'if_login': if_login})
	

def profile(request, idha):
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = '''SELECT id FROM players
				WHERE account_id = {}'''.format(idha)
	cursor.execute(text)
	if_exist = True
	try:
		cursor.fetchall()[0][0]
	except IndexError:
		if_exist = False
	url = 'https://api.opendota.com/api/players/{}'.format(str(idha))
	url = urllib.request.urlopen(url)
	datass = json.loads(url.read())
	data = {}
	data['name'] = datass['profile']['personaname']
	data['rank'] = datass['rank_tier']
	text = '''SELECT name from ranks where rank_id={}'''.format(data['rank'])
	cursor.execute(text)
	data['rank'] = cursor.fetchall()[0][0]
	data['avatar'] = datass['profile']['avatarfull']
	data['steam_url'] = datass['profile']['profileurl']
	if if_exist:
		text = '''SELECT region, lang, team FROM players WHERE account_id = {}'''.format(str(idha))
		cursor.execute(text)
		text = cursor.fetchall()[0]
		data['region'] = text[0]
		text = '''SELECT LOWER(id) FROM country WHERE name = "{}"'''.format(data['region'])
		cursor.execute(text)
		data['region'] = cursor.fetchall()[0][0]
		data['lang'] = text[1]
		data['team'] = text[2]
	else:
		data['region'],data['lang'],data['team'] = 'Have no info.','Have no info.','Have no info.'
	url = 'https://api.opendota.com/api/players/{}/heroes'.format(str(idha))
	url = urllib.request.urlopen(url)
	datass = json.loads(url.read())
	i = 0
	heroes = []
	while i != 3:
		stat = {}
		stat['id'] = datass[i]['hero_id']
		stat['games'] = datass[i]['games']
		stat['win'] = datass[i]['win']
		stat['lose'] = stat['games'] - stat['win']
		stat['wr'] = str(int(stat['win'])/int(stat['games'])*100)
		if len(stat['wr']) != 1:
			stat['wr'] = stat['wr'][:2]
		else:
			stat['wr'] = stat['wr'][0]
		heroes.append(stat)	
		i+=1
	matches = logic.last_matches(idha)		
	print(data,heroes)
	cnx.close()
	return render(request, 'profile.html', {'data': data, 'heroes': heroes, 'matches': matches, 'exist': if_exist})				

def team(request, team_id):
	cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
	cursor = cnx.cursor()
	text = '''SELECT * FROM teams WHERE id={}'''.format(str(team_id))
	cursor.execute(text)
	team = cursor.fetchall()[0]
	team_info = {}
	team_info['name'] = team[1]
	team_info['region'] = team[2]
	team_info['lang'] = team[3]
	team_info['rating'] = team[4]
	text = '''SELECT player_id FROM teamplay WHERE team_id = {} AND confirm = "yes" AND in_team = "yes"'''.format(str(team_id))
	cursor.execute(text)
	players = cursor.fetchall()
	players_info = []
	print(players)
	for i in players:
		p = {}
		text = '''SELECT account_id, region FROM players WHERE id = {}'''.format(str(i[0]))
		cursor.execute(text)
		text = cursor.fetchall()[0]
		p['account_id'] = str(text[0])
		p['region'] = text[1]
		text = '''SELECT LOWER(id) FROM country WHERE name="{}"'''.format(p['region'])
		cursor.execute(text)
		p['region'] = cursor.fetchall()[0][0]
		url = 'https://api.opendota.com/api/players/{}'.format(p['account_id'])
		url = urllib.request.urlopen(url)
		player = json.loads(url.read())
		p['name'] = player['profile']['personaname']
		p['rank'] = player['rank_tier']
		text = '''SELECT name FROM ranks WHERE rank_id = {}'''.format(str(p['rank']))
		cursor.execute(text)
		p['rank'] = cursor.fetchall()[0][0]
		players_info.append(p)
	gr = len(players_info)	
	print(players_info, team_info)			
	return render(request, 'team.html', {'team_info':team_info, 'players_info':players_info, 'gr': gr})	

def match(request, match_id):
	players_info = logic.match(match_id)
	return render(request, 'match.html', {'radiant':players_info[0],'dire':players_info[1]})

def exit(request):
	request.session['login'] = None
	return redirect('http://127.0.0.1:8090/main_menu')

#API_PART

def api_teaminvite(request, team_id, player_id):
	res = api.teaminvite(team_id, player_id)
	return JsonResponse(res)

def api_teamsrating(request):
	res = api.teamsrating()
	return JsonResponse(res, safe=False)

#TEST

def test(request):
	return render(request, 'test_comp.html')
