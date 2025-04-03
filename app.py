
#author: Connor Comstock

from PyQt5 import QtCore, QtGui, QtWidgets
from tableDialog import Ui_Table_Dialog
from queryDialog import Ui_Query_Dialog


import databaseManager


class Ui_MainWindow(object):
    def __init__(self,*args,**kwargs):
        super(Ui_MainWindow,self).__init__(*args,**kwargs)
        self.dbm = databaseMangaer.DatabaseMangaer("airport")
        self.window_dict = {}
        self.query_list = [
        """
    SELECT passenger_name
    FROM passenger, buys, ticket
    WHERE passenger.passenger_id = buys.passenger_id
    AND ticket.ticket_id = buys.ticket_id
    AND ticket.flight_id = '27777';""",

        """
    SELECT flight_id from pilot, flies
    WHERE pilot.pilot_id = flies.pilot_id
    AND pilot.pilot_name = 'Sam'
    AND role = 'pilot';""",

        """
    SELECT flight_id,MAX(b) as num_passengers
    FROM
        (SELECT flight_id,COUNT(flight_id) as b
        FROM ticket
        GROUP BY flight_id)""",

        """
    SELECT pilot_name
    FROM flies,pilot,
        (SELECT flight_id,MAX(a) as num_passengers
        FROM
            (SELECT flight_id,COUNT(flight_id) as a
            FROM ticket
            GROUP BY flight_id)
        ) as b
    WHERE flies.flight_id = b.flight_id
    AND flies.role = 'pilot'
    AND flies.pilot_id = pilot.pilot_id""",

        """
    SELECT pilot_name
    FROM pilot,flies,ticket
    WHERE pilot.pilot_id = flies.pilot_id
    AND flies.flight_id = ticket.flight_id
    AND pilot.training_hrs = 'n'
    GROUP BY pilot_name;""",

        """
    SELECT passenger_name
    FROM ticket,buys,passenger
    WHERE passenger.passenger_id=buys.passenger_id
    AND buys.ticket_id=ticket.ticket_id
    AND ticket.flight_id=
        (SELECT flight_id
        FROM ticket,passenger,buys
        WHERE passenger.passenger_id=buys.passenger_id
        AND buys.ticket_id=ticket.ticket_id
        AND passenger.passenger_name='Kai');""",

        """
    SELECT pilot_name
    FROM pilot, flies as a
    INNER JOIN
        (SELECT flight_id
        FROM flies
        GROUP BY flight_id
        HAVING COUNT(flight_id) >1) as b
    ON
    a.flight_id = b.flight_id
    where pilot.pilot_id = a.pilot_id
        """,

        """
    SELECT flight_id,destination,origin,ABS(arrival_time-departure_time) as flight_length
    FROM flight
    ORDER BY ABS(arrival_time-departure_time);""",

        """
    SELECT passenger_name from passenger, buys, ticket
    WHERE passenger.passenger_id=buys.passenger_id
    AND buys.ticket_id=ticket.ticket_id
    AND ticket.ticket_class='first';""",

        """
    SELECT pilot_name,yrs_exp
    FROM pilot
    ORDER by yrs_exp;""",

        """
    SELECT passenger_name
    FROM passenger,ticket,buys
    WHERE passenger.passenger_id=buys.passenger_id
    AND buys.ticket_id=ticket.ticket_id
    AND checked_baggage = 'y' ;"""
            ]

    #-----Main GUI Setup-----
    def setupUi(self, MainWindow):
        #Main window stuff
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1066, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #----------------------------------------
        #--------External Table View Setup-------
        #----------------------------------------
        self.Db_viewer_GB = QtWidgets.QGroupBox(self.centralwidget)
        self.Db_viewer_GB.setObjectName("Db_viewer_GB")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Db_viewer_GB)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabels_VL = QtWidgets.QVBoxLayout()
        self.tabels_VL.setSpacing(0)
        self.tabels_VL.setObjectName("tabels_VL")

        #-----Pilot View Table-----
        #--------------------------
        self.pilot_HL = QtWidgets.QHBoxLayout()
        self.pilot_HL.setObjectName("pilot_HL")
        self.pilot_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.pilot_label.setObjectName("pilot_label")
        self.pilot_HL.addWidget(self.pilot_label)
        #View Button
        self.pilot_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.pilot_button.setObjectName("pilot_button")
        self.pilot_button.clicked.connect(self.show_relevant_table_window)
        #Add to Layout
        self.pilot_HL.addWidget(self.pilot_button)
        self.tabels_VL.addLayout(self.pilot_HL)

        #-----Flies View Table-----
        #--------------------------
        self.flies_HL = QtWidgets.QHBoxLayout()
        self.flies_HL.setObjectName("flies_HL")
        self.flies_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.flies_label.setObjectName("flies_label")
        self.flies_HL.addWidget(self.flies_label)

        self.flies_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.flies_button.setObjectName("flies_button")
        self.flies_button.clicked.connect(self.show_relevant_table_window)

        self.flies_HL.addWidget(self.flies_button)
        self.tabels_VL.addLayout(self.flies_HL)

        #-----Buys View Table-----
        #-------------------------
        self.buys_HL = QtWidgets.QHBoxLayout()
        self.buys_HL.setObjectName("buys_HL")
        self.buys_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.buys_label.setObjectName("buys_label")
        self.buys_HL.addWidget(self.buys_label)

        self.buys_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.buys_button.setObjectName("buys_button")
        self.buys_button.clicked.connect(self.show_relevant_table_window)

        self.buys_HL.addWidget(self.buys_button)
        self.tabels_VL.addLayout(self.buys_HL)

        #-----Flight View Table-----
        #---------------------------
        self.flight_HL = QtWidgets.QHBoxLayout()
        self.flight_HL.setObjectName("flight_HL")
        self.flight_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.flight_label.setObjectName("flight_label")
        self.flight_HL.addWidget(self.flight_label)

        self.flight_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.flight_button.setObjectName("flight_button")
        self.flight_button.clicked.connect(self.show_relevant_table_window)

        self.flight_HL.addWidget(self.flight_button)
        self.tabels_VL.addLayout(self.flight_HL)

        #-----Ticket View Table-----
        #---------------------------
        self.ticket_HL = QtWidgets.QHBoxLayout()
        self.ticket_HL.setObjectName("ticket_HL")
        self.ticket_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.ticket_label.setObjectName("ticket_label")
        self.ticket_HL.addWidget(self.ticket_label)

        self.ticket_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.ticket_button.setObjectName("ticket_button")
        self.ticket_button.clicked.connect(self.show_relevant_table_window)

        self.ticket_HL.addWidget(self.ticket_button)
        self.tabels_VL.addLayout(self.ticket_HL)

        #----Passenger View Table-----
        #-----------------------------
        self.passenger_HL = QtWidgets.QHBoxLayout()
        self.passenger_HL.setObjectName("passenger_HL")
        self.passenger_label = QtWidgets.QLabel(self.Db_viewer_GB)
        self.passenger_label.setObjectName("passenger_label")
        self.passenger_HL.addWidget(self.passenger_label)

        self.passenger_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.passenger_button.setObjectName("passenger_button")
        self.passenger_button.clicked.connect(self.show_relevant_table_window)


        self.passenger_HL.addWidget(self.passenger_button)
        self.tabels_VL.addLayout(self.passenger_HL)

        #Reset Tables Button
        self.default_button = QtWidgets.QPushButton(self.Db_viewer_GB)
        self.default_button.setObjectName("default_button")
        self.passenger_button.clicked.connect(self.reset_tables)
        self.tabels_VL.addWidget(self.default_button)

        #----------------------------------------
        #----------Question View Setup-----------
        #----------------------------------------
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tabels_VL.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.tabels_VL)
        self.horizontalLayout.addWidget(self.Db_viewer_GB)
        self.Qs_and_Qs_GB = QtWidgets.QGroupBox(self.centralwidget)
        self.Qs_and_Qs_GB.setStyleSheet("")
        self.Qs_and_Qs_GB.setMinimumWidth(250)
        self.Qs_and_Qs_GB.setFlat(False)
        self.Qs_and_Qs_GB.setObjectName("Qs_and_Qs_GB")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Qs_and_Qs_GB)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.allQs_ScrollArea = QtWidgets.QScrollArea(self.Qs_and_Qs_GB)
        self.allQs_ScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.allQs_ScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.allQs_ScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.allQs_ScrollArea.setWidgetResizable(True)
        self.allQs_ScrollArea.setObjectName("allQs_ScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 265, 483))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.allQs_VL = QtWidgets.QVBoxLayout()
        self.allQs_VL.setObjectName("allQs_VL")
        self.qs_HL = QtWidgets.QHBoxLayout()
        self.qs_HL.setSpacing(0)
        self.qs_HL.setObjectName("qs_HL")
        self.q1_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)

        #-----Create Question 1-------
        #(manually)

        self.q1_label.setWordWrap(True)
        self.q1_label.setObjectName("q1_label")
        self.qs_HL.addWidget(self.q1_label, 0, QtCore.Qt.AlignTop)
        self.q_buttons_VL_1 = QtWidgets.QVBoxLayout()
        self.q_buttons_VL_1.setSpacing(0)
        self.q_buttons_VL_1.setObjectName("q_buttons_VL_1")

        self.runQ1_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ1_button.setObjectName("runQ1_button")
        self.runQ1_button.clicked.connect(self.corrolate_and_run_query)

        self.q_buttons_VL_1.addWidget(self.runQ1_button)

        self.viewQ1_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ1_Button.setObjectName("viewQ1_Button")
        self.viewQ1_Button.clicked.connect(self.show_relevant_query_window)

        self.q_buttons_VL_1.addWidget(self.viewQ1_Button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.q_buttons_VL_1.addItem(spacerItem1)
        self.qs_HL.addLayout(self.q_buttons_VL_1)
        self.allQs_VL.addLayout(self.qs_HL)

        #-----Create Question 2-------
        #Using makeAnyQuestion, helps condense code
        self.q2_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ2_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ2_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ2_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ2_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q2_label,self.runQ2_button,self.viewQ2_Button)

        #-----Create Question 3-------
        self.q3_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ3_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ3_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ3_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ3_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q3_label,self.runQ3_button,self.viewQ3_Button)

        #-----Create Question 4-------
        self.q4_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ4_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ4_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ4_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ4_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q4_label,self.runQ4_button,self.viewQ4_Button)

        #-----Create Question 5-------
        self.q5_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ5_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ5_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ5_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ5_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q5_label,self.runQ5_button,self.viewQ5_Button)

        #-----Create Question 6-------
        self.q6_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ6_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ6_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ6_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ6_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q6_label,self.runQ6_button,self.viewQ6_Button)

        #-----Create Question 7-------
        self.q7_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ7_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ7_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ7_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ7_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q7_label,self.runQ7_button,self.viewQ7_Button)

        #-----Create Question 8-------
        self.q8_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ8_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ8_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ8_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ8_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q8_label,self.runQ8_button,self.viewQ8_Button)

        #-----Create Question 9-------
        self.q9_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ9_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ9_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ9_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ9_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q9_label,self.runQ9_button,self.viewQ9_Button)

        #-----Create Question 10-------
        self.q10_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ10_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ10_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ10_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ10_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q10_label,self.runQ10_button,self.viewQ10_Button)

        #-----Create Question 11-------
        self.q11_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.runQ11_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.runQ11_button.clicked.connect(self.corrolate_and_run_query)
        self.viewQ11_Button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.viewQ11_Button.clicked.connect(self.show_relevant_query_window)
        self.makeAnyQuestion(self.q11_label,self.runQ11_button,self.viewQ11_Button)

        #-----Finilize question layout-------
        self.verticalLayout.addLayout(self.allQs_VL)

        #----------------------------------------
        #----------Main Table View Setup-----------
        #----------------------------------------
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.allQs_ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.allQs_ScrollArea)
        self.horizontalLayout.addWidget(self.Qs_and_Qs_GB, 0, QtCore.Qt.AlignLeft)
        self.TableCMD_GB = QtWidgets.QGroupBox(self.centralwidget)
        self.TableCMD_GB.setObjectName("TableCMD_GB")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.TableCMD_GB)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.VL_TableCMD = QtWidgets.QVBoxLayout()
        self.VL_TableCMD.setObjectName("VL_TableCMD")

        ##-----Query Entry Box-------
        self.enterQuery_lineEdit = QtWidgets.QLineEdit(self.TableCMD_GB)
        self.enterQuery_lineEdit.setObjectName("enterQuery_lineEdit")
        self.VL_TableCMD.addWidget(self.enterQuery_lineEdit)

        ##-----Run Query Button-------
        self.runQuery_button = QtWidgets.QPushButton(self.TableCMD_GB)
        self.runQuery_button.setObjectName("runQuery_button")
        self.runQuery_button.clicked.connect(self.update_table_cmd)
        self.VL_TableCMD.addWidget(self.runQuery_button)

        #-----Main Data Table-------
        self.data_table = QtWidgets.QTableWidget(self.TableCMD_GB)
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(0)
        self.data_table.setRowCount(0)
        self.VL_TableCMD.addWidget(self.data_table)
        self.verticalLayout_10.addLayout(self.VL_TableCMD)
        self.horizontalLayout.addWidget(self.TableCMD_GB)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #-----Set Gui Text-----
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data View App"))
        self.Db_viewer_GB.setTitle(_translate("MainWindow", "Database Viewer"))

        self.pilot_label.setText(_translate("MainWindow", "pilot"))
        self.pilot_button.setText(_translate("MainWindow", "Show"))
        self.flies_label.setText(_translate("MainWindow", "flies"))
        self.flies_button.setText(_translate("MainWindow", "Show"))
        self.buys_label.setText(_translate("MainWindow", "buys"))
        self.buys_button.setText(_translate("MainWindow", "Show"))
        self.flight_label.setText(_translate("MainWindow", "flight"))
        self.flight_button.setText(_translate("MainWindow", "Show"))
        self.ticket_label.setText(_translate("MainWindow", "ticket"))
        self.ticket_button.setText(_translate("MainWindow", "Show"))
        self.passenger_label.setText(_translate("MainWindow", "passenger"))
        self.passenger_button.setText(_translate("MainWindow", "Show"))
        self.default_button.setText(_translate("MainWindow","Reset Tables"))
        self.Qs_and_Qs_GB.setTitle(_translate("MainWindow", "Questions and Queries"))
        self.runQ1_button.setText(_translate("MainWindow", "Run"))
        self.viewQ1_Button.setText(_translate("MainWindow", "View"))
        self.runQ2_button.setText(_translate("MainWindow", "Run"))
        self.viewQ2_Button.setText(_translate("MainWindow", "View"))
        self.runQ3_button.setText(_translate("MainWindow", "Run"))
        self.viewQ3_Button.setText(_translate("MainWindow", "View"))
        self.runQ4_button.setText(_translate("MainWindow", "Run"))
        self.viewQ4_Button.setText(_translate("MainWindow", "View"))
        self.runQ5_button.setText(_translate("MainWindow", "Run"))
        self.viewQ5_Button.setText(_translate("MainWindow", "View"))
        self.runQ6_button.setText(_translate("MainWindow", "Run"))
        self.viewQ6_Button.setText(_translate("MainWindow", "View"))
        self.runQ7_button.setText(_translate("MainWindow", "Run"))
        self.viewQ7_Button.setText(_translate("MainWindow", "View"))
        self.runQ8_button.setText(_translate("MainWindow", "Run"))
        self.viewQ8_Button.setText(_translate("MainWindow", "View"))
        self.runQ9_button.setText(_translate("MainWindow", "Run"))
        self.viewQ9_Button.setText(_translate("MainWindow", "View"))
        self.runQ10_button.setText(_translate("MainWindow", "Run"))
        self.viewQ10_Button.setText(_translate("MainWindow", "View"))
        self.runQ11_button.setText(_translate("MainWindow", "Run"))
        self.viewQ11_Button.setText(_translate("MainWindow", "View"))


        #Set question text
        self.q1_label.setText(_translate("MainWindow", "1. List all the passengers on the flight with id 27777"))
        self.q2_label.setText(_translate("MainWindow", "2. List all flights where Sam is the pilot"))
        self.q3_label.setText(_translate("MainWindow", "3. List the flight id that has the most passengers"))
        self.q4_label.setText(_translate("MainWindow", "4. Which pilot's flight has the most passengers"))
        self.q5_label.setText(_translate("MainWindow", "5. Which pilots are flying a flight, but have not yet completed their training hours"))
        self.q6_label.setText(_translate("MainWindow", "6. List all passengers on Kai's flight"))
        self.q7_label.setText(_translate("MainWindow", "7. List all pilots and co-pilots who are not flying alone"))
        self.q8_label.setText(_translate("MainWindow", "8. List flights from shortest to longest"))
        self.q9_label.setText(_translate("MainWindow", "9. List all first class passengers"))
        self.q10_label.setText(_translate("MainWindow", "10. Pilots years of experience from least to most"))
        self.q11_label.setText(_translate("MainWindow", "11. Passengers with checked baggage"))


        self.TableCMD_GB.setTitle(_translate("MainWindow", "Table Viewer and Query Command Line"))
        self.runQuery_button.setText(_translate("MainWindow", "Run Query"))

    def makeAnyQuestion(self, label,runQ_button,viewQ_button):

        #-----Make horizontal layout-----
        hl = QtWidgets.QHBoxLayout()
        hl.setSpacing(0)
        label.setWordWrap(True)
        #add to HL
        hl.addWidget(label, 0, QtCore.Qt.AlignTop)
        #-----Make vertical button layout
        q_buttons_VL = QtWidgets.QVBoxLayout()
        q_buttons_VL.setSpacing(0)
        #make run button
        q_buttons_VL.addWidget(runQ_button)
        #make view button
        q_buttons_VL.addWidget(viewQ_button)
        #addspacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        q_buttons_VL.addItem(spacerItem)
        #add to HL
        hl.addLayout(q_buttons_VL)
        #addHL to Vertial List, which then becomes scrollable
        self.allQs_VL.addLayout(hl)

    def show_relevant_table_window(self):
        """
            Creates and keeps track of pop up windows that show the tables
            Uses the button object(sender) as a dictionary key
            This returns the relevant table query, and also stores/retrieves the window object
            this saves a lot of coding and allows for a dynamic amount of windows
        """
        sender = self.MainWindow.sender()

        switch = {
                self.pilot_button:"select * from pilot",
                self.flies_button:"select * from flies",
                self.buys_button:"select * from buys",
                self.flight_button:"select * from flight",
                self.ticket_button:"select * from ticket",
                self.passenger_button:"select * from passenger",

        }

        #using sender(button objects) as keys because they are directly responsible for the creation of the window
        #Test if window has been created, if not, make, add to dictionary, and show
        if sender not in self.window_dict:
            table_window = QtWidgets.QDialog()
            #can reference Table_Dialog from table_ui.Table_Dialog, table_ui's are stored in ui_dict
            #determine window title based on query
            query = switch.get(sender,"")
            split_query = query.split(" ")#gets query from dictionary above
            table_name = split_query[(len(split_query)-1)]
            #create window and table
            table_ui = Ui_Table_Dialog(table_name)
            table_ui.setupUi(table_window)
            table_ui.update_table(query)
            table_window.show()
            self.window_dict[sender] = table_ui
        else:
            #table has been created, find in the dictionary, update, and show
            self.window_dict[sender].update_table(switch.get(sender,""))
            self.window_dict[sender].Table_Dialog.show()
            self.window_dict[sender].Table_Dialog.raise_()

    def show_relevant_query_window(self):
        """
        Similar principle to show_relevant_table_window().
        Instead used for creating pop up with relevant query information
        """
        sender = self.MainWindow.sender()

        switch = {
                self.viewQ1_Button:self.query_list[0],
                self.viewQ2_Button:self.query_list[1],
                self.viewQ3_Button:self.query_list[2],
                self.viewQ4_Button:self.query_list[3],
                self.viewQ5_Button:self.query_list[4],
                self.viewQ6_Button:self.query_list[5],
                self.viewQ7_Button:self.query_list[6],
                self.viewQ8_Button:self.query_list[7],
                self.viewQ9_Button:self.query_list[8],
                self.viewQ10_Button:self.query_list[9],
                self.viewQ11_Button:self.query_list[10]
        }

        if sender not in self.window_dict:
            query_text = switch.get(sender,"")

            query_window = QtWidgets.QDialog()
            table_ui = Ui_Query_Dialog("Query View")
            table_ui.setupUi(query_window)
            table_ui.update_text(query_text)
            query_window.show()
            self.window_dict[sender] = table_ui
        else:
            self.window_dict[sender].Query_Dialog.show()
            self.window_dict[sender].Query_Dialog.raise_()

    def run_query(self,query):
        data = self.dbm.run_query(query)
        return data

    def corrolate_and_run_query(self):
        """
        Uses dictionary to correlate question button object with relevant query.
        Then runs the query and updates main view table
        """
        sender = self.MainWindow.sender()
        switch = {
            self.runQ1_button:self.query_list[0],
            self.runQ2_button:self.query_list[1],
            self.runQ3_button:self.query_list[2],
            self.runQ4_button:self.query_list[3],
            self.runQ5_button:self.query_list[4],
            self.runQ6_button:self.query_list[5],
            self.runQ7_button:self.query_list[6],
            self.runQ8_button:self.query_list[7],
            self.runQ9_button:self.query_list[8],
            self.runQ10_button:self.query_list[9],
            self.runQ11_button:self.query_list[10]

        }
        print(switch.get(sender,""))
        self.update_table(switch.get(sender,""))

    def update_table(self, query):
        #updates the main table view, with data from query provided
        data = self.run_query(query)

        #Detect no entry in the text box
        if len(data) == 0:
            self.data_table.setRowCount(1)
            self.data_table.setColumnCount(1)
            self.data_table.setItem(0, 0, QtWidgets.QTableWidgetItem("No Data"))
            return
        #Sets table size according to data
        rowCount = len(data)
        colCount = len(data[0])
        self.data_table.setRowCount(rowCount)
        self.data_table.setColumnCount(colCount)

        #Fills table with data
        for y, row in enumerate(data):
            for x, col in enumerate(data[y]):
                item = QtWidgets.QTableWidgetItem()
                if isinstance(data[y][x], int):
                    item.setData(QtCore.Qt.EditRole, data[y][x])
                    self.data_table.setItem(y, x, item)
                else:
                    self.data_table.setItem(y, x, QtWidgets.QTableWidgetItem(data[y][x]))

    def update_table_cmd(self):
        #Used to update main view table from query text box
        query = self.enterQuery_lineEdit.text()
        self.update_table(query)

    def reset_tables(self):
        self.dbm.load_default_data()



if __name__ == "__main__":
    #Runs app
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
