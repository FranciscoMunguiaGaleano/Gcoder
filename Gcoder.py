# coding=utf-8
#!/usr/local/bin/Python2.7
#import RPi.GPIO as GPIO
import threading
import sys
from OpenGL.GL import *
from PyQt4 import QtCore, QtGui, QtOpenGL,Qt
from PyQt4.QtOpenGL import *
import numpy
import math
from stl import mesh
import time
import serial
try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
            "PyOpenGL must be installed to run this program.")
    sys.exit(1)
#from ctypes import
#pausa= CDLL('/home/pi/Desktop/Gcoder/pausa.so')

#micropausa=pausa.dormir
#micropausa.argtypes=[c_uint]
#micropausa.restype=c_int
########################IO config.##########
class GCODER(QtGui.QMainWindow):
    
    def __init__(self):
        super(GCODER, self).__init__()
#####variables       
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)
        self.pestanas=QtGui.QTabWidget()
        mainLayout.addWidget(self.pestanas)
        self.grafico=GLWidget()
        
        self.widget=QtGui.QWidget()
        self.widget1=QtGui.QWidget()
        self.widget2=QtGui.QWidget()
        self.widget3=QtGui.QWidget()
        self.widget4=QtGui.QWidget()
        self.control=QtGui.QTabWidget()
        self.line=""
        self.filename = ""
        self.filename_1=""
        self.arvivo=""
        self.des=16.7888
        self.LA=14.369
        self.LB=3.5
        self.L1=20
        self.LE=2.3
        self.arriba=0
        self.abajo=0
        self.start=1
        self.ejecutar=0
        self.casa=0
        self.distancia_1=10.0
        self.distancia_2=10.0
        self.distancia_3=10.0
        self.distancia_4=10.0
        self.distancia_5=0.0
        self.pos1_i=0.0
        self.pos2_i=0.0
        self.pos3_i=0.0
        self.pos4_i=0.0
        self.pos5_i=0.0
        self.pos1_f=0.0
        self.pos2_f=0.0
        self.pos3_f=0.0
        self.pos4_f=0.0
        self.pos5_f=0.0
        self.pos1g_i=0.0
        self.pos2g_i=0.0
        self.pos3g_i=0.0
        self.pos4g_i=0.0
        self.pos5g_i=0.0
        self.pos6g_i=0.0
        self.pos1g_f=0.0
        self.pos2g_f=0.0
        self.pos3g_f=0.0
        self.pos4g_f=0.0
        self.pos5g_f=0.0
        self.pos6g_f=0.0
        self.tiempo=8.0
        self.direccion=0 #0 abajo 1 arriba
        self.ejez=0
        self.sis_unidades=400
        self.Xr=0.0
        self.Yr=0.0
        self.Zr=0.0
        self.px=0.0
        self.py=0.0
        self.pz=0.0
        self.x=0
        self.y=0
        self.z=0
        self.mot1=0
        self.mot2=0
        self.mot3=0
        self.mot4=0
        self.mot5=0
        self.xmas=0
        self.e=0.0
        self.interpretador=0
        self.contadordelinea=0
        self.conter=0
        self.parar=0
        self.router=0
        self.g=0
        self.puerto=""
        self.puerto1=""
        self.conectado=0
        self.conectado1=0
        self.velocidadg=400
        self.avanceg=5.0
        self.xgpri=0.0
        self.xgprf=0.0
        self.xg=0.0
        self.ygpri=0.0
        self.ygprf=0.0
        self.yg=0.0
        self.zgpri=0.0
        self.zgprf=0.0
        self.zg=0.0
        self.cgpri=0.0
        self.cgprf=0.0
        self.cg=0.0
        self.dgpri=0.0
        self.dgprf=0.0
        self.dg=0.0
        self.egpri=0.0
        self.egprf=0.0
        self.eg=0.0
        self.fgprf=self.velocidadg
        self.fg=0.0
        self.pv=0
        self.herramienta=0#0 impresora 1 gripper
#######Threads
        threading.stack_size(8192000)
        interpreteG=threading.Thread(target=self.interprete)
        interpreteG.start()
        self.statusBar()
#Accion de movimiento
        up= QtGui.QAction(QtGui.QIcon('arriba.png'), 'Axis Z up', self)
        up.setShortcut('Ctrl+U')
        up.setStatusTip('Axis Z up')
        up.triggered.connect(self.moveup)
        
        down= QtGui.QAction(QtGui.QIcon('abajo.png'), 'Axis Z down', self)
        down.setShortcut('Ctrl+D')
        down.setStatusTip('Axis Z down')
        down.triggered.connect(self.movedown)

        right= QtGui.QAction(QtGui.QIcon('derecha.png'), 'Right', self)
        right.setShortcut('Ctrl+R')
        right.setStatusTip('Moving right')
        right.triggered.connect(self.moveright)

        left= QtGui.QAction(QtGui.QIcon('izquierda.png'), 'Left', self)
        left.setShortcut('Ctrl+L')
        left.setStatusTip('Moving left')
        left.triggered.connect(self.moveleft)

        foward= QtGui.QAction(QtGui.QIcon('enfrente.png'), 'Foward', self)
        foward.setShortcut('Ctrl+F')
        foward.setStatusTip('Moving foward')
        foward.triggered.connect(self.movefoward)

        behind= QtGui.QAction(QtGui.QIcon('atras.png'), 'Behind', self)
        behind.setShortcut('Ctrl+A')
        behind.setStatusTip('Moving behind')
        behind.triggered.connect(self.movebehind)
        
        home= QtGui.QAction(QtGui.QIcon('home.png'), 'Home', self)
        home.setShortcut('Ctrl+H')
        home.setStatusTip('Go Home')
        home.triggered.connect(self.gohome)
