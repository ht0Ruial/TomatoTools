import sys
import codecs
import os
import json

from PyQt5.QtWidgets import QApplication, QWidget, QFontDialog, QMenu, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import pyqtSlot, Qt

from Crypto_func import *
from functools import partial
from GUI.ui_QWFormDoc import Ui_QWFormDoc


# 导入自定义加解密插件
with open("./Plug/config.json", 'r+', encoding='utf-8') as f:
    Crypto_json = json.load(f)
for i in Crypto_json['Plug']:
    for j in Crypto_json['Plug'][i]:
        str1 = "from Plug.{type}.{crypto_name} import {crypto_name}".format(
            type=i, crypto_name=j["crypto_name"])
        exec(str1)


class QmyFormDoc(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_QWFormDoc()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        self.setWindowTitle("New")  # 窗口标题
        self.setWindowIcon(QIcon("./GUI/images/1.png"))
        self.setAttribute(Qt.WA_DeleteOnClose)  # MDI子窗口会被自动删除

        self.__currentFile = ""  # 当前文件名
        self.__fileOpened = False  # 是否已打开文件

        self.createContextMenu()

    def showContextMenu(self, pos):
        self.menuList.exec(QCursor.pos())


# ==============自定义功能函数============

    def loadFromFile(self, aFileName):  # 打开文件
        aFile = codecs.open(aFileName, encoding='utf-8')
        try:
            for eachLine in aFile:  # 每次读取一行
                self.ui.plainTextEdit.appendPlainText(eachLine.rstrip())
        finally:
            aFile.close()

        self.__currentFile = aFileName
        self.__fileOpened = True

        baseFilename = os.path.basename(aFileName)  # 去掉目录后的文件名
        self.setWindowTitle(baseFilename)

    def currentFileName(self):  # 返回当前文件名
        return self.__currentFile

    def isFileOpened(self):  # 文件是否打开
        return self.__fileOpened

    def textSetFont(self):  # 设置字体
        self.setWindowIcon(QIcon("./GUI/images/7.png"))
        iniFont = self.ui.plainTextEdit.font()  # 获取文本框的字体
        font, OK = QFontDialog.getFont(iniFont)  # 选择字体, 注意与C++版本不同
        if (OK):  # 选择有效
            self.ui.plainTextEdit.setFont(font)


# =============自定义槽函数===============================
    def createContextMenu(self):

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.menuList = QMenu(self)  # 创建菜单

        # encode
        encode = self.menuList.addMenu("Encode加密")
        # Base系列加密
        en_baseseries = encode.addMenu("Base系列")
        en_base16 = en_baseseries.addAction("Base16")
        en_base32 = en_baseseries.addAction("Base32")
        en_base64 = en_baseseries.addAction("Base64")
        en_base85 = en_baseseries.addAction("Base85")
        en_base91 = en_baseseries.addAction("Base91")
        en_base92 = en_baseseries.addAction("Base92")
        en_baseOther = en_baseseries.addMenu("只支持输入数字的base编码")
        en_base36 = en_baseOther.addAction("Base36")
        en_base58 = en_baseOther.addAction("Base58")
        en_base62 = en_baseOther.addAction("Base62")

        # rot系列
        en_rots = encode.addMenu("ROT系列")
        en_rot5 = en_rots.addAction("ROT5")
        en_rot13 = en_rots.addAction("ROT13")
        en_rot18 = en_rots.addAction("ROT18")
        en_rot47 = en_rots.addAction("ROT47")

        # 奇奇怪怪的编码
        en_odd = encode.addMenu("奇奇怪怪系列")
        en_AAencode = en_odd.addAction("AAencode")
        en_Brainfuck = en_odd.addAction("Brainfuck")
        # http://www.atoolbox.net/Tool.php?Id=937
        en_Emoji = en_odd.addAction("Emoji")
        # en_Emoji_aes = en_odd.addAction("Emoji-AES") #https://aghorler.github.io/emoji-aes/#
        en_JJencode = en_odd.addAction("JJencode")
        en_JSfuck = en_odd.addAction("JSFuck")
        en_Jother = en_odd.addAction("Jother")
        en_Socialism = en_odd.addAction("核心价值观编码")
        en_Buddha = en_odd.addAction("与佛论禅")

        # 古典密码
        en_Classical = encode.addMenu("古典密码")
        en_Morse = en_Classical.addAction("莫斯密码")
        en_Baconian = en_Classical.addAction("培根密码")
        en_yunyin = en_Classical.addAction("云影密码")
        en_Atbash = en_Classical.addAction("埃特巴什码")
        # en_pig = en_Classical.addAction("猪圈密码")
        # en_Templar = en_Classical.addAction("圣堂武士密码")
        en_Polybius = en_Classical.addAction("波利比奥斯方阵密码")
        en_Caesar = en_Classical.addAction("凯撒密码")
        en_Fence = en_Classical.addAction("栅栏密码")

        ##
        en_Shellcode = encode.addAction("Shellcode")
        en_XXencode = encode.addAction("XXencode")
        en_UUencode = encode.addAction("UUencode")
        en_Handycode = encode.addAction("Handycode")
        en_Url = encode.addAction("URL编码")
        en_Tapcode = encode.addAction("敲击码")
        en_a1z26code = encode.addAction("A1z26密码")
        en_010 = encode.addAction("二进制010编码")
        en_Quoted = encode.addAction("Quoted-printable编码")

        # decode
        decode = self.menuList.addMenu("Decode解密")
        # Base系列解密
        de_baseseries = decode.addMenu("Base系列")
        de_base16 = de_baseseries.addAction("Base16")
        de_base32 = de_baseseries.addAction("Base32")
        de_base36 = de_baseseries.addAction("Base36")
        de_base58 = de_baseseries.addAction("Base58")
        de_base62 = de_baseseries.addAction("Base62")
        de_base64 = de_baseseries.addAction("Base64")
        de_base85 = de_baseseries.addAction("Base85")
        de_base91 = de_baseseries.addAction("Base91")
        de_base92 = de_baseseries.addAction("Base92")

        # rot系列
        de_rots = decode.addMenu("ROT系列")
        de_rot5 = de_rots.addAction("ROT5")
        de_rot13 = de_rots.addAction("ROT13")
        de_rot18 = de_rots.addAction("ROT18")
        de_rot47 = de_rots.addAction("ROT47")

        # 奇奇怪怪的编码
        de_odd = decode.addMenu("奇奇怪怪系列")
        de_AAencode = de_odd.addAction("AAencode")
        de_Brainfuck = de_odd.addAction("Brainfuck")
        # http://www.atoolbox.net/Tool.php?Id=937
        de_Emoji = de_odd.addAction("Emoji")
        # de_Emoji_aes = de_odd.addAction("Emoji-AES") #https://aghorler.github.io/emoji-aes/#
        de_JJencode = de_odd.addAction("JJencode")
        de_JSfuck = de_odd.addAction("JSFuck")
        de_Jother = de_odd.addAction("Jother")
        de_Socialism = de_odd.addAction("核心价值观编码")
        de_Buddha = de_odd.addAction("与佛论禅")

        # 古典密码
        de_Classical = decode.addMenu("古典密码")
        de_Morse = de_Classical.addAction("莫斯密码")
        de_Baconian = de_Classical.addAction("培根密码")
        de_yunyin = de_Classical.addAction("云影密码")
        de_Atbash = de_Classical.addAction("埃特巴什码")
        # de_pig = de_Classical.addAction("猪圈密码")
        # de_Templar = de_Classical.addAction("圣堂武士密码")
        de_Polybius = de_Classical.addAction("波利比奥斯方阵密码")
        de_Caesar = de_Classical.addAction("凯撒密码")
        de_Fence = de_Classical.addAction("栅栏密码")

        ##
        de_Shellcode = decode.addAction("Shellcode")
        de_XXencode = decode.addAction("XXencode")
        de_UUencode = decode.addAction("UUencode")
        de_Handycode = decode.addAction("Handycode")
        de_Url = decode.addAction("URL解码")
        de_Tapcode = decode.addAction("敲击码")
        de_a1z26code = decode.addAction("A1z26密码")
        de_010 = decode.addAction("二进制010编码")
        de_Quoted = decode.addAction("Quoted-printable编码")

        # Plug插件
        plug = self.menuList.addMenu("Plug插件")
        plug_encode = plug.addMenu("Encode")
        plug_decode = plug.addMenu("Decode")

        # 加载json
        with open("./Plug/config.json", 'r+', encoding='utf-8') as f:
            self.Crypto_json = json.load(f)

        # 添加自定义加解密插件及其信号
        for i in self.Crypto_json['Plug']:
            for j in self.Crypto_json['Plug'][i]:
                for k in "key", "replace":
                    if k not in j:
                        j[k] = False
                exec("{crypto_name} = plug_{i}.addAction(\"{name}\")".format(
                    crypto_name=j["crypto_name"], i=i, name=j["name"]))
                exec("{crypto_name}.triggered.connect(partial(self.trig_func,\"{crypto_name}\",{key},\"{i}\",{replace}))".format(
                    crypto_name=j["crypto_name"], key=j["key"], i=i, replace=j["replace"]))

        # 信号
        # encode信号
        en_base16.triggered.connect(
            lambda: self.trig_func("en_base16", False, "encode", False))
        en_base32.triggered.connect(
            lambda: self.trig_func("en_base32", False, "encode", False))
        en_base64.triggered.connect(
            lambda: self.trig_func("en_base64", False, "encode", False))
        en_base85.triggered.connect(
            lambda: self.trig_func("en_base85", False, "encode", False))
        en_base91.triggered.connect(
            lambda: self.trig_func("en_base91", False, "encode", False))
        en_base92.triggered.connect(
            lambda: self.trig_func("en_base92", False, "encode", False))
        en_base36.triggered.connect(
            lambda: self.trig_func("en_base36", False, "encode", False))
        en_base58.triggered.connect(
            lambda: self.trig_func("en_base58", False, "encode", False))
        en_base62.triggered.connect(
            lambda: self.trig_func("en_base62", False, "encode", False))

        en_rot5.triggered.connect(
            lambda: self.trig_func("rot5", False, "encode", False))
        en_rot13.triggered.connect(
            lambda: self.trig_func("rot13", False, "encode", False))
        en_rot18.triggered.connect(
            lambda: self.trig_func("rot18", False, "encode", False))
        en_rot47.triggered.connect(
            lambda: self.trig_func("rot47", False, "encode", False))

        # 奇奇怪怪系列
        en_AAencode.triggered.connect(
            lambda: self.trig_func("en_AAencode", False, "encode", False))
        en_Brainfuck.triggered.connect(
            lambda: self.trig_func("en_Brainfuck", False, "encode", False))
        en_Emoji.triggered.connect(
            lambda: self.trig_func("en_Emoji", False, "encode", False))
        # en_Emoji_aes.triggered.connect(lambda: self.trig_func("en_Emoji_aes",True,"encode", False))
        en_JJencode.triggered.connect(
            lambda: self.trig_func("en_JJencode", False, "encode", False))
        en_JSfuck.triggered.connect(
            lambda: self.trig_func("en_JSfuck", False, "encode", False))
        en_Jother.triggered.connect(
            lambda: self.trig_func("en_Jother", False, "encode", False))
        en_Socialism.triggered.connect(
            lambda: self.trig_func("en_Socialism", False, "encode", False))
        en_Buddha.triggered.connect(
            lambda: self.trig_func("en_Buddha", False, "encode", False))

        #
        en_Shellcode.triggered.connect(
            lambda: self.trig_func("en_Shellcode", False, "encode", False))
        en_XXencode.triggered.connect(
            lambda: self.trig_func("en_XXencode", False, "encode", False))
        en_UUencode.triggered.connect(
            lambda: self.trig_func("en_UUencode", False, "encode", False))
        en_Handycode.triggered.connect(
            lambda: self.trig_func("en_Handycode", False, "encode", False))
        en_Tapcode.triggered.connect(
            lambda: self.trig_func("en_Tapcode", False, "encode", False))
        en_Morse.triggered.connect(
            lambda: self.trig_func("en_Morse", False, "encode", False))
        en_Baconian.triggered.connect(
            lambda: self.trig_func("en_Baconian", False, "encode", False))
        en_yunyin.triggered.connect(
            lambda: self.trig_func("en_yunyin", False, "encode", False))
        en_Atbash.triggered.connect(
            lambda: self.trig_func("en_Atbash", False, "encode", False))

        en_Polybius.triggered.connect(
            lambda: self.trig_func("en_Polybius", False, "encode", False))
        en_Quoted.triggered.connect(
            lambda: self.trig_func("en_Quoted", False, "encode", False))
        en_Caesar.triggered.connect(
            lambda: self.trig_func("en_Caesar", True, "encode", False))
        en_Fence.triggered.connect(
            lambda: self.trig_func("en_Fence", True, "encode", False))
        en_a1z26code.triggered.connect(
            lambda: self.trig_func("en_a1z26code", False, "encode", False))
        en_010.triggered.connect(
            lambda: self.trig_func("en_010", False, "encode", False))
        en_Url.triggered.connect(
            lambda: self.trig_func("en_Url", False, "encode", False))

        # decode信号
        de_base16.triggered.connect(lambda: self.trig_func(
            "de_base16", False, "decode", False))
        de_base32.triggered.connect(lambda: self.trig_func(
            "de_base32", False, "decode", False))
        de_base36.triggered.connect(lambda: self.trig_func(
            "de_base36", False, "decode", False))
        de_base58.triggered.connect(lambda: self.trig_func(
            "de_base58", False, "decode", False))
        de_base62.triggered.connect(lambda: self.trig_func(
            "de_base62", False, "decode", False))
        de_base64.triggered.connect(lambda: self.trig_func(
            "de_base64", False, "decode", False))
        de_base85.triggered.connect(lambda: self.trig_func(
            "de_base85", False, "decode", False))
        de_base91.triggered.connect(lambda: self.trig_func(
            "de_base91", False, "decode", False))
        de_base92.triggered.connect(lambda: self.trig_func(
            "de_base92", False, "decode", False))

        de_rot5.triggered.connect(
            lambda: self.trig_func("rot5", False, "decode", False))
        de_rot13.triggered.connect(
            lambda: self.trig_func("rot13", False, "decode", False))
        de_rot18.triggered.connect(
            lambda: self.trig_func("rot18", False, "decode", False))
        de_rot47.triggered.connect(
            lambda: self.trig_func("rot47", False, "decode", False))

        # 奇奇怪怪系列
        de_AAencode.triggered.connect(lambda: self.trig_func(
            "de_AAencode", False, "decode", False))
        de_Brainfuck.triggered.connect(lambda: self.trig_func(
            "de_Brainfuck", False, "decode", False))
        de_Emoji.triggered.connect(lambda: self.trig_func(
            "de_Emoji", False, "decode", False))
        # de_Emoji_aes.triggered.connect(lambda: self.trig_func("de_Emoji_aes",True,"decode"))
        de_JJencode.triggered.connect(lambda: self.trig_func(
            "de_JJencode", False, "decode", False))
        de_JSfuck.triggered.connect(lambda: self.trig_func(
            "de_JSfuck", False, "decode", False))
        de_Jother.triggered.connect(lambda: self.trig_func(
            "de_Jother", False, "decode", False))
        de_Socialism.triggered.connect(lambda: self.trig_func(
            "de_Socialism", False, "decode", False))
        de_Buddha.triggered.connect(lambda: self.trig_func(
            "de_Buddha", False, "decode", False))

        #
        de_Shellcode.triggered.connect(lambda: self.trig_func(
            "de_Shellcode", False, "decode", False))
        de_XXencode.triggered.connect(lambda: self.trig_func(
            "de_XXencode", False, "decode", False))
        de_UUencode.triggered.connect(lambda: self.trig_func(
            "de_UUencode", False, "decode", False))
        de_Handycode.triggered.connect(lambda: self.trig_func(
            "de_Handycode", False, "decode", False))
        de_Tapcode.triggered.connect(lambda: self.trig_func(
            "de_Tapcode", False, "decode", False))
        de_Morse.triggered.connect(lambda: self.trig_func(
            "de_Morse", False, "decode", True))
        de_Baconian.triggered.connect(lambda: self.trig_func(
            "de_Baconian", False, "decode", False))
        de_yunyin.triggered.connect(lambda: self.trig_func(
            "de_yunyin", False, "decode", False))
        de_Atbash.triggered.connect(lambda: self.trig_func(
            "de_Atbash", False, "decode", False))

        de_Polybius.triggered.connect(lambda: self.trig_func(
            "de_Polybius", False, "decode", False))
        de_Quoted.triggered.connect(lambda: self.trig_func(
            "de_Quoted", False, "decode", False))
        de_Caesar.triggered.connect(lambda: self.trig_func(
            "de_Caesar", False, "decode", False))
        de_Fence.triggered.connect(lambda: self.trig_func(
            "de_Fence", False, "decode", False))
        de_a1z26code.triggered.connect(lambda: self.trig_func(
            "de_a1z26code", False, "decode", True))
        de_010.triggered.connect(lambda: self.trig_func(
            "de_010", False, "decode", True))
        de_Url.triggered.connect(lambda: self.trig_func(
            "de_Url", False, "decode", False))

# =============自定义加解密函数===============================
    # 槽函数
    def trig_func(self, cryp, key_status, type, replace_status):
        en_de = {"en": "加密", "de": "解密"}
        cryptostr = self.ui.plainTextEdit.toPlainText()
        if cryptostr == '':
            QMessageBox.about(self, "温馨提示", "请输入内容！！")
            return 0
        try:

            # 处理字符串
            if self.Crypto_json['G_S_Replace'] and replace_status:
                search_value = QInputDialog.getText(self, "温馨提示", "要查找的字符")[0]
                replace_value = QInputDialog.getText(self, "温馨提示", "替换为")[0]
                cryptostr = cryptostr.replace(search_value, replace_value)

            if key_status:
                value = QInputDialog.getText(self, "温馨提示", "输入keyword")[0]
                result = (globals().get("{}".format(cryp))
                          (cryptostr, value)).decode()
            else:
                result = (globals().get("{}".format(cryp))(cryptostr)).decode()

            if len(result) != 0 and result[:3] != "[-]":
                self.ui.plainTextEdit.setPlainText(result)
                QMessageBox.about(
                    self, "温馨提示", "{}成功！！".format(en_de[type[:2]]))
            elif result[:3] != "[-]":
                QMessageBox.about(
                    self, "温馨提示", "{}失败！！".format(en_de[type[:2]]))
            else:
                QMessageBox.about(self, "温馨提示", "无法请求在线接口，请检查您的网络状态！")
        except:
            QMessageBox.about(self, "温馨提示", "{}失败！！".format(en_de[type[:2]]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = QmyFormDoc()
    form.show()
    sys.exit(app.exec_())
