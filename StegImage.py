# coding:UTF-8

class ImageLSB():
    def __init__(self,inputImage):
        self.image = inputImage
        self.row,self.column,self.channels = inputImage.shape
        self.size = inputImage.size
        # Lưu thông tin về vị trí đang làm việc.
        self.currentRow = 0
        self.currentColumn = 0
        self.currentChannels = 0 # Có thể là 0 - 1 - 2. Ứng với 3 giá trị R,G,B trong mảng.

        # Mặt nạ để OR khi muốn đặt bit là 1.
        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)
        # Mặt nạ để AND khi muốn đặt bit là 0.
        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)
    '''
    Hàm để LSB n bits vào ảnh.
    '''
    def putBits(self,bits):
        for onebit in bits:
            rgb = self.image[self.currentRow,self.currentColumn] # Lấy được 3 giá trị R,G,B.
            if onebit == '1':
                rgb[self.currentChannels] = int(rgb[self.currentChannels] | self.maskONE)
            else:
                rgb[self.currentChannels] = int(rgb[self.currentChannels] & self.maskZERO)
            self.image[self.currentRow, self.currentColumn] = rgb
            self.viTriTiepTheo()
    '''
    Chuyển channels: Đang ở R -> G, G -> B. Nếu đang ở B:
    -> Chuyển cột: Cột 1 -> 2 ... Nếu ở cột cuối cùng:
    -> Chuyển hàng: Hàng 1 -> 2 ... Nếu ở hàng cuối cùng:
    -> Chuyển bit đang dấu: Trọng số bé nhất là bit số 8 -> dấu ở bit số 7. Nếu hết bit để dấu:
    -> Pó tay.
    '''
    def viTriTiepTheo(self):
        if self.currentChannels == self.channels - 1: # Trừ 1 bởi vì mảng bắt đầu từ 0.
            self.currentChannels = 0
            if self.currentColumn == self.column - 1:
                self.currentColumn = 0
                if self.currentRow == self.row - 1:
                    self.currentRow = 0
                    if self.maskONE == 128:
                        print "DATA IS TOO BIG!!"
                        exit(0)
                    else:
                        # Lấy ra phần tử tiếp theo.
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.currentRow += 1
            else:
                self.currentColumn += 1
        else:
            self.currentChannels += 1


    def readOneBit(self):
            curLocation = self.image[self.currentRow, self.currentColumn][self.currentChannels]
            bit = int(curLocation) & self.maskONE
            self.viTriTiepTheo()
            if bit > 0:
                return "1"
            else:
                return "0"


    def read_bits(self, n): # Đọc n bit.
            bits = ""
            for i in range(n):
                bits += self.readOneBit()
            return bits


    def intToBin(self,int,size):
        curBin = bin(int)[2:]
        if len(curBin) > size:
            pass
        while len(curBin) < size:
            curBin = '0' + curBin
        return curBin


    def hideMes(self,text):
        doDaiText = len(text)
        self.putBits(self.intToBin(doDaiText,16)) # Dấu size định dạng 16 bit vào trước để tiện cho việc decode sau này.
        for char in text:
            self.putBits(self.intToBin(ord(char),8))
        return self.image
    def getMes(self):
        doDaiText = int(self.read_bits(16),2);
        message = ""
        i = 0;
        while i < doDaiText:
            i += 1
            tmp = self.read_bits(8)
            message += chr(int(tmp, 2))
        return message