# It allows users to play video files, pause playback, crop specific regions from the video, 
# and save the cropped images. The application supports keyboard interactions for a smooth 
# user experience, including playback control, cropping interface, and navigation through 
# the video using a trackbar. 

import cv2
import os
import numpy as np

VIDEO_PATH = ''
SAVE_PATH = ''

cap = None
trackbarActive = False

def save_crop(crop, videoName, folder='cropped_images'):
    print(videoName)
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f'{videoName}_{cv2.getTickCount()}.jpg')
    cv2.imwrite(filename, crop)
    print(f"Image {filename} Saved")

def apply_dim_effect(frame, brightness=0.8):
    return (frame * brightness).astype(np.uint8) 

def on_trackbar(val): 
    global cap, trackbarActive
    if trackbarActive:
        index = cv2.getTrackbarPos('Seek', 'Video')
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

def main():
    global cap, trackbarActive
    cap = cv2.VideoCapture(VIDEO_PATH)
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    cv2.namedWindow('Video') 
    cv2.createTrackbar('Seek', 'Video', 0, totalFrames, on_trackbar)
    
    paused = False
    roi_selected = False
    crop = None

    while True:
        if not (paused or roi_selected):
            ret, frame = cap.read()
            
            if not ret:
                break
            
            trackbarActive = False
            currentFrame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cv2.setTrackbarPos('Seek', 'Video', currentFrame - 1) 
            trackbarActive = True
        
        frame = cv2.resize(frame, (1920,1080))

        key = cv2.waitKey(33) & 0xFF 

        if key == 32:  # Space bar
            paused = not paused
            if roi_selected:
                roi_selected = False  
                save_crop(crop, VIDEO_PATH.split('\\')[-1].split('.mp4')[0], SAVE_PATH)
                cv2.destroyWindow("Cropped Preview")
                paused = False
            else:
                dim_frame = apply_dim_effect(frame)
                r = cv2.selectROI('Video', dim_frame, fromCenter=False, showCrosshair=True)
                if any(r):
                    x, y, w, h = r
                    if w>0 and h >0: 
                        crop = frame[y:y+h, x:x+w]
                        roi_selected = True
                        cv2.imshow('Cropped Preview', crop)
                    else: paused = False
                else: paused = False

        elif key == 27:  # Esc
            if roi_selected:
                cv2.destroyWindow("Cropped Preview") 
            roi_selected = False
            paused = False
            
        elif key == ord('i'):
            trackbarActive = False
            currentFrame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame - 1 - 50)
            trackbarActive = True
            
        
        elif key == ord('p'):
            trackbarActive = False
            currentFrame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame - 1 + 50)
            trackbarActive = True
        
        elif key == ord('q'):
            break
        
            
        cv2.imshow('Video', frame)

        if cv2.getWindowProperty('Video', 0) == -1: 
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
