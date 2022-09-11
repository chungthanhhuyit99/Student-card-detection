import cv2


img_counter = 0
vc=cv2.VideoCapture('https://192.168.42.129:4343/video')


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    # cv2.line(img=frame, pt1=(130, 136), pt2=(220, 136), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    # cv2.line(img=frame, pt1=(130, 136), pt2=(130,215), color=(255,0,0), thickness=2, lineType=8, shift=0)

    # cv2.line(img=frame, pt1=(510, 136), pt2=(423, 136), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    # cv2.line(img=frame, pt1=(510,136), pt2=(510,214), color=(255,0,0), thickness=2, lineType=8, shift=0)

    # cv2.line(img=frame, pt1=(130, 349), pt2=(130, 265), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    # cv2.line(img=frame, pt1=(130, 349), pt2=(221,349), color=(255,0,0), thickness=2, lineType=8, shift=0)

    # cv2.line(img=frame, pt1=(510, 349), pt2=(510, 265), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    # cv2.line(img=frame, pt1=(510, 349), pt2=(423,349), color=(255,0,0), thickness=2, lineType=8, shift=0)
    
    if key == 27: # exit on ESC
        break    
    elif key%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame.png"
        img_cap=cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        
        img_cap = cv2.imread(img_name)
        #img_cap = cv2.imread("Hello", frame)
        cv2.imshow("output",img_cap)
        
vc.release()
cv2.destroyWindow("preview")