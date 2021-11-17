import unittest

from cv2.cv2 import imread

from pytesseract import pytesseract
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class MyTestCase(unittest.TestCase):
    def test_something(self):
        image_path = 'img.png'

        image = imread(image_path)
        text = pytesseract.image_to_string(image)
        print(f'{text=}')


if __name__ == '__main__':
    unittest.main()
