import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import EncroManager
import pyperclip


class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Gui.ui", self)
        self.Browse.clicked.connect(self.browse_file)
        self.Browsed = False
        self.fname = None
        self.FileName.setEnabled(False)
        self.Encrypt.clicked.connect(self.EncryptFile)
        self.Decrypt.clicked.connect(self.DecryptFile)
        self.Copy.clicked.connect(self.CopyFile)

    def CopyFile(self):
        self.Error.setText("")
        self.Success.setText("")
        if self.Browsed:
            try:
                if len(self.fname[0][0]) > 3:
                    with open(self.fname[0][0], "r") as file:
                        text = file.read()
                    pyperclip.copy(text)
                    self.Success.setText("Copied file")
                else:
                    self.Error.setText("Please choose a valid file")
            except IndexError:
                self.Error.setText("Please choose a valid file")
        else:
            self.Error.setText("Please choose a valid file")

    def browse_file(self):
        self.Browsed = False
        self.Error.setText("")
        self.Success.setText("")
        print(self.Browsed)
        self.fname = QFileDialog.getOpenFileNames(self, "Open file", "C:\EncroNote", "TXT files (*.txt)")
        self.FileName.setText(f"{self.fname[0]}")
        try:
            if len(self.fname[0][0]) > 2:
                self.Browsed = True
        except IndexError:
            pass

    def EncryptFile(self):
        self.Error.setText("")
        self.Success.setText("")
        if self.Browsed:
            if EncroManager.is_encrypted(self.fname[0][0]):
                self.Error.setText("File is already Encrypted")
            else:
                try:
                    if len(self.fname[0][0]) > 3:
                        EncroManager.encrypt_file(self.fname[0][0])
                        self.Success.setText("Encrypted File")
                    else:
                        self.Error.setText("Please choose a valid file")
                except IndexError:
                    self.Error.setText("Please choose a valid file")
        else:
            self.Error.setText("Please choose a valid file")

    def DecryptFile(self):
        self.Error.setText("")
        self.Success.setText("")
        if self.Browsed:
            if not EncroManager.is_encrypted(self.fname[0][0]):
                self.Error.setText("File is already Decrypted")
            else:
                try:
                    if len(self.fname[0][0]) > 3:
                        EncroManager.decrypt_file(self.fname[0][0])
                        self.Success.setText("Decrypted File")
                    else:
                        self.Error.setText("Please choose a valid file")
                except IndexError:
                    self.Error.setText("Please choose a valid file")
        else:
            self.Error.setText("Please choose a valid file")


if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(800)
    widget.setFixedHeight(800)
    widget.show()
    sys.exit(App.exec_())
