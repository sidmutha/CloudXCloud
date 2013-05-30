# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front1.ui'
#
# Created: Sat Mar 16 18:59:34 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import os
import dropbox_down #will import and also request for authetication at the same time
import drive_down #only import, not authenticate
drive_service = drive_down.grunt_work() #this will request for the authentication
global drivList
class Ui_Form(object):
    #drvList = object
    def btnUDrive_clicked(self):
        print "aaaaaaaaaaaa"
        print(self.lineEdit.text())
        drive_down.upload_file(self.lineEdit.text()[7::], drive_service)       
        self.populateDriveList()
        print "Done!"
     
    def populateDbxList(self):
        self.l_dbx.clear()
        l = dropbox_down.list_filenames('/')
        #fnames, isdir = zip(*l) 
        for f in l:
            it = QtGui.QListWidgetItem(f[0][1::])
            if f[1]:
                it.setIcon(QtGui.QIcon(r"dbx.ico")) 
            else:
                it.setIcon(QtGui.QIcon(r"file.ico"))
            self.l_dbx.addItem(it)
                    
            #self.l_dbx.addItem(f[1::])
        #self.l_dbx.addItems(fnames)
        self.setProgressbarValue(self.progressBar_2, dropbox_down.get_space())
        
    def btnUDbx_clicked(self):
        ll = self.lineEdit.text()[7::]
        dropbox_down.upload_file(ll, (ll.split('/'))[-1])
        print(ll.split('/'))
        self.populateDbxList()
   
    def downloadDbxItem(self):#download current item selected in dbx list
        item = self.l_dbx.currentItem().text()
        dropbox_down.download_file(item, item)
        return item
        
    def deleteDbxItem(self):
        item = self.l_dbx.currentItem().text()
        dropbox_down.delete_file(item)
        self.populateDbxList()
       
    def deleteDriveItem(self):
        i = self.l_drive.currentRow()
        
        item = drivList[i]
        fId = item[3]
        drive_down.delete_file(fId, drive_service)
        self.populateDriveList()

    def setProgressbarValue(self, progressBar, valuePair):
        progressBar.setProperty("value", valuePair[0]*100.0/valuePair[1])
    
    
    def x2r(self):
        temp = self.downloadDbxItem()
        drive_down.upload_file(temp, drive_service)
        self.populateDriveList()
        os.remove(temp)
    
    def r2x(self):
        temp = self.downloadDriveItem()
        dropbox_down.upload_file(temp,temp)
        self.populateDbxList()
        os.remove(temp)
        
    def populateDriveList(self):
        self.l_drive.clear()
        global drivList
        drivList = drive_down.list_in_root(drive_service)
        for k in drivList:
            it = QtGui.QListWidgetItem(k[0])
            if k[2]:
                it.setIcon(QtGui.QIcon(r"drv.ico"))
            else:
                 it.setIcon(QtGui.QIcon(r"file.ico"))
            self.l_drive.addItem(it)
        self.setProgressbarValue(self.progressBar, drive_down.get_space(drive_service))
        
    
    def downloadDriveItem(self):
        i = self.l_drive.currentRow()
        item = drivList[i]
        download_url = item[4]
        if download_url:
            resp, content = drive_service._http.request(download_url)
            if resp.status == 200:
                with open(item[0], 'w') as fil:
                    fil.write(content)
                    print fil
            else:
                print 'An error! %s' % resp
        else:
            print 'No URL'
        return item[0]
    
    def showDialog(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(None, 'Open file', '/home/sid/')
        self.lineEdit.setText("file://" + fname)
        
    
    def setupUi(self, Form):
        drivList = object
        Form.setObjectName("Form")
        Form.resize(761, 578)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        
        class lwidget_drive(QtGui.QListWidget):
            def __init__(self,type, parent=None):#type?
                super(lwidget_drive, self).__init__(parent)
                self.setAcceptDrops(True)
                self.setDragEnabled(True)

            def dragEnterEvent(self, e):
                    
                #if e.mimeData().hasFormat('text/plain'):
                    e.accept()
                #else:
                 #   e.ignore() 
            def dragMoveEvent(self, event):
                if event.mimeData().hasText:
                    event.accept()
            def dropEvent(self, e):
                if e.mimeData().hasText:
                    #self.addItem(e.mimeData().text()) #this line is not needed really
                    e.setDropAction(QtCore.Qt.CopyAction)
                    drive_down.upload_file(e.mimeData().text()[7::], drive_service)#call upload function with e.mimeData().text()
                    #self.populateDriveList()
                    self.clear()
                    drivList = drive_down.list_in_root(drive_service)
                    for k in drivList:
                        it = QtGui.QListWidgetItem(k[0])
                        if k[2]:
                            it.setIcon(QtGui.QIcon(r"drv.ico"))
                        else:
                            it.setIcon(QtGui.QIcon(r"file.ico"))
                        self.addItem(it)
                    e.accept()
            def popu(self):
                   self.clear()
                   drivList = drive_down.list_in_root(drive_service)
                   for k in drivList:
                       it = QtGui.QListWidgetItem(k[0])
                       if k[2]:
                           it.setIcon(QtGui.QIcon(r"drv.ico"))
                       else:
                           it.setIcon(QtGui.QIcon(r"file.ico"))
                   self.addItem(it)
                           
                    #TODO:now call the fuction to repopulate the list
        
            
        self.l_drive = lwidget_drive(self.groupBox_3)
        self.verticalLayout_2.addWidget(self.l_drive)
        self.progressBar = QtGui.QProgressBar(self.groupBox_3)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnDDrive = QtGui.QPushButton(self.groupBox_3)
        self.btnDDrive.setObjectName("btnDDrive")
        self.horizontalLayout_5.addWidget(self.btnDDrive)
        self.btnUDrive = QtGui.QPushButton(self.groupBox_3)
        self.btnUDrive.setObjectName("btnUDrive")
        self.horizontalLayout_5.addWidget(self.btnUDrive)
        self.btnDelDrive = QtGui.QPushButton(self.groupBox_3)
        self.btnDelDrive.setObjectName("btnDelDrive")
        self.horizontalLayout_5.addWidget(self.btnDelDrive)
        self.btn_r2x = QtGui.QPushButton(self.groupBox_3)
        self.btn_r2x.setObjectName("btn_r2x")
        self.horizontalLayout_5.addWidget(self.btn_r2x)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        #DropBox listWidget
        class lwidget_dbx(QtGui.QListWidget):
            def __init__(self,type, parent=None):#type?
                super(lwidget_dbx, self).__init__(parent)
                self.setAcceptDrops(True)
                self.setDragEnabled(True)

            def dragEnterEvent(self, e):
                    
                #if e.mimeData().hasFormat('text/plain'):
                    e.accept()
                #else:
                 #   e.ignore() 
            def dragMoveEvent(self, event):
                if event.mimeData().hasText:
                    event.accept()
            def dropEvent(self, e):
                if e.mimeData().hasText:
                    #self.addItem(e.mimeData().text()) #this line is not needed really
                    e.setDropAction(QtCore.Qt.CopyAction)
                    mm = e.mimeData().text()[7::]
                    print mm
                    dropbox_down.upload_file(mm, mm.split('/')[-1]) 
                    #self.populateDbxList()
                    self.clear()
                    l = dropbox_down.list_filenames('/')
                    #fnames, isdir = zip(*l)
                    for f in l:
                        it = QtGui.QListWidgetItem(f[0][1::])
                        if f[1]:
                            it.setIcon(QtGui.QIcon(r"dbx.ico"))
                        else:
                            it.setIcon(QtGui.QIcon(r"file.ico"))
                        self.addItem(it)
                    
                    e.accept()
                    
            def popu(self):
                self.clear()
                l = dropbox_down.list_filenames('/')
                    #fnames, isdir = zip(*l)
                for f in l:
                    it = QtGui.QListWidgetItem(f[0][1::])
                    if f[1]:
                        it.setIcon(QtGui.QIcon(r"dbx.ico"))
                    else:
                        it.setIcon(QtGui.QIcon(r"file.ico"))
                    self.addItem(it)
                        
        self.l_dbx = lwidget_dbx(self.groupBox_2)

        self.verticalLayout_3.addWidget(self.l_dbx)
        
        self.progressBar_2 = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.verticalLayout_3.addWidget(self.progressBar_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_x2r = QtGui.QPushButton(self.groupBox_2)
        self.btn_x2r.setObjectName("btn_x2r")
        self.horizontalLayout_6.addWidget(self.btn_x2r)
        self.btnDDbx = QtGui.QPushButton(self.groupBox_2)
        self.btnDDbx.setObjectName("btnDDbx")
        self.horizontalLayout_6.addWidget(self.btnDDbx)
        self.btnUDbx = QtGui.QPushButton(self.groupBox_2)
        self.btnUDbx.setObjectName("btnUDbx")
        self.horizontalLayout_6.addWidget(self.btnUDbx)
        self.btnDelDbx = QtGui.QPushButton(self.groupBox_2)
        self.btnDelDbx.setObjectName("btnDelDbx")
        self.horizontalLayout_6.addWidget(self.btnDelDbx)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setAcceptDrops(True)
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        #self.listWidget_3 = QtGui.QListWidget(self.groupBox)
        #self.listWidget_3.setAcceptDrops(True)
        #self.listWidget_3.setObjectName("listWidget_3")
        #self.verticalLayout_4.addWidget(self.listWidget_3)
        class lwidget_magic(QtGui.QListWidget):
            def __init__(self,type, parent=None):#type?
                super(lwidget_magic, self).__init__(parent)
                self.setAcceptDrops(True)
                self.setDragEnabled(True)

            def dragEnterEvent(self, e):
                    
                #if e.mimeData().hasFormat('text/plain'):
                    e.accept()
                #else:
                 #   e.ignore() 
            def dragMoveEvent(self, event):
                if event.mimeData().hasText:
                    event.accept()
            def dropEvent(self, e):
                if e.mimeData().hasText:
                    e.setDropAction(QtCore.Qt.CopyAction)
                    sysPath = e.mimeData().text()[7::]
                    self.addItem(QtGui.QListWidgetItem(QtGui.QIcon(r'file.ico'), sysPath.split('/')[-1]))
                    size = os.path.getsize(sysPath)
                    
                    dbxUsed, dbxTot = dropbox_down.get_space()
                    drvUsed, drvTot = drive_down.get_space(drive_service)
                    freeDbx = dbxTot - dbxUsed
                    freeDrv = drvTot - drvUsed
                    
                    if size < freeDbx:
                        dropbox_down.upload_file(sysPath, sysPath.split('/')[-1])
                       # l_dbx.popu()
                    elif size < freeDrv:
                        drive_down.upload_file(sysPath, drive_service)
                       # l_drive.popu()
                    else:
                        pass
                    
#this line is not needed really
                    #call upload function with e.mimeData().text()
                    e.accept()
            
        self.l_magic = lwidget_magic(self.groupBox_3)
        self.verticalLayout_4.addWidget(self.l_magic)
        #self.progressBar_3 = QtGui.QProgressBar(self.groupBox)
        #self.progressBar_3.setProperty("value", 24)
        #self.progressBar_3.setObjectName("progressBar_3")
        #self.verticalLayout_4.addWidget(self.progressBar_3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
       # self.pushButton_9 = QtGui.QPushButton(self.groupBox)
        #self.pushButton_9.setObjectName("pushButton_9")
       # self.horizontalLayout_7.addWidget(self.pushButton_9)
        self.pushButton_4 = QtGui.QPushButton(self.groupBox)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_7.addWidget(self.pushButton_4)
        #self.pushButton_10 = QtGui.QPushButton(self.groupBox)
        #self.pushButton_10.setObjectName("pushButton_10")
        #self.horizontalLayout_7.addWidget(self.pushButton_10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.groupBox)
        
        #openFile = QtGui.QAction(QtGui.QIcon(r'drv.ico'), 'Open', self)
            
        self.retranslateUi(Form)
        #---some initial functions
        self.populateDbxList()
        self.populateDriveList()
        #self.setProgressbarValue(self.progressBar, drive_down.get_space(drive_service))
        #----connections----
        self.pushButton.clicked.connect(self.showDialog)
        self.btnUDrive.clicked.connect(self.btnUDrive_clicked)
        self.btnUDbx.clicked.connect(self.btnUDbx_clicked)
        self.btnDDbx.clicked.connect(self.downloadDbxItem)
        self.btnDDrive.clicked.connect(self.downloadDriveItem)
        self.btnDelDbx.clicked.connect(self.deleteDbxItem)
        self.btnDelDrive.clicked.connect(self.deleteDriveItem)
        self.btn_r2x.clicked.connect(self.r2x)
        self.btn_x2r.clicked.connect(self.x2r)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        
        
        
            
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "CxC", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Form", "Google Drive", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDDrive.setText(QtGui.QApplication.translate("Form", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUDrive.setText(QtGui.QApplication.translate("Form", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelDrive.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_r2x.setText(QtGui.QApplication.translate("Form", "-->", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Dropbox", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_x2r.setText(QtGui.QApplication.translate("Form", "<--", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDDbx.setText(QtGui.QApplication.translate("Form", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUDbx.setText(QtGui.QApplication.translate("Form", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelDbx.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "&Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Magic", None, QtGui.QApplication.UnicodeUTF8))
       # self.pushButton_9.setText(QtGui.QApplication.translate("Form", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Form", "&Magic Upload", None, QtGui.QApplication.UnicodeUTF8))
       # self.pushButton_10.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))

#-------defining functions----
    


#--------main method-----
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

