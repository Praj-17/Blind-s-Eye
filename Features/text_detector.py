import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract(image):
    Actual_image = cv2.imread(image)
    Sample_img = cv2.resize(Actual_image,(400,350))
    Image_ht,Image_wd,Image_thickness = Sample_img.shape
    Sample_img = cv2.cvtColor(Sample_img,cv2.COLOR_BGR2RGB)
    texts = pytesseract.image_to_data(Sample_img) 
    mytext=""
    prevy=0
    for cnt,text in enumerate(texts.splitlines()):
        if cnt==0:
            continue
        text = text.split()
        if len(text)==12:
            x,y,w,h = int(text[6]),int(text[7]),int(text[8]),int(text[9])
            if(len(mytext)==0):
                prey=y
            if(prevy-y>=10 or y-prevy>=10):
                print(mytext)
                #Label(root,text=mytext,font=('Times',15,'bold')).pack()
                mytext=""
            mytext = mytext + text[11]+" "
            prevy=y
    return mytext
def text_detector(image):
    # Reading image 
    img = cv2.imread(image)

    # Convert to RGB 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect texts from image
    texts = pytesseract.image_to_string(img)
    print(texts)
    if texts == "":
        return "No text detected"
    return texts
# print("Printing the text from the image:",end = ' ')
# print(text_detect('3.webp'))
# print(text_detector(r"C:\Users\pwayk\Downloads\WhatsApp Image 2022-05-31 at 10.07.24 PM.jpeg"))
print(extract(r"logs\object_detect_images\10.59.14_2022-07-12.png"))
