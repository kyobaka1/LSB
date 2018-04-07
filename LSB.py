#!/usr/bin/env python
# coding:UTF-8
"""LSB.py
Usage:
  LSB.py image encode -i <input> -o <output> -m <message>
  LSB.py image decode -i <input>
  LSB.py audio decode -i <input>
  LSB.py audio encode -i <input> -o <output> -m <message>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
  -m,--message=<message>    Message to hide.
"""
import docopt
import os
import cv2
import sys
from StegImage import ImageLSB
from StegAudio import AudioLSB,makeNewAudioFile


def Main():
    args = docopt.docopt(__doc__, version="6.9")
    file_in = args["--in"]
    if os.path.isfile(file_in):
        pass
    else:
        raise IOError('File does not exists')
    if args['image']:
        in_img = cv2.imread(file_in)
        steg = ImageLSB(in_img)
        if args['encode']:
            file_out = args["--out"][0]
            message = args["--message"]
            result = steg.hideMes(message)
            cv2.imwrite(file_out,result)
        elif args['decode']:
            message = steg.getMes()
            print "Hide message: "+ message
        else:
            raise IOError('Wrong input value!')
    elif args['audio']:
        in_audio = AudioLSB(file_in)
        if args['encode']:
            file_out = args["--out"]
            message = args["--message"]
            data = in_audio.hideMes(message)
            makeNewAudioFile(file_out,in_audio.params,data)
        elif args['decode']:
            message = in_audio.getMes()
            print "Hide message: "+ message
        else:
            raise IOError('Wrong input value!')
if __name__ == "__main__":
    Main()

