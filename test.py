#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ball import *
from Palet import *

class Principale(QWidget):
   
    def __init__(self):
        super(Principale, self).__init__()
 
        self.setWindowTitle('ma super fenetre')
        self.resize(600, 600)
         
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left: print("ca marche")
        if event.key() == Qt.Key_Right: print ("ca marche")
 
 



app = QApplication(sys.argv)
princ = Principale()
princ.show()
sys.exit(app.exec_())
"""
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

class Layout(QWidget):
    def __init__(self, parent=None):
        super(Layout,self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.browser = QTextBrowser()
        self.area = QFrame()
        self.area.setFrameShape(QFrame.Box)
        self.area.setMinimumWidth(self.width() / 2)
        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.area)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        print("poc")
        if event.key() == Qt.Key_Left: print("ca marche")
        if event.key() == Qt.Key_Right: print ("ca marche")
        
        self.update()

    def mousePressEvent(self, event):
        self.browser.append("<b>%s</b>: QPoint(%d,%d)" % ("MousePress", event.pos().x(), event.pos().y()))
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.browser.append("<b>%s</b>: QPoint(%d,%d)" % ("MouseDoubleClick", event.pos().x(), event.pos().y()))
        self.update()

    def resizeEvent(self, event):
        print("resize")
        self.browser.append("<b>%s</b>: QSize(%d,%d)" % ("Resize", event.size().width(), event.size().height() ))
        self.update()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def closeEvent(self,event):
        QCoreApplication.instance().quit()

    def initUI(self):
        self.setWindow()
        self.setCenter()
        self.setLayout()
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setLayout(self):
        self.layout = Layout()
        self.setCentralWidget(self.layout)

    def setWindow(self):
        width = QDesktopWidget().availableGeometry().width()/2
        height = QDesktopWidget().availableGeometry().height()/2
        self.setGeometry(10, 10, width, height)
        self.setWindowTitle("Gestion d'événements sous Qt")


app = Application([])
win = Window()
app.exec_()
"""