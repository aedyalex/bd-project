from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel, QComboBox, QTableWidget, QPushButton, QCommandLinkButton, QTableWidgetItem

from src.GUI.Adaugare_produs import Adaugare_produs


class Meniu_comanda():
    def __init__(self,widget,controler):
        #super.__init__(widget,controller)
        self.widget = widget
        self.controler = controler

        self.combobox1 = None
        self.combobox2 = None
        self.title_label = None
        self.instruction_label = None
        self.label1 = None

        self.pushButton_1 = None
        self.pushButton_2 = None
        self.pushButton_3 = None

        self.table1 = None
        self.length = 0
        self.table2 = None

        self.command_button = None
        self.add_produs_window = None

        self.data = []

        self.setupUi(self.widget)

    def setupUi(self, CommandaWindow):
        CommandaWindow.resize(961, 413)

        self.title_label = QLabel(self.widget)
        self.title_label.setGeometry(QRect(20,20,191,51))
        self.title_label.setText("Meniu comenzi")

        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.show()

        self.instruction_label = QLabel(self.widget)
        self.instruction_label.setGeometry(QRect(20,110,101,16))
        self.instruction_label.setText("Selectati clientul")
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(8)
        self.instruction_label.setFont(font)
        self.instruction_label.show()

        self.label1 = QLabel(self.widget)
        self.label1.setGeometry(QRect(300,110,221,16))
        self.label1.setText("Selectati angajatul care o va procesa:")
        self.label1.show()

        self.combobox1 = QComboBox(self.widget)
        self.combobox1.setGeometry(QRect(130,110,141,22))
        self.controler.cursor.execute('SELECT NUME FROM CLIENTI')
        result = [i[0] for i in self.controler.cursor]

        self.combobox1.addItems(result)
        # DE ADAUGAT CLIENTII
        self.combobox1.show()

        self.combobox2 = QComboBox(self.widget)
        self.combobox2.setGeometry(QRect(530,110,171,22))
        self.controler.cursor.execute("SELECT NUME FROM ANGAJATI WHERE ID_DEPT = (SELECT ID_DEPT FROM DEPARTAMENTE WHERE NUME='Vanzari')")
        result = [i[0] for i in self.controler.cursor]
        self.combobox2.addItems(result)
        self.combobox2.show()

        self.table1 = QTableWidget(self.widget)
        self.table1.setGeometry(QRect(10,160,461,192))
        self.table1.setColumnCount(3)
        self.table1.setRowCount(self.length)

        self.table1.setHorizontalHeaderLabels(["Nume produs", "Categorie", "Cantitate"])
        #self.table1.setItem(0,1,QTableWidgetItem("aaaa"))
        #self.table1.activated(self.add_table_data)
        self.table1.show()

        self.pushButton_1 = QtWidgets.QPushButton(self.widget)
        self.pushButton_1.setGeometry(QRect(10,370,151,28))
        self.pushButton_1.setText("Stergeti produs")
        self.pushButton_1.clicked.connect(self.delete_product)
        self.pushButton_1.show()

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QRect(170,370,141,28))
        self.pushButton_2.setText("Adaugare produs")
        self.pushButton_2.clicked.connect(self.display_add_produs)
        self.pushButton_2.show()

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QRect(800,370,151,28))
        self.pushButton_3.setText("Finalizare comanda")
        self.pushButton_3.clicked.connect(self.submit_data)
        self.pushButton_3.show()

        self.command_button = QtWidgets.QCommandLinkButton(self.widget)
        self.command_button.setGeometry(QRect(480,160,31,41))
        self.command_button.clicked.connect(self.display_total)
        self.command_button.show()

        self.table2 = QTableWidget(self.widget)
        self.table2.setGeometry(QRect(520,160,431,192))
        #self.table2.setColumnCount(2)
        #self.table2.setRowCount(0)


    def retranslateUi(self, InsertWindow):
        pass

    def display_total(self):
        data = []
        names = []
        for i in range(0,self.length):
            data.append(self.table1.item(i,2).text())
            names.append(self.table1.item(i,0).text())
        print(data)
        print(names)
        prices = []

        for i in range(0,self.length):
            print(f"select pret_per_unitate from produse where nume='{names[i]}'")
            self.controler.cursor.execute(f"select pret_per_unitate from produse where nume='{names[i]}'")
            result = [i[0] for i in self.controler.cursor][0]
            prices.append((int)(result) * (int)(data[i]))

        print(prices)
        self.table2.setRowCount(self.length+1)
        self.table2.setColumnCount(2)
        self.table2.setHorizontalHeaderLabels(["", ""])

        for i in range(0,self.length):
            self.table2.setItem(i,0,QTableWidgetItem(names[i]))
            self.table2.setItem(i,1,QTableWidgetItem(str(prices[i])))

        print(sum(prices))
        self.table2.setItem(self.length,0,QTableWidgetItem("Total de plata"))
        self.table2.setItem(self.length,1,QTableWidgetItem(str(sum(prices))))

    def delete_product(self):
        print(len(self.table1.selectionModel().selectedRows()))
        if len(self.table1.selectionModel().selectedRows()) == 1:
            index = self.table1.currentRow()
            self.table1.removeRow(index)
            self.length -= 1
        # indices = self.table1.selectionModel().selectedRows()
        # print(indices)
        # for index in sorted(indices):
        #     self.table1.removeRow(index)

    def submit_data(self):
        # initializare comanda noua
        self.controler.cursor.execute(f"INSERT INTO COMENZI VALUES (COMENZI_ID_COMANDA_SEQ.nextval,SYSDATE,'in procesare',(SELECT ID_CLIENT FROM CLIENTI WHERE NUME='{self.combobox1.currentText()}'),(SELECT ID_ANGAJAT FROM ANGAJATI WHERE NUME='{self.combobox2.currentText()}'))")

        # adaugare produse in comanda
        # adaugare cantitate pentru fiecare produs
        self.controler.cursor.execute(f"SELECT MAX(ID_COMANDA) FROM COMENZI")
        max = [i[0] for i in self.controler.cursor][0]
        print(max)
        data = []
        names = []
        for i in range(0, self.length):
            data.append(self.table1.item(i, 2).text())
            names.append(self.table1.item(i, 0).text())
            self.controler.cursor.execute(f"INSERT INTO DETALII_COMANDA VALUES({data[i]},{max},(SELECT id_produs FROM PRODUSE WHERE NUME='{names[i]}'))")
        print(data)
        print(names)

        # update stocuri
        for i in range(0, self.length):
            self.controler.cursor.execute(
                f"UPDATE PRODUSE SET CANTITATE_PE_STOC = CANTITATE_PE_STOC - {data[i]} WHERE NUME = '{names[i]}'")

        # commit
        #self.controler.cursor.execute('COMMIT')

        self.widget.close()

    def display_add_produs(self):
        self.add_produs_window = Adaugare_produs(QtWidgets.QWidget(),self.controler,self)
        self.add_produs_window.show()

        #self.table1.setItem(0,0,self.data)

    # def add_table_data(self):
    #     self.table1.setItem(0,0,self.data)

    def show(self):
        self.widget.show()
        #pass

