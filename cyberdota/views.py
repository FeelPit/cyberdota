from django.shortcuts import render
from django import forms
from django.utils.translation import ugettext as _
from bs4 import BeautifulSoup
import requests
import mysql.connector
import urllib.request
import json


class PlayersRegistrationForm(forms.Form):
    idha = forms.IntegerField(label=_(u'idha'))
    region = forms.CharField(label=_(u'region'))
    lang = forms.CharField(label=_(u'lang'))
class TeamRegistrationForm(forms.Form):
	name = forms.CharField(label=_(u'name'))
	region = forms.CharField(label=_(u'region'))
	lang = forms.CharField(label=_(u'lang'))
class LoginForm(forms.Form):
	pers = forms.CharField(label=_(u'pers'))
	idha = forms.IntegerField(label=_(u'idha'))
class SearchForm(forms.Form):
	name = forms.CharField(label=_(u'name'))

def registration(request):
	form = PlayersRegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		steam_id = form.cleaned_data.get('idha', None)
		reg = form.cleaned_data.get('region', None)
		langg = form.cleaned_data.get('lang', None)

		url = 'https://api.opendota.com/api/players/' + str(steam_id)
		url = urllib.request.urlopen(url)

		datass = json.loads(url.read())
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		print(steam_id, datass['profile']['personaname'], datass['profile']['avatar'], datass['rank_tier'], reg, langg)
		text = '''
			INSERT INTO players(account_id, personanname, avatar, rank, region, lang)
			VALUES ({},'{}','{}',{},'{}','{}')
		'''.format(steam_id, 'vova', datass['profile']['avatar'], datass['rank_tier'], reg, langg)
		print(steam_id, datass['profile']['personaname'], datass['profile']['avatar'], datass['rank_tier'], reg, langg)
		cursor.execute(text)
		cnx.commit()
		cnx.close()
		return render(request, 'test.html')
	else:
		return render(request, 'registration.html')	

def main_page(request):
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
			return render(request, 'aaa.html', {'pers': person})
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')

def search(request):
	form = SearchForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		name = form.cleaned_data.get('name', None)
		cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='cyber_dota')
		cursor = cnx.cursor()
		stats = '''
			SELECT rank, region, lang FROM players
			WHERE personanname = '{}'
		'''.format(name)
		cursor.execute(stats)
		stats = cursor.fetchone()	
		text = ''' SELECT personanname, region, rank, lang FROM players
				   WHERE rank <= {} + 5 and region = '{}' and lang = '{}'
				   ORDER BY abs({} - rank)
				   '''.format(stats[0], stats[1], stats[2], stats[0])
		cursor.execute(text)
		res_row = cursor.fetchall()
		cnx.close()
		res = []
		for i in res_row:
			if i[0] == name:
				pass
			else:
				res.append(i)
		return render(request, 'search_result.html', {'res': res})
	else:
		return render(request, 'search.html')

def create_team(request):
	form = TeamRegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		name = form.cleaned_data.get('name', None)
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




