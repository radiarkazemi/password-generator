from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QSlider, QLabel, \
    QProgressBar, QCheckBox
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
import sys
import pyperclip
import random
import math
from password_strength import PasswordStats


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("password_Gen.ui", self)

        # Define The Widgets
        self.show_pass = self.findChild(QLineEdit, "password_lineEdit")
        self.copy_button = self.findChild(QPushButton, "copyBotton")
        self.length_slider = self.findChild(QSlider, "length_horizontalSlider")
        self.length_label = self.findChild(QLabel, "lengthShowLabel")
        # self.low_radio = self.findChild(QRadioButton, "low_radioButton")
        # self.medium_radio = self.findChild(QRadioButton, "medium_radioButton")
        # self.strong_radio = self.findChild(QRadioButton, "strong_radioButton")
        self.generate_button = self.findChild(QPushButton, "generate_pushButton")
        self.check_strength_label = self.findChild(QLabel, "check_strength_label")
        self.check_strength_prog = self.findChild(QProgressBar, "checkStrength_progressBar")
        self.low_checkbox = self.findChild(QCheckBox, "lower_checkBox")
        self.upper_checkbox = self.findChild(QCheckBox, "upper_checkBox")
        self.num_checkbox = self.findChild(QCheckBox, "num_checkBox")
        self.sym_checkbox = self.findChild(QCheckBox, "sym_checkBox")

        # Connecting Generate Button To The Function
        self.generate_button.clicked.connect(self.generate)
        # Connecting Copy Button To The Function
        self.copy_button.clicked.connect(self.copy)

        self.length_slider.valueChanged.connect(self.slider_value)

        self.lower = "abcdefghijklmnopqrstuvwxyz"
        # self.upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.upper = self.upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # self.digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
        self.digit = "0123456789"
        self.sym = "!@#$%^&*()></.}{;:|"
        self.pass_list = ""
        self.password = ""

        self.show()

    # Show Slide Length On Label
    def slider_value(self, value):
        self.length_label.setText(str(value))

    def generate(self):
        try:
            self.password = ""
            self.pass_list = ""
            length = self.length_slider.value()
            if self.low_checkbox.isChecked():
                self.pass_list = self.pass_list + self.lower
                for item in range(0, length):
                    self.password = self.password + random.choice(self.pass_list)

            if self.upper_checkbox.isChecked():
                self.password = ""
                self.pass_list = self.pass_list + self.upper
                for item in range(0, length):
                    self.password = self.password + random.choice(self.pass_list)

            if self.num_checkbox.isChecked():
                self.password = ""
                self.pass_list = self.pass_list + self.digit
                for item in range(0, length):
                    self.password = self.password + random.choice(self.pass_list)

            if self.sym_checkbox.isChecked():
                self.password = ""
                self.pass_list = self.pass_list + self.sym
                for item in range(0, length):
                    self.password = self.password + random.choice(self.pass_list)

            self.show_pass.setText(self.password)

            self.check_strength()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Select At Least One Checkbox!")
            msg.setIcon(QMessageBox.Critical)

            x = msg.exec_()

    # Generate Function
    # def generate(self):
    #     self.password = ""
    #
    #     length = self.length_slider.value()
    #     if self.low_radio.isChecked():
    #         for number in range(0, length):
    #             self.password = self.password + random.choice(self.lower)
    #     if self.medium_radio.isChecked():
    #         for number in range(0, length):
    #             self.password = self.password + random.choice(self.upper)
    #     if self.strong_radio.isChecked():
    #         for number in range(0, length):
    #             self.digit = chr(random.randint(33, 126))
    #             self.password = self.password + self.digit
    #     self.show_pass.setText(self.password)
    #
    #     self.check_strength()

    def check_strength(self):
        result = PasswordStats(self.show_pass.text())
        final = result.strength()
        # self.check_strength_label.setText(str(math.ceil(final * 100)) + "%")
        final = math.ceil(final * 100)
        self.check_strength_prog.setValue(final)

        if (final >= 0) and (final < 20):
            self.check_strength_prog.setStyleSheet("QProgressBar::chunk "
                                                   "{"
                                                   "background-color: red;"
                                                   "}")
            self.check_strength_label.setText("Weak")
            self.check_strength_label.setStyleSheet(
                "QLabel"
                "{"
                "background-color: red;"
                "color: white;"
                "}")

        if (final >= 20) and (final < 60):
            self.check_strength_prog.setStyleSheet("QProgressBar::chunk "
                                                   "{"
                                                   "background-color: orange;"
                                                   "}")
            self.check_strength_label.setText("Medium")
            self.check_strength_label.setStyleSheet(
                "QLabel"
                "{"
                "background-color: orange;"
                "color: white;"
                "}")

        if final >= 60:
            self.check_strength_prog.setStyleSheet("QProgressBar::chunk "
                                                   "{"
                                                   "background-color: green;"
                                                   "}")
            self.check_strength_label.setText("Strong")
            self.check_strength_label.setStyleSheet(
                "QLabel"
                "{"
                "background-color: green;"
                "color: white;"
                "}")

    # Copy Function
    def copy(self):
        password = self.show_pass.text()
        pyperclip.copy(password)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
