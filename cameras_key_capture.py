import cv2
import os

def setup_cameras():
    CAML = cv2.VideoCapture(1)  # Adjust camera indices if needed
    CAMR = cv2.VideoCapture(2)
    
    # Set camera properties based on README values
    for cap in [CAML, CAMR]:
        cap.set(cv2.CAP_PROP_EXPOSURE, -6.0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 120.0)
    
    return CAML, CAMR

def capture_images(CAML, CAMR):
    num = 0
    total_photos = 10   

    os.makedirs('images2/stereoLeft')
    os.makedirs('images2/stereoRight')

    while CAML.isOpened() and num < total_photos:

        succes1, img = CAML.read()
        succes2, img2 = CAMR.read()

        k = cv2.waitKey(5)

        if k == 27:
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            cv2.imwrite('images2/stereoLeft/imageL' + str(num) + '.png', img)
            cv2.imwrite('images2/stereoright/imageR' + str(num) + '.png', img2)
            print("images saved!")
            num += 1

        cv2.imshow('Img 1',img)
        cv2.imshow('Img 2',img2)

    # Release and destroy all windows before termination
    CAML.release()
    CAMR.release()
    cv2.destroyAllWindows()

    print("Photo capture completed!")

if __name__ == "__main__":
    CAML, CAMR = setup_cameras()
    capture_images(CAML, CAMR)