#Creating actions whose are going to be used at the status bar        
        newAction = QtGui.QAction(QtGui.QIcon('new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Creates a new file')
        newAction.triggered.connect(self.new)

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.cerrar)

        openAction = QtGui.QAction(QtGui.QIcon('OPEN.png'), 'Open ', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.showopen)

        saveAction = QtGui.QAction(QtGui.QIcon('guardar.png'), 'Save ', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save a file')
        saveAction.triggered.connect(self.save)

        saveasAction = QtGui.QAction(QtGui.QIcon('guardar_como.png'), 'Save as', self)
        saveasAction.setShortcut('Ctrl+Shift+S')
        saveasAction.setStatusTip('Save a file as')
        saveasAction.triggered.connect(self.saveas)
        

####################################################################
        undoAction = QtGui.QAction(QtGui.QIcon('undo.png'), 'Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.setStatusTip('Undo')
        undoAction.triggered.connect(self.doundo)
        redoAction = QtGui.QAction(QtGui.QIcon('redo.png'), 'Redo', self)
        redoAction.setShortcut('Ctrl+Shift+Z')
        redoAction.setStatusTip('Redo')
        redoAction.triggered.connect(self.doredo)
        
        copyAction = QtGui.QAction(QtGui.QIcon('copy.png'), 'Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy')
        copyAction.triggered.connect(self.docopy)
        cutAction = QtGui.QAction(QtGui.QIcon('cut.png'), 'Cut', self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.setStatusTip('Cut')
        cutAction.triggered.connect(self.docut)
        pasteAction = QtGui.QAction(QtGui.QIcon('paste.png'), 'Paste', self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.setStatusTip('Paste')
        pasteAction.triggered.connect(self.dopaste)
######################################################################
        playAction = QtGui.QAction(QtGui.QIcon('play.png'), 'Run ', self)
        playAction.setShortcut('Ctrl+R')
        playAction.setStatusTip('Run the program')
        playAction.triggered.connect(self.play)
        pauseAction = QtGui.QAction(QtGui.QIcon('pause.png'), 'Pause', self)
        pauseAction.setShortcut('Ctrl+P')
        pauseAction.setStatusTip('Pause the program')
        pauseAction.triggered.connect(self.pause)
        fowardAction = QtGui.QAction(QtGui.QIcon('foward.png'), 'Foward', self)
        fowardAction.setShortcut('Ctrl+F')
        fowardAction.setStatusTip('Run step by step the program')
        fowardAction.triggered.connect(self.foward)
        stopAction = QtGui.QAction(QtGui.QIcon('stop.png'), 'Stop', self)
        stopAction.setShortcut('Ctrl+N')
        stopAction.setStatusTip('Stop the program')
        stopAction.triggered.connect(self.stop)
######################################################################

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveasAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        fileMenu = menubar.addMenu('&Edit')
        fileMenu.addAction(undoAction)
        fileMenu.addAction(redoAction)
        fileMenu.addSeparator()
        fileMenu.addAction(copyAction)
        fileMenu.addAction(cutAction)
        fileMenu.addAction(pasteAction)
        fileMenu = menubar.addMenu('&Run')
        fileMenu.addAction(playAction)
        fileMenu.addAction(pauseAction)
        fileMenu.addAction(fowardAction)
        fileMenu.addAction(stopAction)
        fileMenu = menubar.addMenu('&Help')


        toolbar = self.addToolBar('File')
        toolbar.addAction(newAction)

        toolbar.addSeparator()
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        toolbar.addAction(saveasAction)
        toolbar1 = self.addToolBar('Edit')
        toolbar1.addAction(copyAction)
        toolbar1.addAction(cutAction)
        toolbar1.addAction(pasteAction)
        toolbar1.addAction(redoAction)
        toolbar1.addSeparator()
        toolbar1.addAction(undoAction)
        toolbar2 = self.addToolBar('Run')
        toolbar2.addAction(playAction)
        toolbar2.addAction(pauseAction)
        toolbar2.addAction(fowardAction)
        toolbar2.addAction(stopAction)
        toolbar2.addSeparator()
        toolbar2.addAction(exitAction)
        toolbar2.addSeparator()
        toolbar2.addAction(up)
        toolbar2.addAction(down)
        toolbar2.addAction(left)
        toolbar2.addAction(right)
        toolbar2.addAction(foward)
        toolbar2.addAction(behind)
        toolbar2.addAction(home)
        self.pestanas.addTab(self.widget,'G Coder')
        self.pestanas.addTab(self.widget1,'Viewer')
        self.control.addTab(self.widget2,'3D')
        self.control.addTab(self.widget4,'Slicer')
        self.control.addTab(self.widget3,'Pick & Place')
        self.setCentralWidget(self.pestanas)
        self.initUI()
        self.init1UI()
        
    def initUI(self):               
        self.widget.review = QtGui.QLabel('Error')
        self.widget.recived= QtGui.QLabel('Data')
        self.widget.send= QtGui.QPushButton('Send')
        self.widget.textEdit = QtGui.QTextEdit()
        self.widget.reviewEdit = QtGui.QLineEdit()
        self.widget.recivedEdit= QtGui.QLineEdit()
        self.widget.sendEdit= QtGui.QLineEdit()
        self.widget.send.clicked.connect(self.sending)
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.widget.textEdit, 2,0, 3, 0)
        grid.addWidget(self.widget.review, 6, 0)
        grid.addWidget(self.widget.reviewEdit,6,1)
        grid.addWidget(self.widget.recived,7,0)
        grid.addWidget(self.widget.recivedEdit,7,1)
        self.widget.setLayout(grid)
        self.setGeometry(50, 50, 750, 600)
        self.setWindowTitle('G coder')
        self.setWindowIcon(QtGui.QIcon('logo.png'))
    def phome(self):
        if self.conectado1==1:
            self.widget.reviewEdit.setText("Pick and place to home")
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0500000000000000000000000000000000000000000000000000000000000000000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def conect(self):
        print "Pick and place conected"
    def saver(self):
        if not self.filename:
            self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.gcode)")
        coordenada=""
        if self.pv==0:
            self.pv=1
            archivo=open(self.filename,"r")
            contenido=archivo.read()
            final_de_archivo=archivo.tell()
            archivo=open(self.filename,"r+")
            archivo.seek(final_de_archivo)
            archivo.write("M06\n")
            #archivo.seek(final_de_archivo)
            #nuevo_contenido=archivo.read()
            archivo=open(self.filename,"r")
            contenido=archivo.read()
            final_de_archivo=archivo.tell()
            archivo=open(self.filename,"r+")
            archivo.seek(final_de_archivo)
            archivo.write("G28\n")
            #archivo.seek(final_de_archivo)
            #nuevo_contenido=archivo.read()
            #print nuevo_contenido
        if self.xg!=self.xgprf:
            coordenada=coordenada+" X"+str(self.xgprf)
        if self.yg!=self.ygprf:
            coordenada=coordenada+" Y"+str(self.ygprf)
        if self.zg!=self.zgprf:
            coordenada=coordenada+" Z"+str(self.zgprf)
        if self.cg!=self.cgprf:
            coordenada=coordenada+" C"+str(self.cgprf)
        if self.dg!=self.dgprf:
            coordenada=coordenada+" D"+str(self.dgprf)
        if self.eg!=self.egprf:
            coordenada=coordenada+" E"+str(self.egprf)
        if self.fg!=self.fgprf:
            coordenada=coordenada+" F"+str(self.fgprf)
        coordenada="G1"+str(coordenada)+"\n"
        archivo=open(self.filename,"r")
        contenido=archivo.read()
        final_de_archivo=archivo.tell()
        archivo=open(self.filename,"r+")
        archivo.seek(final_de_archivo)
        archivo.write(coordenada)
        
        #nuevo_contenido=archivo.read()
        #print nuevo_contenido
        self.xg=self.xgprf
        self.yg=self.ygprf
        self.zg=self.zgprf
        self.cg=self.cgprf
        self.dg=self.dgprf
        self.eg=self.egprf
        self.fg=self.fgprf
    def mspeed(self):
        self.velocidadg=self.velocidadg+10
        if self.velocidadg > 500:
            self.velocidadg=500
        self.fgprf=self.velocidadg
    def lspeed(self):
        self.velocidadg=self.velocidadg-10
        if self.velocidadg<1:
            self.velocidadg=1
        self.fgprf=self.velocidadg
    def mdistance(self):
        self.avanceg=self.avanceg+0.1
    def ldistance(self):
        self.avanceg=self.avanceg-0.1
        if self.avanceg<0.05:
            self.avance=0.05
    def pup(self):
        if self.conectado1==1:
            self.zgprf=self.zgpri-self.avanceg
            self.widget.reviewEdit.setText( "Arriba")
            av2=int(self.avanceg*400)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.zgpri=self.zgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def pdown(self):
        if self.conectado1==1:
            self.zgprf=self.zgpri+self.avanceg
            self.widget.reviewEdit.setText( "Abajo")
            av2=int(self.avanceg*400)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000004"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.zgpri=self.zgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def pright(self):
        if self.conectado1==1:
            self.ygprf=self.ygpri+self.avanceg
            self.widget.reviewEdit.setText( "Derecha")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000000000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.ygpri=self.ygprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def pleft(self):
        if self.conectado1==1:
            self.ygprf=self.ygpri-self.avanceg
            self.widget.reviewEdit.setText( "Izquierda")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000000000000000002"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.ygpri=self.ygprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def pfoward(self):
        if self.conectado1==1:
            self.xgprf=self.xgpri+self.avanceg
            self.widget.reviewEdit.setText( "Adelante")
            av2=int(self.avanceg*400)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000000000000000000000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.xgpri=self.xgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def pbackward(self):
        if self.conectado1==1:
            self.xgprf=self.xgpri-self.avanceg
            self.widget.reviewEdit.setText( "Atrás")
            av2=int(self.avanceg*400)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000000000000000000000000000000000000001"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.xgpri=self.xgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def tfoward(self):
        if self.conectado1==1:
            self.cgprf=self.cgpri+self.avanceg
            self.widget.reviewEdit.setText( "Griper Adelante")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000008"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.cgpri=self.cgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def tbackward(self):
        if self.conectado1==1:
            self.cgprf=self.cgpri-self.avanceg
            self.widget.reviewEdit.setText( "Griper Atrás")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.cgpri=self.cgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def tright(self):
        if self.conectado1==1:
            self.dgprf=self.dgpri+self.avanceg
            self.widget.reviewEdit.setText( "Gira derecha")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"10"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.dgpri=self.dgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def tleft(self):
        if self.conectado1==1:
            self.dgprf=self.dgpri-self.avanceg
            self.widget.reviewEdit.setText( "Gira izquierda")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.dgpri=self.dgprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def topen(self):
        if self.conectado1==1:
            self.egprf=self.egpri-self.avanceg
            self.widget.reviewEdit.setText( "Abre")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000000"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.egpri=self.egprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    def tclose(self):
        if self.conectado1==1:
            self.egprf=self.egpri+self.avanceg
            self.widget.reviewEdit.setText( "Cierra")
            av2=int(self.avanceg*80)
            Tt=self.avanceg/self.velocidadg
            t=int(2000000*Tt/av2)
            t=hex(t).split('x')[-1]
            j=6-len(t)
            av2=hex(av2).split('x')[-1]
            k=6-len(str(av2))
            griper=serial.Serial(str(self.puerto1), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0a000000000000000000000000000000000000000000000000"+k*"0"+str(av2)+j*"0"+str(t)+"00000000000020"
            griper.write(ins)
            time.sleep(0.01)
            r=""
            r=griper.read()  
            griper.close()
            self.egpri=self.egprf
        else:
            self.widget.reviewEdit.setText("Connect pick and place")
    
    def init1UI(self):               
        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()
        ##############BOTONES###############
        self.widget3.conect= QtGui.QPushButton('')
        self.widget3.conect.clicked.connect(self.conect)
        self.widget3.conect.setIcon(QtGui.QIcon('exit.png'))
        self.widget3.conect.setIconSize(QtCore.QSize(24,24))
        self.widget3.saver= QtGui.QPushButton('')
        self.widget3.saver.clicked.connect(self.saver)
        self.widget3.saver.setIcon(QtGui.QIcon('guardar.png'))
        self.widget3.saver.setIconSize(QtCore.QSize(24,24))
        self.widget3.mspeed= QtGui.QPushButton('F')
        self.widget3.mspeed.clicked.connect(self.mspeed)
        self.widget3.mspeed.setIcon(QtGui.QIcon('arriba.png'))
        self.widget3.mspeed.setIconSize(QtCore.QSize(24,24))
        self.widget3.lspeed= QtGui.QPushButton('S')
        self.widget3.lspeed.clicked.connect(self.lspeed)
        self.widget3.lspeed.setIcon(QtGui.QIcon('abajo.png'))
        self.widget3.lspeed.setIconSize(QtCore.QSize(24,24))
        self.widget3.mdistance= QtGui.QPushButton('M')
        self.widget3.mdistance.clicked.connect(self.mdistance)
        self.widget3.mdistance.setIcon(QtGui.QIcon('arriba.png'))
        self.widget3.mdistance.setIconSize(QtCore.QSize(24,24))
        self.widget3.ldistance= QtGui.QPushButton('L')
        self.widget3.ldistance.clicked.connect(self.ldistance)
        self.widget3.ldistance.setIcon(QtGui.QIcon('abajo.png'))
        self.widget3.ldistance.setIconSize(QtCore.QSize(24,24))
        
        
        self.widget3.pfoward= QtGui.QPushButton('')
        self.widget3.pfoward.clicked.connect(self.pfoward)
        self.widget3.pfoward.setIcon(QtGui.QIcon('adelante.png'))
        self.widget3.pfoward.setIconSize(QtCore.QSize(48,48))
        
        self.widget3.pbackard= QtGui.QPushButton('')
        self.widget3.pbackard.clicked.connect(self.pbackward)
        self.widget3.pbackard.setIcon(QtGui.QIcon('atras.png'))
        self.widget3.pbackard.setIconSize(QtCore.QSize(48,48))
        
        self.widget3.tfoward= QtGui.QPushButton('T')
        self.widget3.tfoward.clicked.connect(self.tfoward)
        self.widget3.tfoward.setIcon(QtGui.QIcon('adelante.png'))
        self.widget3.tfoward.setIconSize(QtCore.QSize(48,48))
        
        self.widget3.tbackard= QtGui.QPushButton('T')
        self.widget3.tbackard.clicked.connect(self.tbackward)
        self.widget3.tbackard.setIcon(QtGui.QIcon('atras.png'))
        self.widget3.tbackard.setIconSize(QtCore.QSize(48,48))

        self.widget3.pup= QtGui.QPushButton('')
        self.widget3.pup.clicked.connect(self.pup)
        self.widget3.pup.setIcon(QtGui.QIcon('arriba.png'))
        self.widget3.pup.setIconSize(QtCore.QSize(48,48))
        self.widget3.pdown= QtGui.QPushButton('')
        self.widget3.pdown.clicked.connect(self.pdown)
        self.widget3.pdown.setIcon(QtGui.QIcon('abajo.png'))
        self.widget3.pdown.setIconSize(QtCore.QSize(48,48))

        self.widget3.pright= QtGui.QPushButton('')
        self.widget3.pright.clicked.connect(self.pright)
        self.widget3.pright.setIcon(QtGui.QIcon('derecha.png'))
        self.widget3.pright.setIconSize(QtCore.QSize(48,48))
        
        self.widget3.pleft= QtGui.QPushButton('')
        self.widget3.pleft.clicked.connect(self.pleft)
        self.widget3.pleft.setIcon(QtGui.QIcon('izquierda.png'))
        self.widget3.pleft.setIconSize(QtCore.QSize(48,48))

        self.widget3.topen= QtGui.QPushButton('')
        self.widget3.topen.clicked.connect(self.topen)
        self.widget3.topen.setIcon(QtGui.QIcon('abrir.png'))
        self.widget3.topen.setIconSize(QtCore.QSize(24,24))
        self.widget3.tclose= QtGui.QPushButton('')
        self.widget3.tclose.clicked.connect(self.tclose)
        self.widget3.tclose.setIcon(QtGui.QIcon('cerrar.png'))
        self.widget3.tclose.setIconSize(QtCore.QSize(24,24))

        self.widget3.tright= QtGui.QPushButton('')
        self.widget3.tright.clicked.connect(self.tright)
        self.widget3.tright.setIcon(QtGui.QIcon('undo.png'))
        self.widget3.tright.setIconSize(QtCore.QSize(24,24))
        
        self.widget3.tleft= QtGui.QPushButton('')
        self.widget3.tleft.clicked.connect(self.tleft)
        self.widget3.tleft.setIcon(QtGui.QIcon('redo.png'))
        self.widget3.tleft.setIconSize(QtCore.QSize(24,24))

        self.widget3.phome= QtGui.QPushButton('')
        self.widget3.phome.clicked.connect(self.phome)
        self.widget3.phome.setIcon(QtGui.QIcon('home.png'))
        self.widget3.phome.setIconSize(QtCore.QSize(48,48))
        ####################################
        
        ####################################
        #grafico=self.grafico.makeObject()
        self.xSlider.valueChanged.connect(self.grafico.setXRotation)
        self.grafico.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.grafico.setYRotation)
        self.grafico.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.grafico.setZRotation)
        self.grafico.zRotationChanged.connect(self.zSlider.setValue)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(345 * 16)
        self.zSlider.setValue(0 * 16)
        grid = QtGui.QGridLayout()
        grid1 = QtGui.QGridLayout()
        grid2 = QtGui.QGridLayout()
        grid3 = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid1.setSpacing(10)
        grid2.setSpacing(10)
        #grid3.setSpacing(10)
        grid.addWidget(self.grafico,0,1,2,1)
        grid.addWidget(self.control,0,2,2,4)
        grid1.addWidget(self.xSlider,0,1,2,1)
        grid1.addWidget(self.ySlider,0,2,2,3)
        grid1.addWidget(self.zSlider,0,3,2,3)
        
        grid2.addWidget(self.widget3.conect,0,0,1,1)
        grid2.addWidget(self.widget3.mspeed,0,2,1,2)
        grid2.addWidget(self.widget3.mdistance,0,4,1,4)
        grid2.addWidget(self.widget3.saver,2,0,3,1)
        grid2.addWidget(self.widget3.lspeed,2,2,3,2)
        grid2.addWidget(self.widget3.ldistance,2,4,3,4)

        grid2.addWidget(self.widget3.pfoward,4,0,5,1)
        grid2.addWidget(self.widget3.pup,4,2,5,2)
        grid2.addWidget(self.widget3.tfoward,4,4,5,4)
        
        grid2.addWidget(self.widget3.pleft,6,0,7,1)
        grid2.addWidget(self.widget3.phome,6,2,7,2)
        grid2.addWidget(self.widget3.pright,6,4,7,4)

        grid2.addWidget(self.widget3.tbackard,8,0,9,1)
        grid2.addWidget(self.widget3.pdown,8,2,9,2)
        grid2.addWidget(self.widget3.pbackard,8,4,9,4)

        grid2.addWidget(self.widget3.topen,10,0,11,1)
        
        grid2.addWidget(self.widget3.tclose,10,4,11,4)

        grid2.addWidget(self.widget3.tleft,12,0,13,1)
        
        grid2.addWidget(self.widget3.tright,12,4,13,4)
        
        self.widget1.setLayout(grid)
        self.widget2.setLayout(grid1)
        self.widget3.setLayout(grid2)
        self.widget4.setLayout(grid3)
    def createSlider(self):
        slider = QtGui.QSlider(QtCore.Qt.Vertical)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QtGui.QSlider.TicksRight)
        return slider
    def sending(self,recivedEdit):
        C=self.recivedEdit.text()
        self.sendEdit.setText(C)
        
        valores="1 %d%d %d%d %d%d 4"%(int(C[0]),int(C[1]),int(C[3]),int(C[4]),int(C[6]),int(C[7]))
        str(valores)
        
        line_1=valores+'\n'
        self.textEdit.setText(self.line+line_1)
        self.line=self.line+line_1
