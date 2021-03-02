import re

class Departamente:
    def __init__(self,data):
        self.map = {}
        self.map['nume'] = data[0]

    def insert(self):
        #print(self.nume)
        if( self.map['nume'] == "''" ):
            return -1

        if( re.search('[^a-zA-Z]',self.map['nume']) != None):
            return -1

        querie = f'INSERT INTO DEPARTAMENTE VALUES(DEPARTAMENTE_ID_DEPT_SEQ.nextval,\'{self.map["nume"]}\')'
        print(querie)
        return querie
