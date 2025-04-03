#author: Connor Comstock

from PyQt5 import QtCore, QtGui, QtWidgets
import databaseManager


class Ui_Table_Dialog(object):
    """
        Window to display table information
    """
    def __init__(self,window_title,*args,**kwargs):#(*,** take extra parameters, init is constuctor)
        super(Ui_Table_Dialog,self).__init__(*args,**kwargs)#Super.init calls QMainWindow constructor
        self.dbm = databaseManager.DatabaseMangaer("airport")
        self.window_title = window_title
    def setupUi(self, Table_Dialog):
        self.Table_Dialog = Table_Dialog
        Table_Dialog.setObjectName("Table_Dialog")
        Table_Dialog.resize(600, 400)
        self.gridLayout = QtWidgets.QGridLayout(Table_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(Table_Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Table_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Table_Dialog)

    def retranslateUi(self, Table_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Table_Dialog.setWindowTitle(_translate("Table_Dialog", self.window_title))

    def update_table(self, query):
        #Updates windows table
        data = self.run_query(query)

        if len(data) == 0:#Tests for an empty query
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("No Data"))
            return
        #Set table size
        rowCount = len(data)
        colCount = len(data[0])
        self.tableWidget.setRowCount(rowCount)
        self.tableWidget.setColumnCount(colCount)

        #Resize window for table
        #5col takes up about 650 650/5 =130
        #11row takes up about 400 400/11 =~ 36
        self.Table_Dialog.resize(colCount*130, rowCount*36)


        #Fill table
        for y, row in enumerate(data):
            for x, col in enumerate(data[y]):
                item = QtWidgets.QTableWidgetItem()
                if isinstance(data[y][x], int):
                    item.setData(QtCore.Qt.EditRole, data[y][x])
                    self.tableWidget.setItem(y, x, item)
                else:
                    self.tableWidget.setItem(y, x, QtWidgets.QTableWidgetItem(data[y][x]))

    def run_query(self,query):
        data = self.dbm.run_query(query)
        return data
