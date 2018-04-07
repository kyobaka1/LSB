LSB-Steganography
=================
Mục đích bài tập: Triển khai kĩ thuật dấu tin LSB vào tập tin hình ảnh và âm thanh.

Installation
------------
Tool này yêu cầu cài đặt một số thư viện: <br>
OpenCV : Đọc vào tập tin hình ảnh. <br>
wave   : Đọc vào tập tin âm thanh có định dạng .wav <br>
docopt : Thư viện cho phép truyền các tham số đầu vào.
```bash
pip install -r requirements.txt
```
Usage
-----

```bash
LSB.py
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
```
Python module
-------------
ImageSteg:
```
```

AudioSteg:

```
```







