# About.py


import sys
import os
import webbrowser as web

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMdiArea, QMessageBox

from PyQt5.QtCore import pyqtSlot, Qt


from GUI.Ui_About import Ui_About


class QmyAbout(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)

        self.__dlgSetHeaders = None
        self.setAutoFillBackground(True)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        web.open("https://github.com/ht0Ruial/TomatoTools")  # 打开项目地址


if __name__ == "__main__":
    app = QApplication(sys.argv)
    formAbout = QmyAbout()
    formAbout.show()
    sys.exit(app.exec_())
