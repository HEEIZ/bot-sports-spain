#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import requests,json
from telebot import types
from flask import Flask, request
import os
from datetime import datetime



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
	print(eventos_hoy)

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
		else:
			emoji[i] = "🏆"

		mensaje += emoji[i]+" "+titulo[i]+" - "+hora[i]+" - "+canal[i]+"\n\n"

	mensaje += "\n\n\n 🤖: @sports_spain_bot"
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

