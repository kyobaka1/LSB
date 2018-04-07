# coding:UTF-8
import wave
#Thư viện dùng để đọc và ghi file .wav.

class AudioLSB:
    def __init__(self, inputAudio):
        self.file = wave.open(inputAudio,'rb')
        self.channels = self.file.getnchannels() #Stereo or Mono
        self.frames = self.file.getnframes()     #Tổng số frames của file.
        self.params = self.file.getparams()

        self.startFrame = 30
        self.soFrameConLai = self.file.getnframes()

        # Mặt nạ để OR khi muốn đặt bit là 1.
        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)
        # Mặt nạ để AND khi muốn đặt bit là 0.
        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

    def putOneBit(self,int, bit):
        if bit == '1':
            return int | self.maskONE
        else:
            return int & self.maskZERO

    def intToBin(self,int,size):
        curBin = bin(int)[2:]
        if len(curBin) > size:
            pass
        while len(curBin) < size:
            curBin = '0' + curBin
        return curBin

    def hideMes(self,message):
        new = [] # Lưu data mới để tạo ra file audio có dấu tin.

        #Copy số frame đầu, ko thay đổi gì hết.
        for x in range(self.startFrame):
            self.soFrameConLai -= 1
            new.append(self.file.readframes(1))

        byteInFrame = len(str(new[0])) # Kiểm tra xem 1 frame có độ dài là bao nhiêu?
        '''
        Cách dấu như sau:
        B1. Xác định số bit cần dấu.
        B2. Xác định số frame cần để dấu số bit đấy. Ví dụ 1 frame có 4 byte thì dấu được 4 bit. Cần dấu 16bit -> 4 frame.
        B3. Dấu trong từng kí tự của frame.
        B4. Thêm vào list lưu data mới đã sửa đổi.
        '''
        # Dấu độ dài message (Dùng 16bit để lưu).
        MAX_LENMESSAGE = 16
        lenMes = self.intToBin(len(message),MAX_LENMESSAGE)
        i = 0
        for frame in range(16 / byteInFrame):
            currentFrame = self.file.readframes(1)
            self.soFrameConLai -= 1
            newFrame = ''
            for char in currentFrame:
                newFrame += chr(self.putOneBit(ord(char), lenMes[i]))
                i += 1
            new.append(newFrame)

        #Dấu message.
        for kitu in message:
            binkitu = self.intToBin(ord(kitu),8)
            i = 0
            for frame in range(2):
                currentFrame = self.file.readframes(1)
                self.soFrameConLai -= 1
                newFrame = ''
                for char in currentFrame:
                    newFrame += chr(self.putOneBit(ord(char), binkitu[i]))
                    i += 1
                new.append(newFrame)
        #Phần còn lại giữ nguyên như cũ.
        for x in range(self.soFrameConLai):
            new.append(self.file.readframes(1))

        #Trả về data.
        return new
    def getMes(self):
        # Bỏ qua số frame đầu.
        self.file.readframes(self.startFrame)
        # Xác định độ dài của message.
        lenMes = ''
        MAX_LENMESSAGE = 16
        for x in range(MAX_LENMESSAGE/(self.channels*2)):
            currentFrame = self.file.readframes(1)
            for char in currentFrame:
                if ord(char) & self.maskONE > 0:
                    lenMes += '1'
                else:
                    lenMes += '0'
        lenMes = int(lenMes,2)

        #Xác định message. 1 kí tự chỉ có 8 bit.
        message = ''
        i = 0;
        while i < lenMes:
            i += 1
            binMes8 = ''
            for x in range(8/(self.channels*2)):
                currentFrame = self.file.readframes(1)
                for char in currentFrame:
                    if ord(char) & self.maskONE > 0:
                        binMes8 += '1'
                    else:
                        binMes8 += '0'
            message += chr(int(binMes8,2))
        return message
def makeNewAudioFile(outputFileName, params, data):
    f = wave.open(outputFileName, 'wb')
    f.setparams(params)
    f.writeframes(''.join(x for x in data))
    f.close()