import re

class Clienti:
    def __init__(self,data):
        self.map = {}
        self.map['nume'] = data[0]
        self.map['tip_client'] = data[1]
        self.map['telefon'] = data[2]
        if( len(data) > 3):
            self.map['data_ultimei_comenzi'] = data[3]
        else:
            self.map['data_ultimei_comenzi'] = ''
        if( len(data) > 4):
            self.map['adresa_domiciliu'] = data[4]

    def insert(self):
        print(self.map)
        if( self.map['nume'] == '' or self.map['tip_client'] == '' or self.map['telefon'] == ''):
            print(1)
            return -1

        if (re.search("[0-9]", self.map['nume'])):
            print(2)
            return -1

        # if (re.match("persoana_fizica",self.map['tip_client']) == None or re.match("persoana_juridica",self.map['tip_client']) == None):
        #     print(self.map['tip_client'])
        #     print(3)
        #     return -1

        if (re.search("[^0-9]",self.map['telefon'])):
            print(4)
            return -1

        if (re.search('^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$', self.map['data_ultimei_comenzi']) == None and self.map['data_ultimei_comenzi'] != ''):
            print(5)
            return -1

        fields = ""
        for i in list(self.map.keys()):
            if self.map[i] != '':
                fields += i + ", "

        fields = fields[0:-2]
        print(fields)
        values = ""

        for k in self.map:
            if k == 'data_ultimei_comenzi' and self.map['data_ultimei_comenzi'] != '':
                values += f"TO_DATE('{self.map[k]}','dd.mm.yyyy'),"
            elif self.map[k] != '':
                values += "'" + str(self.map[k]) + "',"


        values = values[0:-1]
        print(values)
        querie = f'INSERT INTO CLIENTI(id_client,{fields}) VALUES(CLIENTI_ID_CLIENT_SEQ.nextval,{values})'
        print(querie)
        return querie

if __name__ == '__main__':
    c = Clienti(['Popica','persoana_fizica','010414151','01.2415'])

    print(re.search('^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$','1.504'))
    c.insert()
