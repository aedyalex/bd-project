import re

class Detalii_angajat():
    def __init__(self,data):
        self.map = dict()
        self.map["id_angajat"] = data[0]
        self.map["data_nasterii"] = data[1]
        self.map["telefon"] = data[2]
        self.map["data_angajarii"] = data[3]
        self.map['salariu'] = data[4]
        if(len(data) > 5):
            self.map["data_incheiere_contract"] = data[5]
        else:
            self.map["data_incheiere_contract"] = ''
        if(len(data) > 6):
            self.map["adresa_domiciliu"] = data[6]
        else:
            self.map["adresa_domiciliu"] = ''

        print(self.map.keys())

    def insert(self):
        print(11)
        date_format = "'dd.mm.yyyy'"
        if( self.map['id_angajat'] == "" or self.map['data_nasterii'] == "" or self.map['telefon'] == "" or self.map['data_angajarii'] == "" or self.map['salariu'] == ""):
            print('Eroare 1')
            return -1

        # if( re.search('[^0-9]',self.id_angajat)):
        #     return -1

        if( re.search('^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$',self.map['data_nasterii']) == None):
            print(2)
            return -2

        if( re.search('[^0-9\']',self.map['telefon']) != None):
            print(3)
            return -2

        if( re.search('^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$',self.map['data_angajarii']) == None):
            print(4)
            return -2

        if( self.map["data_incheiere_contract"] != '' and re.search('^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$',self.map["data_incheiere_contract"]) == None):
            print(5)
            return -2

        fields = ""
        print(self.map.keys())
        for i in list(self.map.keys()):
            if self.map[i] != '':
                fields += i + ", "

        fields = fields[0:-2]
        print(fields)
        values = ""

        for k in self.map:
            if (k == 'data_incheiere_contract' and self.map['data_incheiere_contract'] != '') or (k == 'data_nasterii') or (k == 'data_angajarii'):
                values += f"TO_DATE('{self.map[k]}','dd.mm.yyyy'),"
            elif (k == 'salariu' or k == 'id_angajat'):
                values += (str)(self.map[k]) + ','
            elif self.map[k] != '':
                values += "'" + str(self.map[k]) + "',"

        values = values[0:-1]
        print(values)

        print(values)
        querie = f'INSERT INTO DETALII_ANGAJAT({fields}) VALUES({values})'
        print(querie)

        return querie

if __name__ == '__main__':
    d = Detalii_angajat([1,'11.11.1999','1818181811','11.11.2019',1200,'12.12.2021','Pacurari'])
    print(d.insert())
    print(re.search('^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$','1.1.1978'))
    print(re.search('[^0-9]','081727141'))
