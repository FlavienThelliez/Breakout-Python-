#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Palet():
	def __init__(self):
		self.x = QDesktopWidget().availableGeometry().width()//4-100
		self.y = QDesktopWidget().availableGeometry().height()-100
		self.etat = "normal"

	def moveLeft(self):
		if (self.etat=="normal"):
			if self.x-5 > 0:
				self.x = self.x-5
			else :
				self.x = 0

		if (self.etat=="freeze"):
			if self.x-3 > 0:
				self.x = self.x-3
			else :
				self.x = 0


	def moveRight(self):
		if (self.etat=="normal"):
			if self.x+105 < QDesktopWidget().availableGeometry().width()//2:
				self.x = self.x+5
			else :
				self.x = QDesktopWidget().availableGeometry().width()//2-100

		if (self.etat=="freeze"):
			if self.x+103 < QDesktopWidget().availableGeometry().width()//2:
				self.x = self.x+3
			else :
				self.x = QDesktopWidget().availableGeometry().width()//2-100

	#Replace au centre
	def reset(self):
		self.x = QDesktopWidget().availableGeometry().width()//4-100
		self.y = QDesktopWidget().availableGeometry().height()-100