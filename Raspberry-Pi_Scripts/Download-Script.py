import gdown, sys
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap

class ThirdTabLoads(QWidget):

    def download_file(past_version):    
        MetaData = 'https://drive.google.com/drive/folders/1puoqf_UirRiVxkcEQswCr_uah8xzKnJ0?usp=share_link'
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=share_link'
        current_version = 0
        gdown.download_folder(MetaData)
        f = open("Metadata/MetaData.txt", "r")
        print(f.read())
        for items in f:
            if items.split(':') == "version":
                current_version = items.split(':')[1]
            elif items.split(':') == "filename":
                name = items.split(':')[1]

        if current_version > past_version :
            gdown.download_folder(url)
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


if __name__ == '__main__':
    w = ThirdTabLoads()
    w.download_file(3)
