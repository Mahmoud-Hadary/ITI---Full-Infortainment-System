# Our Needed Libraries
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
def Delete_Key(Gfilename):
    """
    Deletes a file with a given name from Google Drive.

    Args:
        Gfilename (str): The name of the file to delete.

    Returns:
        None
    """
    global drive
    global folder

    # Get a list of all files in the folder with the specified ID and that are not in the trash.
    file_list = drive.ListFile({'q': "'1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' in parents and trashed=false"}).GetList()

    # Loop through each file in the list.
    for file1 in file_list:
        # If the file has the same title as the one we want to delete, delete it.
        if file1['title'] == Gfilename:
            drive.CreateFile({
                'title': file1['title'],
                'id': file1['id'],
                'parents': [{
                    'kind': 'drive#fileLink',
                    'id': '1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO'
                }]
            }).Delete()

            # Print a message indicating that the file has been deleted.
            print('title: %s, id: %s and is deleted' % (file1['title'], file1['id']))


def Delete_Key_GSM(Gfilename):
    """
    Deletes a file with a given name from GSM Google Drive Folder.

    Args:
        Gfilename (str): The name of the file to delete.

    Returns:
        None
    """
    global drive
    global folder

    # Get a list of all files in the folder with the specified ID and that are not in the trash.
    file_list = drive.ListFile({'q': "'1KGUhNt6M64gnHKs3s68Umok8oSabzraZ' in parents and trashed=false"}).GetList()

    # Loop through each file in the list.
    for file1 in file_list:
        # If the file has the same title as the one we want to delete, delete it.
        if file1['title'] == Gfilename:
            drive.CreateFile({
                'title': file1['title'],
                'id': file1['id'],
                'parents': [{
                    'kind': 'drive#fileLink',
                    'id': '1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO'
                }]
            }).Delete()

            # Print a message indicating that the file has been deleted.
            print('title: %s, id: %s and is deleted' % (file1['title'], file1['id']))
   


def encrypt_file(file_path, folder):
    """
    Encrypt the specified file with a randomly generated key and initialization vector,and saves the encrypted data to a new file.

    Args:
        file_path (str): The path of the file to be encrypted.
        folder (GoogleDriveFolder): The Google Drive folder to upload the secure key and iv file.

    Returns:
        str: The path of the encrypted file.
    """

    global Key_Folder

    with open(file_path, "rb") as f:
        hex_file = f.read()

    # Generate a random key and initialization vector
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Save the key and IV to a secure file
    secure_file_path = "secure_key_and_iv.bin"
    with open(secure_file_path, "wb") as f:
        f.write(key + iv)

    # Delete the previous secure file from Google Drive
    Delete_Key(secure_file_path)

    # Create a new secure file and upload it to the specified folder on Google Drive
    secure = drive.CreateFile({
        'title': secure_file_path,
        'parents': [{
            'kind': 'drive#fileLink', 
            'id': folder['id'] 
        }]
    })
    sourceFile = Key_Folder + '/' + secure_file_path
    secure.SetContentFile(sourceFile)
    secure.Upload()    

    # Encrypt the key and IV
    # Create a new AES-ECB cipher
    cipher = AES.new(key, AES.MODE_ECB)

    # Encrypt the hex file
    hex_file = pad(hex_file, 16)
    ciphertext = cipher.encrypt(hex_file)

    # Save the encrypted data to a new file
    encrypted_file_path = os.path.splitext(file_path)[0] 
    splited = encrypted_file_path.split("v")[0]
    splited = splited + "_encryptedv"+encrypted_file_path.split("v")[1]+".bin"
    encrypted_file_path = splited
    with open(encrypted_file_path, "wb") as f:
        f.write(ciphertext)

    print(f"File has been encrypted successfully and saved to {encrypted_file_path}")

    return encrypted_file_path


def encrypt_file_GSM(file_path,folder):
    """
    Encrypt the specified GSM file with a randomly generated key and initialization vector,and saves the encrypted data to a new file.

    Args:
        file_path (str): The path of the file to be encrypted.
        folder (GoogleDriveFolder): The Google Drive folder to upload the secure key and iv file.

    Returns:
        str: The path of the encrypted file.
      
    """
    global Key_Folder
    with open(file_path, "rb") as f:
        hex_file = f.read()

    # Generate a random key and initialization vector
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Save the key and IV to a secure file
    secure_file_path = "secure_key_and_iv.bin"
    with open(secure_file_path, "wb") as f:
        f.write(key + iv)
    
    Delete_Key_GSM(secure_file_path)
    secure = drive.CreateFile({
                'title': secure_file_path,
                'parents': [{
                'kind': 'drive#fileLink', 
                'id': folder['id'] 
                    }]})
    sourceFile = Key_Folder + '/' + secure_file_path
    secure.SetContentFile(sourceFile)
    secure.Upload()    
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
    """
    Search for a folder with a specific name in Google Drive.

    Args:
        folderName (str): the name of the folder to search for.

    Returns:
        dict or None, a dictionary object representing the found folder if it exists, or None otherwise.
    
    Raises:
        QMessageBox.Critical: If the folder was not found.    
    """
    global drive

    # Get a list of all folders in Google Drive
    response = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

    # Search for the folder with the given name
    for folder in response:
        if (folder['title'] == folderName):
            print("Folder '" + folderName + "' found")
            return folder

    # If the folder was not found, show an error message and exit the program
    msg4 = QMessageBox()
    msg4.setWindowTitle("Error")
    msg4.setText("Could not find " + folderName)
    msg4.setIcon(QMessageBox.Critical)
    msg4.exec_()
    exit()

        
