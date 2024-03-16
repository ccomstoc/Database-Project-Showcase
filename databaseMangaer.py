#author: Connor Comstock

import sqlite3
import csv
import sys
import traceback

class DatabaseMangaer:
    """
    An interface for sqlite3 databases
    Made for use with my pyqt5 database showcase app
    """
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.con = sqlite3.connect(databaseName+ ".db")
        self.cur = self.con.cursor()
    def __del__(self):
        self.con.commit()
        self.con.close()


    def clear_table(self,table_name):
        self.cur.execute("DELETE FROM " + table_name)

    def load_default_data(self):
        """
        Uses cvs' to recover the tables the
        program was intended to function with
        """
        self.clear_table("buys")
        self.clear_table("flies")
        self.clear_table("flight")
        self.clear_table("passenger")
        self.clear_table("pilot")
        self.clear_table("ticket")
        self.load_csv("./defaultTables/buys.csv","buys")
        self.load_csv("./defaultTables/flies.csv","flies")
        self.load_csv("./defaultTables/flight.csv","flight")
        self.load_csv("./defaultTables/passenger.csv","passenger")
        self.load_csv("./defaultTables/pilot.csv","pilot")
        self.load_csv("./defaultTables/ticket.csv","ticket")


    def load_csv(self,filename,table_name):
        self.clear_table(table_name)
        """
        Inserts all csv information into table, csv must have correct header for table
        """
        #transfers csv data to rows list
        rows = []
        with open(filename, 'r') as file:
          csvreader = csv.reader(file)
          for row in csvreader:
            rows.append(row)
        header = rows.pop(0)

        # build insert statment
        num_col = len(header)
        q_adder =""
        feild_list=""
        for i in range(num_col):
            if(i == num_col-1):
                q_adder += "?"
                feild_list += header[i]
            else:
                q_adder += "?, "
                feild_list += (header[i] + ", ")


        insert_records = "INSERT INTO " + table_name + " (" + feild_list + ") VALUES(" + q_adder + ")"
        self.cur.executemany(insert_records, rows)
        self.con.commit()
        file.close()

    def run_query(self,query):
        #Runs SQLite query and returns data

        #Check for drop statment
        if len(query) >=4:
            queryLower = []
            for i in range(4):
                queryLower.append(query[i].lower())
            if ''.join(queryLower) == "drop" :
                return [['Drop Not Supported']]
        try:#try to call query
            responce = self.cur.execute(query)
            self.con.commit()
            if self.cur.description is None:#catches empty error
                return []
            header = list(map(lambda x: x[0], self.cur.description))
            data = responce.fetchall()
            data.insert(0,header)
            self.con.commit()
        except sqlite3.Error as er:#catches SQL error
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return [[' '.join(er.args)]]
        return data
