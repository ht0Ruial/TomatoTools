# AutoGetFlag.py

# 输入密文  keyword  然后分析  调用CipherAnalyse的分析模块


import sys
import os
import json
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QMovie
from CipherAnalyse import Cipherase
from treelib import Tree, Node
from subprocess import Popen
from Crypto_func import *
from GUI.Ui_GetFlag import Ui_GetFlag

# 添加自定义加解密插件及其
with open("./Plug/config.json", 'r+', encoding='utf-8') as f:
    Crypto_json = json.load(f)
for i in Crypto_json['Plug']:
    for j in Crypto_json['Plug'][i]:
        str1 = "from Plug.{type}.{crypto_name} import {crypto_name}".format(
            type=i, crypto_name=j["crypto_name"])
        exec(str1)

# 将密文和分析的加密函数放到一块


def Crypto_list_str(crypto_ans, cryptostr):
    result = []
    for i in crypto_ans:
        m = []
        m.append(i)  # 分析后的加密类型
        m.append(cryptostr)  # 密文
        result.append(m)
    return result

# 子进程分析识别密文getFlag


class Cipher_Thread(QThread):
    signal = pyqtSignal(str, str, str, bool)

    def __init__(self, cryptostr, keyword, value, log):
        super().__init__()
        self.cryptostr = cryptostr
        self.keyword = keyword
        self.value = value
        self.log = log

    def name_c(self, result):
        with open("./Plug/config.json", 'r', encoding='utf-8') as f:
            Crypto_json = json.load(f)
        # 由result中的crypto_name获取name
        name_result = {}  # {"crypto_name":"name",...}
        for i in result:
            for j in Crypto_json["Base_crypto"]:
                if i == j["crypto_name"]:
                    name_result[j["crypto_name"]] = j["name"]
        return name_result

    def run(self):
        fenxi_result = Cipherase(
            self.cryptostr, self.value)  # 密文分析后的cryptoname
        result = Crypto_list_str(fenxi_result, self.cryptostr)  # 返回识别后的密文列表

        if self.log:
            name_fenxi_result = self.name_c(fenxi_result)  # 将crypto_name转为name

            # 生成第一个父子节点
            FandS_node = []  # 0为父节点，其他为子节点，格式为 [ ["parent","name1","name2"],[...] ]
            temp_FS_node = []

            cry_path = Tree()
            tree = cry_path.create_node(tag='Path',)  # 解密路线树
            for i in name_fenxi_result.values():
                test = cry_path.create_node(tag=i, parent=tree)
                temp_FS_node.append(test.identifier)
                FandS_node.append(temp_FS_node)

        Flag = False  # 判断flag存不存在的关键词
        self.res = ''
        filename = ''
        cry_cryptostr = ''
        while(len(result) != 0 and len(result) < 100):
            # 每轮广度遍历时初始化变量
            temporary = []
            result_dict = {}
            temp_FandS_node = []

            # 获取由 result[i[0]] 与相应的key 组成的字典
            for i in result:
                for j in Crypto_json["Base_crypto"]:
                    if i[0] == j["crypto_name"]:
                        try:
                            result_dict[i[0]] = j["key"]
                            break
                        except:
                            result_dict[i[0]] = 'False'  # key不存在的时候，默认为 False
                            break

            for i in result:
                try:
                    if result_dict[i[0]] == 'True' and self.value != '':
                        self.res = (globals().get(i[0])(
                            i[1], self.value)).decode()  # 调用函数解密
                    else:
                        self.res = (globals().get(i[0])(
                            i[1])).decode()  # 调用函数解密
                    if self.keyword in self.res:
                        Flag = True
                        if self.log:
                            cry_path.create_node(
                                tag=self.res, parent=FandS_node[result.index(i)][0], data=self.res)
                        break
                except:
                    pass

                # 密文分析后的cryptoname
                fenxi_result = Cipherase(self.res, self.value)

                # 不需要导日志则不必要生成crypto_name与name的字典
                temp_FS_node = []
                if self.log and len(FandS_node) != 0:
                    name_fenxi_result = self.name_c(
                        fenxi_result)
                    for j in name_fenxi_result.values():
                        test = cry_path.create_node(
                            tag=j, parent=FandS_node[result.index(i)][0], data=self.res)
                        temp_FS_node.append(test.identifier)
                        temp_FandS_node.append(temp_FS_node)

                temporary.extend(Crypto_list_str(fenxi_result, self.res))

            if Flag:
                break
            result = temporary
            FandS_node = temp_FandS_node

        if self.log:
            len_k = ''
            for k in cry_path.paths_to_leaves():
                if len(k) > len(len_k):
                    len_k = k
            if Flag == False:
                cry_path.create_node(
                    tag=self.keyword + "【无法解密】", parent=len_k[-1])

            # 最长解密链 max_long_cry
            test_m = []
            for m in len_k:
                test_m.append(cry_path.get_node(m).tag)
            if Flag == False:
                test_m.append(self.keyword)
            max_long_cry = ' -> '.join(test_m)

            # 最终密文
            cry_fin = cry_path.get_node(len_k[-1]).data

            cry_path.save2file(
                "./Logs/d59b74dc39de47e8fc67e502beff02e1.txt")

            # 读取解析树
            try:
                with open("./Logs/d59b74dc39de47e8fc67e502beff02e1.txt", "r", encoding="utf-8") as f:
                    cry_tree = f.read()
                os.remove("./Logs/d59b74dc39de47e8fc67e502beff02e1.txt")
            except:
                pass

            # 处理初始密文
            if len(self.cryptostr) > 32:
                cry_cryptostr = self.cryptostr[:16] + \
                    "......"+self.cryptostr[-16:]
            else:
                cry_cryptostr = self.cryptostr

            txt = "\nflag关键词：{}\n\n密钥：{}\n\n初始密文：{}\n\n解析树：\n{}\n最长解密链：\n{}\n\n最终密文：\n{}\n\n最终解密结果：\n{}\n\n".format(
                self.keyword, self.value, cry_cryptostr, cry_tree, max_long_cry, cry_fin, self.res)
            filename = "{}.txt".format(time.strftime(
                "%Y%m%d%H%M%S", time.localtime()))
            with open("./Logs/{}".format(filename), "w", encoding="utf-8") as f:
                f.write(txt)

        self.signal.emit(self.res, self.keyword, filename, self.log)  # 发出信号


