#!/usr/bin/python
from gi.repository import Gtk, GObject, GdkPixbuf
from sensors import SensorReader
import threading

class pyGIsensors:
	def __init__(self):
		self.sensors = SensorReader()
		self.readvalues()
		self.launchtitlelist = self.sensors.titlelist
		self.labelarray = {}

		mainwindow = Gtk.Window()
		mainwindow.connect('destroy', Gtk.main_quit)
		mainwindow.set_default_size(400,200)
		mainwindow.set_title("PSensors") 
		mainwindow.set_icon(GdkPixbuf.Pixbuf().new_from_file('psensors.svg'))

		notebook = Gtk.Notebook()
		notebook.set_tab_pos(Gtk.PositionType.LEFT)
		for x in range(0, len(self.launchtitlelist)):
			self.createpage(self.launchtitlelist[x],notebook)

		mainwindow.add(notebook)
		mainwindow.show_all()
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
					self.labelarray[self.launchtitlelist[x]+i.replace(" ","")].set_text(v + " RPM")
			if self.launchtitlelist[x] in self.sensors.temperaturearray:
				for i, v in self.sensors.temperaturearray[self.launchtitlelist[x]].iteritems():
					self.labelarray[self.launchtitlelist[x]+i.replace(" ","")].set_text(v)
		return True
		

	def createpage(self, title, notebook):
		alabel = Gtk.Label(title.split("-")[0])
		aVbox = Gtk.VBox()
		if title in self.sensors.fanarray:
			for i, v in self.sensors.fanarray[title].iteritems():
				temphbox = Gtk.HBox()
				temphbox.set_homogeneous(True)
				fanname = Gtk.Label(i)
				self.labelarray[title+i.replace(" ","")] = Gtk.Label(v + " RPM")
				temphbox.pack_start(fanname, False, True, 5)
				temphbox.pack_end(self.labelarray[title+i.replace(" ","")], False, True, 5)
				aVbox.pack_start(temphbox, False, True, 4)
		aVbox.pack_start(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), False, True, 4)
		if title in self.sensors.temperaturearray:
			for i, v in self.sensors.temperaturearray[title].iteritems():
				temphbox = Gtk.HBox()
				temphbox.set_homogeneous(True)
				fanname = Gtk.Label(i)
				self.labelarray[title+i.replace(" ","")] = Gtk.Label(v)
				temphbox.pack_start(fanname, False, True, 5)
				temphbox.pack_end(self.labelarray[title+i.replace(" ","")], False, True, 5)
				aVbox.pack_start(temphbox, False, True, 4)
		notebook.append_page(aVbox, alabel)
app = pyGIsensors()
if __name__ == '__main__':
	Gtk.main()
