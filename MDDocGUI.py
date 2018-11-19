#!/usr/bin/python3
# MDDocGUI
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow, QFileDialog, QTableView, QMessageBox
from PyQt5.uic import loadUi
import time
import string
from MDDoc import MDDoc
from subprocess import call
import http.server
import socketserver
# Load paremeters
#import Param
#Param.param.init('H:/cloud/cloud_data/Projects/REFT/Software/GUIApp/REFTCode/init/init.xml')
#Param.param.read()
#Param.param.printParams()

fileDirMDDoc = os.path.dirname(os.path.abspath(__file__))
sys.path.append(fileDirMDDoc + '\\init')
import Param

import threading
from shutil import copyfile, rmtree
from YAML import YAML
#param = Param('H:/cloud/cloud_data/Projects/MDDoc/init/init.xml')
#param.read()


            
class MDDocGUI(QMainWindow):
    
    # Events
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    drawing = None
    orders = None
    params = None
    current_order = None
    milling = None
    doc = MDDoc()
    httpd = None
    doc_exist = False
    doc_open = False
    thread_server = None
    yaml = YAML()
    paramsRestart = dict()   
    ui = None
    
    def __init__(self):
        # Init GUI  
        print('test')
        Param.param.read()
        Param.param.printParams()
        self.params=Param.param.params;
        
        
        print('UIPath: ', self.params['UIPath'])
        UIPath = self.params['UIPath']
        super(MDDocGUI,self).__init__()
        
        self.ui = loadUi(UIPath, self)
        self.setWindowTitle('MDDoc')
        
        # Init parameter
        self.paramsRestart = self.yaml.load(self.params['ParamsRestartPath'])
        self.SourceFolder.setText(self.paramsRestart['SourceFolder'])
        self.DestinationFolder.setText(self.paramsRestart['DestinationFolder'])
        
        # Set callback functions
        self.CreateDocButton.clicked.connect(self.on_CreateDocButton)
        self.StatusLine.append("Initialization started")
        self.SourceButton.clicked.connect(self.on_SourceButton)
        self.DestinationButton.clicked.connect(self.on_DestinationButtonButton)
        
        self.OpenDocButton.clicked.connect(self.on_OpenDocButton)
        self.CloseDocButton.clicked.connect(self.on_CloseDocButton)
        
        
        self.SourceFolder.textChanged.connect(self.on_textChanged_SourceFolder)
        self.DestinationFolder.textChanged.connect(self.on_textChanged_DestinationFolder)
        
        SourceFolder = self.SourceFolder.text()
        DestinationFolder = self.DestinationFolder.text()
        self.doc_exist = os.path.isfile(DestinationFolder + '/index.html')
        
        if (not os.path.isdir(SourceFolder)) or (not os.path.isdir(DestinationFolder)):
            self.CreateDocButton.setEnabled(False)
            
        self.OpenDocButton.setEnabled(self.doc_exist)
        self.CloseDocButton.setEnabled(self.doc_open)
        
        #self.ui.btnExit.clicked.connect(self.close)
        #self.ui.actionExit.triggered.connect(self.close)
        
        #self.milling = Milling.Milling('milling', self.params['DatabaseSQLitePath'])
        #reload(DrawingClass)
        
        # Drawing tab
        #self.LoadOrdersButton.clicked.connect(self.on_LoadOrdersButton)
        #self.CreateDrawingButton.clicked.connect(self.on_CreateDrawingButton)
        #self.OrdersTable.clicked.connect(self.on_clicked_OrdersTable)      
        #self.StatusLine.append("Initialization started")
        
        # Milling tab
        #self.LoadOrdersMillingButton.clicked.connect(self.on_LoadOrdersButton)
        #self.CreateMillingButton.clicked.connect(self.on_clicked_CreateMillingButton)
        #self.OrdersMillingTable.clicked.connect(self.on_clicked_OrdersMillingTable)    
    
    def closeEvent(self, event):
        print("event")
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:         
            self.paramsRestart['SourceFolder'] = self.SourceFolder.text()
            self.paramsRestart['DestinationFolder'] = self.DestinationFolder.text()
            self.yaml.save(self.paramsRestart, self.params['ParamsRestartPath'])
            event.accept()
        else:
            event.ignore()
            
    def serverfunc(self, DestinationFolder):
        os.chdir(DestinationFolder)      
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler      
        with socketserver.TCPServer(("", PORT), Handler) as self.httpd:
            self.httpd.serve_forever()
            self.StatusLine.append('Closing server')
            
    @pyqtSlot()
    def on_textChanged_SourceFolder(self):
        SourceFolder = self.SourceFolder.text()
        DestinationFolder = self.DestinationFolder.text()
        if (not os.path.isdir(SourceFolder)) or (not os.path.isdir(DestinationFolder)):
            self.CreateDocButton.setEnabled(False)
        else:
            self.CreateDocButton.setEnabled(True)
        
    @pyqtSlot()
    def on_textChanged_DestinationFolder(self):
        SourceFolder = self.SourceFolder.text()
        DestinationFolder = self.DestinationFolder.text()
        if (not os.path.isdir(SourceFolder)) or (not os.path.isdir(DestinationFolder)):
            self.CreateDocButton.setEnabled(False)
        else:
            self.CreateDocButton.setEnabled(True)
        self.doc_exist = os.path.isfile(DestinationFolder + '/index.html')
        self.OpenDocButton.setEnabled(self.doc_exist)

        
    @pyqtSlot()
    def on_CloseDocButton(self):
        print('on_CloseDocButton')
        self.httpd.shutdown()
        self.thread_server.join()
        #self.thread_server._stop()
        DestinationFolder = self.DestinationFolder.text()
        self.doc_exist = os.path.isfile(DestinationFolder + '/index.html')
        self.OpenDocButton.setEnabled(self.doc_exist)
        self.doc_open = False
        self.CloseDocButton.setEnabled(self.doc_open)
        
    @pyqtSlot()
    def on_OpenDocButton(self):             
        DestinationFolder = self.DestinationFolder.text()
        if os.path.isdir(DestinationFolder):
            call(["C:/Program Files/Mozilla Firefox/firefox.exe", "-new-window", "http://127.0.0.1:8000/"])  
            self.thread_server = threading.Thread(target=self.serverfunc,args=[self.DestinationFolder.text()])
            self.thread_server.start()
            self.StatusLine.append('Opening server')
            self.doc_open = True
            self.CloseDocButton.setEnabled(self.doc_open)
            self.OpenDocButton.setEnabled(not self.doc_open)
        else:
            self.StatusLine.append('Destination folder not found!')
            self.doc_open = False
            self.CloseDocButton.setEnabled(self.doc_open)

    @pyqtSlot()
    def on_SourceButton(self):        
        self.SourceFolder.setText(str(QFileDialog.getExistingDirectory(self, "Select source folder")))
    
    @pyqtSlot()
    def on_DestinationButtonButton(self):        
        self.DestinationFolder.setText(str(QFileDialog.getExistingDirectory(self, "Select destination folder")))
            
    @pyqtSlot()
    def on_CreateDocButton(self):        
        if self.CopyCheckBox.isChecked():
            # Deep copy
            sourceFolder = self.SourceFolder.text()
            destinationFolder = self.DestinationFolder.text()
            if not sourceFolder:
                self.StatusLine.append("Source folder is not defined!")
                return
            if not destinationFolder:
                self.StatusLine.append("Target folder is not defined!")
                return
            YMlFilepath = self.params['YMLPath']
            created = self.doc.createMKDocs(sourceFolder, destinationFolder, YMlFilepath)
        else:
            # Extract markdown files and copy in tmp folder
            sourceFolder = self.SourceFolder.text()
            destinationFolder = self.DestinationFolder.text()          
            if not sourceFolder:
                self.StatusLine.append("Source folder is not defined!")
                return
            if not destinationFolder:
                self.StatusLine.append("Target folder is not defined!")
                return
            
            num=len(sourceFolder)
            for root, directories, filenames in os.walk(sourceFolder):
                files = [ file for file in filenames if file.endswith( ('.md') ) ]
                for filename in files: 
                    filepath = os.path.join(root,filename)                
                    src = filepath
                    tmp_path = os.path.dirname(sourceFolder) + "/tmp"
                    dst = tmp_path + src[num:]    
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    copyfile(src, dst)
            
            # Shellow copy
            dir_path = os.path.dirname(os.path.realpath(__file__))
            sourceFolder = dir_path + "\\tmp"
            destinationFolder = self.DestinationFolder.text()
            YMlFilepath = self.params['YMLPath']
            created = self.doc.createMKDocs(tmp_path, destinationFolder, YMlFilepath) 
            
            # Delete tmp folder
            if os.path.exists(tmp_path) and os.path.isdir(tmp_path):
                rmtree(tmp_path)
        if created:
            self.StatusLine.append("Documentation creation succeeded.")
            self.doc_exist = True
            self.OpenDocButton.setEnabled(True)
        else:
            self.StatusLine.append("Documentation creation failed.")
            self.doc_exist = False
            self.OpenDocButton.setEnabled(False)
        
    #@pyqtSlot()
    def on_clicked_OrdersMillingTable(self, signal):
        row = signal.row()
        parameter = self.orders[row][2]
        self.updateParameter(parameter)
        self.current_order = self.orders[row]
        
    #@pyqtSlot()
    def on_clicked_OrdersTable(self, signal):
        row = signal.row()
        parameter = self.orders[row][2]
        self.updateParameter(parameter)
        self.current_order = self.orders[row]
    
    @pyqtSlot()
    def on_LoadOrdersButton(self):
    
        print('on_LoadOrdersButton')
        # Init OrdersTable
        self.orders = self.drawing.database.getOrders()
        self.OrdersTable.setSelectionBehavior(QTableView.SelectRows);
        self.OrdersMillingTable.setSelectionBehavior(QTableView.SelectRows);
        self.model = QtGui.QStandardItemModel(parent=self)
        self.model.takeRow
        header = ['OrderID', 'FurnitureID', 'Paremter']
        self.model.setHorizontalHeaderLabels(header)
         
        # Set orders data
        row = 0
        for o in self.orders:
            for column in range(len(header)):
                item = QtGui.QStandardItem()
                item.setText(str(o[column]))
                self.model.setItem(row, column, item)
            row = row + 1
        self.OrdersTable.setModel(self.model)
        self.OrdersMillingTable.setModel(self.model)
    
    @pyqtSlot()
    def on_CreateDrawingButton(self):        
        # Start FreeCAD and open furniture
        furnitureID = self.current_order[0]
        column = 'name'
        furnitureName = self.drawing.database.getFurniture(furnitureID, column)[0][0]
        furnituresPath = self.drawing.database.getParameter('furnituresPath')[0]
        furnitureFilePath = furnituresPath + '/' + furnitureName + '/' + furnitureName + '.FCStd'
        freecadPath = self.params['FreeCADPath']
        self.drawing.startFreecad(furnitureFilePath, freecadPath)
        
    def updateParameter(self, parameter):
        
        # Split milling part names
        self.Parameters.setText('')
        params = parameter.split(",")
        for txt in params:
            txt=txt.replace(" ", "")
            self.Parameters.append(txt)
        
def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True

def startGUI():
    # Start GUI
    app = QApplication(sys.argv)
    widget = MDDocGUI()
    widget.show();
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
    
def main():

    # Start GUI
    startGUI()
    
if __name__ == '__main__':
    main()