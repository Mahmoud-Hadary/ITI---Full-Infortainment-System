import os
import sys
import serial
import tkinter as tk
#from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from PyQt5.QtCore import (
    QPropertyAnimation, QSequentialAnimationGroup, QPoint, QSize,QEasingCurve,QParallelAnimationGroup)
#download script
import gdown
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import shutil



ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
root = tk.Tk()
root.title("Hex File Transfer")


################################################################################################
# Convert UI to PyQt5 py file
################################################################################################
os.system("pyuic5 -o analoggaugewidget_demo_ui.py analoggaugewidget_demo.ui")
# os.system("pyuic5 -o analoggaugewidget_demo_ui.py analoggaugewidget_demo.ui.oQCkCR")

################################################################################################
# Import the generated UI
################################################################################################
from analoggaugewidget_demo_ui import *

################################################################################################
# MAIN WINDOW CLASS
################################################################################################
class MainWindow(QMainWindow):

    #download Script
    def decrypt_file(self):
        # open
        hex_file_name = None
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-Main"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break

        Fpath= "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-Main/"+str(hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()

        # Open the secure file and read the key and IV
        secure_file_path = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-Main/secure_key_and_iv.bin"    
        with open(secure_file_path, "rb") as f:
            secure_file = f.read()
        key = secure_file[:16]
        iv = secure_file[16:]

        # Create a new AES-ECB cipher
        cipher = AES.new(key, AES.MODE_ECB)

        # Decrypt the encrypted file
        hex_file = cipher.decrypt(encrypted_file)

        # Save the decrypted data to a new file
        #decrypted_file_path = os.path.splitext(encrypted_file_path)[0] + "_decrypted.hex"
        Dpath = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-Main/"+str(hex_file_name)+ "_decrypted.hex"
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        print(f"File has been decrypted successfully and saved")

    def decrypt_file_GSM(self):
        # Open file dialog to select an encrypted file
        hex_file_name = None
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-GSM"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_GSM_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break

        Fpath= "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-GSM/"+str(hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()

        # Open the secure file and read the key and IV
        secure_file_path = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-GSM/secure_key_and_iv.bin"    
        with open(secure_file_path, "rb") as f:
            secure_file = f.read()
        key = secure_file[:16]
        iv = secure_file[16:]

        # Create a new AES-ECB cipher
        cipher = AES.new(key, AES.MODE_ECB)

        # Decrypt the encrypted file
        hex_file = cipher.decrypt(encrypted_file)

        # Save the decrypted data to a new file
        #decrypted_file_path = os.path.splitext(encrypted_file_path)[0] + "_decrypted.hex"
        Dpath = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-GSM/"+str(hex_file_name)+ "_decrypted.hex"
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        print(f"File has been decrypted successfully and saved")

#shutil.rmtree(path, ignore_errors=False, onerror=None, *, dir_fd=None)
    def download_file(self):    
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=sharing'
        current_version = 0
        gdown.download_folder(url)
        f = open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/FOTA-Version-Control-Main/Metadata.txt", "r")
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-Main/Metadata.txt", "r") as NEV :
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
        gdown.download_folder(url)
        f = open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/FOTA-Version-Control-GSM/Metadata.txt", "r")
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_Scripts/Old_FOTA-Version-Control-GSM/Metadata.txt", "r") as NEV :
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
            shutil.rmtree("Old_FOTA-Version-Control-GSM/")
            os.rename("FOTA-Version-Control-GSM","Old_FOTA-Version-Control-GSM")
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            self.decrypt_file_GSM()
        else:
            shutil.rmtree("FOTA-Version-Control-GSM/")
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()

####################################################################################################
####################################################################################################
    #card number script
####################################################################################################
####################################################################################################
    def initUI(self):
        # Set the central widget to the subscribe button
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("<h1>Subscribe</h1>")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        subscribe_button = QtWidgets.QPushButton("Subscribe", self)
        subscribe_button.clicked.connect(self.open_card_number_window)
        subscribe_button.setStyleSheet("background-color: #3498db; color: white; font-size: 20px; padding: 10px;")
        layout.addWidget(subscribe_button, alignment=QtCore.Qt.AlignCenter)

        central_widget.setLayout(layout)

        self.card_number_window = None

    def open_card_number_window(self):
        if self.card_number_window is None:
            self.card_number_window = QtWidgets.QWidget(self, QtCore.Qt.Window)
            self.card_number_window.setWindowTitle("Card Number")
            self.card_number_window.setGeometry(50, 50, 300, 200)
            self.card_number_window.setWindowIcon(QtGui.QIcon("card.png"))  # set an icon for the window

            layout = QtWidgets.QVBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignCenter)

            card_number_label = QtWidgets.QLabel("<h2>Enter Card Number:</h2>")
            layout.addWidget(card_number_label)

            self.card_number_input = QtWidgets.QLineEdit()
            self.card_number_input.setStyleSheet("background-color: #ecf0f1; padding: 10px; font-size: 18px;")
            layout.addWidget(self.card_number_input)

            self.check_button = QtWidgets.QPushButton("Check")
            self.check_button.clicked.connect(self.check_card_number)
            self.check_button.setStyleSheet("background-color: #3498db; color: white; font-size: 20px; padding: 10px; margin-top: 20px;")
            layout.addWidget(self.check_button)

            self.result_label = QtWidgets.QLabel("")
            self.result_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(self.result_label)
            self.card_number_window.setLayout(layout)

        self.card_number_window.show()

    def check_card_number(self):
        global Sub
        card_number = self.card_number_input.text()
        if card_number.isdigit() and len(card_number) == 16:
            self.result_label.setText("<h3 style='color: green;'>Valid Card Number</h3>")
            Sub = True
            self.download_file_GSM()
                
        else:
            self.result_label.setText("<h3 style='color: red;'>Invalid Card Number</h3>")




    #raspberry handler script




    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        global Sub
        ################################################################################################
        # Setup the UI main window
        ################################################################################################
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Updates = QtWidgets.QPushButton("Check For Updates", self)
        self.False_Alarm = QtWidgets.QPushButton("False Alarm", self)
        self.Sub = QtWidgets.QPushButton("Subscribe", self)
        self.Flash = QtWidgets.QPushButton("Flash", self)

        if Sub == False:
            self.Updates.clicked.connect(self.download_file)   
        else:
            self.Updates.clicked.connect(self.download_file_GSM)   

        self.Sub.clicked.connect(self.initUI)
        self.Flash.click.connect(self.)

        self.Flash.move(1300,215)
        self.Updates.move(1300, 50)
        self.Sub.move(1300, 380)
        self.False_Alarm.move(80, 240)
        self.Sub.hide()
        self.Updates.hide()
        self.False_Alarm.hide()
        self.Flash.hide()

        #effect = QtWidgets.QGraphicsBlurEffect()
        #effect.setBlurRadius(4)
        
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child.resize(10, 10)
        #self.child.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEndValue(QPoint(1300, 50))
        self.anim.setDuration(1500)
        self.anim_2 = QPropertyAnimation(self.child, b"size")
        self.anim_2.setEndValue(QSize(150, 50))
        self.anim_2.setDuration(1000)
        self.anim_group = QSequentialAnimationGroup()
        self.Panim_group = QParallelAnimationGroup()


        self.child_False = QWidget(self)
        self.child_False.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child_False.resize(10, 10)
        #self.child.setGraphicsEffect(effect)
        self.anim_False = QPropertyAnimation(self.child_False, b"pos")
        self.anim_False.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim_False.setEndValue(QPoint(50, 215))
        self.anim_False.setDuration(1500)
        self.anim_False_2 = QPropertyAnimation(self.child_False, b"size")
        self.anim_False_2.setEndValue(QSize(150, 50))
        self.anim_False_2.setDuration(1000)


        self.child_Flash = QWidget(self)
        self.child_Flash.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child_Flash.resize(10, 10)
        #self.child_Flash.setGraphicsEffect(effect)
        self.anim_flash = QPropertyAnimation(self.child_Flash, b"pos")
        self.anim_flash.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim_flash.setEndValue(QPoint(1300, 215))
        self.anim_flash.setDuration(1500)
        self.anim_flash_2 = QPropertyAnimation(self.child_Flash, b"size")
        self.anim_flash_2.setEndValue(QSize(150, 50))
        self.anim_flash_2.setDuration(1000)


        self.child2 = QWidget(self)
        self.child2.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child2.resize(10, 10)
        self.anim2 = QPropertyAnimation(self.child2, b"pos")
        self.anim2.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim2.setEndValue(QPoint(1300, 380))
        self.anim2.setDuration(1500)
        self.anim_3 = QPropertyAnimation(self.child2, b"size")
        self.anim_3.setEndValue(QSize(150, 50))
        self.anim_3.setDuration(1000)

        effect1 = QtWidgets.QGraphicsBlurEffect()
        effect1.setBlurRadius(3)
        effect2 = QtWidgets.QGraphicsBlurEffect()
        effect2.setBlurRadius(3)
        effect = QtWidgets.QGraphicsBlurEffect()
        effect.setBlurRadius(3)
        effect3 = QtWidgets.QGraphicsBlurEffect()
        effect3.setBlurRadius(3)

        self.child.setGraphicsEffect(effect)
        self.child_Flash.setGraphicsEffect(effect1)
        self.child2.setGraphicsEffect(effect2)
        self.child_False.setGraphicsEffect(effect3)


        self.Panim_group.addAnimation(self.anim)
        self.Panim_group.addAnimation(self.anim2)
        self.Panim_group.addAnimation(self.anim_2)
        self.Panim_group.addAnimation(self.anim_3)
        self.Panim_group.addAnimation(self.anim_flash)
        self.Panim_group.addAnimation(self.anim_flash_2)
        self.Panim_group.addAnimation(self.anim_False)
        self.Panim_group.addAnimation(self.anim_False_2)

        self.Panim_group.start()
        #self.anim_group.start()



        self.Label_Updates = QLabel('Check For Updates', self)
        self.Label_Updates.resize(160, 50)
        self.Label_Updates.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Updates.move(1310,50)

        self.Label_Sub = QLabel('Subscribe', self)
        self.Label_Sub.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Sub.move(1340,380)
        self.Label_Sub.resize(160, 50)


        self.Label_Flash = QLabel('Flash Update', self)
        self.Label_Flash.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Flash.move(1330,215)
        self.Label_Flash.resize(160, 50)


        self.Label_Flash = QLabel('False Alarm', self)
        self.Label_Flash.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Flash.move(80,215)
        self.Label_Flash.resize(160, 50)

    
        ################################################################################################
        # Show window
        ################################################################################################
        self.show()

        



########################################################################
## EXECUTE APP
########################################################################
if __name__ == '__main__':
    Sub =False
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

########################################################################
## END===>
########################################################################  