import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def text_detector(image):
    # Reading image 
    img = cv2.imread(image)

    # Convert to RGB 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect texts from image
    texts = pytesseract.image_to_string(img)
    return texts
# print("Printing the text from the image:",end = ' ')
# print(text_detect('3.webp'))