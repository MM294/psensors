#!/usr/bin/python
from gi.repository import Gtk, GObject, GdkPixbuf
from sensors import SensorReader
import threading

class IconoTray:
	def __init__(self, iconname):
		self.menu = Gtk.Menu()

		APPIND_SUPPORT = 1
		try: from gi.repository import AppIndicator3
		except: APPIND_SUPPORT = 0

		if APPIND_SUPPORT == 1:
			self.ind = AppIndicator3.Indicator.new("Soprano2", iconname, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
			self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
			self.ind.set_menu(self.menu)
		else:
			self.myStatusIcon = Gtk.StatusIcon()
			self.myStatusIcon.set_from_icon_name(iconname)
			self.myStatusIcon.connect('popup-menu', self.right_click_event_statusicon)
	
	def add_menu_item(self, command, title):
		aMenuitem = Gtk.MenuItem()
		aMenuitem.set_label(title)
		aMenuitem.connect("activate", command)

		self.menu.append(aMenuitem)
		self.menu.show_all()
		return aMenuitem

	def add_seperator(self):
		aMenuitem = Gtk.SeparatorMenuItem()
		self.menu.append(aMenuitem)
		self.menu.show_all()

	def get_tray_menu(self):
		return self.menu		

	def right_click_event_statusicon(self, icon, button, time):
		self.get_tray_menu()

		def pos(menu, aicon):
			return (Gtk.StatusIcon.position_menu(menu, aicon))

		self.menu.popup(None, None, pos, icon, button, time)

def blank(title):
	pass

class pyGIsensors:
	def __init__(self):
		self.sensors = SensorReader()
		self.readvalues()
		self.launchtitlelist = self.sensors.titlelist
		self.labelarray = {}

		self.tray = IconoTray("psensors-tray")
		self.tray.add_menu_item(blank, "Psensors")

		for x in range(0, len(self.launchtitlelist)):
			self.createtraystring(self.launchtitlelist[x])
		self.tray.add_seperator()
		self.tray.add_menu_item(Gtk.main_quit, "Quit")

		timer = GObject.timeout_add(2000, self.updatelabels)

	def readvalues(self):
		self.sensors.updatevalues()

	def printvalues(self):
		self.sensors.printvalues()

	def updatelabels(self):
		self.readvalues()
		for x in range(0, len(self.launchtitlelist)):
			if self.launchtitlelist[x] in self.sensors.fanarray:
				for i, v in self.sensors.fanarray[self.launchtitlelist[x]].iteritems():
					self.labelarray[self.launchtitlelist[x]+i.replace(" ","")].set_label(i + " : " + v + " RPM")
			if self.launchtitlelist[x] in self.sensors.temperaturearray:
				for i, v in self.sensors.temperaturearray[self.launchtitlelist[x]].iteritems():
					self.labelarray[self.launchtitlelist[x]+i.replace(" ","")].set_label(i + " : " + v)
		return True
				
	def createtraystring(self, title):
		self.tray.add_seperator()
		self.tray.add_menu_item(blank, title.split("-")[0])
		self.tray.add_seperator()
		if title in self.sensors.fanarray:
			for i, v in sorted(self.sensors.fanarray[title].iteritems()):
				self.labelarray[title+i.replace(" ","")] = self.tray.add_menu_item(blank, i + " : " + v + " RPM")		
		if title in self.sensors.temperaturearray:
			for i, v in sorted(self.sensors.temperaturearray[title].iteritems()):
				self.labelarray[title+i.replace(" ","")] = self.tray.add_menu_item(blank, i + " : " + v)
	
app = pyGIsensors()

if __name__ == '__main__':
	Gtk.main()
