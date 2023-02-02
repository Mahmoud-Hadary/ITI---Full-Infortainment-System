import gdown, sys
from urllib.request import urlopen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,QPushButton, QFileDialog,QMessageBox

class ThirdTabLoads(QWidget):

    def download_file(self,past_version):    
        MetaData = 'https://drive.google.com/drive/folders/1puoqf_UirRiVxkcEQswCr_uah8xzKnJ0?usp=share_link'
        url = 'https://drive.google.com/drive/folders/1jow0y1TiAY8OkjUaGkmhYM3jWm6RaWYO?usp=share_link'
        current_version = 0
        gdown.download_folder(MetaData)
        f = open("Metadata/MetaData.txt", "r")
        Lines = f.readlines()
        for items in Lines:
            items = items.split(':')
            print(items)
            if items[0] == "version":
                current_version = int(items[1])
            elif items[0] == "filename":
                name = items[1]
        print(current_version)
        if current_version > past_version :
            gdown.download_folder(url)
            msg1 = QMessageBox()
            msg1.setWindowTitle("Uploaded Suceesfully")
            msg1.setText(f"File {name} has been Downloaded successfully and saved the system")
            msg1.setIcon(QMessageBox.Information)
            msg1.exec_()

        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error")
            msg2.setText("There is no New versions available")
            msg2.setIcon(QMessageBox.Critical)
            msg2.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ThirdTabLoads()
    w.download_file(3)
    w.show()
    sys.exit(app.exec_())
