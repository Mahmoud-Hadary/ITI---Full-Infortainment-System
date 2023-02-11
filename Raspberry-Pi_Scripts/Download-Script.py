import gdown, sys
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox
import os
import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import binascii
import base64
import shutil
from tkinter import filedialog

class ThirdTabLoads(QWidget):
    #Function to browse for an encrypted file and decrypt its content
    def decrypt_file(self):
        # Open file dialog to select an encrypted file
        encrypted_file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.bin")])
        with open(encrypted_file_path, "rb") as f:
            encrypted_file = f.read()

        # Open the secure file and read the key and IV
        secure_file_path = "F:\ITI_Final_Project\ITI_ADAS_Graduation_Project\Raspberry-Pi_Scripts\FOTA-Version-Control\secure_key_and_iv.bin"
        with open(secure_file_path, "rb") as f:
            secure_file = f.read()
        key = secure_file[:16]
        iv = secure_file[16:]

        # Create a new AES-ECB cipher
        cipher = AES.new(key, AES.MODE_ECB)

        # Decrypt the encrypted file
        hex_file = cipher.decrypt(encrypted_file)

        # Save the decrypted data to a new file
        decrypted_file_path = os.path.splitext(encrypted_file_path)[0] + "_decrypted.hex"
        with open(decrypted_file_path, "wb") as f:
            f.write(hex_file)
        print(f"File has been decrypted successfully and saved to {decrypted_file_path}")

#shutil.rmtree(path, ignore_errors=False, onerror=None, *, dir_fd=None)
    def download_file(self):    
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=share_link'
        current_version = 0
        gdown.download_folder(url)
        f = open("FOTA-Version-Control-Main/Metadata.txt", "r")
        with open("Old_FOTA-Version-Control-Main/Metadata.txt", "r") as NEV :
            data = NEV.read()
            for line in data.split("\n"):
                if line.startswith("version:"):
                    past_version = line.split(":")[1].strip()
                    break
            print("past version:", past_version)

        Lines = f.readlines()
        for items in Lines:
            items = items.split(':')
            print(items)
            if items[0] == "version":
                current_version = int(items[1])
            elif items[0] == "filename":
                name = items[1]
        print(current_version)
        if int(current_version) > int(past_version) :
            shutil.rmtree("Old_FOTA-Version-Control-Main/")
            os.rename("FOTA-Version-Control-Main","Old_FOTA-Version-Control-Main")
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            self.decrypt_file()
        else:
            shutil.rmtree("FOTA-Version-Control-Main/")
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()


    def download_file_GSM(self):    
        url = 'https://drive.google.com/drive/folders/1KGUhNt6M64gnHKs3s68Umok8oSabzraZ?usp=share_link'
        current_version = 0
        #------------------------------------------------------
        #change to download file
        gdown.download(url, "MetaData.txt")         
        f = open("FOTA-Version-Control-GSM/Metadata.txt", "r")

        #gdown.download_folder(url)
        
        #get past version then delete metadata
        with open("MetaData.txt", "r") as NEV :
            data = NEV.read()
            for line in data.split("\n"):
                if line.startswith("version:"):
                    past_version = line.split(":")[1].strip()
                    break
            print("past version:", past_version)
        #-------------------------------------------------------   
        Lines = f.readlines()
        for items in Lines:
            items = items.split(':')
            print(items)
            if items[0] == "version":
                current_version = int(items[1])
            elif items[0] == "filename":
                name = items[1]
        print(current_version)
        if current_version < past_version :
            gdown.download_folder(url)
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            self.decrypt_file()
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ThirdTabLoads()
    w.download_file()
    #w.download_file_GSM()
    w.show()
    sys.exit(app.exec_())
