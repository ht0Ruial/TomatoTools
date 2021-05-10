# GUI应用程序主程序入口

import sys

from PyQt5.QtWidgets import QApplication

from MyMainWindow import QmyMainWindow


app = QApplication(sys.argv)
mainform = QmyMainWindow()
mainform.show()
sys.exit(app.exec_())
