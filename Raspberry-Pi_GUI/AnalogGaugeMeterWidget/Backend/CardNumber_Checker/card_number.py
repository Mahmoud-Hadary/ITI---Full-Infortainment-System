import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

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
        card_number = self.card_number_input.text()
        if card_number.isdigit() and len(card_number) == 16:
            self.result_label.setText("<h3 style='color: green;'>Valid Card Number</h3>")
        else:
            self.result_label.setText("<h3 style='color: red;'>Invalid Card Number</h3>")
            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())            



