#author: Connor Comstock

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Query_Dialog(object):
    """
        Window to display query information
    """
    def __init__(self,window_title,*args,**kwargs):#(*,** take extra parameters, init is constuctor)
        super(Ui_Query_Dialog,self).__init__(*args,**kwargs)#Super.init calls QMainWindow constructor
        self.window_title = window_title
    def setupUi(self, Query_Dialog):
        self.Query_Dialog = Query_Dialog
        Query_Dialog.setObjectName("Query_Dialog")
        Query_Dialog.resize(500, 250)
        self.verticalLayout = QtWidgets.QVBoxLayout(Query_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Query_Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.retranslateUi(Query_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Query_Dialog)

    def retranslateUi(self, Query_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Query_Dialog.setWindowTitle(_translate("Query_Dialog", self.window_title))
    def update_text(self, text):

        #Resize table for text
        #23 is about how much space a line takes up
        lines = len(text.splitlines())
        self.Query_Dialog.resize(500, (lines*23))

        #set text
        self.textBrowser.append(text)
