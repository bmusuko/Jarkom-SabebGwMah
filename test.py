import binascii
import sys

class packet(object):
    def __init__(self, TYPE=0, ID=0, SEQUENCE_NUMBER=0, LENGTH = 0, CHECKSUM=0, DATA=bytearray(), parse_bytes=0, parsed_data = 0):
        if (parse_bytes == 0):
            self.TYPE = TYPE
            self.ID = ID
            self.SEQUENCE_NUMBER = SEQUENCE_NUMBER
            self.LENGTH = LENGTH
            self.CHECKSUM = CHECKSUM
            self.DATA = DATA

    def parsing(self):
        result = bytearray(7)

        result[0] = self.TYPE + self.DATA*16
        result[1] = self.SEQUENCE_NUMBER // 256
        result[2] = self.SEQUENCE_NUMBER % 256
        result[3] = self.LENGTH // 256
        result[4] = self.LENGTH % 256
        result[5] = self.CHECKSUM // 256
        result[6] = self.CHECKSUM % 256
        result += self.DATA

        return bytes(result)

    def paket(self, parsed_data, ID, SEQUENCE_NUMBER, TYPE):
        self.TYPE = TYPE
        self.ID = ID
        self.SEQUENCE_NUMBER = SEQUENCE_NUMBER
        self.LENGTH = len(parsed_data)
        self.DATA = parsed_data
        self.CHECKSUM = 0

        list_nilai = []

        cek = bytearray(self.parsing())
        n = 0
        LENGTH = len(cek)
        s = 0

        for x in cek:
            list_nilai.append(x)

        # print(list_nilai)
        # list_nilai =[x for x in cek]
        LENGTH = len(list_nilai)//2
        b = len(list_nilai)%2

        while (n < LENGTH):
            s ^= (list_nilai[n*2]*256 + list_nilai[n*2+1])
            n+=1
        if (b > 0):
            s ^=  list_nilai[n*2]
        
        self.CHECKSUM = s
