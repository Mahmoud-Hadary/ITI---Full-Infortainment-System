import os
import sys
import serial
import time
import RPi.GPIO as GPIO
#import tkinter as tk
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
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break

        Fpath= "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main/"+str(hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()

        # Open the secure file and read the key and IV
        secure_file_path = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main/secure_key_and_iv.bin"    
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
        Dpath = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main/"+str(hex_file_name)+ "_decrypted.hex"
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        print(f"File has been decrypted successfully and saved")

    def decrypt_file_GSM(self):
        # Open file dialog to select an encrypted file
        hex_file_name = None
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_GSM_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break

        Fpath= "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM/"+str(hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()

        # Open the secure file and read the key and IV
        secure_file_path = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM/secure_key_and_iv.bin"    
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
        Dpath = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM/"+str(hex_file_name)+ "_decrypted.hex"
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        print(f"File has been decrypted successfully and saved")

#shutil.rmtree(path, ignore_errors=False, onerror=None, *, dir_fd=None)
    def download_file(self):    
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=sharing'
        current_version = 0
        gdown.download_folder(url)
        f = open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/FOTA-Version-Control-Main/Metadata.txt", "r")
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main/Metadata.txt", "r") as NEV :
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
        f = open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/FOTA-Version-Control-GSM/Metadata.txt", "r")
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM/Metadata.txt", "r") as NEV :
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
    

    def open_card_number_window(self):
        self.card_number_window = QtWidgets.QWidget(self, QtCore.Qt.Window)
        self.card_number_window.setWindowTitle("Card Number")
        self.card_number_window.setGeometry(50, 50, 500, 350)
        self.card_number_window.setWindowIcon(QtGui.QIcon("card.png"))  # set an icon for the window

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        card_number_label = QtWidgets.QLabel("<h2>Enter Card Number:</h2>")
        layout.addWidget(card_number_label)

        self.card_number_input = QtWidgets.QLineEdit()
        self.card_number_input.setStyleSheet("background-color: #ecf0f1; padding: 10px; font-size: 18px; border-radius: 10px;")
        layout.addWidget(self.card_number_input)

        self.check_button = QtWidgets.QPushButton("Check")
        self.check_button.clicked.connect(self.check_card_number)
        self.check_button.setStyleSheet("background-color: #3498db; color: white; font-size: 20px; padding: 10px; margin-top: 20px; border-radius: 10px;")
        layout.addWidget(self.check_button)

        self.result_label = QtWidgets.QLabel("")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.result_label)

        numbers_layout = QtWidgets.QGridLayout()

        button1 = QtWidgets.QPushButton("1")
        button1.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "1"))
        button1.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button1, 0, 0)

        button2 = QtWidgets.QPushButton("2")
        button2.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "2"))
        button2.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button2, 0, 1)

        button3 = QtWidgets.QPushButton("3")
        button3.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "3"))
        button3.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button3, 0, 2)
            
        button4 = QtWidgets.QPushButton("4")
        button4.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "4"))
        button4.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button4, 1, 0)

        button5 = QtWidgets.QPushButton("5")
        button5.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "5"))
        button5.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button5, 1, 1)

        button6 = QtWidgets.QPushButton("6")
        button6.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "6"))
        button6.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button6, 1, 2)

        button7 = QtWidgets.QPushButton("7")
        button7.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "7"))
        button7.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button7, 2, 0)

        button8 = QtWidgets.QPushButton("8")
        button8.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "8"))
        button8.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button8, 2, 1)

        button9 = QtWidgets.QPushButton("9")
        button9.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "9"))
        button9.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button9, 2, 2)

        button0 = QtWidgets.QPushButton("0")
        button0.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "0"))
        button0.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button0, 3, 1)

        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.card_number_input.setText(""))
        clear_button.setStyleSheet("background-color: #e74c3c; color: #ecf0f1; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(clear_button, 3, 0)

        back_button = QtWidgets.QPushButton("<-")
        back_button.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text()[:-1]))
        back_button.setStyleSheet("background-color: #e74c3c; color: #ecf0f1; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(back_button, 3, 2)
        layout.addLayout(numbers_layout)
        
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

        
    def Flash_Event(self):
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(21,GPIO.OUT)
            GPIO.output(21,GPIO.HIGH)
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
            #root = tk.Tk()
            #root.title("Hex File Transfer")
            def send_hex_record(record):
                # You send size of record to STM and tell stm the first one byte it will received size of each record (for example)	
               # size = len(record)
                ser.write( record.encode())
                print(record)
                # after STM Received each record it will send OK and raspberry will received it to send another Recode.....
                response = ser.read(2).decode() 
                #response = ser.read(ser.inWaiting).decode()
                print(response)
                # check if Rasp received another thing it will raise error
                
                if response != 'ok':
                    print('Error:', response)
                            
                #  Show Communication between STM , Raspberry
                #display.insert(tk.END, "Sent: " + record)
                #display.insert(tk.END, "Received: " + response + "\n")
                return response
            # Read the hex file
            try:
                hex_file_name = None
                hex_file_path = None
                if Sub == False : 
                        
                        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main"
                elif Sub == True : 
                        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM"
                for file in os.listdir(directory):
                        if file.endswith("decrypted.hex"):
                                hex_file_name = file
                                print(hex_file_name)
                                break   
                hex_file_path = directory+'/'+hex_file_name                         
                with open(hex_file_path, 'r') as f:
                    hex_file = f.readlines()
            except FileNotFoundError:
                print("Error: Hex file not found.")
                
                exit()

            #display = tk.Text(root, height=20, width=80)
            #display.pack()
            time.sleep(1)
            GPIO.output(21,GPIO.LOW)

            # Send each record, its size, and check for receipt
            for record in hex_file:
                #if record[7:9] == "01":
                 #  break
                   # flag=1
                    # End-of-file (EOF) record received
                    # EOF record identified by the record type in the eighth and ninth position of the hex record being equal to "01". 
                   # if you want to do thing
                
                try:
                    check =send_hex_record(record)
                    #if flag == 1:
                     # break
                except Exception as e:
                    #display.insert(tk.END, str(e) + "\n")
                    #display.insert(tk.END, "Transfer failed.\n")
                    print("Transfer * failed.\n") 
                    break
                else:
                # If All File Transferred Successfully
                    if check == "ok":
                        print("Transfer * successful.\n")    
                        #display.insert(tk.END, "Transfer * successful.\n")
                    else:
                        print("waiting")
            ser.close()
            #root.mainloop()   
    





    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        global Sub
        ################################################################################################
        # Setup the UI main window
        ################################################################################################
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #self.Sub.hide()
        #self.Updates.hide()
        #self.False_Alarm.hide()
        #self.Flash.hide()

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

        self.Updates = QtWidgets.QPushButton("Check For Updates", self)
        self.False_Alarm = QtWidgets.QPushButton("False Alarm", self)
        self.Sub = QtWidgets.QPushButton("Subscribe", self)
        self.Flash = QtWidgets.QPushButton("Flash", self)
        self.Updates.setStyleSheet("background : transparent;border : 0;color: white;")
        self.Updates.resize(160,50)
        self.False_Alarm.setStyleSheet("background : transparent;border : 0;color: white;")
        self.Sub.setStyleSheet("background : transparent;border : 0;color: white;")
        self.Flash.setStyleSheet("background : transparent;border : 0;color: white;")
        if Sub == False:
            self.Updates.clicked.connect(self.download_file)   
        else:
            self.Updates.clicked.connect(self.download_file_GSM)   

        self.Sub.clicked.connect(self.open_card_number_window)
        self.Flash.clicked.connect(self.Flash_Event)

        self.Flash.move(1325,225)
        self.Updates.move(1295, 50)
        self.Sub.move(1325, 390)
        self.False_Alarm.move(75, 225)

        '''self.Label_Updates = QLabel('Check For Updates', self)
        self.Label_Updates.resize(160, 50)
        self.Label_Updates.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Updates.move(1310,50)'''

        '''self.Label_Sub = QLabel('Subscribe', self)
        self.Label_Sub.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Sub.move(1340,380)
        self.Label_Sub.resize(160, 50)'''


        '''self.Label_Flash = QLabel('Flash Update', self)
        self.Label_Flash.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Flash.move(1330,215)
        self.Label_Flash.resize(160, 50)'''


        '''self.Label_Flash = QLabel('False Alarm', self)
        self.Label_Flash.setStyleSheet("background-color: transparent;color: white;font-size: 12pt;")
        self.Label_Flash.move(80,215)
        self.Label_Flash.resize(160, 50)'''

    
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
