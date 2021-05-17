# AddPlug.py

# GUI 独立程序

# 管理 encode/decode 插件


import sys
import json

from hashlib import md5

from importlib import import_module

from os import getcwd, remove

from shutil import copyfile

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from PyQt5.QtCore import pyqtSlot

from GUI.Ui_Plug import Ui_Plug


class QmyAddPlug(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Plug()
        self.ui.setupUi(self)

        self.__dlgSetHeaders = None
        self.setAutoFillBackground(True)

    # 插件管理

    def Plugss(self, crypto_type, addsub_type):
        lspath = getcwd()  # 当前启动位置
        curPath = getcwd() + "{}".format("\\Plug\\{}\\".format(crypto_type))  # 获取路径
        filename = QFileDialog.getOpenFileName(self, "选择你的{}插件".format(crypto_type), curPath,
                                               "文本文件(*.py)")[0]
        if (filename == ""):
            return

        # 加载json
        with open("./Plug/config.json", 'r+', encoding='utf-8') as f:
            Crypto_json = json.load(f)

        file_ss = filename.rsplit('/')
        modulname = '.{}'.format(file_ss[-1][:-3])

        try:
            # 添加
            if self.ui.radioButton.isChecked():
                file_ss_md5 = '.{}'.format(md5(modulname.encode()).hexdigest())
                lsfilename = "{}\\Plug\\{}.py".format(
                    lspath, file_ss_md5[1:])  # 临时文件
                copyfile(filename, lsfilename)
                test = import_module(file_ss_md5, "Plug")
                remove(lsfilename)  # 删除临时文件

                if test.dicts['crypto_name'] != file_ss[-1][:-3]:
                    QMessageBox.about(self, "添加失败", " 文件名 “{}” 应和 函数名 “{}”保持一致！！".format(
                        modulname[1:], test.dicts['crypto_name']))
                    return
                # 判断是否存在同名crypto_name
                for i in Crypto_json['Plug'][crypto_type]:
                    if test.dicts['crypto_name'] == i['crypto_name']:
                        QMessageBox.about(self, "添加失败", " {} 插件里的 {} 函数已存在，请勿重复添加！！".format(
                            test.dicts['name'], test.dicts['crypto_name']))
                        return

                if crypto_type == "decode":
                    Crypto_json['Base_crypto'].append(test.dicts)
                Crypto_json['Plug'][crypto_type].append(test.dicts)
                with open("./Plug/config.json", 'w+', encoding='utf-8') as f:
                    f.write(json.dumps(Crypto_json))
                try:
                    copyfile(filename, curPath+file_ss[-1])
                except:
                    pass
                QMessageBox.about(
                    self, "添加成功", " {} 插件已成功添加！请自行重启程序！".format(test.dicts['name']))

            # 删除
            else:
                rex_curPath = curPath.replace("\\", '/')
                # 与decode同一目录
                if rex_curPath not in filename:
                    QMessageBox.about(
                        self, "删除失败", "选中的 {} 不是有效插件！！".format(modulname[1:]))
                    return
                test = import_module(modulname, "Plug.{}".format(crypto_type))
                Crypto_json['Plug'][crypto_type].remove(test.dicts)
                if crypto_type == "decode":
                    Crypto_json['Base_crypto'].remove(test.dicts)
                with open("./Plug/config.json", 'w+', encoding='utf-8') as f:
                    f.write(json.dumps(Crypto_json))
                remove(filename)
                QMessageBox.about(
                    self, "删除成功", " {} 插件已成功移除！！".format(test.dicts['name']))
        except:
            QMessageBox.about(self, "温馨提示", " 所选插件格式有误！！")

    @pyqtSlot()  # 选择Encode插件
    def on_pushButton_clicked(self):
        if self.ui.radioButton.isChecked():
            flags = True
        else:
            flags = False
        self.Plugss("encode", flags)

    @pyqtSlot()  # 选择Decode插件
    def on_pushButton_2_clicked(self):
        if self.ui.radioButton.isChecked():
            flags = True
        else:
            flags = False
        self.Plugss("decode", flags)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    formPlug = QmyAddPlug()
    formPlug.show()
    sys.exit(app.exec_())
