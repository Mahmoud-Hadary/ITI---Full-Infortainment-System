# Our Nedded Libraries
import os
import sys
import serial
import time
import RPi.GPIO as GPIO
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from PyQt5.QtCore import (
    QPropertyAnimation, QSequentialAnimationGroup, QPoint, QSize,QEasingCurve,QParallelAnimationGroup)
import gdown
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import shutil

################################################################################################

# Raspberry Pi Pin Configuration 

################################################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.HIGH)

################################################################################################

# Convert UI to PyQt5 py file

################################################################################################
os.system("pyuic5 -o analoggaugewidget_demo_ui.py analoggaugewidget_demo.ui")
################################################################################################

# Import the generated UI

################################################################################################
from analoggaugewidget_demo_ui import *
################################################################################################

# MAIN WINDOW CLASS

################################################################################################

class MainWindow(QMainWindow):

    def decrypt_file(self):
        """
        This function decrypts an encrypted file using AES-ECB mode and a key and IV read from another secure file. The function performs the following steps:

        1. Searches for an encrypted file with a specific name in a directory.
        2. Reads the encrypted file.
        3. Reads the secure file containing the key and IV.
        4. Creates a new AES-ECB cipher using the key and IV.
        5. Decrypts the encrypted file using the cipher.
        6. Saves the decrypted data to a new file.

        Args:
            self: An instance of the class.

        Returns:
            None.

        Raises:
            FileNotFoundError: If the encrypted file or secure file cannot be found in the specified directory.
            ValueError: If the length of the key or IV is incorrect.
            Crypto.Error: If there is an error decrypting the file.

        """

        # Step 1: Search for the encrypted file
        hex_file_name = None
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break
        
        # Check if the encrypted file was found
        if not hex_file_name:
            raise FileNotFoundError(f"No encrypted file found in directory {directory}")
        
        # Step 2: Read the encrypted file
        Fpath = os.path.join(directory, hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()
        
        # Step 3: Read the secure file containing the key and IV
        secure_file_path = os.path.join(directory, "secure_key_and_iv.bin")
        with open(secure_file_path, "rb") as f:
            secure_file = f.read()
        
        # Step 4: Get the key and IV
        key = secure_file[:16]
        iv = secure_file[16:]
        
        # Check if the length of the key and IV is correct
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 16 bytes each")
        
        # Step 5: Create a new AES-ECB cipher and decrypt the encrypted file
        cipher = AES.new(key, AES.MODE_ECB)
        try:
            hex_file = cipher.decrypt(encrypted_file)
        except Crypto.Error as e:
            raise Crypto.Error("Error decrypting file") from e
        
        # Step 6: Save the decrypted data to a new file
        Dpath = os.path.join(directory, f"{hex_file_name}_decrypted.hex")
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        
        print(f"File has been decrypted successfully and saved to {Dpath}")


    def decrypt_file_GSM(self):
        """
        This function finds an GSM encrypted file in a specified directory and decrypts it using AES-ECB mode and a key and IV read from another secure file.
        The function performs the following steps:

        1. Searches for a GSM encrypted file with a specific name in a directory.
        2. Reads the encrypted file.
        3. Reads the secure file containing the key and IV.
        4. Creates a new AES-ECB cipher using the key and IV.
        5. Decrypts the encrypted file using the cipher.
        6. Saves the decrypted data to a new file.        

        Args:
            self: An instance of the class.

        Returns:
            None.

        Raises:
            FileNotFoundError: If the encrypted file or secure file cannot be found in the specified directory.
            ValueError: If the length of the key or IV is incorrect.
            Crypto.Error: If there is an error decrypting the file.
        """

        # Step 1: Search for the GSM encrypted file in the specified directory
        hex_file_name = None
        directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM"
        for file in os.listdir(directory):
            if file.startswith("ITI_STM32F401CC_GSM_encrypted"):
                hex_file_name = file
                print(hex_file_name)
                break          
                
        # Check if the encrypted file was found
        if hex_file_name is None:
            raise FileNotFoundError("Encrypted file not found in directory")

        # Step 2: Read the encrypted file
        Fpath = os.path.join(directory, hex_file_name)
        with open(Fpath, "rb") as f:
            encrypted_file = f.read()
        
        # Step 3: Read the secure file containing the key and IV
        secure_file_path = os.path.join(directory, "secure_key_and_iv.bin")
        with open(secure_file_path, "rb") as f:
            secure_file = f.read()
        
        # Step 4: Get the key and IV
        key = secure_file[:16]
        iv = secure_file[16:]
        
        # Check if the length of the key and IV is correct
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 16 bytes each")
        
        # Step 5: Create a new AES-ECB cipher and decrypt the encrypted file
        cipher = AES.new(key, AES.MODE_ECB)
        try:
            hex_file = cipher.decrypt(encrypted_file)
        except Crypto.Error as e:
            raise Crypto.Error("Error decrypting file") from e
        
        # Step 6: Save the decrypted data to a new file
        Dpath = os.path.join(directory, f"{hex_file_name}_decrypted.hex")
        with open(Dpath, "wb") as f:
            f.write(hex_file)
        
        print(f"File has been decrypted successfully and saved to {Dpath}")


    def download_file(self):   
        """
        Downloads a file from a Google Drive URL, checks its metadata, and replaces the previous version
        with the new version if the new version is newer.

        The function performs the following steps:
        1. Define the URL of the Google Drive folder to download.
        2. Initialize a variable for the current version number.
        3. Download the folder from the Google Drive URL using gdown.
        4. Read the metadata file of the new version.
        5. Read the metadata file of the previous version.
        6. Find the version number of the previous version.
        7. Find the version number of the current version and the name of the downloaded file.
        8. Replace the previous version with the current version if the current version is newer.
        9. Display a success message and decrypt the downloaded file.
        10. Display an error message if the current version is not newer.
        
        Args:
            self: An instance of the class.

        Returns:
            None.

        Raises:
            None.

        """
        # Step 1: Define the URL of the Google Drive folder to download.
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=sharing'

        # Step 2: Initialize a variable for the current version number.
        current_version = 0

        # Step 3: Download the folder from the Google Drive URL using gdown.
        gdown.download_folder(url)

        # Step 4: Read the metadata file of the new version.
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/FOTA-Version-Control-Main/Metadata.txt", "r") as f:
            # Step 5: Read the metadata file of the previous version.
            with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main/Metadata.txt", "r") as NEV:
                data = NEV.read()
                # Step 6: Find the version number of the previous version.
                for line in data.split("\n"):
                    if line.startswith("version:"):
                        past_version = line.split(":")[1].strip()
                        break
                print("past version:", past_version)

            # Step 7: Find the version number of the current version and the name of the downloaded file.
            Lines = f.readlines()
            for items in Lines:
                items = items.split(':')
                print(items)
                if items[0] == "version":
                    current_version = int(items[1])
                elif items[0] == "filename":
                    name = items[1]
            print(current_version)

        # Step 8: Replace the previous version with the current version if the current version is newer.
        if int(current_version) > int(past_version):
            shutil.rmtree("Old_FOTA-Version-Control-Main/")
            os.rename("FOTA-Version-Control-Main","Old_FOTA-Version-Control-Main")
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            self.decrypt_file()

        # Step 9: Display an error message if the current version is not newer.
        else:
            shutil.rmtree("FOTA-Version-Control-Main/")
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()


    def download_file_GSM(self):    

        """
        Downloads a GSM file from a Google Drive URL, checks its metadata, and replaces the previous version
        with the new version if the new version is newer.

        The function performs the following steps:
        1. Define the URL of the Google Drive folder containing the FOTA update for GSM module.
        2. Initialize a variable for the current version number.
        3. Download the folder from the Google Drive URL using gdown.
        4. Read the metadata file of the new version.
        5. Read the metadata file of the previous version.
        6. Find the version number of the previous version.
        7. Find the version number of the current version and the name of the downloaded file.
        8. Replace the previous version with the current version if the current version is newer.
        9. Display a success message and decrypt the downloaded file.
        10. Display an error message if the current version is not newer.
        
        Args:
            self: An instance of the class.

        Returns:
            None.

        Raises:
            None.

        """
        # Step 1: Define the URL of the Google Drive folder to download.
        url = 'https://drive.google.com/drive/folders/1KGUhNt6M64gnHKs3s68Umok8oSabzraZ?usp=share_link'
        # Step 2: Initialize a variable for the current version number.
        current_version = 0
        # Step 3: Download the folder from the Google Drive URL using gdown.
        gdown.download_folder(url)
        # Step 4: Read the metadata file of the new version.
        f = open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/FOTA-Version-Control-GSM/Metadata.txt", "r")
        # Step 5: Read the metadata file of the previous version.
        with open("/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-GSM/Metadata.txt", "r") as NEV:
            data = NEV.read()
            # Step 6: Find the version number of the previous version.
            for line in data.split("\n"):
                if line.startswith("version:"):
                    past_version = line.split(":")[1].strip()
                    break
            print("past version:", past_version)
        # Step 7: Find the version number of the current version and the name of the downloaded file.
        Lines = f.readlines()
        for items in Lines:
            items = items.split(':')
            print(items)
            if items[0] == "version":
                current_version = int(items[1])
            elif items[0] == "filename":
                name = items[1]
        print(current_version)
        # Step 8: Replace the previous version with the current version if the current version is newer.
        if int(current_version) > int(past_version) :
            shutil.rmtree("Old_FOTA-Version-Control-GSM/")
            os.rename("FOTA-Version-Control-GSM","Old_FOTA-Version-Control-GSM")
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            self.decrypt_file_GSM()
            
        # Step 9: Display an error message if the current version is not newer.
        else:
            shutil.rmtree("FOTA-Version-Control-GSM/")
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()


    def play_music(self):  
        """
        This function starts or stops playing music based on the current state.

        The function performs the following steps:
        1. Check the current state of the music player.
        2. If the music is not playing, start the music player and update the state.
        3. If the music is already playing, stop the music player and update the state.

        Args:
            self: An instance of the class.

        Returns:
            None.
        
        Raises:
            None.        
        """
        global State 
        # Step 1 : Check the current state of the music player
        if State == 0:
            # Step 2 : If the music is not playing, start the music.
            msg1 = QMessageBox()
            msg1.setWindowTitle("Music ON")
            msg1.setText("Your Music is Running Now.....")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            music_folder = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Music"
            os.system("mpg321 -Z -q " + music_folder + "/* &")
            State = 1
        elif State == 1:
            # Step 3 : If the music is already playing, stop the music.
            msg1 = QMessageBox()
            msg1.setWindowTitle("Music OFF")
            msg1.setText("Your Music is Stopping Now.....")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()
            os.system("pkill mpg321")
            State = 0

    def open_card_number_window(self):
        """
        Create a window for entering a card number and checking its validity.
        
        The function performs the following steps:
        1. Creates a new window with a title, size, and icon.
        2. Adds a label and input field for entering the card number.
        3. Adds a button to check the card number.
        4. Adds a label to display the result of the card number check.
        5. Adds a grid layout with buttons for entering numbers.
        6. Connects the buttons to update the card number input field when clicked.
        7. Displays the window.
        
        
        Args:
            self: an instance of the class

        Returns:
            None
            
        Raises:
            None.
            
        """
        
        # Step 1: Create a new window with a title, size, and icon.
        self.card_number_window = QtWidgets.QWidget(self, QtCore.Qt.Window)
        self.card_number_window.setWindowTitle("Card Number")
        self.card_number_window.setGeometry(50, 50, 500, 350)
        self.card_number_window.setWindowIcon(QtGui.QIcon("card.png"))
        
        # Step 2: Add a label and input field for entering the card number.
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        card_number_label = QtWidgets.QLabel("<h2>Enter Card Number:</h2>")
        layout.addWidget(card_number_label)
        self.card_number_input = QtWidgets.QLineEdit()
        self.card_number_input.setStyleSheet("background-color: #ecf0f1; padding: 10px; font-size: 18px; border-radius: 10px;")
        layout.addWidget(self.card_number_input)
        
        # Step 3: Add a button to check the card number.
        self.check_button = QtWidgets.QPushButton("Check")
        self.check_button.clicked.connect(self.check_card_number)
        self.check_button.setStyleSheet("background-color: #3498db; color: white; font-size: 20px; padding: 10px; margin-top: 20px; border-radius: 10px;")
        layout.addWidget(self.check_button)
        
        # Step 4: Add a label to display the result of the card number check.
        self.result_label = QtWidgets.QLabel("")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Step 5: Add a grid layout with buttons for entering numbers.
        numbers_layout = QtWidgets.QGridLayout()
        # Button for number 1
        button1 = QtWidgets.QPushButton("1")
        # Step 6: Connects the buttons to update the card number input field when clicked
        button1.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "1"))
        button1.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button1, 0, 0)
        # Button for number 2
        button2 = QtWidgets.QPushButton("2")
        button2.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "2"))
        button2.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button2, 0, 1)
        # Button for number 3
        button3 = QtWidgets.QPushButton("3")
        button3.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "3"))
        button3.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button3, 0, 2)
        # Button for number 4    
        button4 = QtWidgets.QPushButton("4")
        button4.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "4"))
        button4.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button4, 1, 0)
        # Button for number 5
        button5 = QtWidgets.QPushButton("5")
        button5.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "5"))
        button5.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button5, 1, 1)
        # Button for number 6
        button6 = QtWidgets.QPushButton("6")
        button6.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "6"))
        button6.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button6, 1, 2)
        # Button for number 7
        button7 = QtWidgets.QPushButton("7")
        button7.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "7"))
        button7.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button7, 2, 0)
        # Button for number 8
        button8 = QtWidgets.QPushButton("8")
        button8.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "8"))
        button8.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button8, 2, 1)
        # Button for number 9
        button9 = QtWidgets.QPushButton("9")
        button9.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "9"))
        button9.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button9, 2, 2)
        # Button for number 0
        button0 = QtWidgets.QPushButton("0")
        button0.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text() + "0"))
        button0.setStyleSheet("background-color: #ecf0f1; color: #3498db; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(button0, 3, 1)
        # Button for Clear All text
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.card_number_input.setText(""))
        clear_button.setStyleSheet("background-color: #e74c3c; color: #ecf0f1; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(clear_button, 3, 0)
        # Button for Backspace
        back_button = QtWidgets.QPushButton("<-")
        back_button.clicked.connect(lambda: self.card_number_input.setText(self.card_number_input.text()[:-1]))
        back_button.setStyleSheet("background-color: #e74c3c; color: #ecf0f1; font-size: 20px; padding: 10px; margin: 5px; border-radius: 10px;")
        numbers_layout.addWidget(back_button, 3, 2)
        layout.addLayout(numbers_layout)    
        self.card_number_window.setLayout(layout)
        
        # Step 7: Displays the window
        self.card_number_window.show()

   
    def check_card_number(self):
        """
        Check if the entered card number is valid and download the GSM file if it is.

        This method checks if the card number entered in the input field is a 16-digit number. If it is valid,
        the method displays a success message, sets the `Sub` variable to `True` indicating that the user has
        subscribed, and downloads the GSM file. If the card number is invalid, the method displays an error message.

        Args:
            self: an instance of the class

        Returns:
            None
            
        Raises:
            None.  
            
        """
        
        # allows Sub variable to be accessed from other methods
        global Sub
        
        # gets the text entered in the card number input field
        card_number = self.card_number_input.text()
        
        # checks if the card number is a 16-digit number
        if card_number.isdigit() and len(card_number) == 16:
            # displays a success message
            self.result_label.setText("<h3 style='color: green;'>Valid Card Number</h3>")
            # sets Sub to True, indicating that the user has subscribed
            Sub = True
            # downloads the GSM file
            self.download_file_GSM()
        else:
            # displays an error message
            self.result_label.setText("<h3 style='color: red;'>Invalid Card Number</h3>")


    def Flash_Event(self):
        """
        Flash the STM32 microcontroller with the corresponding hex file.

        This method reads the hex file from the directory specified by `directory` variable based on the value of `Sub`.
        It then sends each record of the hex file to the STM32 microcontroller, waits for a receipt, and checks for any
        errors. Finally, it blinks an LED to reset the bootloader.

        Args:
            self: an instance of the class

        Returns:
            None
            
        Raises:
            None.  
            
        """
        
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
        
        def send_hex_record(record):
            """
            Send a single record of the hex file to the STM32 microcontroller.

            This function takes a single record of the hex file as input and sends it to the STM32 microcontroller.
            It then waits for a receipt and checks if it is 'ok'. If it is not 'ok', it prints an error message.

            Args:
                record (str): A single record of the hex file.

            Returns:
                str: The receipt received from the STM32 microcontroller.
                
            Raises:
                None.
                
            """
            ser.write(record.encode())
            print(record)
            response = ser.read(2).decode()
            print(response)
            if response != 'ok':
                print('Error:', response)
            return response

        try:
            # Read the hex file
            hex_file_name = None
            hex_file_path = None
            if Sub == False :
                # Main Application Hexa
                directory = "/home/pi/Desktop/Test/ITI_ADAS_Graduation_Project/Raspberry-Pi_GUI/AnalogGaugeMeterWidget/Old_FOTA-Version-Control-Main"
            elif Sub == True :
                # GSM Application Hexa            
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

        # Led Blinking to reset Bootloader    
        GPIO.output(21,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(21,GPIO.HIGH)

        # Send each record, its size, and check for receipt
        for record in hex_file:
            try:
                check = send_hex_record(record)
            except Exception as e:
                print("Transfer * failed.\n")
                break
            else:
                if check == "ok":
                    print("Transfer * successful.\n")
                else:
                    print("waiting")
                    
        ser.close()


            

    
    class MainWindow(QMainWindow):
    """
    The MainWindow class sets up the main window of the UI and initializes various child widgets
    and animations for the UI elements.

    Args:
        parent (QObject): The parent object for this widget.

    Attributes:
        Sub (bool): A global boolean value indicating the subscription status of the user.
        State (int): A global integer value indicating the current state of the UI.
        ui (Ui_MainWindow): The UI_MainWindow object representing the user interface.
        child (QWidget): A child widget used for animations.
        anim (QPropertyAnimation): A QPropertyAnimation object controlling the position animation of the child widget.
        anim_2 (QPropertyAnimation): A QPropertyAnimation object controlling the size animation of the child widget.
        anim_group (QSequentialAnimationGroup): A QSequentialAnimationGroup object containing the position and size animations of the child widget.
        Panim_group (QParallelAnimationGroup): A QParallelAnimationGroup object containing all the animations for the UI elements.
        child_Flash (QWidget): A child widget used for flash animations.
        anim_flash (QPropertyAnimation): A QPropertyAnimation object controlling the position animation of the flash child widget.
        anim_flash_2 (QPropertyAnimation): A QPropertyAnimation object controlling the size animation of the flash child widget.
        child_False (QWidget): A child widget used for false animations.
        anim_False (QPropertyAnimation): A QPropertyAnimation object controlling the position animation of the false child widget.
        anim_False_2 (QPropertyAnimation): A QPropertyAnimation object controlling the size animation of the false child widget.
        child2 (QWidget): A child widget used for animations.
        anim2 (QPropertyAnimation): A QPropertyAnimation object controlling the position animation of the child2 widget.
        anim_3 (QPropertyAnimation): A QPropertyAnimation object controlling the size animation of the child2 widget.

    """
    def __init__(self, parent=None):
        """Initializes the MainWindow object and sets up the UI main window and its child widgets and animations."""
        QMainWindow.__init__(self, parent)

        # Initialize global variables
        global Sub
        global State

        # Setup the UI main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize child widget for animations
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child.resize(10, 10)

        # Set up position and size animations for child widget
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setEndValue(QPoint(800, 50))
        self.anim.setDuration(1500)
        self.anim_2 = QPropertyAnimation(self.child, b"size")
        self.anim_2.setEndValue(QSize(150, 50))
        self.anim_2.setDuration(1000)

        # Set up parallel and sequential animation groups
        self.anim_group = QSequentialAnimationGroup()
        self.Panim_group = QParallelAnimationGroup()

        # Initialize child widgets for flash and false animations
        self.child_Flash = QWidget(self)
        self.child_Flash.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child_Flash.resize(10, 10)
        self.child_False = QWidget(self)
        self.child_False.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child_False.resize(10, 10)

        # Set up position and size animations for flash and false child widgets
        self.anim_flash = QPropertyAnimation(self.child_Flash, b"pos")
        self.anim_flash.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim_flash.setEndValue(QPoint(800, 215))
        self.anim_flash.setDuration(1500)
        self.anim_flash_2 = QPropertyAnimation(self.child_Flash, b"size")
        self.anim_flash_2.setEndValue(QSize(150, 50))
        self.anim_flash_2.setDuration(1000)
        self.anim_False = QPropertyAnimation(self.child_False, b"pos")
        self.anim_False.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim_False.setEndValue(QPoint(50, 215))
        self.anim_False.setDuration(1500)
        self.anim_False_2 = QPropertyAnimation(self.child_False, b"size")
        self.anim_False_2.setEndValue(QSize(150, 50))
        self.anim_False_2.setDuration(1000)
        # Initialize child widget for animations
        self.child2 = QWidget(self)
        self.child2.setStyleSheet("background-color:#6665DD;border-radius:15px;")
        self.child2.resize(10, 10)
        # Set up position and size animations for child2 widget
        self.anim2 = QPropertyAnimation(self.child2, b"pos")
        self.anim2.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim2.setEndValue(QPoint(800, 380))
        self.anim2.setDuration(1500)
        self.anim_3 = QPropertyAnimation(self.child2, b"size")
        self.anim_3.setEndValue(QSize(150, 50))
        self.anim_3.setDuration(1000)
        # Create blur effects and apply them to child widgets
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
        # Add animations to a QParallelAnimationGroup and start them
        self.Panim_group.addAnimation(self.anim) 
        self.Panim_group.addAnimation(self.anim2) 
        self.Panim_group.addAnimation(self.anim_2) 
        self.Panim_group.addAnimation(self.anim_3) 
        self.Panim_group.addAnimation(self.anim_flash) 
        self.Panim_group.addAnimation(self.anim_flash_2)
        self.Panim_group.addAnimation(self.anim_False) 
        self.Panim_group.addAnimation(self.anim_False_2)
        # Start the animation 
        self.Panim_group.start() 
        # Create and style push button widgets and connect them to event handlers
        self.Updates = QtWidgets.QPushButton("Check For Updates", self)
        self.Sub = QtWidgets.QPushButton("Subscribe", self) 
        self.Flash = QtWidgets.QPushButton("Flash", self) 
        self.Music = QtWidgets.QPushButton("My Music", self)
        self.Updates.setStyleSheet("background : transparent;border : 0;color: white;")
        self.Updates.resize(160,50) 
        self.Sub.setStyleSheet("background : transparent;border : 0;color: white;") 
        self.Flash.setStyleSheet("background : transparent;border : 0;color: white;") 
        self.Music.setStyleSheet("background : transparent;border : 0;color: white;") 
        # Check if Sub is False
        if Sub == False: 
            # Connect self.Updates to self.download_file
            self.Updates.clicked.connect(self.download_file) 
        else:
            # Connect self.Updates to self.download_file_GSM
            self.Updates.clicked.connect(self.download_file_GSM)   
        self.Sub.clicked.connect(self.open_card_number_window)
        self.Flash.clicked.connect(self.Flash_Event)
        self.Music.clicked.connect(self.play_music)
        self.Flash.move(825,225)
        self.Updates.move(795, 50)
        self.Sub.move(825, 390)
        self.Music.move(75, 225)
        self.show()

if __name__ == '__main__':
    Sub =False
    State = 0
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())





