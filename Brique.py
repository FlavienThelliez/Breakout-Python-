#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Brique verte de base, sert aussi à définir les autres briques
class Brique():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 1
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("green")
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet

#Indestructible !
class Brique_Indestructible(Brique):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 100
		self.point = 0
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("darkGray")
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		return self.effet

#Explosion ! Diminue de 1 la résistance de toute les briques adjacente. Ne détruit pas l'Indestructible.
class Brique_Explosive(Brique):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 10
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("red")
		self.effet = "explosion"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet

#De l'air, quoi d'autre ? 
class Brique_Air(Brique):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 0
		self.point = 0
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("green")
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		return self.effet

#2 Point de vie
class Brique_Armor2():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 2
		self.point = 2
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		#vert altéré
		self.color = QColor(121, 137, 51, 255)
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		if (self.HP==1):
			self.color = QColor("Green")
		return self.effet

#3 point de vie, solide.
class Brique_Armor3():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 3
		self.point = 2
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		#Marron
		self.color = QColor(139,66,29,255)
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		if (self.HP==2):
			self.color = QColor(121, 137, 51, 255)
		if (self.HP==1):
			self.color = QColor("Green")
		return self.effet

#Transforme la balle en éclair qui fonce vers le bas, hehe, attention aux mauvaises surprise.
class Brique_Lightning():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 25
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("yellow")
		self.effet = "lightning"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet

#Une brique rare rapportant beaucoup de point
class Brique_Bonus():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 50
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor(128,0,128,255)
		self.effet = "aucun"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet

#Une brique qui ralenti la barre, bonne chance ^^.
class Brique_Freeze():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 15
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor(135,206,250,255)
		self.effet = "freeze"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet

class Brique_OneUp():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.HP = 1
		self.point = 100
		self.width = (QDesktopWidget().availableGeometry().width()/2)//10
		self.height = 25
		self.color = QColor("white")
		self.effet = "OneUp"

	def position(self, number):
		self.x = self.width*(number-(number//10*10))
		self.y = self.height*(number//10)

	def hit(self):
		self.HP = self.HP-1
		return self.effet