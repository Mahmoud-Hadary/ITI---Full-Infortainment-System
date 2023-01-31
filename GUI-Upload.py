import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
import pandas as pd
import xlwt
import os
import openpyxl
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import binascii
import base64

# SENDING IS C5D9F1
# RECIEVING IS E6B8B7
coloumn_count = 0
import json
import requests


def searchFolder(folderName):
    global drive
    response = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in response:
        if (folder['title'] == folderName):
            print("Folder '" + folderName + "' found")
            return folder

    print("Could not find " + folderName)
    exit()
        
def searchFile(Gfilename):
    global drive
    global folder
    file_list = drive.ListFile({'q': "'1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        file_hype = file1['title'].split('v')
        if file_hype[0] ==  Gfilename:
            drive.CreateFile({
                'title': file1['title'],
                'id': file1['id'],
                'parents': [{
                    'kind': 'drive#fileLink', 
                    'id': '1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' 
                    }]}).Delete()

            print('title: %s, id: %s' % (file1['title'], file1['id']))
            version = file_hype[1].split('.')
            version = int(version[0])
            return version
    print("Could not find the file named "+Gfilename)
    exit()
        
class ThirdTabLoads(QWidget):

    def __init__(self, parent=None):
        super(ThirdTabLoads, self).__init__(parent)    
        self.setFixedSize(560,450)
        self.setWindowTitle('Upload')
        self.setWindowIcon(QIcon('download.png'))

        Upload_button = QtWidgets.QPushButton("Upload File")
        
        Save_button = QtWidgets.QPushButton("Save")
        #self.Save_button = QPushButton('&Export',clicked=self.switch_window)
        #layout.addWidget(self.Save_button)
        #Save_button.clicked.connect(table.savefile)  #saves the data and transfers it into an excel sheet then opens a new window

        delete_button = QtWidgets.QPushButton("Delete")

        CON_button = QtWidgets.QPushButton("Encrypt .hex file")
        #CON_button.clicked.connect()
        Upload_button.clicked.connect(self.upload_file)
        CON_button.clicked.connect(self.encrypt_file)


        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(Upload_button, alignment=QtCore.Qt.AlignBottom)
        button_layout.addWidget(delete_button, alignment=QtCore.Qt.AlignTop)
        button_layout.addWidget(Save_button, alignment=QtCore.Qt.AlignBottom)
        try:
            button_layout.addWidget(CON_button, alignment=QtCore.Qt.AlignBottom)
        except:
            QtWidgets.QMessageBox.critical(self, "Invalid Input", "There is nothing to animate yet")
        tablehbox = QtWidgets.QHBoxLayout()
        tablehbox.setContentsMargins(10, 10, 10, 10)
        #tablehbox.addWidget(table)

        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(button_layout, 0, 1)
        grid.addLayout(tablehbox, 0, 0)   
        
             
    def upload_file(self):
        global filename
        global sourceFolder
        global Google_DriveFolder
        filename1,_ = QFileDialog.getOpenFileName(self, 'Single File', sourceFolder , '*.hex')
        filename = filename1.split('/')
        filename = filename[-1]
        file_type=filename.split("v")
        sourceFile = sourceFolder+'/'+ filename
        folder = searchFolder(Google_DriveFolder)
        version = int(file_type[1].split('.')[0])
        print(version)
        print(filename)
        old_version = searchFile("mainApplication")
        if version> old_version:    
            file = drive.CreateFile({
        'title': filename,
        'parents': [{
            'kind': 'drive#fileLink', 
            'id': folder['id'] 
            }]
        })
            file.SetContentFile(sourceFile)
            file.Upload()
            
        else:
            print("You are trying to upload an older version")    
    # Function to browse for a file and encrypt its content
    def encrypt_file():
        # Open file dialog to select a hex file
        with open(filename1, "rb") as f:
            hex_file = f.read()

        # Generate a random key and initialization vector
        key = get_random_bytes(16)
        iv = get_random_bytes(16)

        # Save the key and IV to a secure file
        secure_file_path = "secure_key_and_iv.bin"
        with open(secure_file_path, "wb") as f:
            f.write(key + iv)

        # Encrypt the key and IV
        # Create a new AES-ECB cipher
        cipher = AES.new(key, AES.MODE_ECB)

        # Encrypt the hex file
        hex_file = pad(hex_file, 16)
        ciphertext = cipher.encrypt(hex_file)

        # Save the encrypted data to a new file
        encrypted_file_path = os.path.splitext(filename1)[0] + "_encrypted.bin"
        with open(encrypted_file_path, "wb") as f:
            f.write(ciphertext)
        print(f"File has been encrypted successfully and saved to {encrypted_file_path}")        
            #print(filename)
            #self.QtGui.ui.lineEdit.setText(fileName)

        
        

if __name__ == '__main__':
    filename = ""
    Google_DriveFolder = "FOTA-Version-Control"
    sourceFolder = os.path.expanduser('~')
    print(sourceFolder)
    app = QtWidgets.QApplication(sys.argv)
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    #drive = GoogleDrive(gauth)
    w = ThirdTabLoads()
    w.show()
    sys.exit(app.exec_())