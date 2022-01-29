from random import shuffle
from cv2 import *
import time
import threading
import os, glob
import re


images_folder = "imgs"
seconds_between_pic = 15


def check_if_seconds_have_passed(ts, secods):
    return time.time() - ts >= secods

def remove_files_from_folder(folder):
    files = glob.glob(f"{folder}/*")
    for f in files:
        os.remove(f)


# Param "params" is a list of parameters
# index 0 must be an boolean that represents if program should continue
# index 1 must be an boolean that represents if images capture should continue
def capture_image(params):
    cam_port = 0
    cam = VideoCapture(cam_port)
    ts = None


    while (params[0]):
        if (params[1] == True and (ts is None or check_if_seconds_have_passed(ts, seconds_between_pic))):
            result, image = cam.read()
            ts = time.time()

            if (result):
                # showing result, it take frame name and image 
                # output
                #imshow("GeeksForGeeks", image)
            
                # saving image in local storage
                imwrite(f"{images_folder}/{ts}.png", image)
                print("Image saved")

                # If keyboard interrupt occurs, destroy image 
                # window
                #waitKey(0)
                #destroyWindow("GeeksForGeeks")
            
            # If captured image is corrupted, moving to else part
            else:
                print("No image detected. Please! try again")

params = [True, True]

th = threading.Thread(target=capture_image, args=(params,))
th.start()

while (params[0]):
    entry = input()

    if (entry == "pause"):
        params[1] = False
        
    elif (entry == "play"):
        params[1] = True

    elif (entry == "stop"):
        params[0] = False

    elif (entry == "clean"):
        remove_files_from_folder(images_folder)

    elif (re.search("seconds (\\d+)", entry)):
        result = re.search("seconds (\\d+)", entry)
        seconds_between_pic = int(result[1])

th.join()