import discord
import os
import shutil
from discord.ext.commands import Bot
from discord.ext import commands

bot = discord.Client()
bot_prefix= "&"
description = "RobotechBot"
bot = commands.Bot(command_prefix=bot_prefix, description=description)

@bot.event
async def on_ready():
    global startsondage
    global nbchoix
    global logChannel
    global tresorChannel
    global montant
    startsondage = 0
    nbchoix = 0
    montant = []
    logChannel = bot.get_channel("416282481621336068")
    tresorChannel = bot.get_channel("428884965929779203")
    print("Logged in as")
    print(bot.user.name)
    print("----------------")

@bot.event
async def on_error(event, type, value, tb):
    pass

@bot.command(pass_context=True)
async def chanlist(ctx):
	channels = ctx.message.server.channels
	msg = "```Les channels sont :\n"
	for channel in channels:
		msg += channel.name + ": " + channel.id + "\n"
	msg += "```"
	await bot.say(msg)

@bot.command(pass_context=True)
async def roleslist(ctx):
    roles = ctx.message.server.role_hierarchy
    result = "```Les rôles sont :\n"
    for role in roles:
    	result += role.name + ": " + role.id + "\n"
    result += "```"
    
    await bot.say(result)

"""-------------------- SONDAGE --------------------"""
@bot.command(pass_context=True)
async def startsondage(ctx, *, n:int=2):
    global logChannel
    global startsondage
    global nbchoix
    if (startsondage == 0):
        startsondage = 1
        nbchoix = n
        msg = "Votons ! Vous avez " + str(n) + " choix."
        lines = open(".\\sondage\\sondage", "w")
        for i in range(n):
            lines.write("0\n")
        lines.close()
        await bot.say(msg)
        msg = "Un sondage a débuté.\n"
        lines = open(".\\sondage\\sondage", "r")
        i = 1
        for line in lines:
        	msg += "Choix " + str(i) + " : " + line
        	i += 1
        lines.close()
        await bot.send_message(logChannel, msg)
    else:
    	msg = "Sondage en cours."
    	await bot.say(msg)

@bot.command(pass_context=True)
async def vote(ctx, *, n:int=1):
	global logChannel
	global startsondage
	global nbchoix
	if (startsondage == 1 and n > 0 and n <= nbchoix):
		authorID = ctx.message.author.id
		try:
			lines = open(authorID + ".\\sondage\\sondage", "r")
			number = int(lines.read())
			if (number != 0):
				lines0 = open(".\\sondage\\sondage", "r")
				msg = ""
				i = 1
				for line in lines0:
					if (i == number):
						msg += str(int(line) - 1) + "\n"
					else:
						msg += line
					i += 1
				lines0.close()
				lines0 = open(".\\sondage\\sondage", "w")
				lines0.write(msg)
				lines0.close()
			lines.close()
		except:
			pass
		lines = open(authorID + ".\\sondage\\sondage", "w")
		lines.write(str(n))
		lines.close()
		lines = open(".\\sondage\\sondage", "r")
		msg = ""
		i = 1
		for line in lines:
			if (i == n):
				msg += str(int(line) + 1) + "\n"
			else:
				msg += line
			i += 1
		lines.close()
		lines = open(".\\sondage\\sondage", "w")
		lines.write(msg)
		lines.close()
		await bot.send_message(logChannel, authorID + " a fait le choix " + str(n) + ".")
	else:
		msg = "Pas de sondage en cours."
		await bot.say(msg)

@bot.command(pass_context=True)
async def devote(ctx):
	global logChannel
	global startsondage
	global nbchoix
	authorID = ctx.message.author.id
	try:
		lines = open(authorID + ".\\sondage\\sondage", "r")
		number = int(lines.read())
		if (number != 0):
			lines0 = open(".\\sondage\\sondage", "r")
			msg = ""
			i = 1
			for line in lines0:
				if (i == number):
					msg += str(int(line) - 1) + "\n"
				else:
					msg += line
				i += 1
			lines0.close()
			lines0 = open(".\\sondage\\sondage", "w")
			lines0.write(msg)
			lines0.close()
		lines.close()
	except:
		pass
	lines = open(authorID + ".\\sondage\\sondage", "w")
	lines.write("0\n")
	lines.close()
	await bot.send_message(logChannel, authorID + " a retiré son vote.")

@bot.command(pass_context=True)
async def voirsondage(ctx):
	global startsondage
	if (startsondage == 1):
		msg = "Sondage en cours :\n"
		lines = open(".\\sondage\\sondage", "r")
		i = 1
		for line in lines:
			msg += "Choix " + str(i) + " : " + line
			i += 1
		lines.close()
		await bot.say(msg)
	else:
		msg = "Pas de sondage en cours."
		await bot.say(msg)

