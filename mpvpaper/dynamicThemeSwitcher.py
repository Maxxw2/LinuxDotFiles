import cv2
import time 
import os
import subprocess


"""
Please note that this script does take pictures with your webcam, all proccessing happens on your machine and the image will never be
sent anywhere. Images will be destroyed once processing finishes. 

dependencies pacman install:
    sudo pacman -S python-opencv 
"""


##############
### CONFIG ###
##############

# How often the camera takes and processes a image (seconds) 
timeInterval = 1

# Default camera is == 0
camera = 0 

# Brightness threshold (at what point should the theme change?)
brightnessThresshold = 120

# LightMode is the standard startup mode
lightMode = True

# Change path to your wallpapers here
lightModePATH = "~/.config/hypr/wallpapers/YumeWaterWallpaper.mp4"
darkModePATH = "~/.config/hypr/wallpapers/ShinyYumeWallpaper.mp4"


#####################
### END OF CONFIG ###
#####################

def captureImage():
    # (0 == default camera)
    cam = cv2.VideoCapture(camera)
    ret, frame = cam.read()
    cam.release()
    
    if ret:
        # cv2.imshow(Captured frame, frame) 
        cv2.imwrite("tempfile.png", frame)

        # Make image gray scale
        img = cv2.imread("tempfile.png")
        grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("GrayScale", grayScale) #Debug
        cv2.imwrite("tempfile.png", grayScale)
        # cv2.waitKey(0) # Debug 
        # cv2.destroyWindow("captured") #Debug 

        img = cv2.imread("tempfile.png")
        lightAverage = cv2.mean(img)[0]
        print(f"Brightness Value: {lightAverage}")
        return lightAverage

    else:
        "Image Capture failed, Make sure the camera is connected"

def decideTheme(lightAverage):
    # Yes i realise now how fucking stupid this function is
    # This function only exists to make it easier for people to add more color profiles
    if lightAverage > brightnessThresshold: # Change light threshold here
        setLightMode()
        global lightMode 
        lightMode = True

    else:
        setDarkMode()
        global darkMode 
        lightMode = False

##################
### LIGHT MODE ###
##################

def setLightMode():
    if lightMode == False:
        print("setting light mode")
        # Change wallpaper
        # Replaces old wallpaper with new one if neccessary
        pid = subprocess.getoutput("pidof mpvpaper")
        if pid:
            print(f"mpvpaper is runnin with PID: {pid}")
            changeTheme = subprocess.Popen(['mpvpaper', '-o', '--loop', 'ALL', lightModePATH])
            time.sleep(0.3)
            killOldProcess = subprocess.Popen(['kill', '-9', pid])
        else:
            changeTheme = subprocess.Popen([
                'mpvpaper', '-o', '--loop', 'ALL', lightModePATH]) 
    else: 
        print("LightMode is already active \nNo changes where made")


#################
### DARK MODE ###
#################

def setDarkMode():
    if lightMode == True:
        print("setting dark mode")
        # Change wallpaper 
        # Replaces old wallpaper with new one if neccessary
        pid = subprocess.getoutput("pidof mpvpaper")
        if pid:
            print(f"mpvpaper is running with PID: {pid}")
            changeTheme = subprocess.Popen(['mpvpaper', '-o', '--loop', 'ALL', darkModePATH])
            time.sleep(0.3)
            killOldProcess = subprocess.Popen(['kill', '-9', pid])
        else:
            changeTheme = subprocess.Popen(['mpvpaper', '-o', '--loop', 'ALL', darkModePATH])


if __name__ == "__main__":
    loop = True

    while loop:
        lightAverage = captureImage()
        decideTheme(lightAverage)
        time.sleep(timeInterval)


