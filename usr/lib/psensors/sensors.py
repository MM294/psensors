from subprocess import call, Popen, PIPE

class SensorReader:
	def __init__(self):
		self.updatevalues()

	def updatevalues(self):
		variable = Popen("sensors -A", stdout=PIPE, shell=True).stdout.read()
		splitvar = variable.splitlines()
		if variable == "":
			print("no sensors")
			return False
		self.titlelist = []
		self.fanarray = {}
		self.temperaturearray = {}
		for x in range(0, len(splitvar)):
			if not(splitvar[x] == ""):
				#sensors output means only titles lack a colon
				if (splitvar[x].find(':') == -1): 
					self.titlelist.append(splitvar[x])
					currentsection = splitvar[x]
				#find all the fan lines
				elif not(splitvar[x].find('fan') == -1):
					splitline = splitvar[x].split()
					data = [(currentsection, splitline[0], splitline[1])]
					for busdevice, sensor, value in data:
						self.fanarray.setdefault(busdevice, {})[sensor] = value
				#find all the lines with a degree sign in
				elif not(splitvar[x].find('\xc2') == -1):
					splitline = splitvar[x].split(':')
					data = [(currentsection,splitline[0],splitline[1].split()[0])]
					for busdevice, sensor, value in data:
						self.temperaturearray.setdefault(busdevice, {})[sensor] = value

	def printvalues(self):
		for i in range(0, len(self.titlelist)):
			if (self.titlelist[i] in self.temperaturearray):
				print(self.titlelist[i])
				for k, v in self.temperaturearray[self.titlelist[i]].iteritems():
					print(k.capitalize() + " " + v)
		for i in range(0, len(self.titlelist)):
			if (self.titlelist[i] in self.fanarray):
				print(self.titlelist[i])
				for k, v in self.fanarray[self.titlelist[i]].iteritems():
					print(k.capitalize() + " " + v + " RPM")

	"""for k, v in self.fanarray.iteritems():
		for l, w in v.iteritems():
			print(k, l, w)
	for k, v in self.temperaturearray.iteritems():
		for l, w in v.iteritems():
			print(k, l, w)"""

#app = SensorReader()
#app.printvalues()
