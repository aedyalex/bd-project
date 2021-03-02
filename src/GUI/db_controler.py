import cx_Oracle
from src.Tables import Angajati, Detalii_angajat, Departamente, Clienti


class Controler:
    def __init__(self):
        dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'xe')
        connection = cx_Oracle.connect("edi_bd","123456789",dsn_tns)
        connection.autocommit = False

        self.cursor = connection.cursor()

        self.querie = ''

    def generic_print(self,tabel_name):
        if (tabel_name == "..."):
            return "Error"
        if (tabel_name == 'Angajati'):
            self.querie = 'select a.id_angajat,a.nume,a.email,d.nume "Nume departament" from angajati a, departamente d where a.id_dept = d.id_dept'
        elif (tabel_name == 'Detalii_angajat'):
            self.querie = 'select a.id_angajat, a.nume, a.email, d.data_nasterii, d.telefon, d.data_angajarii, d.salariu, d.data_incheiere_contract, d.adresa_domiciliu from angajati a, detalii_angajat d where a.id_angajat=d.id_angajat'
        elif (tabel_name == 'Comenzi'):
            self.querie = 'select co.id_comanda, co.data_initiere, co.status_tranzactie, c.nume "Nume client", a.nume "Nume angajat" from comenzi co, angajati a, clienti c where co.id_angajat = a.id_angajat and co.id_client = c.id_client'
        elif (tabel_name == 'Detalii_comanda'):
            self.querie = 'select co.id_comanda, p.nume, d.cantitate from comenzi co, produse p, detalii_comanda d where co.id_comanda = d.id_comanda and p.id_produs = d.id_produs order by d.id_comanda'
        elif (tabel_name == 'Produse'):
            self.querie = 'select p.id_produs, p.nume, p.tip_cantitate, p.cantitate_pe_stoc, p.pret_per_unitate "Pret unitar", cat.nume "Categorie", p.urmatoarea_aprovizionare from produse p, categorii_produse cat where p.id_categorie = cat.id_categorie'
        else:
            self.querie = f'SELECT * FROM {tabel_name}'
        self.cursor.execute(self.querie)
        result = []
        for i in self.cursor:
            result.append(i)

        return result

    def get_column_names(self,tabel_name):
        return  [row[0] for row in self.cursor.description]


    def insert_into_table(self,table_name,data):
        if table_name == 'Angajati':
            table = Angajati.Angajati(data)

        elif table_name == 'Detalii_angajat':
            table = Detalii_angajat.Detalii_angajat(data)

        elif table_name == 'Departamente':
            table = Departamente.Departamente(data)

        elif table_name == 'Clienti':
            table = Clienti.Clienti(data)

        elif table_name == 'Produse':
            pass
        if table.insert() == -1:
            return -1
        elif table.insert() == -2:
            return -2

        print('done')
        self.cursor.execute(table.insert())


if __name__ == '__main__':
    c = Controler()
    nume = "'Rolex'"
    c.cursor.execute(f"INSERT INTO DEPARTAMENTE VALUES(DEPARTAMENTE_ID_DEPT_SEQ.nextval,{nume})")

    # c.generic_print('Detalii_comanda')
    # print(c.get_column_names('Angajati'))


