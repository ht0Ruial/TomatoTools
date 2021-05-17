# GUI 独立程序 密文分析

import sys
import os
import json
from re import compile

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QMovie

from Crypto_func import *
from GUI.Ui_Cipher import Ui_Cipher

# 导入自定义解密插件
with open("./Plug/config.json", 'r+', encoding='utf-8') as f:
    Crypto_json = json.load(f)
for i in Crypto_json['Plug']:
    for j in Crypto_json['Plug'][i]:
        str1 = "from Plug.{type}.{crypto_name} import {crypto_name}".format(
            type=i, crypto_name=j["crypto_name"])
        exec(str1)

# 识别密文


def Cipherase(cryptostr, value):

    redo_crypto = set(cryptostr.replace('\n', '').replace('\r', ''))  # 密文字符去重
    maybe_list = []  # 密文可能在的列表
    maybe_list_name = []  # 密文可能在的列表-名字
    maby_list_name = []  # 密文大概率在的列表，长度与密文表相等-名字
    back_list_name = []  # 不可能的加密方式-名字

    with open("./Plug/config.json", 'r', encoding='utf-8') as f:
        Crypto_json = json.load(f)
    for i in Crypto_json["Base_crypto"]:
        if len(redo_crypto) <= int(i["alphabet_num"]):
            maybe_list.append(i)
            maybe_list_name.append(i["crypto_name"])
        if len(redo_crypto) == int(i["alphabet_num"]):
            maby_list_name.append(i["crypto_name"])

    # 正则匹配密文的每个字符，不在范围内将该加密类型加入黑名单
    for i in maybe_list:
        a = str(i["range"])
        pattern = compile(r'' + a + '')
        for j in redo_crypto:
            if pattern.match(j) == None:
                back_list_name.append(i["crypto_name"])
                break

    # 移除黑名单中的加密类型
    for i in back_list_name:
        maybe_list_name.remove(i)
        try:
            maby_list_name.remove(i)
        except:
            pass

    # 重选
    if len(maby_list_name) != 0:
        # 取 maybe_list_name 与 maby_list_name 的交集
        result_list = list(
            set(maybe_list_name).intersection(set(maby_list_name)))
    else:
        result_list = maybe_list_name
    result = single_decry(result_list, cryptostr, value, Crypto_json)
    return result


def single_decry(result_list, cryptostr, value, Crypto_json):
    # 获取由 result_list 与相应的key 组成的字典
    result_dict = {}
    for i in result_list:
        for j in Crypto_json["Base_crypto"]:
            if i == j["crypto_name"]:
                try:
                    result_dict[i] = j["key"]
                    break
                except:
                    result_dict[i] = 'False'  # key不存在的时候，默认为 False
                    break

    # 看能否正常解密
    for i in result_list:
        try:
            if result_dict[i] == 'True' and value != '':
                res = (globals().get(i)(cryptostr, value)).decode()  # 调用函数解密
            else:
                res = (globals().get(i)(cryptostr)).decode()  # 调用函数解密

            if len(res) != 0 and res[:3] != "[-]" and res != cryptostr:  # 成功返回解密结果
                pass
            else:
                result_list[result_list.index(i)] = ''
        except:
            result_list[result_list.index(i)] = ''
    result = [i for i in result_list if i != '']

    return result


# 子进程分析识别密文


class Cipher_Thread(QThread):
    signal = pyqtSignal(list)

    def __init__(self, cryptostr, value):
        super().__init__()
        self.cryptostr = cryptostr  # 密文
        self.value = value  # 密钥

    def run(self):

        # 识别密文
        self.result = Cipherase(self.cryptostr, self.value)  # 调用函数分析密文

        # 发出信号
        self.signal.emit(self.result)


class QmyCipher(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cipher()
        self.ui.setupUi(self)

        self.__dlgSetHeaders = None
        self.setAutoFillBackground(True)

# ==============自定义功能函数============

    @pyqtSlot(list)
    def Cipherxxx(self, result):
        # 由result中的crypto_name获取name
        with open("./Plug/config.json", 'r', encoding='utf-8') as f:
            Crypto_json = json.load(f)
        name_result = []
        for i in result:
            for j in Crypto_json["Base_crypto"]:
                if i == j["crypto_name"]:
                    name_result.append(j["name"])
        # 隐藏label
        self.ui.label.setVisible(False)

        if len(name_result) == 0:
            QMessageBox.about(self, "温馨提示", "无法识别该密文类型！！")
        else:
            self.ui.plainTextEdit.setPlainText(
                "可能的密文类型："+"\n\n"+'\n'.join(name_result))
            QMessageBox.about(self, "温馨提示", "已经识别出密文类型！！")

    @pyqtSlot()
    def on_pushButton_clicked(self):
        cryptostr = self.ui.plainTextEdit.toPlainText()  # 获取密文
        value = self.ui.lineEdit_2.text()  # 获取密钥
        if len(cryptostr) != 0:
            self.ui.label.setVisible(True)  # 显示label控件
            # 加载gif
            self.loads = QMovie("./GUI/images/20.gif")
            self.ui.label.setMovie(self.loads)
            self.loads.start()
            # 子线程分析密文
            self.thread = Cipher_Thread(cryptostr, value)
            self.thread.signal.connect(self.Cipherxxx)
            self.thread.start()    # 启动线程

        else:
            QMessageBox.about(self, "温馨提示", "请输入密文！！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = QmyCipher()
    form.show()
    sys.exit(app.exec_())
