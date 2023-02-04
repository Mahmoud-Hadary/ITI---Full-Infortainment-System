import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor,QPalette,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDial, QPushButton

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.heart_rate = 0
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 920, 480)
        # Set the background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("40.png")))
        self.setPalette(palette)

        # Create a vertical layout for the widget
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Create a horizontal layout for the heart rate monitor
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        # Add a label to display the heart rate monitor title
        label = QLabel("Heart Rate Monitor")
        label.setAlignment(Qt.AlignCenter)
        hbox.addWidget(label)

        # Add a dial to display the heart rate
        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.dial.setMaximum(200)
        self.dial.setValue(self.heart_rate)
        hbox.addWidget(self.dial)

        # Add a label to display the heart rate value
        self.heart_rate_label = QLabel(str(self.heart_rate) + " BPM")
        self.heart_rate_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.heart_rate_label)

        # Add three buttons: Check for Updates, I'm Fine, and Buy Feature
        self.check_for_updates_button = QPushButton("Check for Updates")
        vbox.addWidget(self.check_for_updates_button)

        self.iam_fine_button = QPushButton("I'm Fine")
        vbox.addWidget(self.iam_fine_button)

        self.buy_feature_button = QPushButton("Buy Feature")
        vbox.addWidget(self.buy_feature_button)

        # Add two labels: LED State and Buzzer State
        self.led_state_label = QLabel("LED State: Off")
        vbox.addWidget(self.led_state_label)

        self.buzzer_state_label = QLabel("Buzzer State: Off")
        vbox.addWidget(self.buzzer_state_label)

        # Start a timer to update the heart rate and the label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateHeartRate)
        self.timer.start(1000) # update every 1000 milliseconds (1 second)

    def updateHeartRate(self):
        self.heart_rate = random.randint(50, 150) # simulate a random heart rate reading between 50 and 150 BPM
        self.dial.setValue(self.heart_rate)
        self.heart_rate_label.setText(str(self.heart_rate) + " BPM")

app = QApplication(sys.argv)
dashboard = Dashboard()
dashboard.show()
sys.exit(app.exec_())
