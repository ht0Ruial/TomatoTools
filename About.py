# About.py


import sys
import json
import webbrowser as web

from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtCore import pyqtSlot


from GUI.Ui_About import Ui_About


class QmyAbout(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)
        f = open("./Plug\config.json", 'r', encoding='utf-8')
        self.Crypto_json = json.load(f)
        f.close()
        if self.Crypto_json['G_S_Replace']:
            self.ui.checkBox.setChecked(True)
        if self.Crypto_json['G_S_Crypk']:
            self.ui.checkBox_2.setChecked(True)
        if self.Crypto_json['G_S_Flag']:
            self.ui.checkBox_3.setChecked(True)
        self.__dlgSetHeaders = None
        self.setAutoFillBackground(True)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        web.open("https://github.com/ht0Ruial/TomatoTools")  # 打开项目地址

    @pyqtSlot()
    def on_checkBox_clicked(self):
        with open("./Plug\config.json", 'w+', encoding='utf-8') as f:
            if self.ui.checkBox.isChecked():
                self.Crypto_json['G_S_Replace'] = True
                f.write(json.dumps(self.Crypto_json))
            else:
                self.Crypto_json['G_S_Replace'] = False
                f.write(json.dumps(self.Crypto_json))

    @pyqtSlot()
    def on_checkBox_2_clicked(self):
        with open("./Plug\config.json", 'w+', encoding='utf-8') as f:
            if self.ui.checkBox_2.isChecked():
                self.Crypto_json['G_S_Crypk'] = True
                f.write(json.dumps(self.Crypto_json))
            else:
                self.Crypto_json['G_S_Crypk'] = False
                f.write(json.dumps(self.Crypto_json))

    @pyqtSlot()
    def on_checkBox_3_clicked(self):
        with open("./Plug\config.json", 'w+', encoding='utf-8') as f:
            if self.ui.checkBox_3.isChecked():
                self.Crypto_json['G_S_Flag'] = True
                f.write(json.dumps(self.Crypto_json))
            else:
                self.Crypto_json['G_S_Flag'] = False
                f.write(json.dumps(self.Crypto_json))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    formAbout = QmyAbout()
    formAbout.show()
    sys.exit(app.exec_())
