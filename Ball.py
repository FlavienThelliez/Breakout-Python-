#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ball():
	def __init__(self):
		self.x = QDesktopWidget().availableGeometry().width()//4-100
		self.y = 300
		self.sens_x = 1
		self.sens_y = 10
		self.speed = 50
		self.life = 3
		self.etat = "normal"

	def collisionX(self):
		self.sens_x = self.sens_x*(-1)
		if self.x <= 0 :
			self.x = 0
		if self.x >= QDesktopWidget().availableGeometry().width()//2-10 :
			self.x = QDesktopWidget().availableGeometry().width()//2-10
		

	def collisionY(self):
		self.sens_y = self.sens_y*(-1)
	
	def collisionPalet(self, mod):
		self.sens_y = self.sens_y*(-1)
		if self.sens_x > 0:
			if mod<12:
				self.sens_y = self.sens_y-2
				self.sens_x = self.sens_x-2
			if mod>12 and mod<34 :
				self.sens_y = self.sens_y-1
				self.sens_x = self.sens_x-1
			if mod>56 and mod<78 :
				self.sens_y = self.sens_y+1
				self.sens_x = self.sens_x+1
			if mod>78 :
				self.sens_y = self.sens_y+2
				self.sens_x = self.sens_x+2

			#La balle change va dans le sens opposé en touchant le bord du palet
			if self.sens_x < 1 :
				self.sens_y = -10
				self.sens_x = -1
			#La balle touche l'autre bord du palet
			if self.sens_x > 8:
				self.sens_y = -3
				self.sens_x = 8

		else:
			if mod<12:
				self.sens_y = self.sens_y+2
				self.sens_x = self.sens_x-2
			if mod>12 and mod<34 :
				self.sens_y = self.sens_y+1
				self.sens_x = self.sens_x-1
			if mod>56 and mod<78 :
				self.sens_y = self.sens_y-1
				self.sens_x = self.sens_x+1
			if mod>78 :
				self.sens_y = self.sens_y-2
				self.sens_x = self.sens_x+2

			#La balle change va dans le sens opposé en touchant le bord du palet
			if self.sens_x > -1:
				self.sens_y = -10
				self.sens_x = 1
			#La balle touche l'autre bord du palet
			if self.sens_x < -8:
				self.sens_y = -3
				self.sens_x = -8
		#Ajout pour éviter les problèmes avec le bloc "lightning"
		if(self.sens_y>10):
			self.sens_y = 10

		if(self.sens_y<-10):
			self.sens_y = -10 


	def move(self):
		self.x = self.sens_x+self.x
		self.y = self.sens_y+self.y


	def lifeLost(self):
		self.life = self.life-1
		self.reset()
		
	def reset(self):
		self.x = QDesktopWidget().availableGeometry().width()//4-100
		self.y = 300
		self.sens_x = 1
		self.sens_y = 10
		self.speed = 50
	