#        try:
#            S=serial.Serial(0,9600)
#        except:
#            self.reviewEdit.setText('Error: Robot no conectado')
        for i in [0,2,3,5,6,8,9,11]:
            S=serial.Serial(0,9600)
#            print valores[i]
            S.write(valores[i])
            S.close()
        self.reviewEdit.setText('Enviado')                    

                       
    def gohome(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 38400, timeout=10,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0500000000000000000000000000000000000000000000000000"
            impresora.write(ins)
            time.sleep(5)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Posicion en Home")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
    def docopy(self):
        self.textEdit.copy()
    def dopaste(self):
        self.textEdit.paste()
    def docut(self):
        self.textEdit.cut()
    def doundo(self):
        self.textEdit.undo()
    def doredo(self):
        self.textEdit.redo()
    def new(self):
        condicion=0
        self.textEdit.clear()
        self.filename = ""
    def showopen(self,filename):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.gcode)")
        if self.filename:
            with open(self.filename,"r") as file:
                a=0
                for line in file:
                    self.arvivo=self.arvivo+line
                    a=a+1
                    if a==100:
                        break
                self.widget.textEdit.setText(self.arvivo)
    def save(self,filename):
        if  not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File',".","(*.gcode)")
        
        with open(self.filename,"w") as file:
            file.write(self.textEdit.toPlainText())
            file.close()

    def saveas(self,filename_1):
        self.filename_1 = QtGui.QFileDialog.getSaveFileName(self, 'Save File as',".","(*.gcode)")
        with open(self.filename_1,"w") as file:
            file.write(self.textEdit.toPlainText())
            file.close()
    def interprete(self):
        xsteps=0
        ysteps=0
        zsteps=0
        esteps=0
        x=0.0
        y=0.0
        z=0.0
        e=0.0
        direccion=0
        hexa=("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
        while self.start==1:
            
            while self.interpretador==1:
                if not self.filename:
                    self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.gcode)")
                with open(self.filename,"r") as file:
                    if self.conectado==1:
                        impresora=serial.Serial(str(self.puerto), 115200, timeout=20,parity=serial.PARITY_EVEN, rtscts=1)
                        griper=serial.Serial(str(self.puerto1), 115200, timeout=20,parity=serial.PARITY_EVEN, rtscts=1)
                    else:
                        break
                    num=0
                    for line in file:
                        linea=str(line)
            
                        try:
                            if self.interpretador==0:
                                self.conter=self.contadordelinea
                                self.contadordelinea=0
                                if self.parar==0:
                                        self.conter=0
                                ##print self.conter
                                break
                            elif self.contadordelinea < self.conter:
                                self.contadordelinea= self.contadordelinea+1
                                pass
                            elif linea[0] == ";":
                                self.contadordelinea= self.contadordelinea+1
                                print "Comentario"
                            elif linea[0]+linea[1]+linea[2] == "G21":
                                self.contadordelinea= self.contadordelinea+1
                                print "Unidades en milimetros"
                            elif linea[0]+linea[1]+linea[2] == "M06":
                                print "Cambio de herramienta"
                                if self.herramienta==0:
                                    print "Cambio de herramienta a griper"
                                    self.herramienta=1
                                    self.pos3_i=0.0 
                                    self.pos4_i=0.0 
                                    self.pos1g_i=0.0
                                    self.pos2g_i=0.0
                                    self.pos3g_i=0.0
                                    self.pos4g_i=0.0
                                    self.pos5g_i=0.0
                                    self.pos6g_i=0.0
                                    x=0.0 
                                    y=0.0
                                    z=0.0
                                    c=0.0
                                    d=0.0
                                    e=0.0
                                    f=0.0
                                else:
                                    print "Cambio de herramienta a impresora"
                                    self.herramienta=0
                                self.contadordelinea= self.contadordelinea+1
                            elif linea[0]+linea[1]+linea[2]+linea[3] == "M107":
                                self.contadordelinea= self.contadordelinea+1
                            elif linea[0]+linea[1]+linea[2]+linea[3] == "M190":
                                self.contadordelinea= self.contadordelinea+1
                                print "La temperatura de la cama de impresion es: "+str(line[6]+line[7]+line[8])
                            elif linea[0]+linea[1]+linea[2]+linea[3] == "M104":
                                self.contadordelinea= self.contadordelinea+1
                                print "La temperatura de la boquilla de impresion es: "+str(line[6]+line[7]+line[8])
                            elif linea[0]+linea[1]+linea[2] == "G28":
                                self.contadordelinea= self.contadordelinea+1
                                if self.herramienta==0:
                                    print "Home"
                                    self.pos1_i=0
                                    self.pos2_i=-30
                                    self.pos3_i=0
                                    self.pos4_i=0
                                    ins="0500000000000000000000000000000000000000000000000000"
                                    impresora.write(ins)
                                    time.sleep(20)
                                    r=""
                                    r=impresora.read()
                                    if r=="1":
                                        self.widget.reviewEdit.setText("Posicion en Home")   
                                    print "Ready"
                                else:
                                    self.pos1g_i=0
                                    self.pos2g_i=0
                                    self.pos3g_i=0
                                    self.pos4g_i=0
                                    self.pos5g_i=0
                                    self.pos6g_i=0
                                    ins="0500000000000000000000000000000000000000000000000000000000000000000000000000"
                                    griper.write(ins)
                                    time.sleep(30)
                                    r=""
                                    r=griper.read()
                                    if r=="1":
                                        self.widget.reviewEdit.setText("Posicion en Home")   
                                    print "Ready"
                                    
                            elif linea[0]+linea[1]+linea[2]+linea[3] == "M109":
                                self.contadordelinea= self.contadordelinea+1
                                print " Aguanta la riata hasta que alcance los " +line[6]+line[7]+line[8] + " grados " 
                            elif linea[0]+linea[1]+linea[2] == "G90":
                                self.contadordelinea= self.contadordelinea+1
                                print "Coordenadas absolutas"
                            elif linea[0]+linea[1]+linea[2] == "G92":
                                self.pos4_i=0
                                e=0
                                print "Reset extrusor"
                                self.contadordelinea= self.contadordelinea+1
                                
                            elif linea[0]+linea[1]+linea[2] == "M82":
                                self.contadordelinea= self.contadordelinea+1
                                print "Distancias absolutas para el extrusor"
                            elif linea[0]+linea[1]== "G1":
                                #print str(linea)
                                if self.herramienta==0:
                                    self.contadordelinea= self.contadordelinea+1
                                    for i in range(len(linea)):
                                        if linea[i]=='X':
                                            x=self.identer(linea,i)
                                        elif linea[i]=='Y':
                                            y=self.identer(linea,i) 
                                        elif linea[i]=='Z':
                                            z=self.identer(linea,i)
                                            print z
                                        elif linea[i]=='E':
                                            e=self.identer(linea,i)
                                        elif linea[i]=='F':
                                            f=self.identer(linea,i)
                                            fast=int(f/4)
                                            if fast > 350:
                                                fast=350
                                        else:
                                            pass
                                    
                                    avance1=float(x)-float(self.pos1_i)
                                    avance2=float(y)-float(self.pos2_i)
                                    avance3=float(z)-float(self.pos3_i)
                                    avance4=float(e)-float(self.pos4_i)
                                    paso=80.0
                                    av1=int(avance1*paso)
                                    av2=int(avance2*paso)
                                    av3=int(avance3*400)
                                    av4=int(avance4*1.0*paso)
                                    self.pos1_i=float(self.pos1_i+float(av1)/paso)
                                    self.pos2_i=float(self.pos2_i+float(av2)/paso)
                                    self.pos3_i=float(self.pos3_i+float(av3)/400)
                                    self.pos4_i=float(self.pos4_i+float(av4)/(1.0*paso))
                                    
                                    
                                    aa=(avance1)*(avance1)
                                    bb=(avance2)*(avance2)
                                    cc=(avance3)*(avance3)
                                    
                                    distancia=math.sqrt(aa+bb+cc)
                                    Tt=distancia/fast
                                    cadena="0a"
                                    #print "X"+str(x)+"Y"+str(y)+"Z"+str(z)+"F"+str(fast)
                                    #print "X"+str(float(self.pos1_i))+"Y"+str(float(self.pos2_i))+"Z"+str(float(self.pos3_i))
                                    if av1!=0:
                                        if av1 < 0:
                                            av1=av1*(-1)
                                            direccion= direccion & 14
                                        else:
                                            direccion= direccion | 1
                                        t=int(2000000*Tt/av1)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av1=hex(av1).split('x')[-1]
                                        k=6-len(str(av1))
                                        cadena=cadena+k*"0"+str(av1)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av2!=0:
                                        if av2 < 0:
                                            av2=av2*(-1)
                                            direccion= direccion & 13
                                        else:
                                            direccion= direccion | 2
                                        t=int(2000000*Tt/av2)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av2=hex(av2).split('x')[-1]
                                        k=6-len(str(av2))
                                        cadena=cadena+k*"0"+str(av2)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av3!=0:
                                        if av3 < 0:
                                            av3=av3*(-1)
                                            direccion= direccion & 11
                                        else:
                                            direccion= direccion | 4
                                        t=int(2000000*Tt/av3)
                                        if t<120:
                                            t=120
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av3=hex(av3).split('x')[-1]
                                        k=6-len(str(av3))
                                        cadena=cadena+k*"0"+str(av3)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av4!=0:
                                        if av4 < 0:
                                            av4=av4*(-1)
                                            direccion= direccion & 7
                                        else:
                                            direccion= direccion | 8
                                        t=int(2000000*Tt/av4)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av4=hex(av4).split('x')[-1]
                                        k=6-len(str(av4))
                                        cadena=cadena+k*"0"+str(av4)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    direccion=int(direccion)    
                                    dr=hexa[direccion]
                                    cadena=cadena+"0"+dr
                                    #print cadena
                                    impresora.write(cadena)
                                    s=impresora.read()
                                    print s
                                else:
                                    self.contadordelinea= self.contadordelinea+1
                                    for i in range(len(linea)):
                                        if linea[i]=='X':
                                            x=self.identer(linea,i)
                                        elif linea[i]=='Y':
                                            y=self.identer(linea,i) 
                                        elif linea[i]=='Z':
                                            z=self.identer(linea,i)
                                        elif linea[i]=='C':
                                            c=self.identer(linea,i)
                                        elif linea[i]=='D':
                                            d=self.identer(linea,i)
                                        elif linea[i]=='E':
                                            e=self.identer(linea,i)
                                        elif linea[i]=='F':
                                            f=self.identer(linea,i)
                                            fast=int(f)
                                            if fast > 580:
                                                fast=580
                                        else:
                                            pass
                                    
                                    avance1=float(x)-float(self.pos1g_i)
                                    avance2=float(y)-float(self.pos2g_i)
                                    avance3=float(z)-float(self.pos3g_i)
                                    avance4=float(c)-float(self.pos4g_i)
                                    avance5=float(d)-float(self.pos5g_i)
                                    avance6=float(e)-float(self.pos6g_i)
                                    paso=80.0
                                    av1=int(avance1*400)
                                    av2=int(avance2*80)
                                    av3=int(avance3*400)
                                    av4=int(avance4*80)
                                    av5=int(avance5*400)
                                    av6=int(avance6*80)
                                      
                                    self.pos1g_i=float(self.pos1g_i+float(av1)/400)#X
                                    self.pos2g_i=float(self.pos2g_i+float(av2)/80) #Y
                                    self.pos3g_i=float(self.pos3g_i+float(av3)/400)#Z
                                    self.pos4g_i=float(self.pos4g_i+float(av4)/80) #C
                                    self.pos5g_i=float(self.pos5g_i+float(av5)/400)#D
                                    self.pos6g_i=float(self.pos6g_i+float(av6)/80) #E
                                    #print "X"+str(x)+"Y"+str(y)+"Z"+str(z)+"F"+str(fast)    
                                      
                                    aa=(avance1)*(avance1)
                                    bb=(avance2)*(avance2)
                                    cc=(avance3)*(avance3)
                                    dd=(avance4)*(avance4)
                                        
                                    distancia=math.sqrt(aa+bb+cc+dd)
                                    Tt=distancia/fast
                                    cadena="0a"
                                    direccion1=0
                                    
                                    #print "X"+str(float(self.pos1_i))+"Y"+str(float(self.pos2_i))+"Z"+str(float(self.pos3_i))
                                    if av1!=0:
                                        if av1 > 0:
                                            av1=av1*(-1)
                                            direccion= direccion & 14
                                        else:
                                            direccion= direccion | 1
                                        t=int(2000000*Tt/av1)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av1=hex(av1).split('x')[-1]
                                        k=6-len(str(av1))
                                        cadena=cadena+k*"0"+str(av1)+j*"0"+str(t)
                                    else:
                                         cadena=cadena+12*"0"
                                    if av2!=0:
                                        if av2 > 0:
                                            av2=av2*(-1)
                                            direccion= direccion & 13
                                        else:
                                            direccion= direccion | 2
                                        t=int(2000000*Tt/av2)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av2=hex(av2).split('x')[-1]
                                        k=6-len(str(av2))
                                        cadena=cadena+k*"0"+str(av2)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av3!=0:
                                        if av3 < 0:
                                            av3=av3*(-1)
                                            direccion= direccion & 11
                                        else:
                                            direccion= direccion | 4
                                        t=int(2000000*Tt/av3)
                                        if t<120:
                                            t=120
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av3=hex(av3).split('x')[-1]
                                        k=6-len(str(av3))
                                        cadena=cadena+k*"0"+str(av3)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av4!=0:
                                        if av4 < 0:
                                            av4=av4*(-1)
                                            direccion= direccion & 7
                                        else:
                                            direccion= direccion | 8
                                        t=int(2000000*Tt/av4)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av4=hex(av4).split('x')[-1]
                                        k=6-len(str(av4))
                                        cadena=cadena+k*"0"+str(av4)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av6!=0:
                                        distancia=avance6
                                        Tt=(4*distancia)/fast
                                        if av6 < 0:
                                            av6=av6*(-1)
                                            direccion1= direccion1 & 13
                                        else:
                                            direccion1= direccion1 | 2
                                        t=int(2000000*Tt/av6)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av6=hex(av6).split('x')[-1]
                                        k=6-len(str(av6))
                                        cadena=cadena+k*"0"+str(av6)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    if av5!=0:
                                        distancia=avance5
                                        Tt=(4*distancia)/fast
                                        if av5 < 0:
                                            av5=av5*(-1)
                                            direccion1= direccion1 & 14
                                        else:
                                            direccion1= direccion1 | 1
                                        t=int(2000000*Tt/av5)
                                        t=hex(t).split('x')[-1]
                                        j=6-len(t)
                                        av5=hex(av5).split('x')[-1]
                                        k=6-len(str(av5))
                                        cadena=cadena+k*"0"+str(av5)+j*"0"+str(t)
                                    else:
                                        cadena=cadena+12*"0"
                                    
                                    direccion=int(direccion)    
                                    dr=hexa[direccion]
                                    direccion1=int(direccion1)    
                                    dr1=hexa[direccion1]
                                    cadena=cadena+dr1+dr
                                    print cadena
                                    griper.write(cadena)
                                    s=griper.read()
                                    print s
                            else:
                                self.contadordelinea= self.contadordelinea+1
                                
                        except:
                            self.contadordelinea= self.contadordelinea+1
                print "Ya esta"
                impresora.close()
                griper.close()
                file.close
                self.pos1_i=0
                self.pos2_i=0
                self.pos3_i=0
                self.pos4_i=0
                self.pos1g_i=0
                self.pos2g_i=0
                self.pos3g_i=0
                self.pos4g_i=0
                self.pos1g_i=0
                self.pos2g_i=0
                self.interpretador=0
    def identer(self,linea,i):
        x=""
        numero=range(10)
        for l in range(i+1,len(linea)):
            if linea[l]!=' ':
                x=x+linea[l]
            else:
                break
        x=float(x)
        return x
    def play(self):
        self.papar=1
        self.interpretador=1              
    def stop(self):
        self.interpretador=0
        self.parar=0
    def foward(self):
        self.Xr=5.0
        self.Yr=0.0
        self.Zr=0.0
        self.xmas=1
    def x_mas(self):
        while self.start==1:
            while self.xmas==1:
                dx=self.Xr-self.px
                dy=self.Yr-self.py
                dz=self.Zr-self.pz
                fragmentos=int(math.sqrt((dx*dx)+(dy*dy)+(dz*dz))/0.1)
                self.tiempo=(math.sqrt((dx*dx)+(dy*dy)+(dz*dz))/1.0)/fragmentos
                self.iteraciones=-1
                for i in range(fragmentos):
                    self.x=((1+i)*(dx/fragmentos))+self.px
                    self.y=((1+i)*(dy/fragmentos))+self.py
                    self.z=((1+i)*(dz/fragmentos))+self.pz
                    self.cinematica_inversa()
                    self.posisiones1[i]=self.distancia_1
                    self.posisiones2[i]=self.distancia_2
                    self.posisiones3[i]=self.distancia_3
                    self.posisiones4[i]=self.distancia_4
                    self.iteraciones=self.iteraciones+1
                for j in range(self.iteraciones):
                    self.distancia_1=self.posisiones1[j]
                    self.distancia_2=self.posisiones2[j]
                    self.distancia_3=self.posisiones3[j]
                    self.distancia_4=self.posisiones4[j]
                    self.mot1=1
                    self.mot2=1
                    self.mot3=1
                    self.mot4=1
                    self.ejecutar=1
                    while  self.mot1==1 or  self.mot2==1 or  self.mot3==1 or self.mot4==1:
                        pass
                self.px=self.Xr
                self.py=self.Yr
                self.pz=self.Zr
                self.xmas=0
    def cinematica_inversa(self):
        pi=3.14159
        x1= self.y*math.sin(0)+self.x*math.cos(0)
        y1= self.y*math.cos(0)-self.x*math.sin(0)
        x2= self.y*math.sin(pi/2)+self.x*math.cos(pi/2)
        y2= self.y*math.cos(pi/2)-self.x*math.sin(pi/2)
        x3= self.y*math.sin(pi)+self.x*math.cos(pi)
        y3= self.y*math.cos(pi)-self.x*math.sin(pi)
        x4= self.y*math.sin(3*(pi/2))+self.x*math.cos(3*(pi/2))
        y4= self.y*math.cos(3*(pi/2))-self.x*math.sin(3*(pi/2))
        alfa1=math.sqrt((((self.LA-self.LB+x1)*(self.LA-self.LB+x1))+(y1*y1)))/(self.L1)
        alfa1=math.asin(alfa1)
        self.distancia_1= self.LE+self.z+(self.L1*math.cos(alfa1))
        alfa2=math.asin(math.sqrt((((self.LA-self.LB+x2)*(self.LA-self.LB+x2))+(y2*y2)))/self.L1)
        self.distancia_2= self.LE+self.z+(self.L1*math.cos(alfa2))
        alfa3=math.asin(math.sqrt((((self.LA-self.LB+x3)*(self.LA-self.LB+x3))+(y3*y3)))/self.L1)
        self.distancia_3= self.LE+self.z+(self.L1*math.cos(alfa3))
        alfa4=math.asin(math.sqrt((((self.LA-self.LB+x4)*(self.LA-self.LB+x4))+(y4*y4)))/self.L1)
        self.distancia_4= self.LE+self.z+(self.L1*math.cos(alfa4))

    def cerrar(self):
        mensage=""
        mensage1=""
        for i in range(3,10):
            try:
                if "COM"+str(i)!= self.puerto1 or self.puerto=="":
                    impresora=serial.Serial('COM'+str(i), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
                    impresora.write("0100000000000000000000000000000000000000000000000000")
                    printer=impresora.read(15)
                    if printer=="Impresora      ":
                        if self.conectado==1:
                            self.conectado=0
                            mensage="Impresora desconectada"
                            
                        else:
                            self.conectado=1
                            self.puerto=impresora.name
                            mensage="Impresora conectada en "+str(self.puerto)
                            
                    impresora.close()
                    break
                else:
                    pass
            except:
                pass
        for i in range(4,10):
            try:
                if "COM"+str(i)!= self.puerto and self.puerto!="":
                    griper=serial.Serial('COM'+str(i), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
                    griper.write("0100000000000000000000000000000000000000000000000000000000000000000000000000")
                    griper=griper.read(15)
                    if griper=="Griper         ":
                        if self.conectado1==1:
                            self.conectado1=0
                            mensage1=" Griper desconectado"
                            
                        else:
                            self.conectado1=1
                            self.puerto1="COM"+str(i)
                            mensage1=", Griper conectado en "+str(self.puerto1)
                    griper.close()
                    break
                else:
                    pass
            except:
                pass
        mensage=str(mensage)+str(mensage1)
        self.widget.reviewEdit.setText(str(mensage))
        
    def pause(self):
        self.parar=1
        self.interpretador=0
    def moveright(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0600000000000000000000000000000000000000000000000001"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")  
    def moveleft(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto),115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0600000000000000000000000000000000000000000000000000"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
    def movefoward(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0700000000000000000000000000000000000000000000000002"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
    def movebehind(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0700000000000000000000000000000000000000000000000000"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
    def moveup(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0800000000000000000000000000000000000000000000000004"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
    def movedown(self):
        if self.conectado==1:
            impresora=serial.Serial(str(self.puerto), 115200, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
            ins="0800000000000000000000000000000000000000000000000000"
            impresora.write(ins)
            time.sleep(0.01)
            r=""
            r=impresora.read()
            if r=="1":
                self.widget.reviewEdit.setText("Acaba")   
            impresora.close()
        else:
            self.widget.reviewEdit.setText("Impresora no conectada")
class GLWidget(QtOpenGL.QGLWidget):
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)
    GL_MULTISAMPLE = 0x809D
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.22, 0.22,0.01, 0.0)
        
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(500, 500)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def initializeGL(self):
        light_ambient = (0.0, 0.0, 0.0, 1.0 )
        light_diffuse = (1.0, 1.0, 1.0, 1.0 )
        light_specular = ( 1.0, 1.0, 1.0, 1.0 )
        light_position = ( 150.0, -150.0, 1.0, 1000.0 )
        mat_specular=(0.0,0.0,0.9,1.0)
        mat_shininess=5.0
        no_mat= (0.0, 0.0, 0.0, 1.0)
        mat_ambient= ( 0.7, 0.7, 0.7, 1.0 )
        mat_ambient_color= ( 0.8, 0.8, 0.2, 1.0 )
        mat_diffuse= ( 0.1, 0.5, 0.8, 1.0 )
        mat_specular = ( 1.0, 1.0, 1.0, 1.0 )
        no_shininess= ( 0.0 )
        low_shininess= ( 5.0 )
        high_shininess= ( 100.0 )
        mat_emission= (0.3, 0.2, 0.2, 0.0)
        self.qglClearColor(self.trolltechPurple.dark())#
        #glShadeModel(GL_SMOOTH)
        #glMaterialfv(GL_FRONT,GL_SPECULAR,mat_specular)
        #glMaterialfv(GL_FRONT,GL_SHININESS,mat_shininess)
        #glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
        glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
        glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
        #glLightfv(GL_LIGHT0,GL_AMBIENT, light_ambient)
        #glLightfv(GL_LIGHT0,GL_DIFFUSE, light_diffuse)
        #glLightfv(GL_LIGHT0,GL_SPECULAR, light_specular)
        #glLightfv(GL_LIGHT0,GL_POSITION, light_position)
        #glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0001)
        #glEnable(GL_CULL_FACE)
        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        self.object = self.makeObject()
    def paintGL(self):
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        GL.glEnable(GLWidget.GL_MULTISAMPLE)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 50.0, -35.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)
        glPopMatrix()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) // 2, (height - side) // 2, side, side)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-120, +120, +120, -100,-250,250.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot - 8 * dy)
            self.setYRotation(self.yRot - 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot - 8 * dy)
            self.setZRotation(self.zRot - 8 * dx)

        self.lastPos = event.pos()
    def Area(self,u1,u2,u3,v1,v2,v3,w1,w2,w3):
        dx=v1-u1
        dy=v2-u2
        dz=v3-u3
        a=math.sqrt(dx*dx+dy*dy+dz*dz)
        dx=v1-w1
        dy=v2-w2
        dz=v3-w3
        b=math.sqrt(dx*dx+dy*dy+dz*dz)
        dx=w1-u1
        dy=w2-u2
        dz=w3-u3
        c=math.sqrt(dx*dx+dy*dy+dz*dz)
        theta=math.acos((a*a+b*b-c*c)/(2*a*b))
        h=b*math.sin(theta)
        A=a*h/2
        return A
    def rec(self):
        Ax=0
        Ay=0
        Az=0
        Ao=0
        for triangulo in self.your_mesh.vectors:
            A=self.Area(triangulo[0,0],triangulo[0,1],triangulo[0,2],triangulo[1,0],triangulo[1,1],triangulo[1,2],triangulo[2,0],triangulo[2,1],triangulo[2,2])
            if triangulo[0,0]==triangulo[1,0] and triangulo[0,0]==triangulo[2,0]:
                Ax=Ax+A
            elif triangulo[0,1]==triangulo[1,1] and triangulo[0,1]==triangulo[2,1]:
                Ay=Ay+A
            elif triangulo[0,2]==triangulo[1,2] and triangulo[0,2]==triangulo[2,2]:
                Az=Az+A
            else:
                Ao=Ao+A
        if Ax>Ay and Ax>Az:
            #print 'La cara esta en el plano x'
            self.your_mesh.rotate([0.0, 1.0, 0.0], math.radians(90))
        elif Ay>Ax and Ay>Az:
            #print 'La cara esta en el plano y'
            self.your_mesh.rotate([1.0, 0.0, 0.0], math.radians(90))
        elif Az>Ay and Az>Ax:
            #print 'La cara esta en el plano z'
            #self.your_mesh.rotate([0.0, 1.0, 0.0], math.radians(90))
            pass
        else:
            #print 'La cara esta en un plano desconocido'
            pass
        vectores=self.your_mesh.vectors
        less=vectores[0,0,2]
        for triangulo in self.your_mesh.vectors:
            for vertice in triangulo:
                if vertice[2]<less:
                    less=vertice[2]
                else:
                    pass
        self.your_mesh.z -=less
        volume, cog, inertia = self.your_mesh.get_mass_properties()
        self.your_mesh.x -=cog[0]
        self.your_mesh.y -=cog[1]
    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)
        self.meshname = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.stl)")
        self.your_mesh = mesh.Mesh.from_file(self.meshname)
        self.rec()
        vertices=((100,100,0),(100,-100,0),(-100,-100,0),(-100,100,0))
        lineas=((0,1),(1,2),(2,3),(3,0))
        edges = (
            (0,1),
            (0,2),
            (2,1))
        surface=(0,1,2,3)
        triangulo=(0,1,2)
        glPushMatrix()
        GL.glBegin(GL_LINES)
        for linea in lineas:
            for vertex in linea:
                GL.glColor3fv((0.0,0.0,0.0))
                GL.glVertex3fv(vertices[vertex])
        for i in range(10,100,10):
            GL.glColor3fv((0.1,0.1,0.1))
            GL.glVertex3fv((100,100-i,0))
            GL.glVertex3fv((-100,100-i,0))
        for i in range(0,100,10):
            GL.glColor3fv((0.1,0.1,0.1))
            GL.glVertex3fv((100,-i,0))
            GL.glVertex3fv((-100,-i,0))
        for i in range(10,100,10):
            GL.glColor3fv((0.1,0.1,0.1))
            GL.glVertex3fv((100-i,100,0))
            GL.glVertex3fv((100-i,-100,0))
        for i in range(0,100,10):
            GL.glColor3fv((0.1,0.1,0.1))
            GL.glVertex3fv((-i,100,0))
            GL.glVertex3fv((-i,-100,0))
        GL.glEnd()
        glPopMatrix()
        glPushMatrix()

        GL.glBegin(GL_TRIANGLES)
        for vector in self.your_mesh.vectors:
            for vertex in triangulo:
                GL.glColor3fv((0.0, 0.1, 0.6))
                GL.glVertex3fv(vector[vertex])
        GL.glEnd()
        glPopMatrix()
        
        GL.glEndList()
        return genList

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
def main():
    app = QtGui.QApplication(sys.argv)
    ex = GCODER()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()    
