import discord
import datetime
import time
import os
import matplotlib.pyplot as plt

bot = discord.Client()

@bot.event
async def on_ready():
	print("Logged in as")
	print(bot.user.name)
	print("----------------")
	genChannel = bot.get_channel("416282336183713803")
	
	#tresorerie
	month = datetime.datetime.today().month
	day = datetime.datetime.today().day
	x = [0]
	xlabel = [str(day) + "/" + str(month)]
	y = []
	f = open(".\\tresorerie\\tresorerie", "r")
	montant = float(f.read())
	f.close()
	y.append(montant)
	plt.plot(x,y)
	plt.xlabel("Jour/Mois")
	plt.ylabel("Euros")
	plt.title("Trésorerie en construction")
	plt.savefig(".\\tresorerie\\tresorerie.png")
	#tresorerie

	while (1):
		hour = datetime.datetime.now().hour
		minute = datetime.datetime.now().minute
		second = datetime.datetime.now().second
		if (hour == 8 and minute == 0 and second == 0):

			year = datetime.datetime.today().year
			month = datetime.datetime.today().month
			day = datetime.datetime.today().day

			#tresorerie
			x.append(x[-1]+1)
			xlabel.append(str(day) + "/" + str(month))
			x0 = []
			xlabel0 = []
			for i in range(0,len(x),1+int(len(x)/10)):
				x0.append(x[i])
				xlabel0.append(xlabel[i])
			f = open(".\\tresorerie\\tresorerie", "r")
			montant = float(f.read())
			f.close()
			y.append(montant)
			plt.plot(x,y,'r+')
			plt.xlim(0, x[-1])
			plt.ylim(min(min(y)-100,0), max(y)+100)
			plt.xticks(x0, xlabel0, rotation=45)
			plt.xlabel("Jour/Mois")
			plt.ylabel("Euros")
			plt.title("Trésorerie " + str((year)))
			plt.savefig(".\\tresorerie\\tresorerie.png", dpi=166)
			#tresorerie
	
			try:
				f = open(".\\rappel\\" + str(day) + "_" + str(month), "r")
				await bot.send_message(genChannel, f.read())
				f.close()
				os.remove(".\\rappel\\" + str(day) + "_" + str(month))
			except:
				pass
			time.sleep(86399)

bot.run("Token")
