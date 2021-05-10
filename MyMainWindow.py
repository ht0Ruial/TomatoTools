import sys,os
import json
from PyQt5.QtWidgets import  QApplication, QMainWindow,QFileDialog,QMdiArea,QMessageBox

from PyQt5.QtCore import  pyqtSlot, Qt
from PyQt5.QtGui import  QIcon

from GUI.ui_MainWindow import Ui_MainWindow

from About import QmyAbout
from AddPlug import QmyAddPlug
from AutoGetFlag import QmyGetFlag
from CipherAnalyse import QmyCipher
from MyFormDoc import QmyFormDoc


class QmyMainWindow(QMainWindow):

   def __init__(self, parent=None):
      super().__init__(parent)   #调用父类构造函数，创建窗体
      self.ui=Ui_MainWindow()    #创建UI对象
      self.ui.setupUi(self)      #构造UI界面
      self.setWindowIcon(QIcon("./GUI/images/0.png"))
      self.setCentralWidget(self.ui.mdiArea)    #填充满工作区
      # self.setWindowState(Qt.WindowMaximized) #窗口最大化显示
      self.ui.mainToolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

      self.ui.actCipher_Analyse.setEnabled(True)   #启用action
      self.ui.actAuto_Flag.setEnabled(True)
      self.ui.actCipher_Plug.setEnabled(True)


##  ==============事件处理函数===================
   def closeEvent(self, event):
      reply = QMessageBox.question(self,'温馨提示','你确定要退出吗？',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
      if reply == QMessageBox.Yes:
         self.ui.mdiArea.closeAllSubWindows()   #关闭所有子窗口
         event.accept()
      else:
         event.ignore()


##  ==============自定义功能函数============
   def __enableEditActions(self,enabled):
      self.ui.actEdit_Font.setEnabled(enabled)
      self.ui.actDoc_CloseALL.setEnabled(enabled)
        
        
##  ==========由connectSlotsByName() 自动连接的槽函数==================        
   @pyqtSlot()    ##新建
   def on_actDoc_New_triggered(self):
      formDoc = QmyFormDoc(self)
      self.ui.mdiArea.addSubWindow(formDoc)   #文档窗口添加到MDI
      formDoc.show()    #在单独的窗口中显示
      self.__enableEditActions(True)

   @pyqtSlot()    ##打开
   def on_actDoc_Open_triggered(self): 
      needNew=False   # 是否需要新建子窗口
      if len(self.ui.mdiArea.subWindowList())>0: #如果有打开的MDI窗口，获取活动窗口
         formDoc=self.ui.mdiArea.activeSubWindow().widget()
         needNew=formDoc.isFileOpened()   #文件已经打开，需要新建窗口
      else:
         needNew=True

      curPath=os.getcwd()  #获取当前路径
      filename=QFileDialog.getOpenFileName(self,"打开一个文件",curPath,
                  "文本文件(*.txt);;所有文件(*.*)")[0]
      if (filename==""):
         return

      if(needNew):
         formDoc = QmyFormDoc(self)    #必须指定父窗口
         self.ui.mdiArea.addSubWindow(formDoc)  #添加到MDI区域
        
      formDoc.loadFromFile(filename)
      formDoc.show()
      self.__enableEditActions(True)
        

   @pyqtSlot()    ##关闭全部
   def on_actDoc_CloseALL_triggered(self):
      reply = QMessageBox.question(self,'温馨提示','你确定要关闭全部吗？',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
      if reply == QMessageBox.Yes:
         self.ui.mdiArea.closeAllSubWindows()

   @pyqtSlot(bool)      ##MDI模式
   def on_actMDI_Mode_triggered(self,checked):
      if checked:     #Tab多页显示模式
         self.ui.mdiArea.setViewMode(QMdiArea.TabbedView)    #Tab多页显示模式
         self.ui.mdiArea.setTabsClosable(True)       #页面可关闭
         self.ui.actMDI_Cascade.setEnabled(False)
         self.ui.actMDI_Tile.setEnabled(False)
      else:       #子窗口模式
         self.ui.mdiArea.setViewMode(QMdiArea.SubWindowView)   #子窗口模式
         self.ui.actMDI_Cascade.setEnabled(True)
         self.ui.actMDI_Tile.setEnabled(True)

   @pyqtSlot()    ##级联展开
   def on_actMDI_Cascade_triggered(self):
      self.ui.mdiArea.cascadeSubWindows()
        
   @pyqtSlot()    ##平铺展开
   def on_actMDI_Tile_triggered(self):  
      self.ui.mdiArea.tileSubWindows()


   @pyqtSlot()    ##密文分析
   def on_actCipher_Analyse_triggered(self):
      formCipher=QmyCipher(self)
      formCipher.setAttribute(Qt.WA_DeleteOnClose)
      formCipher.setWindowTitle("密文分析")
      formCipher.setWindowIcon(QIcon("./GUI/images/4.png"))
      # formCipher.setWindowOpacity(0.9) #透明度
      formCipher.show()
    
   @pyqtSlot()    ##自动提取flag
   def on_actAuto_Flag_triggered(self):
      formAbout=QmyGetFlag(self)
      formAbout.setAttribute(Qt.WA_DeleteOnClose)
      formAbout.setWindowTitle("自动提取flag")
      formAbout.setWindowIcon(QIcon("./GUI/images/5.png"))
      formAbout.show()

   @pyqtSlot()    ##插件
   def on_actCipher_Plug_triggered(self):
      formAbout=QmyAddPlug(self)
      formAbout.setAttribute(Qt.WA_DeleteOnClose)
      formAbout.setWindowTitle("插件")
      formAbout.setWindowIcon(QIcon("./GUI/images/6.png"))
      formAbout.show()

   @pyqtSlot()    ##字体设置
   def on_actEdit_Font_triggered(self):
      formDoc=self.ui.mdiArea.activeSubWindow().widget()
      formDoc.textSetFont()

   @pyqtSlot()    ##关于
   def on_actAbout_triggered(self):
      ##打开新的GUI页面
      formAbout=QmyAbout(self)
      formAbout.setAttribute(Qt.WA_DeleteOnClose)
      formAbout.setWindowTitle("关于")
      formAbout.setWindowIcon(QIcon("./GUI/images/11.png"))
      formAbout.show()

   @pyqtSlot(type)   ##子窗口切换
   def on_mdiArea_subWindowActivated(self,arg1):
      cnt=len(self.ui.mdiArea.subWindowList())
      if (cnt==0):
         self.__enableEditActions(False)
         self.ui.statusBar.clearMessage()
      else:
         formDoc=self.ui.mdiArea.activeSubWindow().widget()
         self.ui.statusBar.showMessage(formDoc.currentFileName()) #显示子窗口的文件名        

        
   
if  __name__ == "__main__":
   app = QApplication(sys.argv)
   form=QmyMainWindow()
   form.show()
   sys.exit(app.exec_())
