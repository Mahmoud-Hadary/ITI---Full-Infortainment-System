import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
import pandas as pd
import os
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

def encrypt_file(file_path):
    with open(file_path, "rb") as f:
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
    encrypted_file_path =  os.path.splitext(file_path)[0] 
    splited = encrypted_file_path.split("v")[0]
    splited = splited + "_encryptedv"+encrypted_file_path.split("v")[1]+".bin"
    encrypted_file_path = splited
    with open(encrypted_file_path, "wb") as f:
        f.write(ciphertext)
    
    print(f"File has been encrypted successfully and saved to {encrypted_file_path}")   
    return encrypted_file_path    
    
def searchFolder(folderName):
    global drive
    response = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in response:
        if (folder['title'] == folderName):
            print("Folder '" + folderName + "' found")
            return folder

    msg4 = QMessageBox()
    msg4.setWindowTitle("Error")
    msg4.setText("Could not find " + folderName)
    msg4.setIcon(QMessageBox.Critical)
    msg4.exec_()    
    #QWidgets.QMessageBox.Critical(self,"Could not find " + folderName)
    exit()
        
def searchFile(Gfilename):
    global drive
    global folder
    file_list = drive.ListFile({'q': "'1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        file_hype = file1['title'].split('v')
        if file_hype[0] ==  Gfilename:
            version = file_hype[1].split('.')
            version = int(version[0])
            return version
    msg3 = QMessageBox()
    msg3.setWindowTitle("Error")
    msg3.setText("Could not find the file named "+Gfilename)
    msg3.setIcon(QMessageBox.Critical)
    msg3.exec_()        
    #QWidgets.QMessageBox.Critical(self,"Could not find the file named "+Gfilename)
    exit()
def Delete_GFile(Gfilename):
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

            print('title: %s, id: %s and is deleted' % (file1['title'], file1['id']))

class ThirdTabLoads(QWidget):

    def __init__(self, parent=None):
        super(ThirdTabLoads, self).__init__(parent)    
        self.setFixedSize(360,250)
        self.setWindowTitle('Upload')
        self.setWindowIcon(QIcon('upload.png'))
        # Set the background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("background.png")))
        self.setPalette(palette)
        
        # Create a QVBoxLayout
        layout = QVBoxLayout()
        
        # Add widgets to the layout
        Upload_button = QPushButton("Upload File")
        layout.addWidget(Upload_button)
        
        # Set the layout
        self.setLayout(layout)
        
        # Connect the button to the function
        Upload_button.clicked.connect(self.upload_file)
        
        # Add stylesheet
        self.setStyleSheet("""
            QPushButton:hover {
                background-color: red;
            }
            QPushButton {
                background-color: green;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)


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
        old_version = searchFile("mainApplication_encrypted")
        if version> old_version: 
            Delete_GFile("mainApplication_encrypted") 
            if filename1:
                path = encrypt_file(filename1)
                name = path.split("/")
                name = name[-1]
                file = drive.CreateFile({
                'title': name,
                'parents': [{
                'kind': 'drive#fileLink', 
                'id': folder['id'] 
                    }]})
                file.SetContentFile(sourceFile)
                file.Upload()
                msg1 = QMessageBox()
                msg1.setWindowTitle("Uploaded Suceesfully")
                msg1.setText(f"File {name} has been Uploaded successfully and saved to Google Drive")
                msg1.setIcon(QMessageBox.Information)
                msg1.exec_()
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("You are trying to upload an older version.")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()
            #print("You are trying to upload an older version")
            #QWidgets.QMessageBox.Critical(self,"You are trying to upload an older version")    
    # Function to browse for a file and encrypt its content
    
        
        

if __name__ == '__main__':
    filename = ""
    Google_DriveFolder = "FOTA-Version-Control"
    sourceFolder = 'C:/Users/m_god/TOBEOPIED/Mahmoud_HardDRIVE/data/GradProject/ITI_ADAS_Graduation_Project/Upload-Folder'
    print(sourceFolder)
    app = QtWidgets.QApplication(sys.argv)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    w = ThirdTabLoads()
    w.show()
    sys.exit(app.exec_())