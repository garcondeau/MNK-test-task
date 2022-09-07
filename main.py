import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QStatusBar, QComboBox, QProgressBar, QFrame

from connection import connect_ftp
from consts import auth_info
from fileprocess import process_file
from getfile import get_files, download_file
from styles import styled_button, info_label


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.file = ""

        self.setFixedWidth(480)
        self.setFixedHeight(320)
        self.setWindowTitle("MNK test task")

        app_statusbar = QStatusBar(self)
        app_statusbar.resize(self.width(), 40)
        app_statusbar.setStyleSheet("background-color: #71696b")

        ip_label = QLabel(self)
        ip_label.setStyleSheet(info_label)
        ip_label.setText("IP: " + auth_info["FTP_IP"])
        ip_label.setGeometry(20, 5, 100, 30)

        user_label = QLabel(self)
        user_label.setStyleSheet(info_label)
        user_label.setText("USER: " + auth_info["FTP_USER"])
        user_label.setGeometry(150, 5, 100, 30)

        self.login_btn = QPushButton(self)
        self.login_btn.setText("Connect")
        self.login_btn.clicked.connect(self.login_onclick)
        self.login_btn.setGeometry(360, 8, 100, 22)
        self.login_btn.setStyleSheet(styled_button)

        self.file_menu = QComboBox(self)
        self.file_menu.addItem("Choose file")
        self.file_menu.activated[str].connect(self.onActivated)
        self.file_menu.setGeometry(10, 50, 150, 32)
        self.file_menu.setEnabled(False)

        self.fbrowse_btn = QPushButton('Select file', self)
        self.fbrowse_btn.clicked.connect(self.browse_onclick)
        self.fbrowse_btn.setGeometry(360, 50, 100, 30)
        self.fbrowse_btn.setEnabled(False)

        self.download_progress_label = QLabel(self)
        self.download_progress_label.setText("No file chosen")
        self.download_progress_label.setStyleSheet("color:#2774ee")
        self.download_progress_label.setGeometry(18, 100, 100, 30)

        self.download_progress = QProgressBar(self)
        self.download_progress.setGeometry(14, 80, 440, 30)

        self.hseparator = QFrame(self)
        self.hseparator.setFrameShape(QFrame.HLine)
        self.hseparator.setGeometry(0, 140, 480, 1)

        self.process_btn = QPushButton('Process file', self)
        self.process_btn.clicked.connect(self.process_file)
        self.process_btn.setGeometry(14, 160, 100, 30)
        self.process_btn.hide()

    def login_onclick(self):
        connect_ftp(self.fbrowse_btn, self.login_btn, self.file_menu)
        for item in get_files():
            self.file_menu.addItem(item)

    def browse_onclick(self):
        for i in range(100):
            self.download_progress.setValue(i)
        download_file(self.file)
        self.download_progress_label.setStyleSheet("color: #62bb45")
        self.download_progress_label.setText("Done")
        print(self.file)
        if self.file.endswith('.rar'):
            self.process_btn.show()

    def onActivated(self, text):
        self.download_progress_label.setText("Waiting...")
        self.file = text

    def process_file(self):
        process_file(self.file)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
