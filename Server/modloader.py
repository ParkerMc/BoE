import mods
from mods import *
import inspect



class modloader():

	def __init__(self):
		self.SinitL = []
		self.CinitL = []
		self.messageL = []
		self.newidL = []
		self.ScloseL = []
		self.CcloseL = []
		for i in mods.__all__:
			print i
			print inspect.getmembers(getattr(mods, i), predicate=inspect.isfunction)
			for j, k in inspect.getmembers(getattr(mods, i), predicate=inspect.isfunction):
				if j == "Sinit":
					self.SinitL.append(k)
				if j == "Cinit":
					self.CnitL.append(k)
				elif j == "message":
					self.messageL.append(k)
				elif j == "newid":
					self.newidL.append(k)
				elif j == "Sclose":
					self.ScloseL.append(k)
				elif j == "Cclose":
					self.CcloseL.append(k)

	def Sinit(self, server):
		for i in self.SinitL:
			i(server)

	def Cinit(self, client, server):
		for i in self.CinitL:
			i(client, server)

	def message(self, client, server):
		for i in self.messageL:
			i(client, server)
			
	def newid(self, client, server):
		for i in self.newidL:
			i(client, server)

	def Sclose(self, server):
		for i in self.ScloseL:
			i(server)

	def Cclose(self, client, server):
		for i in self.CcloseL:
			i(client, server)		