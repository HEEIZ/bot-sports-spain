#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import requests,json
from telebot import types
from flask import Flask, request
import os
from datetime import datetime, timedelta, date



TOKEN = os.environ['TOKEN']
WEBHOOK = os.environ['WEBHOOK']


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['programacion'])
def eventos(message):

	url = "https://www.marca.com/programacion-tv.html"
	cid = message.chat.id

	r = requests.get(url)
	resp= r.text

	evento = {}
	hora = {}
	canal = {}
	titulo = {}
	deporte = {}
	emoji = {}


	hoy = resp.split('<span class="title-section-widget"><strong>')[1].split('</span>')[0]
	hoy = hoy.replace("</strong>", " ")
	proximos_eventos = resp.split('<span class="title-section-widget"><strong>')[1].split('<span class="title-section-widget"><strong>')[0]
	eventos_hoy = proximos_eventos.count('<li class="dailyevent">')

	mensaje = "["+hoy+"]\n\n\n"

	for i in range (eventos_hoy):
		i = i+1
		evento[i] = proximos_eventos.split('<li class="dailyevent">')[i].split('</li>')[0]
		hora[i] = evento[i].split('<strong class="dailyhour">')[1].split('</strong>')[0]
		titulo[i] = evento[i].split('<a href="" title="')[1].split('">')[0]
		canal [i] = evento[i].split('<span class="dailychannel"><i class="icon-pantalla"></i>')[1].split('</span>')[0]
		deporte[i] = evento[i].split('<i class="')[1].split('"></i>')[0]
		if (deporte[i] == "icon-futbol" ):
			emoji[i] = "⚽"
		elif (deporte[i] == "icon-baloncesto" ):
			emoji[i]= "🏀"
		elif (deporte[i] == "icon-ciclismo" ):
			emoji[i] = "🚴‍♂"
		elif (deporte[i] == "icon-atletismo" ):
			emoji[i] = "🏃‍♀️"
		elif (deporte[i] == "icon-golf" ):
			emoji[i] = "🏌️‍♀️"
		elif (deporte[i] == "icon-rugby" ):
			emoji[i] = "🏉"
		elif (deporte[i] == "icon-boxeo" ):
			emoji[i] = "🥊"
		elif (deporte[i] == "icon-tenis" ):
			emoji[i] = "🎾"
		elif (deporte[i] == "icon-balonmano" ):
			emoji[i] = "🤾"
		elif (deporte[i] == "icon-motor" ):
			emoji[i] = "🏎️"
		elif (deporte[i] == "icon-futbol_sala" ):
			emoji[i] = "⚽"
		else:
			emoji[i] = "🏆"

		mensaje += emoji[i]+" "+titulo[i]+" - "+hora[i]+" - "+canal[i]+"\n\n"

	mensaje += "\n\n 🤖: @sports_spain_bot"
	bot.send_message(cid,mensaje)
	bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=['resultados'])
def resultados(message):
	cid = message.chat.id
	today = date.today() 
	d0 = today.strftime("%Y-%m-%d")
	d1 = today.strftime("%d-%m-%Y")
	url = 'https://api.unidadeditorial.es/sports/v1/events/preset/1_99a16e5b?timezoneOffset=1&date='+str(d0)
	respuesta = requests.get(url)
	open('respuesta.json', 'wb').write(respuesta.content)

	f = open('respuesta.json', encoding="utf-8")
	json_file = json.load(f)
	json_str = json.dumps(json_file)
	resp = json.loads(json_str)

	ocurrencias = json_str.count("status")	



	visitante_equipo = {}
	local_equipo = {}
	status = {}
	visitante_score = {}
	local_score = {}
	deporte= {}
	emoji = {}
	mensaje = "RESULTADOS DÍA "+str(d1)+ "\n\n"
	for i in range (ocurrencias):
		try:
			visitante_equipo[i] = resp['data'][i]['sportEvent']['competitors']['awayTeam']['fullName']
			local_equipo[i]= resp['data'][i]['sportEvent']['competitors']['homeTeam']['fullName']
			status[i] = resp['data'][i]['sportEvent']['status']['alternateNames']['esES']

			if (status[i] == 'Sin comenzar'):
				visitante_score[i] = "-"
				local_score[i] = "-"
			else:
				visitante_score[i] = resp['data'][i]['score']['awayTeam']['totalScore']
				local_score[i] = resp['data'][i]['score']['homeTeam']['totalScore']
			deporte[i] = resp['data'][i]['sport']['alternateNames']['esES']
			print(deporte[i])
			if (deporte[i] == ('Baloncesto')):
				emoji[i] = "🏀"
			elif (deporte[i] == ('Fútbol Sala')):
				emoji[i] = "⚽"
			elif (deporte[i] == ('Fútbol')):
				emoji[i] = "⚽"
			elif (deporte[i] == ('Motor')):
				emoji[i] = "🏎️"
			elif (deporte[i] == ('Ciclismo')):
				emoji[i] = "🚴‍♂"
			elif (deporte[i] == ('Atletismo')):
				emoji[i] = "🏃‍♀️"
			elif (deporte[i] == ('Rugby')):
				emoji[i] = "🏉"
			elif (deporte[i] == ('Boxeo')):
				emoji[i] = "🥊"
			elif (deporte[i] == ('Balonmano')):
				emoji[i] = "🤾"
			elif (deporte[i] == ('Tenis')):
				emoji[i] = "🎾"
			else:
				emoji[i] = "🏆"

			mensaje += emoji[i]+" "+local_equipo[i]+" ["+local_score[i]+"] - ["+visitante_score[i]+"] "+visitante_equipo[i]+"\n"
		except:
			pass
		i = i+1

	mensaje = mensaje + "\n🤖 @sports_spain_bot"
	bot.send_message(cid,mensaje)
	bot.delete_message(message.chat.id, message.message_id)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=WEBHOOK + TOKEN)
	return "!", 200

if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