def searchFile(Gfilename):
    """
    Search for a specific file in the Google Drive folder.
    
    Args:
        Gfilename (str): The name of the file to search for.
        
    Returns:
       int: The version number of the specified file.
       
    Raises:
    QMessageBox.Critical: If the file was not found.   
       
    """
    global drive
    global folder
    # Get a list of all files in the Google Drive folder
    file_list = drive.ListFile({'q': "'1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        file_hype = file1['title'].split('v')
        if file_hype[0] ==  Gfilename:
            version = file_hype[1].split('.')
            version = int(version[0])
            return version
    # If the file is not found, display an error message and exit the program
    msg3 = QMessageBox()
    msg3.setWindowTitle("Error")
    msg3.setText("Could not find the file named "+Gfilename)
    msg3.setIcon(QMessageBox.Critical)
    msg3.exec_()        
    exit()

def searchFile_GSM(Gfilename):
    """
    Searches for a file with the given name in the GSM folder on Google Drive.

    Parameters:
    Gfilename (str): The name of the file to search for.

    Returns:
    int: The version number of the file if found.

    Raises:
    QMessageBox.Critical: If the file was not found.
    """
    global drive
    global folder
    # Get a list of all files in the GSM folder on Google Drive.
    file_list = drive.ListFile({'q': "'1KGUhNt6M64gnHKs3s68Umok8oSabzraZ' in parents and trashed=false"}).GetList()
    # Iterate over the files in the folder to find the one with the given name.
    for file1 in file_list:
        file_hype = file1['title'].split('v')
        if file_hype[0] == Gfilename:
            version = file_hype[1].split('.')
            version = int(version[0])
            return version
    # If the file was not found, display an error message and exit the program.
    msg3 = QMessageBox()
    msg3.setWindowTitle("Error")
    msg3.setText("Could not find the file named " + Gfilename)
    msg3.setIcon(QMessageBox.Critical)
    msg3.exec_()
    exit()


def Delete_GFile(Gfilename):
    """
    Deletes a file with the given name from Google Drive.

    Args:
        Gfilename (str): The name of the file to be deleted.

    Returns:
        None
    """
    global drive
    global folder

    # Get a list of all files in the target folder on Google Drive
    file_list = drive.ListFile({'q': "'1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' in parents and trashed=false"}).GetList()

    # Iterate over the files in the folder to find the one with the given name.
    for file1 in file_list:
        file_hype = file1['title'].split('v')
        if file_hype[0] ==  Gfilename:
            # Delete the file
            drive.CreateFile({
                'title': file1['title'],
                'id': file1['id'],
                'parents': [{
                    'kind': 'drive#fileLink', 
                    'id': '1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO' 
                    }]
                }).Delete()

            # Print a confirmation message
            print('title: %s, id: %s and is deleted' % (file1['title'], file1['id'])))


def Delete_GFile_GSM(Gfilename):
    """
    Deletes the file with the given name from a specific folder in Google Drive.

    Args:
        Gfilename (str): The name of the file to be deleted.
        
    Returns:
       None
    
    """
    global drive
    global folder
    file_list = drive.ListFile({'q': "'1KGUhNt6M64gnHKs3s68Umok8oSabzraZ' in parents and trashed=false"}).GetList()
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
    """
    A class that represents the third tab for uploading files.
    """

    def __init__(self, parent=None):
        """
        Constructs a new ThirdTabLoads object.
        
        Args:
            parent: the parent QWidget (default is None)
           
        Returns:
            None
    
        """
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
        Upload_button = QPushButton("Upload Main Application")
        layout.addWidget(Upload_button)
        # Add widgets to the layout
        Upload_button_GSM = QPushButton("Upload File GSM")
        layout.addWidget(Upload_button_GSM)
        # Set the layout
        self.setLayout(layout)
        
        # Connect the button to the function
        Upload_button.clicked.connect(self.upload_file)
        Upload_button_GSM.clicked.connect(self.upload_file_GSM)
        
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
        """
        Uploads a file to Google Drive if it is a newer version than the currently stored file.
        
        Args:
            self: an instance of the class

        Returns:
            None
            
        """
        global filename
        global sourceFolder
        global Google_DriveFolder

        filename1, _ = QFileDialog.getOpenFileName(self, 'Single File', sourceFolder, '*.hex')
        filename = filename1.split('/')
        filename = filename[-1]
        file_type = filename.split("v")
        sourceFile = sourceFolder + '/' + filename
        print("This is the source file " + sourceFile)

        # Get the folder to upload to in Google Drive
        folder = searchFolder(Google_DriveFolder)

        # Determine the version of the file being uploaded
        version = int(file_type[1].split('.')[0])

        # Get the version of the currently stored file, if it exists
        old_version = searchFile("ITI_STM32F401CC_encrypted")

        if version > old_version:
            # Delete the old version of the file if it exists
            Delete_GFile("ITI_STM32F401CC_encrypted")

            if filename1:
                path_meta = "C:/Users/m_god/TOBEOPIED/Mahmoud_HardDRIVE/data/GradProject/ITI_ADAS_Graduation_Project/Metadata.txt"

                # Encrypt and upload the file to Google Drive
                path = encrypt_file(filename1, folder)
                print("This is the Path file " + path)
                name = path.split("/")
                name = name[-1]
                file = drive.CreateFile({
                    'title': name,
                    'parents': [{
                        'kind': 'drive#fileLink', 
                        'id': folder['id'] 
                    }]
                })
                file.SetContentFile(path)
                file.Upload()

                # Create the metadata file and upload it to Google Drive
                Delete_GFile("Metadata.txt")
                with open("Metadata.txt",'w') as meta:
                    meta.write("version:" + str(version))
                    meta.write('\nfilename:' + name)
                    meta.close()
                    file = drive.CreateFile({
                        'title': "Metadata.txt",
                        'parents': [{
                            'kind': 'drive#fileLink', 
                            'id': folder['id']
                        }]
                    })
                    file.SetContentFile(path_meta)
                    file.Upload()

                # Show a success message box
                msg1 = QMessageBox()
                msg1.setWindowTitle("Uploaded Successfully")
                msg1.setText(f"File {name} has been uploaded successfully and saved to Google Drive.")
                msg1.setIcon(QMessageBox.Information)
                msg1.exec_()
            else:
                # Show an error message box if the file is an older version
                msg2 = QMessageBox()
                msg2.setWindowTitle("Error")
                msg2.setText("You are trying to upload an older version.")
                msg2.setIcon(QMessageBox.Critical)
                msg2.exec_()




    def upload_file_GSM(self):
        """
        Uploads a file to the GSM Google Drive folder.

        This function gets the file to upload using QFileDialog, encrypts it, 
        and uploads it to the Google Drive folder.

        Args:
            self: an instance of the class

        Returns:
            None
        """
        global filename
        global sourceFolder
        global Google_DriveFolder_GSM
        
        filename1, _ = QFileDialog.getOpenFileName(self, 'Single File', sourceFolder, '*.hex')
        filename = filename1.split('/')
        filename = filename[-1]
        file_type = filename.split("v")
        sourceFile = sourceFolder + '/' + filename
        print("This is the source file " + sourceFile)
        
        folder = searchFolder(Google_DriveFolder_GSM)
        version = int(file_type[1].split('.')[0])
        old_version = searchFile_GSM("ITI_STM32F401CC_GSM_encrypted")
        
        if version > old_version:
            Delete_GFile_GSM("ITI_STM32F401CC_GSM_encrypted")
            
            if filename1:
                path_meta = "C:/Users/m_god/TOBEOPIED/Mahmoud_HardDRIVE/data/GradProject/ITI_ADAS_Graduation_Project/Metadata.txt"
                path = encrypt_file_GSM(filename1, folder)
                print("This is the Path file " + path)
                name = path.split("/")
                name = name[-1]
                
                file = drive.CreateFile({
                    'title': name,
                    'parents': [{
                        'kind': 'drive#fileLink', 
                        'id': folder['id']
                    }]
                })
                file.SetContentFile(path)
                file.Upload()

                Delete_GFile_GSM("Metadata.txt")
                with open("Metadata.txt",'w') as meta:
                    meta.write("version:" + str(version))
                    meta.write('\nfilename:' + name)
                    meta.close()
                    file = drive.CreateFile({
                        'title': "Metadata.txt",
                        'parents': [{
                            'kind': 'drive#fileLink', 
                            'id': folder['id'] 
                        }]
                    })
                    file.SetContentFile(path_meta)
                    file.Upload()
                
                msg1 = QMessageBox()
                msg1.setWindowTitle("Uploaded Successfully")
                msg1.setText(f"File {name} has been uploaded successfully and saved to Google Drive")
                msg1.setIcon(QMessageBox.Information)
                msg1.exec_()
                
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("You are trying to upload an older version.")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()

        
        

if __name__ == '__main__':
    filename = ""
    Google_DriveFolder = "FOTA-Version-Control-Main"
    Google_DriveFolder_GSM = "FOTA-Version-Control-GSM"
    sourceFolder = 'C:/Users/m_god/TOBEOPIED/Mahmoud_HardDRIVE/data/GradProject/ITI_ADAS_Graduation_Project/Upload-Folder'
    Key_Folder = 'C:/Users/m_god/TOBEOPIED/Mahmoud_HardDRIVE/data/GradProject/ITI_ADAS_Graduation_Project'
    print(sourceFolder)
    app = QtWidgets.QApplication(sys.argv)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    w = ThirdTabLoads()
    w.show()
    sys.exit(app.exec_())