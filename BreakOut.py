#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from math import *
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ball import *
from Palet import *
from Brique import *

#Commande de lancement conseillé : python3 BreakOut.py

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setFont(QFont("Arial",14))
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette();
        p.setColor(QPalette.Window, QColor(53,53,53))
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,255,255))
        self.setPalette(p)

class RenderArea(QWidget):
    def __init__(self, parent=None):
        super(RenderArea,self).__init__(parent)
        self.initUI()

    def closeEvent(self,event):
        QCoreApplication.instance().quit()

    def initUI(self):
        self.setWindow()
        self.setCenter()
        self.show()
        self.pen = QPen(QColor(255,255,255))
        self.pen.setWidth(1)
        self.brush = QBrush(QColor(255,255,255))

        #Création des objets
        self.balle = Ball()
        self.palet = Palet()
        self.scoring = 0

        #Génère un tableau
        self.generator()

        self.width = QDesktopWidget().availableGeometry().width()//2
        self.height = QDesktopWidget().availableGeometry().height()

        #Timer de tick de mouvement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.movement)
        self.timer.start(self.balle.speed)

        #Timer d'acceleration
        self.speedUp = QTimer(self)
        self.speedUp.timeout.connect(self.faster)
        #1000 = 1 seconde, 10000->vitesse max au bout de 490 secondes
        self.speedUp.start(10000)

    def drawBall(self, painter):
        x = self.balle.x
        y = self.balle.y
        if (self.balle.etat=="normal"):
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
        if (self.balle.etat=="lightning"):
            painter.setPen(QPen(QColor("yellow")))
            painter.setBrush(QBrush(QColor("yellow")))
        painter.drawRect(QRect(QPoint(x,y),QPoint(x+10,y+10)))

    def drawPalet(self, painter):
        x = self.palet.x
        y = self.palet.y
        if(self.palet.etat=="normal"):
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
        if(self.palet.etat=="freeze"):
            painter.setPen(QPen(QColor(135,206,250,255)))
            painter.setBrush(QBrush(QColor(135,206,250,255)))

        painter.drawRect(QRect(QPoint(x,y),QPoint(x+100,y+10)))

    def drawBrique(self,painter):
        width = (QDesktopWidget().availableGeometry().width()/2)//10
        height = self.briques[0].height
        painter.setPen(QColor("black"))
        for i in range(100):
            painter.setBrush(self.briques[i].color)
            if (self.briques[i].HP > 0) :
                x = self.briques[i].x
                y = self.briques[i].y
                painter.drawRect(QRect(QPoint(x,y),QPoint(x+width,y+height)))


    def movement(self):
        self.balle.move()

        #Perte d'une vie
        if self.balle.y+65>=self.height:
            self.gameOver()

        #Collisions murales
        if self.balle.x<=0 or self.balle.x+10>=self.width:
            self.balle.collisionX()
        if self.balle.y<=0:
            self.balle.collisionY()

        #Collision avec le palet
        if (self.balle.x+10>=self.palet.x and self.balle.x<=self.palet.x+100):
            if (self.balle.y+10>=self.palet.y and self.balle.y<=self.palet.y+10) and self.balle.sens_y>0:
                modif = self.balle.x-self.palet.x
                self.balle.collisionPalet(modif)
                self.balle.etat = "normal"

        #J'ai tenté diverse façon et test mais il y a des chances qu'il reste des bugs ici
        #Collision avec une brique
        if (self.balle.etat=="normal"):
            collide = False
        else :
            collide = True
        broken = 0
        for i in range (100):
            
            if (self.briques[i].HP>0):
                #Condition de contact, ne pas utiliser
                #if (self.balle.x <= self.briques[i].x+self.briques[i].width) and (self.balle.x+10 >= self.briques[i].x) and (self.balle.y <= self.briques[i].y+20 and self.balle.y+10 >= self.briques[i].y):
                    #self.balle.collisionY()
                    #self.briques[i].hit()
                
                #Condition contact bas de la brique
                if (self.balle.y <= self.briques[i].y+20) and (self.balle.y+10 >= self.briques[i].y+20) and (self.balle.x <= self.briques[i].x+self.briques[i].width) and (self.balle.x+10 >= self.briques[i].x) and (self.balle.sens_y<0):
                    if collide == False : 
                        self.balle.collisionY()
                        collide = True
                    effet = self.briques[i].hit()
                    #Modifie le score
                    self.scoring += self.briques[i].point
                    #Déclenche l'effet
                    if (effet!="aucun"):
                        self.special(effet, i)
                    #Valide la destruction

                #Condition contact gauche de la brique
                if (self.balle.x <= self.briques[i].x) and (self.balle.x+10 >= self.briques[i].x) and (self.balle.y <= self.briques[i].y+20 and self.balle.y+10 >= self.briques[i].y) and (self.balle.sens_x>0):
                    if collide == False :
                        self.balle.collisionX()
                        collide = True
                    effet = self.briques[i].hit()
                    self.scoring += self.briques[i].point
                    if (effet!="aucun"):
                        self.special(effet, i)

                #Condition contact droite de la brique
                if (self.balle.x <= self.briques[i].x+self.briques[i].width) and (self.balle.x+10 >= self.briques[i].x+self.briques[i].width) and (self.balle.y <= self.briques[i].y+20 and self.balle.y+10 >= self.briques[i].y)and (self.balle.sens_x<0):
                    if collide == False : 
                        self.balle.collisionX()
                        collide = True
                    effet = self.briques[i].hit()
                    self.scoring += self.briques[i].point
                    if (effet!="aucun"):
                        self.special(effet, i)

                #Condition contact haut de la brique
                if (self.balle.y <= self.briques[i].y) and (self.balle.y+10 >= self.briques[i].y) and (self.balle.x <= self.briques[i].x+self.briques[i].width) and (self.balle.x+10 >= self.briques[i].x) and (self.balle.sens_y>0):
                    if collide == False : 
                        self.balle.collisionY()
                        collide = True
                    effet = self.briques[i].hit()
                    self.scoring += self.briques[i].point
                    if (effet!="aucun"):
                        self.special(effet, i)

            else :
                broken+=1
            if (self.briques[i].HP==100):
                broken+=1

        if(broken==100):
            self.generator()
            self.palet.reset()
            self.balle.reset()
            self.timer.stop()
            self.speedUp.stop()
            dialog = QMessageBox(self)
            dialog.setText("LEVEL CLEAR")
            char = "Score actuel : "
            char += str(self.scoring)
            dialog.setInformativeText(char)
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            self.timer.start(self.balle.speed)
            self.speedUp.start(10000)
        self.update()

    #Game Over
    def gameOver(self):
        self.balle.lifeLost()
        if (self.balle.life!=0):
            #Bon faudra coder un game over propre
            self.timer.stop()
            self.speedUp.stop()
            dialog = QMessageBox(self)
            dialog.setText("YOU DIED")
            char = "Continuer ? Vie restante : "
            char += str(self.balle.life)
            dialog.setInformativeText(char)
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            self.timer.start(self.balle.speed)
            self.speedUp.start(10000)
            self.palet.reset()
        else :
            self.timer.stop()
            self.speedUp.stop()
            dialog = QMessageBox(self)
            dialog.setText("GAME OVER")
            char = "Votre score : "
            char += str(self.scoring)
            dialog.setInformativeText(char)
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            self.palet.reset()
            self.scoring = 0
            self.generator()
            self.balle.life = 3

    #Gestion des effets : Explosion, ...
    def special(self, effet, nb):
        if(effet=="explosion"):
            self.briques[nb].effet = "aucun"
            self.explosion(nb)
        if(effet=="lightning"):
            self.briques[nb].effet = "aucun"
            self.lightning()
        if(effet=="freeze"):
            self.briques[nb].effet = "aucun"
            self.freeze()
        if(effet=="OneUp"):
            self.briques[nb].effet = "aucun"
            self.balle.life += 1

    #Attention au bloc de code répétitif pour la gestion des effets en chaine.
    def explosion(self, nb):
        if(nb<10):
            if(nb==0):
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)
                effet = self.briques[nb+11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+11)
            if(nb==9):
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-1)
                effet = self.briques[nb+9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+9)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)
            if(nb>0 and nb<9):
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-1)
                effet = self.briques[nb+9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+9)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)
                effet = self.briques[nb+11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+11)

        if(nb>9 and nb<90):
            if(nb%10==0):
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
                effet = self.briques[nb-9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-9)
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)
                effet = self.briques[nb+11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+11)

            if(nb%10==9):
                effet = self.briques[nb-11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-11)
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-1)
                effet = self.briques[nb+9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+9)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)

            if(nb%10>0 and nb%10<9):
                effet = self.briques[nb-11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-11)
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
                effet = self.briques[nb-9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-9)
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-1)
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb+9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+9)
                effet = self.briques[nb+10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+10)
                effet = self.briques[nb+11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+11)

        if(nb>89):
            if(nb==90):
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb-9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-9)
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
            if(nb==99):
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+-1)
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
                effet = self.briques[nb-11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-11)
            if(nb>90 and nb<99):
                effet = self.briques[nb+1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb+1)
                effet = self.briques[nb-1].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-1)
                effet = self.briques[nb-9].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-9)
                effet = self.briques[nb-10].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-10)
                effet = self.briques[nb-11].hit()
                if (effet!="aucun"):
                    self.special(effet, nb-11)

    #Effet du bloc lightning
    def lightning(self):
        self.balle.sens_x = 0
        self.balle.sens_y = 20
        self.balle.etat = "lightning"

    #Effet du bloc freeze
    def freeze(self):
        if (self.palet.etat!="freeze"):
            self.palet.etat = "freeze"
            self.unfreeze = QTimer(self)
            self.unfreeze.timeout.connect(self.unFreeze)
            #1000 = 1 seconde, 10000 = 10 secondes
            self.unfreeze.start(10000)

    #Rétablie le palet, aprés le gel.
    def unFreeze(self):
        self.palet.etat = "normal"
        self.unfreeze.stop()

    def faster(self):
        if self.balle.speed != 1:
            self.balle.speed = self.balle.speed-1
            self.timer.start(self.balle.speed)
            self.update()

    #Permet de mettre en pause
    def mousePressEvent(self, event):
        if self.timer.isActive() :
            self.timer.stop()
            self.speedUp.stop()
            dialog = QMessageBox(self)
            dialog.setText("PAUSE")
            char = "Score actuel : "
            char += str(self.scoring)
            char += "       Vie restante : "
            char += str(self.balle.life)
            dialog.setInformativeText(char)
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            self.timer.start(self.balle.speed)
            self.speedUp.start(10000)
        else:
            self.timer.start(self.balle.speed)
            self.speedUp.start(10000)
        self.update()

    def keyPressEvent(self, event):
        if self.timer.isActive() :
            if event.key()==Qt.Key_Left:
                self.palet.moveLeft()
            if event.key()==Qt.Key_Right:
                self.palet.moveRight()
            self.update()

    def generator(self):
        #Generateur de brique Aléatoire (5/5/5/3/3/2/3/1/X/10)
        self.briques = []
        for i in range (100):
            rng = random.randint(1,100)
            if (rng<=5):
                self.briques.append(Brique_Indestructible())
            if (rng>5 and rng<=10):
                self.briques.append(Brique_Armor2())
            if (rng>10 and rng <=15):
                self.briques.append(Brique_Armor3())
            if (rng>15 and rng <=18):
                self.briques.append(Brique_Explosive())
            if (rng>18 and rng <=21):
                self.briques.append(Brique_Lightning())
            if (rng>21 and rng <=23):
                self.briques.append(Brique_Bonus())
            if (rng>23 and rng <=26):
                self.briques.append(Brique_Freeze())
            if (rng>26 and rng <=27):
                self.briques.append(Brique_OneUp())
            if (rng>26 and rng <=90):
                self.briques.append(Brique())
            if (rng>90):
                self.briques.append(Brique_Air())
            self.briques[i].position(i)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBall(painter)
        self.drawPalet(painter)
        self.drawBrique(painter)

    def setWindow(self):
        width = QDesktopWidget().availableGeometry().width()/2
        height = QDesktopWidget().availableGeometry().height()
        self.setGeometry(10, 10, width, height)
        self.setWindowTitle("BreakOut !")
        #self.statusBar().showMessage("Score : 0")
        #La status barre semble propre à QMainWindow

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = Application([])
win = RenderArea()
app.exec_()
