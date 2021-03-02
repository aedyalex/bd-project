import re

class Angajati:
    def __init__(self,data):
        self.map = {}
        self.map['nume'] = data[0]
        self.map['email'] = data[1]
        self.map['id_dept'] = data[2]

    def insert(self):
        if (self.map['nume'] == '' or self.map['email'] == ''):
            return -1

        if (re.search("[0-9]", self.map['nume'])):
            return -2

        if (re.search('[A-Za-z0-9._%-]+@[A-Za-z0-9._%-]+\.[A-Za-z]{2,4}',self.map['email']) == None):
            return -2

        fields = ""
        for i in list(self.map.keys()):
            fields += i + ", "

        fields = fields[0:-2]

        values = ""

        for k in self.map:
            if k != 'id_dept':
                values += "'" + str(self.map[k]) + "',"
            else:
                values += str(self.map[k]) + ","

        values = values[0:-1]

        querie = f'INSERT INTO ANGAJATI(id_angajat,{fields}) VALUES(ANGAJATI_ID_ANGAJAT_SEQ.nextval,{values})'
        print(querie)
        return querie

if __name__ == '__main__':
    a = Angajati(['popicaaa','pppp@sss.ccc',5])
    a.insert()
    print(re.search("[0-9]",'Popica'))
