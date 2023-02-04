import sys
import subprocess
import random
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("ADAS Driver-Safety")
        self.setStyleSheet("background-color: #E5E5E5;")


        
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        h_layout = QHBoxLayout()
        h_layout.setAlignment(QtCore.Qt.AlignTop)



        self.check_for_updates_button = QPushButton("Check for updates")
        self.check_for_updates_button.setStyleSheet("background-color: #0099CC; color: white; padding: 10px; border-radius: 5px;")

        self.check_for_updates_button.clicked.connect(self.check_for_updates)
        layout.addWidget(self.check_for_updates_button)
        
        self.i_am_ok_button = QPushButton("I am OK")
        #self.i_am_ok_button.setStyleSheet("background-color: #0099CC; color: white; padding: 10px; border-radius: 5px;")

        self.i_am_ok_button.clicked.connect(self.i_am_ok)
        h_layout.addWidget(self.i_am_ok_button)
        layout.addLayout(h_layout)

        self.heart_rate_label = QLabel("Heart rate: 0 BPM")
        self.heart_rate_label.setStyleSheet("color: green; font-size: 20px;")
        layout.addWidget(self.heart_rate_label)
        
        self.buzzer_status_label = QLabel("Buzzer: OFF")
        self.buzzer_status_label.setStyleSheet("color: green; font-size: 20px;")

        layout.addWidget(self.buzzer_status_label)

        self.led_status_label = QLabel("LED: OFF")
        self.led_status_label.setStyleSheet("color: green; font-size: 20px;")

        layout.addWidget(self.led_status_label)

        self.graphics_view = QGraphicsView()
        self.graphics_view.setStyleSheet("background-color: white; border: 1px solid #0099CC; border-radius: 5px;")

        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        #self.graphics_view.setRenderHint(QtGui.QPainter.Antialiasing)

        layout.addWidget(self.graphics_view)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                display: inline-block;
                font-size: 16px;
                border-radius: 4px;
            }
        
            QLabel {
                color: #333;
                font-size: 18px;
            }
        
            QGraphicsView {
                border: 2px solid #333;
            }
        """)
        self.heart_rate = random.randint(60, 100)


        self.update_heart_rate()

    def check_for_updates(self):
        # receive file and decrypted it
        subprocess.call(["your_update_command"], shell=True)
    def i_am_ok(self):
        self.led_status_label.setStyleSheet("color: green; font-size: 20px;")
        self.buzzer_status_label.setStyleSheet("color: green; font-size: 20px;")
        self.heart_rate_label.setStyleSheet("color: green; font-size: 20px;")
        self.buzzer_status_label.setText("Buzzer: OFF")
        self.led_status_label.setText("LED: OFF")
    

    def update_heart_rate(self):
        heart_rate = random.randint(60, 100)
        self.heart_rate_label.setText(f"Heart rate: {heart_rate} BPM")

        # add rect to graph
        rect = QGraphicsRectItem(0, 0, 100, heart_rate)
        self.graphics_scene.addItem(rect)

        # call update_heart_rate again in 1 second
        QtCore.QTimer.singleShot(1000, self.update_heart_rate)
        if self.heart_rate > 70:
            self.led_status_label.setStyleSheet("color: red; font-size: 20px;")
            self.buzzer_status_label.setStyleSheet("color: red; font-size: 20px;")
            self.heart_rate_label.setStyleSheet("color: red; font-size: 20px;")
            self.buzzer_status_label.setText("Buzzer: ON")
            self.led_status_label.setText("LED: ON")
            QtCore.QTimer.singleShot(10000, self.call_ambulance)
        else:

            self.buzzer_status_label.setText("Buzzer: OFF")
            self.led_status_label.setText("LED: OFF")

    def call_ambulance(self):
        # call ambulance through bootloader
        subprocess.call(["your_bootloader_command"], shell=True)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())


