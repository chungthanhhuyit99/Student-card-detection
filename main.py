from fpt import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from PIL import Image
import PIL.Image
from pytesseract import image_to_string
import pytesseract
from datetime import datetime
import string

def VideoCap():
	img_counter = 0

	vc=cv2.VideoCapture('https://192.168.42.129:4343/video')
	

	if vc.isOpened(): # try to get the first frame
		rval, frame = vc.read()
	else:
		rval = False;

	while rval:
		cv2.imshow("preview", frame)
		rval, frame = vc.read()
		key = cv2.waitKey(20)

		
		   
		if key%256 == 32:
		    # SPACE pressed
		    img_name = "opencv_frame.png"
		    img_cap=cv2.imwrite(img_name, frame)
		    print("{} written!".format(img_name))
		    
		    img_cap = cv2.imread(img_name)
		    #img_cap = cv2.imread("Hello", frame)
		    cv2.imshow("out",img_cap)	
		    break	 
VideoCap()
image = cv2.imread("opencv_frame.png")
ratio =  image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
 

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 75, 200)
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 

for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	if len(approx) == 4:
		screenCnt = approx
		break
 

print("STEP 2: Find contours of card")
try:
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

	cv2.imshow("Outline", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	ims = cv2.resize(warped, (582, 363))
	cv2.imshow("cc",ims)

	im_crop_Name = ims[139:181, 171:558]
	cv2.imshow("crop_Name",im_crop_Name)
	im_crop_NameGray = cv2.cvtColor(im_crop_Name, cv2.COLOR_BGR2GRAY)
	cv2.imshow("crop_Name",im_crop_NameGray)


	im_crop_MSSV = ims[178:205, 285:392]
	#cv2.imshow("crop_MSSV",im_crop_MSSV)
	im_crop_MSSVGray = cv2.cvtColor(im_crop_MSSV, cv2.COLOR_BGR2GRAY)
	cv2.imshow("crop_MSSV",im_crop_MSSVGray)

	im_crop_Avt = ims[105:275, 16:155]
	cv2.imshow("crop_Avt",im_crop_Avt)

	im_crop_Year = ims[215:244, 286:406]
	#cv2.imshow("crop_Avt",im_crop_Year)
	im_crop_YearGray = cv2.cvtColor(im_crop_Year , cv2.COLOR_BGR2GRAY)
	cv2.imshow("crop_Year",im_crop_YearGray)

	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

	text_Name = pytesseract.image_to_string(im_crop_Name,lang = 'vie')
	print("Ten: "+text_Name)	
	

	text_MSSV = pytesseract.image_to_string(im_crop_MSSVGray)
	print("MSSV: "+text_MSSV)		

	text_Year = pytesseract.image_to_string(im_crop_Year)
	print("Nien Khoa:"+ text_Year)
	

	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	 
	# show the scanned image and save one copy in out folder

	imS = cv2.resize(warped, (550, 350))
		
	cv2.waitKey(0)
except: 
	print("Not Found the card!!! ")		
try:
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	f1 = open("text.txt", mode="a",encoding='utf-8')
	
	f1.write(u""+text_Name + " "+text_MSSV +" "+text_Year+" "+dt_string+" \n");
	f1.close()
except:
	print("K ghi dc") 

