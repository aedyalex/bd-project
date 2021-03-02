from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QLineEdit, QTableWidgetItem


#from src.GUI.Meniu_comanda import Meniu_comanda


class Adaugare_produs:
    def __init__(self,widget,controler,meniu_window):
        self.widget = widget
        self.controler = controler

        self.title_label = None
        self.label_1 = None
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None

        self.combobox1 = None
        self.combobox2 = None

        self.meniu_window = meniu_window

        self.lineEdit = None

        self.submit_button = None

        self.setupUI(self.widget)

    def display_popup(self, exit_code):
        self.popup = QtWidgets.QMainWindow()
        self.popup.resize(518, 172)
        self.popup.show()

        self.text = QLabel(self.popup)
        self.text.setGeometry(QtCore.QRect(30, 10, 171, 71))
        self.text.setText("Eroare")
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(24)
        self.text.setFont(font)
        self.text.show()

        self.text2 = QLabel(self.popup)
        self.text2.setGeometry(QtCore.QRect(30, 100, 500, 70))
        if exit_code == -1:
            self.text2.setText('Cantitatea ceruta depaseste cantitatea de pe stoc')
        if exit_code == -2:
            self.text2.setText('Nu ati completat cantitatea ceruta')
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.text2.setFont(font)
        self.text2.show()

    def setupUI(self,Window):
        Window.resize(590,251)

        self.title_label = QLabel(self.widget)
        self.title_label.setGeometry(QRect(20,30,231,31))
        self.title_label.setText("Adaugati produsul")

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg")
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.show()

        self.label_1 = QLabel(self.widget)
        self.label_1.setGeometry(QRect(10,110,111,16))
        self.label_1.setText("Categorie produs:*")
        self.label_1.show()

        self.label_2 = QLabel(self.widget)
        self.label_2.setGeometry(QRect(10,160,101,16))
        self.label_2.setText("Nume produs:*")
        self.label_2.show()

        self.label_3 = QLabel(self.widget)
        self.label_3.setGeometry(QRect(350,110,71,21))
        self.label_3.setText("Cantitate:*")
        self.label_3.show()

        self.combobox1 = QtWidgets.QComboBox(self.widget)
        self.combobox1.setGeometry(QRect(130,110,191,22))
        # de adaugat categoriile
        self.controler.cursor.execute("SELECT NUME FROM CATEGORII_PRODUSE")
        result = [i[0] for i in self.controler.cursor]
        self.combobox1.addItems(result)
        self.combobox1.activated[str].connect(self.update_produse)
        self.combobox1.show()

        self.combobox2 = QtWidgets.QComboBox(self.widget)
        self.combobox2.setGeometry(QRect(130,160,191,22))
        self.controler.cursor.execute(f"SELECT NUME FROM PRODUSE WHERE id_categorie = (SELECT id_categorie from CATEGORII_PRODUSE where nume = '{self.combobox1.currentText()}')")
        result = [i[0] for i in self.controler.cursor]
        self.combobox2.addItems(result)
        self.combobox2.activated[str].connect(self.update_cantitate)
        self.combobox2.show()

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setGeometry(QRect(420,110,141,22))
        self.lineEdit.show()

        self.label_4 = QLabel(self.widget)
        self.label_4.setGeometry(QRect(350,160,210,16))
        #self.label_4.setText("Unitate:*")
        self.controler.cursor.execute(
            f"SELECT TIP_CANTITATE FROM PRODUSE WHERE nume = '{self.combobox2.currentText()}'")
        result = [i[0] for i in self.controler.cursor][0]
        self.label_4.setText(f"Unitate:* {result}")
        self.label_4.show()

        self.submit_button = QtWidgets.QPushButton(self.widget)
        self.submit_button.setGeometry(QRect(480,210,93,28))
        self.submit_button.setText("Submit")
        self.submit_button.clicked.connect(self.insert_data)
        self.submit_button.show()

    def update_produse(self):
        self.combobox2.clear()
        self.controler.cursor.execute(
            f"SELECT NUME FROM PRODUSE WHERE id_categorie = (SELECT id_categorie from CATEGORII_PRODUSE where nume = '{self.combobox1.currentText()}')")
        result = [i[0] for i in self.controler.cursor]
        self.combobox2.addItems(result)
        self.controler.cursor.execute(
            f"SELECT TIP_CANTITATE FROM PRODUSE WHERE nume = '{self.combobox2.currentText()}'")
        result = [i[0] for i in self.controler.cursor]
        self.update_cantitate()

    def update_cantitate(self):
        self.controler.cursor.execute(
            f"SELECT TIP_CANTITATE FROM PRODUSE WHERE nume = '{self.combobox2.currentText()}'")
        result = [i[0] for i in self.controler.cursor][0]
        self.label_4.setText(f"Unitate:* {result}")

    def insert_data(self):
        print(1)
        data = [self.combobox1.currentText(),self.combobox2.currentText(),self.lineEdit.text()]

        print(data)
        self.controler.cursor.execute(f"SELECT CANTITATE_PE_STOC FROM PRODUSE WHERE ID_PRODUS = (SELECT ID_PRODUS FROM PRODUSE WHERE NUME='{self.combobox2.currentText()}')")
        cantitate_pe_stoc = [i[0] for i in self.controler.cursor][0]

        print(cantitate_pe_stoc)

        if( data[2] == ''):
            self.display_popup(-2)
        elif( (int)(cantitate_pe_stoc) < (int)(data[2]) ):
            self.display_popup(-1)
        else:
            self.meniu_window.table1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.meniu_window.table1.setRowCount(self.meniu_window.length+1)

            self.meniu_window.table1.setItem(self.meniu_window.length, 0, QTableWidgetItem(str(data[1])))
            self.meniu_window.table1.setItem(self.meniu_window.length, 1, QTableWidgetItem(str(data[0])))
            self.meniu_window.table1.setItem(self.meniu_window.length, 2, QTableWidgetItem(str(data[2])))
            self.meniu_window.table1.resizeColumnsToContents()
            self.meniu_window.length += 1

            self.widget.close()
        #     self.table.setHorizontalHeaderLabels(["Nume produs","Categorie","Cantitate"])
        #     self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        #     self.table.setItem(0,1,self.combobox2.currentText(),self.combobox1.currentText(),self.lineEdit.text())


    def show(self):
        self.widget.show()




