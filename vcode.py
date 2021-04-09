import pytesseract

from PIL import Image

image = Image.open('111.png')

vcode = pytesseract.image_to_string(image)

print(len(vcode))