@bot.command(pass_context=True)
async def endsondage(ctx):
    global logChannel
    global startsondage
    if (startsondage == 1):
    	startsondage = 0
    	msg = "Fin du sondage :\n"
    	lines = open(".\\sondage\\sondage", "r")
    	i = 1
    	for line in lines:
    		msg += "Choix " + str(i) + " : " + line
    		i += 1
    	lines.close()
    	shutil.rmtree(".\\sondage\\")
    	os.mkdir(".\\sondage\\")
    	await bot.send_message(logChannel, msg)
    else:
    	msg = "Pas de sondage en cours."
    	await bot.say(msg)

"""-------------------- NOTE --------------------"""

@bot.command(pass_context=True)
async def note(ctx, *, mess:str=""):
	author = ctx.message.author
	if (mess != ""):
		f = open(".\\note\\" + author.id, "w")
		f.write(mess)
		f.close()
		await bot.say("Votre note a été mis à jour, tapez &note pour un rappel.")
	else:
		try:
			f = open(".\\note\\" + author.id, "r")
			await bot.say(f.read())
			f.close()
		except:
			await bot.say("Vous n'avez aucune note, utilisez la commande &note <texte>.")

@bot.command(pass_context=True)
async def setDate(ctx, *, date:str=""):
	author = ctx.message.author
	try:
		for i in range(len(date)):
			if date[i] == ' ':
				day = date[:i]
				month = date[i+1:]
		f = open(".\\note\\" + author.id, "r")
		text = f.read()
		f.close()
		f = open(".\\rappel\\" + str(day) + "_" + str(month), "a")
		f.write("Request by " + author.name + "\n")
		f.write(text)
		f.write("\n--------------------\n")
		f.close()
		await bot.say("Votre note vous sera rappelé le " + str(day) + " " + str(month))
	except:
		await bot.say("Vous n'avez aucune note, utilisez la commande &note <texte>.")

"""-------------------- TRESORIER --------------------"""

@bot.command(pass_context=True)
async def tresorerie(ctx):
	author = ctx.message.author
	roles = author.roles
	for role in roles:
		if role.id == "416286513790320642":
			try:
				f = open(".\\tresorerie\\tresorerie", "r")
				result = f.read()
				f.close()
				await bot.say("La trésorerie actuelle est de " + result + " €")
			except:
				await bot.say("Vous n'avez aucune trésorerie")
	await bot.say("Vous n'avez pas les permissions")

@bot.command(pass_context=True)
async def tresorerieAdd(ctx, *, n:float=0.0):
	global tresorChannel
	author = ctx.message.author
	roles = author.roles
	for role in roles:
		if role.id == "416281033772630016" or role.id == "416280908765855755":
			try:
				f = open(".\\tresorerie\\tresorerie", "r")
				result = float(f.read())
				f.close()
				result += n
			except:
				result = n	
			f = open(".\\tresorerie\\tresorerie", "w")
			f.write(str(result))
			f.close()
			await bot.send_message(tresorChannel, "Le trésorier a ajouté " + str(n) + " €")
			return
	await bot.say("Vous n'avez pas les permissions")

@bot.command(pass_context=True)
async def emprunter(ctx, *, n:float=0.0):
	global tresorChannel
	global montant
	name = ctx.message.author.name
	montant.append(n)
	await bot.send_message(tresorChannel, name + " demande un emprunt de " + str(n) + " €")

@bot.command(pass_context=True)
async def tresorerieAccept(ctx, *, n:int=0):
	global tresorChannel
	global montant
	author = ctx.message.author
	roles = author.roles
	if n < len(montant):
		for role in roles:
			if role.id == "416281033772630016" or role.id == "416280908765855755":
				try:
					f = open(".\\tresorerie\\tresorerie", "r")
					result = float(f.read())
					f.close()
					result -= montant[n]
					montant.pop(n)
				except:
					result = -montant[n]
				f = open(".\\tresorerie\\tresorerie", "w")
				f.write(str(result))
				f.close()
				await bot.send_message(tresorChannel, "Le trésorier a accepté la requête n°" + str(n) + ", la trésorerie actuelle est de " + str(result) + " €")
				return
			else:
				await bot.say("Vous n'avez pas les permissions")
	else:
		await bot.say("Il n'y a pas autant de demande")

@bot.command(pass_context=True)
async def tresorerieGraph(ctx):
	author = ctx.message.author
	roles = author.roles
	for role in roles:
		if role.id == "416286513790320642":
			try:
			    await bot.upload(".\\tresorerie\\tresorerie.png")
			except:
			    await bot.say("Pas de graphe")
			return
	await bot.say("Vous n'avez pas les permissions")

bot.run("Token")
