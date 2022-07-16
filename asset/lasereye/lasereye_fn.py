from PIL import Image
import numpy as np
import os
import cv2
from asset.lasereye.gaze_tracking import GazeTracking
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(DIRNAME,"input")

def imagecov(photoname, relative_eye_size, nameonly):
    
    '''
    Keep the image in the folder source_image and 
    put in the name of image in photoname
    '''
    sourcename = DIRNAME + '/input/' + photoname
    finalname =  DIRNAME + '/output/' + nameonly + '_laser.png'

    if "_laser" in photoname:
        finalname = DIRNAME + '/output/' + nameonly + '.png'
    else:
        finalname = DIRNAME + '/output/' + nameonly + '_laser.png'


    '''
    You can change the relative eye size to optimize the image further
    '''
    gaze = GazeTracking()
    frame = cv2.imread(sourcename)

    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    try:
        distance = (left_pupil[0] - right_pupil[0]) * (left_pupil[0] - right_pupil[0]) + (left_pupil[1] - right_pupil[1]) * (left_pupil[1] - right_pupil[1])
    except:
        return False
    distance = np.sqrt(distance)
    
    #print(distance)
    face_image = Image.open(sourcename)
    eye_image = Image.open(DIRNAME + '/source_img/redeye.png')

    eye_image = eye_image.resize((int(distance*2*relative_eye_size),int(distance*relative_eye_size)))
    eye_image = eye_image.rotate(15)

    Image.Image.paste(face_image, eye_image,(left_pupil[0] - int(distance*relative_eye_size),left_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
    Image.Image.paste(face_image, eye_image,(right_pupil[0] - int(distance*relative_eye_size),right_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
    face_image.save(finalname)
    return True