class QmyGetFlag(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_GetFlag()
        self.ui.setupUi(self)

        self.__dlgSetHeaders = None
        self.setAutoFillBackground(True)

    @pyqtSlot(str, str, str, bool)
    def hiddengif(self, res, keyword, filename, log):
        self.ui.label.setVisible(False)  # 隐藏label
        self.ui.statusBar.clearMessage()
        if log:
            self.ui.statusBar.showMessage('./Logs/{}'.format(filename))
        if keyword in res:
            self.ui.plainTextEdit.setPlainText(res)
            QMessageBox.about(self, "温馨提示", "恭喜，成功找到  {}  ".format(keyword))
        else:
            QMessageBox.about(self, "温馨提示", "呜呜没有找到  {}  ".format(keyword))
        if log:
            Popen(['notepad', './Logs/{}'.format(filename)])

    @pyqtSlot()  # 自动获取flag
    def on_pushButton_clicked(self):
        cryptostr = self.ui.plainTextEdit.toPlainText()  # 获取密文
        keyword = self.ui.lineEdit.text()  # 获取flag关键词
        value = self.ui.lineEdit_2.text()  # 获取密钥
        if len(cryptostr) == 0 or len(keyword) == 0:
            QMessageBox.about(self, "温馨提示", "内容不能为空！！")
            return 0
        if self.ui.radioButton.isChecked():
            log = True
        else:
            log = False
        self.ui.label.setVisible(True)  # 显示label控件
        # 加载gif
        self.loads = QMovie("./GUI/images/19.gif")
        self.ui.label.setMovie(self.loads)
        self.loads.start()
        # 子线程分析密文
        self.thread = Cipher_Thread(cryptostr, keyword, value, log)
        self.thread.signal.connect(self.hiddengif)
        self.thread.start()    # 启动线程


if __name__ == "__main__":
    app = QApplication(sys.argv)
    formFlag = QmyGetFlag()
    formFlag.show()
    sys.exit(app.exec_())
